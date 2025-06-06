
    
    

with all_values as (

    select
        payment_method as value_field,
        count(*) as n_records

    from "transactions"."public"."fact_transaction"
    group by payment_method

)

select *
from all_values
where value_field not in (
    'credit_card','debit_card','apple_pay','google_pay'
)


