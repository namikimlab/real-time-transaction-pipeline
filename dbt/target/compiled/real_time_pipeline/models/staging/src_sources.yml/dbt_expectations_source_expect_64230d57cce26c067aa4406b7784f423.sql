






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and longitude >= -125.0 and longitude <= -66.0
)
 as expression


    from "transactions"."public"."fact_transaction"
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors







