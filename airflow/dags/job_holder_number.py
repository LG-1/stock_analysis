import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))  # add root path
sys.path.append(os.path.abspath(os.getcwd()))  # add root path

from utils.stock_markets import get_all_codes


default_args = {
    'owner': 'LG',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(minutes=20),
    'email': ['ourantech@163.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

# dag = DAG('tutorial', default_args=default_args, schedule_interval=timedelta(weeks=1))

dag = DAG('job_holder_number', default_args=default_args,
          schedule_interval=timedelta(minutes=3))


task = PythonOperator(
    task_id='get_all_codes_airflow',
    python_callable=get_all_codes,
    op_kwargs={},
    dag=dag,
)

task
