from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from utils.scraping_loic import scrape_data
from utils.clean_csv_loic import clean
from utils.merge_csv_loic import merge_sorting

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
    schedule_interval='*/1 * * * *',
    start_date=datetime(2024, 9, 12),
    max_active_tasks=1,
    catchup=False,
)

run_scraper = PythonOperator(
    task_id='run_scraper',
    python_callable=scrape_data,
    dag=dag,
)

clean_csv = PythonOperator(
    task_id='clean_csv',
    python_callable=clean,
    dag=dag,
)

final_csv = PythonOperator(
    task_id='merge_sorting',
    python_callable=merge_sorting,
    dag=dag,
)

run_scraper >> clean_csv >> final_csv

