import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def generate_raw_marketing_sources():
    random.seed(42)
    np.random.seed(42)

    # -------------------------------------------------------------------------
    # FONTE 1: METADADOS DE CAMPANHAS (com nomes inconsistentes para tratar no dbt)
    # -------------------------------------------------------------------------
    campaigns_config = [
        (
            1,
            [
                "BlackFriday_2026_Meta",
                "BF-2026-Facebook",
                "black_friday_meta",
                "BLACK_FRIDAY_FB",
            ],
            "Conversão",
            "Carrossel",
        ),
        (
            2,
            [
                "Google_Search_Institucional",
                "institucional_gads",
                "GSEARCH_INST",
            ],
            "Tráfego",
            "Pesquisa",
        ),
        (
            3,
            ["TikTok_Branding_TopFunnel", "tt_branding_v1", "TIKTOK_BRAND"],
            "Conscientização",
            "Vídeo",
        ),
        (
            4,
            [
                "Meta_Remarketing_Carrinho",
                "rmkt_meta_cart",
                "REMARKETING_CAROUSEL",
            ],
            "Conversão",
            "Display",
        ),
    ]

    campaigns_rows = []
    for cid, nomes, objetivo, midia in campaigns_config:
        campaigns_rows.append(
            {
                "campaign_id": cid,
                "campaign_name": random.choice(nomes),  # Inconsistência de strings
                "objective": objetivo,
                "media_type": midia,
                "start_date": "2026-09-01",
                "end_date": "2026-11-30",
                "status": "Ativa",
            }
        )
    df_campaigns = pd.DataFrame(campaigns_rows)

    # -------------------------------------------------------------------------
    # FONTE 2: CADASTRO DO CRM / CLIENTES
    # -------------------------------------------------------------------------
    estados_cidades = {
        "BA": ["Salvador", "Feira de Santana", "Itabuna", "Ilhéus"],
        "SP": ["São Paulo", "Campinas", "Santos"],
        "RJ": ["Rio de Janeiro", "Niterói"],
        "MG": ["Belo Horizonte", "Uberlândia"],
    }

    customers_rows = []
    for cid in range(1, 201):
        uf = random.choice(list(estados_cidades.keys()))
        cidade = random.choice(estados_cidades[uf])
        customers_rows.append(
            {
                "customer_id": cid,
                "age": int(np.random.normal(32, 8)),
                "gender": random.choice(["M", "F", "Outro"]),
                "state": uf,
                "city": cidade,
                "signup_date": (
                    datetime(2026, 1, 1) + timedelta(days=random.randint(0, 250))
                ).strftime("%Y-%m-%d"),
                "customer_segment": random.choices(
                    ["Novo", "Recorrente", "VIP"], weights=[0.6, 0.3, 0.1]
                )[0],
            }
        )
    df_customers = pd.DataFrame(customers_rows)

    # -------------------------------------------------------------------------
    # FONTE 3: RELATÓRIO DE CUSTO DIÁRIO DAS PLATAFORMAS (Meta/Google/TikTok API)
    # -------------------------------------------------------------------------
    datas = pd.date_range(start="2026-09-01", end="2026-10-14", freq="D")
    ad_spend_rows = []
    cost_id = 1

    for d in datas:
        for cid in [1, 2, 3, 4]:
            # Ruído: 5% de falha na API que gera valores nulos ou zerados
            api_failure = random.random() < 0.05
            if api_failure:
                spend = None if random.random() < 0.5 else 0.0
                impressions = 0
                clicks = 0
            else:
                spend = round(random.uniform(80.0, 650.0), 2)
                impressions = int(spend * random.uniform(15, 30))
                clicks = int(impressions * random.uniform(0.015, 0.045))

            ad_spend_rows.append(
                {
                    "cost_id": cost_id,
                    "campaign_id": cid,
                    "date": d.strftime("%Y-%m-%d"),
                    "amount_spent": spend,
                    "total_impressions": impressions,
                    "total_clicks": clicks,
                }
            )
            cost_id += 1
    df_ad_spend = pd.DataFrame(ad_spend_rows)

    # -------------------------------------------------------------------------
    # FONTE 4: LOGS BRUTOS DE EVENTOS DO SITE (Tracking Pixel)
    # -------------------------------------------------------------------------
    events_rows = []
    event_id = 1
    channels = {
        1: "Meta Ads",
        2: "Google Ads",
        3: "TikTok Ads",
        4: "Meta Ads",
    }

    for d in datas:
        for cid in [1, 2, 3, 4]:
            event_count = random.randint(20, 50)

            # Ruído: Ataque ou pico anômalo de bots no dia 2026-09-20 na campanha 1
            is_bot_spike = (d.strftime("%Y-%m-%d") == "2026-09-20") and (cid == 1)
            if is_bot_spike:
                event_count = 1200  # Enxurrada de cliques anômalos

            for _ in range(event_count):
                # Usuário deslogado gera customer_id nulo
                cust_id = (
                    random.randint(1, 200) if random.random() < 0.3 else None
                )

                if is_bot_spike:
                    event_type = "Clique"
                    conversion_value = 0.0
                    device = "Desktop"
                else:
                    event_type = random.choices(
                        ["Impressão", "Clique", "Lead", "Conversão/Compra"],
                        weights=[0.60, 0.28, 0.08, 0.04],
                    )[0]
                    conversion_value = (
                        round(random.uniform(60.0, 500.0), 2)
                        if event_type == "Conversão/Compra"
                        else 0.0
                    )
                    device = random.choices(
                        ["Mobile", "Desktop", "Tablet"],
                        weights=[0.70, 0.25, 0.05],
                    )[0]

                random_time = timedelta(
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                    seconds=random.randint(0, 59),
                )

                events_rows.append(
                    {
                        "event_id": event_id,
                        "campaign_id": cid,
                        "customer_id": cust_id,
                        "event_timestamp": (d + random_time).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "device": device,
                        "traffic_source": channels[cid],
                        "event_type": event_type,
                        "conversion_value": conversion_value,
                    }
                )
                event_id += 1

    df_events = pd.DataFrame(events_rows)

    return {
        "raw_campaigns": df_campaigns,
        "raw_crm_customers": df_customers,
        "raw_ad_spend": df_ad_spend,
        "raw_tracking_events": df_events,
    }