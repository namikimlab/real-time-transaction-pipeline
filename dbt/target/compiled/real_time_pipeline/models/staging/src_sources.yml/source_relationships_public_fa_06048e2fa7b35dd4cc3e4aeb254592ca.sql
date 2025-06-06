
    
    

with child as (
    select merchant_id as from_field
    from "transactions"."public"."fact_transaction"
    where merchant_id is not null
),

parent as (
    select merchant_id as to_field
    from "transactions"."public"."dim_merchant"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


