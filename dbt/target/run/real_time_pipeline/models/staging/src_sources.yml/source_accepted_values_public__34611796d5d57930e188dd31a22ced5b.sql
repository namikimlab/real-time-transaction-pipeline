select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        is_fraud as value_field,
        count(*) as n_records

    from "transactions"."public"."fact_transaction"
    group by is_fraud

)

select *
from all_values
where value_field not in (
    'True','False'
)



      
    ) dbt_internal_test