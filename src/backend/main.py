# Arquivo: src/backend/main.py
from fastapi import FastAPI
import pandas as pd
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API do Dashboard Cannoli")

# Configuração do CORS para permitir a comunicação com o front-end
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lógica para encontrar a pasta /data a partir da localização deste arquivo
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data"

def load_orders_data():
    """Função para carregar e preparar os dados de pedidos."""
    try:
        df = pd.read_json(DATA_PATH / 'orders.json')
        df['total_value'] = df['total'].apply(lambda x: x.get('total', 0))
        return df
    except FileNotFoundError:
        return None

@app.get("/api/kpis/gerais")
def get_general_kpis():
    """Endpoint que retorna os KPIs gerais."""
    df_orders = load_orders_data()
    if df_orders is None:
        return {"error": "Arquivo 'orders.json' não encontrado."}

    total_orders = len(df_orders)
    total_revenue = df_orders['total_value'].sum()
    average_ticket = total_revenue / total_orders if total_orders > 0 else 0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "average_ticket": round(average_ticket, 2)
    }

@app.get("/api/performance/by_sales_channel")
def get_performance_by_channel():
    """Endpoint que retorna a performance por canal de venda."""
    df_orders = load_orders_data()
    if df_orders is None:
        return {"error": "Arquivo 'orders.json' não encontrado."}

    revenue_by_channel = df_orders.groupby('salesChannel')['total_value'].sum()
    formatted_data = revenue_by_channel.round(2).to_dict()

    return formatted_data
