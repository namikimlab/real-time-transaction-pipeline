# 📊 Dashboard Structure - Fraud & Revenue Monitoring

This document describes the structure of the Metabase dashboard built for real-time fraud detection and revenue monitoring.

---

## 📋 Dashboard Name

**Fraud & Revenue Monitoring Dashboard**

---

This dashboard simulates a real-time transaction monitoring use case with both revenue and fraud detection metrics.


## 🔢 KPI Cards

### 1️⃣ 30d Total Revenue

- Metric: Sum of `total_amount` over the past 30 days
- Data Source: `fct_daily_revenue`

### 2️⃣ 30d Avg Fraud Ratio

- Metric: Average `fraud_ratio` over the past 30 days
- Data Source: `fct_daily_fraud_summary`


---

## 📈 Trend Charts

### 3️⃣ Daily Revenue

- Line chart: `total_amount` (left Y-axis), `tx_count` (right Y-axis)
- Time dimension: `tx_date`
- Data Source: `fct_daily_revenue`

### 4️⃣ Daily Fraud

- Line chart: `fraud_count` (left Y-axis), `fraud_ratio` (right Y-axis)
- Time dimension: `tx_date`
- Data Source: `fct_daily_fraud_summary`

---

## 🔍 Tables

### 5️⃣ High Risk Customers

- Columns:
  - `customer_id`
  - `total_transactions`
  - `fraud_transactions`
  - `fraud_ratio`
- Sort: `fraud_ratio DESC`
- Data Source: `fct_customer_behavior`

### 6️⃣ High Risk Merchants

- Columns:
  - `merchant_id`
  - `total_transactions`
  - `fraud_transactions`
  - `fraud_ratio`
- Sort: `fraud_ratio DESC`
- Data Source: `fct_merchant_behavior`

---

## 💡 Notes

- ✅ All data sources are from **dbt marts layer**, fully incremental.
- ✅ Updated daily via Airflow dbt DAG.
- ✅ Transactions flow through Kafka -> Spark -> Postgres -> dbt -> Metabase.



