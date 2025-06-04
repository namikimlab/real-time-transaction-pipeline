# Real-Time Transaction Monitoring Pipeline

🚀 **Full-Stack Streaming Data Engineering Portfolio Project**

---

## Architecture

- Kafka (KRaft mode)
- Spark Structured Streaming (Real-Time ETL)
- Postgres OLAP (Fact-Dimension schema)
- dbt (Data Modeling)
- Airflow (Batch Orchestration)
- Metabase (BI Dashboard)
- Docker Compose (Full stack deployment)

---

## Use Case

Simulates real-time payment transaction system with real-time fraud detection + daily revenue aggregations.

---

## Pipeline Diagram

*(add your architecture diagram here — I can generate one for you if you want)*

---

## Streaming Logic

- Simulated transaction generator (Kafka Producer)
- Spark Structured Streaming reads from Kafka
- Real-time fraud detection logic:
  - High amount threshold
  - Foreign transaction flag
  - Suspicious lat/lon coordinates
- Writes to OLAP Postgres

---

## Batch Logic

- dbt runs daily aggregations
- Airflow orchestrates dbt jobs
- Metabase dashboards for business analytics

---

## Tech Stack

- Kafka (7.5.0 KRaft)
- Spark 3.5.0
- dbt 1.7.9
- Airflow 2.9.0
- Postgres 15
- Metabase latest
- Docker Compose

---

## Setup

```bash
git clone ...
docker compose up -d
# seed dim tables:
cd postgres
python seed_dim_tables.py
```

## Dashboard Previews

## Key Skills Demonstrated
- Full end-to-end streaming + batch integration
- Streaming fraud detection logic
- OLAP schema design with fact/dim structure
- dbt modeling best practices (staging → marts)
- Airflow orchestration inside Docker
- Docker Compose multi-service deployment
- Metabase BI dashboard creation
- Real-world system design patterns

## Future Extensions
- Kafka Connect CDC ingestion
- ML-based fraud scoring
- Kubernetes deployment
- Prometheus + Grafana monitoring
- Cloud-native version (GCP / AWS)