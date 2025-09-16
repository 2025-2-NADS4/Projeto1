# Arquivo: src/backend/main.py (versão robusta)
from fastapi import FastAPI
import pandas as pd
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

app = FastAPI(title="API do Dashboard Cannoli")

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data"

# --- Funções para Carregar Dados ---
def load_data(filename):
    """Função genérica para carregar um arquivo JSON para um DataFrame."""
    try:
        df = pd.read_json(DATA_PATH / filename)
        # Converte colunas de data que existem em múltiplos arquivos
        if 'createdAt' in df.columns:
            df['createdAt'] = pd.to_datetime(df['createdAt'])
        return df
    except FileNotFoundError:
        return None

# --- Endpoints da API Atualizados ---

@app.get("/api/kpis/gerais")
def get_general_kpis():
    df_orders = load_data('orders.json')
    df_customers = load_data('customers.json')

    if df_orders is None or df_customers is None:
        return {"error": "Arquivos de dados não encontrados."}

    df_concluded = df_orders[df_orders['status'] == 'CONCLUDED'].copy()

    # Extrai o valor total do objeto 'total'
    df_concluded['total_value'] = df_concluded['total'].apply(lambda x: x.get('total', 0))

    total_revenue = df_concluded['total_value'].sum()
    total_orders = len(df_concluded)
    average_ticket = total_revenue / total_orders if total_orders > 0 else 0

    # Novos KPIs usando os múltiplos arquivos
    thirty_days_ago = datetime.now() - timedelta(days=30)
    new_customers_last_30d = len(df_customers[df_customers['createdAt'] >= thirty_days_ago])

    total_canceled = len(df_orders[df_orders['status'] == 'CANCELED'])
    cancellation_rate = (total_canceled / len(df_orders)) * 100 if len(df_orders) > 0 else 0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "average_ticket": round(average_ticket, 2),
        "new_customers_last_30d": new_customers_last_30d, # NOVO KPI
        "cancellation_rate": round(cancellation_rate, 2)
    }

@app.get("/api/performance/revenue_last_7_days")
def get_revenue_last_7_days():
    df_orders = load_data('orders.json')
    if df_orders is None: return {}

    df_concluded = df_orders[df_orders['status'] == 'CONCLUDED'].copy()
    df_concluded['total_value'] = df_concluded['total'].apply(lambda x: x.get('total', 0))

    seven_days_ago = datetime.now() - timedelta(days=7)
    df_recent = df_concluded[df_concluded['createdAt'] >= seven_days_ago]

    revenue_by_day = df_recent.set_index('createdAt').resample('D')['total_value'].sum()
    revenue_by_day.index = revenue_by_day.index.strftime('%Y-%m-%d')

    return revenue_by_day.round(2).to_dict()

@app.get("/api/orders/recent")
def get_recent_orders():
    df_orders = load_data('orders.json')
    if df_orders is None: return []

    df_recent = df_orders.sort_values(by='createdAt', ascending=False).head(5)

    # Extrai os valores dos objetos aninhados
    df_recent['customer_name'] = df_recent['customer'].apply(lambda x: x.get('name'))
    df_recent['total_value'] = df_recent['total'].apply(lambda x: x.get('total', 0))

    result = df_recent[['id', 'customer_name', 'total_value', 'status']]
    result = result.rename(columns={'id': 'orderId', 'total_value': 'value'})

    return result.to_dict(orient='records')

# Você pode adicionar os outros endpoints (by_type, by_sales_channel) aqui,
# adaptando-os da mesma forma se precisar deles.