with source as (
    select * from "transactions"."public"."dim_customer"
)

select
    customer_id,
    customer_name,
    customer_email,
    registered_at::timestamp as registered_at
from source