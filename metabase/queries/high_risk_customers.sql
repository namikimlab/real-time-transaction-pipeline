SELECT
    customer_id,
    total_transactions,
    fraud_transactions,
    fraud_ratio,
    total_spent
FROM public.fct_customer_behavior
ORDER BY fraud_ratio DESC
LIMIT 50;