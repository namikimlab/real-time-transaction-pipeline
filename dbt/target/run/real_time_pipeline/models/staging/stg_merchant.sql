
  create view "transactions"."public"."stg_merchant__dbt_tmp"
    
    
  as (
    with source as (
    select * from "transactions"."public"."dim_merchant"
)

select
    merchant_id,
    merchant_name,
    merchant_category,
    country
from source
  );