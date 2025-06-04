# Those are your lookup dimensions.
# In real systems: customer & merchant master data come from operational systems.
# You want them seeded before transactions start 

import psycopg2
import uuid
from faker import Faker
import os
from dotenv import load_dotenv, find_dotenv

# Get absolute path to project root (2 levels up for example)   
load_dotenv(find_dotenv())

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cur = conn.cursor()

# Seed customers
for _ in range(100):
    customer_id = uuid.uuid4()
    cur.execute("""
        INSERT INTO dim_customer (customer_id, customer_name, customer_email, registered_at)
        VALUES (%s, %s, %s, %s)
    """, (
        str(customer_id),
        fake.name(),
        fake.email(),
        fake.date_time_this_decade()
    ))

# Seed merchants
for _ in range(20):
    merchant_id = uuid.uuid4()
    cur.execute("""
        INSERT INTO dim_merchant (merchant_id, merchant_name, merchant_category, country)
        VALUES (%s, %s, %s, %s)
    """, (
        str(merchant_id),
        fake.company(),
        fake.random_element(["Retail", "Food", "Travel", "Entertainment", "Tech"]),
        fake.country()
    ))

conn.commit()
cur.close()
conn.close()
