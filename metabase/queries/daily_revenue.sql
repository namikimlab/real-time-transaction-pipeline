SELECT
    tx_date,
    total_amount,
    tx_count
FROM public.fct_daily_revenue
ORDER BY tx_date DESC;
