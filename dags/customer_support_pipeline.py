import sys

sys.path.append("/opt/airflow/project")

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from pipeline import run_pipeline


default_args = {
    "owner": "Santhoshini",
    "depends_on_past": False,
    "retries": 1,
}


with DAG(

    dag_id="customer_support_pipeline",

    default_args=default_args,

    description="Customer Support Analytics Pipeline",

    start_date=datetime(2026, 7, 1),

    schedule=None,

    catchup=False,

    tags=["portfolio", "data-engineering"],

) as dag:

    pipeline_task = PythonOperator(

        task_id="run_customer_support_pipeline",

        python_callable=run_pipeline,

    )