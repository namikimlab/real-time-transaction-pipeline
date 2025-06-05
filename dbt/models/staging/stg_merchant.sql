with source as (
    select * from {{ source('public', 'dim_merchant') }}
)

select
    merchant_id,
    merchant_name,
    merchant_category,
    country
from source
