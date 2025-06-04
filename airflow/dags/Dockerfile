FROM apache/airflow:2.9.0

# Install dbt
USER root
RUN pip install dbt-core==1.7.9 dbt-postgres==1.7.9 psycopg2-binary==2.9.10

USER airflow
