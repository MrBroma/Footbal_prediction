from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/utils/')


from utils.main import run_scrape_and_download, run_merge_csv_files, run_process_and_save_csv, run_load_csv_to_sqlite



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'web_scraping_dag',
    default_args=default_args,
    description='A DAG for web scraping, merging CSV files, processing them, and uploading to SQLite',
    schedule_interval='@daily',
    catchup=False,
)

scrape_task = PythonOperator(
    task_id='scrape_and_download_task',
    python_callable= run_scrape_and_download,
    dag=dag,
)

merge_task = PythonOperator(
    task_id = 'merge_csv_files_task',
    python_callable= run_merge_csv_files,
    dag = dag
)

process_task = PythonOperator(
    task_id = 'process_and_save_csv_task',
    python_callable= run_process_and_save_csv,
    dag = dag,
)

load_task = PythonOperator(
    task_id = 'load_csv_to_sqlite_task',
    python_callable= run_load_csv_to_sqlite,
    dag = dag,
)


scrape_task >> merge_task >> process_task >> load_task
