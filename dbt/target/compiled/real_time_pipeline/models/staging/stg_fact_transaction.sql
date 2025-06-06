with source as (
    select * from "transactions"."public"."fact_transaction"
)

select
    transaction_id,
    timestamp::timestamp as transaction_ts,
    customer_id,
    merchant_id,
    amount,
    currency,
    latitude,
    longitude,
    device_id,
    payment_method,
    is_foreign,
    is_fraud
from source