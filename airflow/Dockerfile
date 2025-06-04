FROM apache/airflow:2.9.0

USER root

# Install any OS-level dependencies (if needed, none for now)

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt