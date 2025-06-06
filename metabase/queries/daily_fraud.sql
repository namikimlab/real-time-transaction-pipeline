SELECT
  customer_id,
  total_transactions,
  fraud_transactions,
  fraud_ratio
FROM fct_daily_fraud_summary
ORDER BY fraud_ratio DESC
LIMIT 10
