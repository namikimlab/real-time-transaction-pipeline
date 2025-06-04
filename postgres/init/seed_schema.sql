-- Dimension: customer
CREATE TABLE dim_customer (
    customer_id UUID PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    registered_at TIMESTAMP
);

-- Dimension: merchant
CREATE TABLE dim_merchant (
    merchant_id UUID PRIMARY KEY,
    merchant_name TEXT,
    merchant_category TEXT,
    country TEXT
);

-- Fact: transactions
CREATE TABLE fact_transaction (
    transaction_id UUID PRIMARY KEY,
    timestamp TIMESTAMP,
    customer_id UUID REFERENCES dim_customer(customer_id),
    merchant_id UUID REFERENCES dim_merchant(merchant_id),
    amount NUMERIC(10, 2),
    currency TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    device_id UUID,
    payment_method TEXT,
    is_foreign BOOLEAN,
    is_fraud BOOLEAN DEFAULT FALSE
);
