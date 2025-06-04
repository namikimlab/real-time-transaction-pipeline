import psycopg2
import uuid
from faker import Faker

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="transactions",
    user="admin",
    password="admin"
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
