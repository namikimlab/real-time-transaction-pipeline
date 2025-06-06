SELECT
    merchant_id,
    total_transactions,
    fraud_transactions,
    fraud_ratio,
    total_sales
FROM public.fct_merchant_behavior
ORDER BY fraud_ratio DESC
LIMIT 50;