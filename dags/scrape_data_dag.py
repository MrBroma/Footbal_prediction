from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys

from scraping_loic import scrape_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'scrape_data_dag',
    default_args=default_args,
    description='A simple DAG to scrape data every minute',
    schedule_interval='* * * * *',  # Run every minute
    start_date=datetime(2024, 9, 10),  # Start date of the DAG
    catchup=False,
)

run_scraper = PythonOperator(
    task_id='run_scraper',
    python_callable=scrape_data,
    dag=dag,
)

run_scraper
