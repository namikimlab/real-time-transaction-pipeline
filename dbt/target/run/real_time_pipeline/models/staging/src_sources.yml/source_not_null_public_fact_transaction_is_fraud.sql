select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select is_fraud
from "transactions"."public"."fact_transaction"
where is_fraud is null



      
    ) dbt_internal_test