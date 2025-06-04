# Metabase Setup Instructions

## DB Connection

- Host: postgres
- Port: 5432
- DB: transactions
- User: POSTGRES_USER
- Password: POSTGRES_PASSWORD

## Dashboards

### 1️⃣ Daily Revenue Dashboard
- Query: `queries/daily_revenue.sql`
- Visual: Line chart for revenue, bar chart for fraud count

### 2️⃣ Fraud Summary Dashboard
- Query: `queries/fraud_summary.sql`
- Visual: Table / leaderboard of top risky customers

### 3️⃣ Recent Transactions (Optional)
- Query directly from `fact_transaction`
