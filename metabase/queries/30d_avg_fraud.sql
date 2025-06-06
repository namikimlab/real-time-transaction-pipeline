SELECT
    AVG(fraud_rate) AS avg_fraud_30d
FROM public.fct_daily_fraud_summary
WHERE tx_date >= CURRENT_DATE - INTERVAL '30 days';
