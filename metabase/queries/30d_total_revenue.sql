SELECT
    SUM(total_amount) AS total_revenue_30d
FROM public.fct_daily_revenue
WHERE tx_date >= CURRENT_DATE - INTERVAL '30 days';
