with transactions as (
    select * from {{ ref('stg_fact_transaction') }}
    {% if is_incremental() %}
      where transaction_ts > coalesce((select max(transaction_ts) from {{ this }}), '1900-01-01')
    {% endif %}
),

merchants as (
    select * from {{ ref('stg_merchant') }}
),

enriched as (
    select
        t.merchant_id,
        m.merchant_name,
        m.merchant_category,
        m.country,
        t.amount,
        t.is_fraud
    from transactions t
    left join merchants m
        on t.merchant_id = m.merchant_id
),

merchant_metrics as (
    select
        merchant_id,
        merchant_name,
        merchant_category,
        country,
        count(*) as total_transactions,
        sum(amount) as total_sales,
        sum(case when is_fraud then 1 else 0 end) as fraud_transactions,
        round(
            sum(case when is_fraud then 1 else 0 end)::decimal / count(*), 3
        ) as fraud_ratio
    from enriched
    group by merchant_id, merchant_name, merchant_category, country
)

select * from merchant_metrics
order by fraud_ratio desc
