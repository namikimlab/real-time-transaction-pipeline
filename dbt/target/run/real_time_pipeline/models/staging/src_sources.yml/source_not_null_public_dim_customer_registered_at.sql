select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select registered_at
from "transactions"."public"."dim_customer"
where registered_at is null



      
    ) dbt_internal_test