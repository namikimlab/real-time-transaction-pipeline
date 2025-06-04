SELECT
  tx_date,
  tx_count,
  total_amount,
  fraud_count
FROM fct_daily_revenue
ORDER BY tx_date DESC
