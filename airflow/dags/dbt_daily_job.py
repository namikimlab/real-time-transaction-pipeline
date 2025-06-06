from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dbt_daily_models',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    run_dbt_deps = BashOperator(
        task_id='run_dbt_deps',
        bash_command='cd /opt/airflow/dbt && dbt deps'
    )

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/dbt && dbt run'
    )

    test_dbt = BashOperator(
        task_id='test_dbt_models',
        bash_command='cd /opt/airflow/dbt && dbt test'
    )

    run_dbt_deps >> run_dbt >> test_dbt
