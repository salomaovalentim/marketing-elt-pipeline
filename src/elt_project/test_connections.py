import os
import boto3
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Configurações do MinIO
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:9000")
AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")

# Configurações do PostgreSQL
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "elt_db")


def test():
    print("--- 1. A testar ligação ao MinIO ---")
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=AWS_KEY,
            aws_secret_access_key=AWS_SECRET,
            region_name="us-east-1",
        )
        resposta = s3.list_buckets()
        print("[OK] MinIO conectado com sucesso!")
        print(f"     Buckets existentes: {[b['Name'] for b in resposta.get('Buckets', [])]}")
    except Exception as e:
        print(f"[ERRO] Falha no MinIO: {e}")

    print("\n--- 2. A testar ligação ao PostgreSQL ---")
    try:
        url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(url, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            versao = conn.execute(text("SELECT version();")).fetchone()
            print("[OK] PostgreSQL conectado com sucesso!")
            print(f"     Versão: {versao[0]}")
    except Exception as e:
        print(f"[ERRO] Falha no PostgreSQL: {e}")


if __name__ == "__main__":
    test()