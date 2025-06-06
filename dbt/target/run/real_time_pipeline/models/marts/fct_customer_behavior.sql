
  create view "transactions"."public"."fct_customer_behavior__dbt_tmp"
    
    
  as (
    with transactions as (
    select * from "transactions"."public"."stg_fact_transaction"
),

customers as (
    select * from "transactions"."public"."stg_customer"
),

enriched as (
    select
        t.customer_id,
        c.registered_at,
        t.transaction_ts,
        t.amount,
        t.is_fraud,
        t.is_foreign
    from transactions t
    left join customers c
        on t.customer_id = c.customer_id
),

customer_metrics as (
    select
        customer_id,
        min(registered_at) as registered_at,
        count(*) as total_transactions,
        sum(amount) as total_spent,
        avg(amount) as avg_transaction_amount,
        max(amount) as max_transaction_amount,
        min(amount) as min_transaction_amount,
        sum(case when is_fraud then 1 else 0 end) as fraud_transactions,
        round(
            case 
                when count(*) = 0 then 0
                else sum(case when is_fraud then 1 else 0 end)::decimal / count(*)
            end, 
            3
        ) as fraud_ratio,
        sum(case when is_foreign then 1 else 0 end) as foreign_tx_count
    from enriched
    group by customer_id
)

select * from customer_metrics
  );