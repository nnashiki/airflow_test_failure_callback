import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import datetime


def all_time_success():
    print('hello')

def all_time_fail():
    raise Exception('エラーだ!!')

def dag_on_failure_callback(context):
    print('ダグが失敗した時')

def task_on_failure_callback(context):
    print('タスクが失敗した時')

default_args = {
    "owner": "airflow",
    "start_date": airflow.utils.dates.days_ago(1),
}

with DAG(
        dag_id="sample_dag",
        on_failure_callback=dag_on_failure_callback,
        default_args=default_args) as dag:

    success_task = PythonOperator(
        task_id="success_task",
        python_callable=all_time_success
    )

    fail_task = PythonOperator(
        task_id="fail_task",
        python_callable=all_time_fail,
        on_failure_callback=task_on_failure_callback
    )

    success_task >> fail_task
