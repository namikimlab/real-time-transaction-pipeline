select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select customer_email
from "transactions"."public"."dim_customer"
where customer_email is null



      
    ) dbt_internal_test