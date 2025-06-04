import json
import random
import uuid
import time
from datetime import datetime
from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'localhost:9092'})

payment_methods = ["credit_card", "debit_card", "apple_pay", "google_pay"]

def generate_transaction():
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "customer_id": str(uuid.uuid4()),
        "merchant_id": str(uuid.uuid4()),
        "amount": round(random.uniform(10, 5000), 2),
        "currency": "USD",
        "location": {
            "lat": round(random.uniform(-90, 90), 6),
            "lon": round(random.uniform(-180, 180), 6)
        },
        "device_id": str(uuid.uuid4()),
        "payment_method": random.choice(payment_methods),
        "is_foreign": random.choice([True, False])
    }
    return transaction

def delivery_report(err, msg):
    if err is not None:
        print('Delivery failed:', err)
    else:
        print('Delivered message to', msg.topic())

while True:
    txn = generate_transaction()
    p.produce('transactions', json.dumps(txn).encode('utf-8'), callback=delivery_report)
    p.poll(0)
    time.sleep(0.5)
