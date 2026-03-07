from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import requests
import json
import logging

logger = logging.getLogger(__name__)

default_args = {
    'owner': 'sree',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_cso_data(**context):
    url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FY001/JSON-stat/2.0/en"
    logger.info("Fetching CSO population data...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    record_count = len(data.get('value', []))
    logger.info(f"✅ Fetched {record_count} values from CSO API")
    context['ti'].xcom_push(key='record_count', value=record_count)
    return record_count

def validate_data(**context):
    record_count = context['ti'].xcom_pull(key='record_count', task_ids='fetch_cso_data')
    logger.info(f"Validating data — record count: {record_count}")
    if not record_count or record_count < 100:
        raise ValueError(f"Data validation failed — only {record_count} records fetched")
    logger.info(f"✅ Validation passed — {record_count} records")

with DAG(
    dag_id='cso_population_pipeline',
    default_args=default_args,
    description='Fetch CSO Census data and validate',
    schedule_interval='@weekly',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['cso', 'ireland', 'population'],
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_cso_data',
        python_callable=fetch_cso_data,
    )

    validate_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )

    fetch_task >> validate_task