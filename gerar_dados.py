# Arquivo: gerar_dados.py
import pandas as pd
import faker
import random
import json
from datetime import datetime, timedelta
from pathlib import Path

# Garante que a pasta /data exista
Path("data").mkdir(exist_ok=True)

fake = faker.Faker('pt_BR')

STORES = [
    {'id': 'store-001', 'name': 'Cantina da Nona'},
    {'id': 'store-002', 'name': 'Sushi Express'},
    {'id': 'store-003', 'name': 'Burger Place'}
]
NUM_ORDERS = 1000
orders = []

for i in range(NUM_ORDERS):
    order_datetime = datetime.now() - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
    orders.append({
        'id': f'order-{i+1}',
        'companyId': random.choice(STORES)['id'],
        'createdAt': order_datetime.isoformat(),
        'customer': {'id': f'cust-{random.randint(1, 200)}', 'name': fake.name()},
        'orderType': random.choice(['DELIVERY', 'INDOOR', 'TAKEOUT']),
        'salesChannel': random.choice(['IFOOD', 'EPADOCA', 'ANOTAAI']),
        'status': 'CONCLUDED',
        'total': {'total': round(random.uniform(25.0, 450.0), 2)}
    })

# Salva o arquivo dentro da pasta /data
with open('data/orders.json', 'w', encoding='utf-8') as f:
    json.dump(orders, f, ensure_ascii=False, indent=4)

print(f"Arquivo 'orders.json' com {len(orders)} pedidos foi gerado dentro da pasta /data.")