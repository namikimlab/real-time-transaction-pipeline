
      
  
    

  create  table "transactions"."public"."fct_daily_fraud_summary"
  
  
    as
  
  (
    with transactions as (
    select * from "transactions"."public"."stg_fact_transaction"
    
),

daily_fraud as (
    select
        date_trunc('day', transaction_ts) as tx_date,
        count(*) as total_tx,
        sum(case when is_fraud then 1 else 0 end) as fraud_tx,
        round(
            case 
                when count(*) = 0 then 0
                else sum(case when is_fraud then 1 else 0 end)::decimal / count(*)
            end, 
            3
        ) as fraud_rate
    from transactions
    group by 1
)

select * from daily_fraud
order by tx_date desc
  );
  
  