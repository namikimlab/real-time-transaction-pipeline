with tx as (
    select * from {{ ref('stg_fact_transaction') }}
)

select
    date_trunc('day', transaction_ts) as tx_date,
    count(*) as tx_count,
    sum(amount) as total_amount,
    sum(case when is_fraud then 1 else 0 end) as fraud_count
from tx
group by 1
order by 1 desc
