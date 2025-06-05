# Emits synthetic transactions into Kafka topic transactions
# Uses actual customer and merchant UUIDs from dimension tables

import os
import json
import random
import time
import sys
import uuid
from datetime import datetime
from confluent_kafka import Producer
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuration
MESSAGE_LIMIT = None  # Infinite
DELAY_BETWEEN_MESSAGES = 3  # Every 3 seconds
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Database connection settings
DB_CONFIG = {
    'host': 'postgres',
    'port': 5432,
    'database': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD')
}

payment_methods = ["credit_card", "debit_card", "apple_pay", "google_pay"]

def load_dimension_data():
    """Load customer and merchant UUIDs from database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        customer_uuids = [row['customer_id'] for row in cur.fetchall()]
        merchant_uuids = [row['merchant_id'] for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        print(f"📊 Loaded {len(customer_uuids)} customers and {len(merchant_uuids)} merchants from database")
        return customer_uuids, merchant_uuids
        
    except Exception as e:
        print(f"⚠️ Failed to load dimension data from database: {e}")
        print("🔄 Using fallback: generating random UUIDs")
        # Fallback to random UUIDs
        customer_uuids = [str(uuid.uuid4()) for _ in range(1000)]
        merchant_uuids = [str(uuid.uuid4()) for _ in range(50)]
        return customer_uuids, merchant_uuids

def create_producer_with_retry(max_retries=20, delay=5):
    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempting to connect to Kafka (attempt {attempt + 1}/{max_retries})...")
            p = Producer({'bootstrap.servers': bootstrap_servers})  
            
            # Test the connection
            metadata = p.list_topics(timeout=15)
            print(f"✅ Connected to Kafka successfully on attempt {attempt + 1}")
            print(f"📋 Available topics: {list(metadata.topics.keys())}")
            return p
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("💥 Max retries reached. Exiting.")
                sys.exit(1)

def generate_transaction(customer_uuids, merchant_uuids):
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "customer_id": random.choice(customer_uuids),
        "merchant_id": random.choice(merchant_uuids),
        "amount": round(random.uniform(5.99, 299.99), 2),
        "currency": "USD",
        "location": {
            "lat": round(random.uniform(25.0, 49.0), 6),
            "lon": round(random.uniform(-125.0, -66.0), 6)
        },
        "device_id": str(uuid.uuid4()),
        "payment_method": random.choice(payment_methods),
        "is_foreign": random.choices([True, False], weights=[10, 90])[0]
    }
    return transaction

def delivery_report(err, msg):
    if err is not None:
        print(f'❌ Delivery failed: {err}')
    else:
        print(f'✅ Message delivered to {msg.topic()}[{msg.partition()}] at offset {msg.offset()}')

# Main execution
if __name__ == "__main__":
    print("🚀 Starting transaction producer...")
    
    # Load dimension data
    customer_uuids, merchant_uuids = load_dimension_data()
    
    if not customer_uuids or not merchant_uuids:
        print("❌ No dimension data available. Exiting.")
        sys.exit(1)
    
    # Initialize producer
    p = create_producer_with_retry()
    
    # Main loop
    counter = 0
    try:
        print(f"📊 Starting to produce {MESSAGE_LIMIT if MESSAGE_LIMIT else 'unlimited'} transactions...")
        
        while True:
            txn = generate_transaction(customer_uuids, merchant_uuids)
            try:
                p.produce('transactions', json.dumps(txn).encode('utf-8'), callback=delivery_report)
                p.poll(0)
            except Exception as e:
                print(f"⚠️ Failed to produce message {counter}: {e}")
            
            time.sleep(DELAY_BETWEEN_MESSAGES)
            counter += 1
            
            if counter % 10 == 0:
                print(f"📈 Produced {counter} transactions...")
            
            if MESSAGE_LIMIT is not None and counter >= MESSAGE_LIMIT:
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal. Shutting down producer...")
    finally:
        print("⏳ Flushing remaining messages...")
        p.flush()
        print(f"✨ Producer stopped. Total messages produced: {counter}")