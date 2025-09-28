SELECT
    tx_date,
    fraud_count,
    ROUND((fraud_count::decimal / NULLIF(tx_count, 0)), 3) AS fraud_ratio
FROM public.fct_daily_revenue
ORDER BY tx_date DESC;