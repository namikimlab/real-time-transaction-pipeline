
    
    

select
    merchant_id as unique_field,
    count(*) as n_records

from "transactions"."public"."dim_merchant"
where merchant_id is not null
group by merchant_id
having count(*) > 1


