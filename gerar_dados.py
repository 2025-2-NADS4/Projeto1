# Arquivo: gerar_dados.py (versão robusta)
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import faker
import uuid

# --- INICIALIZAÇÃO ---
print("Iniciando a geração de dados robustos...")
fake = faker.Faker('pt_BR')
Path("data").mkdir(exist_ok=True)

# --- DADOS BASE ---
STORES = [{'id': str(uuid.uuid4()), 'name': 'Cantina da Nona'}, {'id': str(uuid.uuid4()), 'name': 'Sushi Express'}, {'id': str(uuid.uuid4()), 'name': 'Burger Place'}]
SAMPLE_PRODUCTS = [
    {'name': 'Pizza Margherita', 'price': 55.00}, {'name': 'Combinado Sushi (20 peças)', 'price': 89.90},
    {'name': 'Cheeseburger Duplo', 'price': 38.50}, {'name': 'Refrigerante Lata', 'price': 6.00},
    {'name': 'Cerveja Long Neck', 'price': 12.00}, {'name': 'Porção de Fritas', 'price': 25.00},
    {'name': 'Tiramisù', 'price': 22.00}, {'name': 'Temaki Salmão', 'price': 32.00}
]

# --- 1. GERAR CLIENTES (customers.json) ---
def generate_customers(num_customers=200):
    customers = []
    for _ in range(num_customers):
        customers.append({
            "id": str(uuid.uuid4()),
            "name": fake.name(),
            "taxId": fake.cpf(),
            "gender": random.choice(["Male", "Female", "Other"]),
            "dateOfBirth": fake.date_of_birth(minimum_age=18, maximum_age=75).isoformat(),
            "status": 1,  # Active
            "createdAt": fake.date_time_between(start_date="-2y").isoformat(),
        })
    with open('data/customers.json', 'w', encoding='utf-8') as f:
        json.dump(customers, f, ensure_ascii=False, indent=4)
    print(f"-> Gerado 'customers.json' com {len(customers)} clientes.")
    return customers

# --- 2. GERAR CAMPANHAS (campaigns.json) ---
def generate_campaigns(stores, num_campaigns=15):
    campaigns = []
    for _ in range(num_campaigns):
        campaigns.append({
            "id": str(uuid.uuid4()),
            "storeId": random.choice(stores)['id'],
            "name": f"Campanha de {random.choice(['Dia dos Pais', 'Fidelidade', 'Happy Hour', 'Lançamento'])}",
            "badge": random.choice(["loyalty", "consumption", "seasonal"]),
            "type": random.choice([1, 2]),  # 1: Promocional, 2: Institucional
            "status": random.choice([3, 4]),  # 3: Publicado, 4: Completado
            "createdAt": fake.date_time_between(start_date="-1y").isoformat(),
        })
    with open('data/campaigns.json', 'w', encoding='utf-8') as f:
        json.dump(campaigns, f, ensure_ascii=False, indent=4)
    print(f"-> Gerado 'campaigns.json' com {len(campaigns)} campanhas.")
    return campaigns

# --- 3. GERAR FILA DE CAMPANHAS (campaign_queue.json) ---
def generate_campaign_queue(customers, campaigns, num_entries=500):
    queue = []
    for _ in range(num_entries):
        customer = random.choice(customers)
        campaign = random.choice(campaigns)
        send_time = fake.date_time_between(start_date="-6m")
        queue.append({
            "id": str(uuid.uuid4()),
            "jobId": str(uuid.uuid4()),
            "campaignId": campaign['id'],
            "storeId": campaign['storeId'],
            "customerId": customer['id'],
            "phoneNumber": fake.phone_number(),
            "scheduledAt": send_time.isoformat(),
            "sendAt": (send_time + timedelta(minutes=random.randint(1, 5))).isoformat(),
            "status": random.choice([2, 3, 4]),  # 2: Send, 3: Received, 4: Read
            "message": "Aproveite nossa promoção especial!",
        })
    with open('data/campaign_queue.json', 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=4)
    print(f"-> Gerado 'campaign_queue.json' com {len(queue)} envios.")
    return queue

# --- 4. GERAR PEDIDOS (orders.json) ---
def generate_orders(customers, stores, num_orders=1500):
    orders = []
    for _ in range(num_orders):
        customer = random.choice(customers)
        store = random.choice(stores)
        order_datetime = fake.date_time_between(start_date="-1y")
        
        # Gera itens e calcula o subtotal
        order_items = []
        subtotal = 0
        for _ in range(random.randint(1, 4)):
            product = random.choice(SAMPLE_PRODUCTS)
            quantity = random.randint(1, 3)
            item_total = product['price'] * quantity
            order_items.append({
                "name": product['name'],
                "quantity": quantity,
                "price": product['price'],
                "total": item_total
            })
            subtotal += item_total

        delivery_fee = 10.00 if random.random() > 0.5 else 0
        total_order_value = subtotal + delivery_fee

        orders.append({
            "id": str(uuid.uuid4()),
            "companyId": store['id'],
            "createdAt": order_datetime.isoformat(),
            "customer": { "id": customer['id'], "name": customer['name'] },
            "orderType": random.choice(['DELIVERY', 'INDOOR', 'TAKEOUT']),
            "salesChannel": random.choice(['IFOOD', 'EPADOCA', 'ANOTAAI']),
            "status": random.choices(['CONCLUDED', 'CANCELED'], weights=[0.9, 0.1], k=1)[0],
            "items": order_items,
            "payments": [{
                "method": random.choice(['CREDIT_CARD', 'DEBIT_CARD', 'PIX']),
                "value": total_order_value
            }],
            "total": {
                "subtotal": subtotal,
                "deliveryFee": delivery_fee,
                "total": total_order_value
            }
        })
    with open('data/orders.json', 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)
    print(f"-> Gerado 'orders.json' com {len(orders)} pedidos detalhados.")
    return orders

# --- EXECUÇÃO ---
if __name__ == "__main__":
    customers_data = generate_customers()
    campaigns_data = generate_campaigns(STORES)
    generate_campaign_queue(customers_data, campaigns_data)
    generate_orders(customers_data, STORES)
    print("\nGeração de dados robustos concluída com sucesso!")