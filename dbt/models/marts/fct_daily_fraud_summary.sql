with tx as (
    select * from {{ ref('stg_fact_transaction') }}
)

select
    customer_id,
    count(*) as total_transactions,
    sum(case when is_fraud then 1 else 0 end) as fraud_transactions,
    round(sum(case when is_fraud then 1 else 0 end)::decimal / count(*), 3) as fraud_ratio
from tx
group by customer_id
order by fraud_ratio desc
