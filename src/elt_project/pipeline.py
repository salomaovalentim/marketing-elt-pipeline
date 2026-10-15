import io
import os
from dotenv import load_dotenv
import boto3
import pandas as pd
from sqlalchemy import create_engine
from src.elt_project.generate_data import generate_raw_marketing_sources

load_dotenv()

# Variáveis do MinIO
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:9000")
AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
BUCKET_NAME = os.getenv("BUCKET_NAME", "raw-lake")

# Variáveis do Postgres
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME")

s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET,
    region_name="us-east-1",
)

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def ensure_bucket_exists():
    buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    if BUCKET_NAME not in buckets:
        s3.create_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' criado com sucesso no MinIO.")


def run():
    ensure_bucket_exists()
    print("Gerando fontes de dados brutas de marketing...")
    sources = generate_raw_marketing_sources()

    for table_name, df in sources.items():
        # 1. Enviar arquivo bruto Parquet para o MinIO (Data Lake Bronze)
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)

        s3_key = f"marketing/{table_name}.parquet"
        s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=buffer.getvalue())
        print(f"-> Salvo no MinIO: s3://{BUCKET_NAME}/{s3_key}")

        # 2. Carregar dados brutos diretamente no PostgreSQL
        df.to_sql(table_name, engine, schema="public", if_exists="replace", index=False)
        print(f"-> Carregado no PostgreSQL: public.{table_name} ({len(df)} registros)")

    print("\nExtract & Load concluído com sucesso!")


if __name__ == "__main__":
    run()