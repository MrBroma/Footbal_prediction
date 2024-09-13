from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from utils.test import create_table_if_not_exists
from utils.test import insert_data_to_db


# Configuration des arguments par défaut du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'db_insertion_dag',
    default_args=default_args,
    description='A simple DAG to scrape data every minute',
    schedule_interval='*/1 * * * *',
    start_date=datetime(2024, 9, 12),
    max_active_tasks=1,
    catchup=False,
)

# Task to load data and create table
load_data_task = PythonOperator(
    task_id='load_football_data',
    python_callable=insert_data_to_db,
    dag=dag,
)


load_data_task