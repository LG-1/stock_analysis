import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))  # add root path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))  # add root path
sys.path.append(os.path.abspath(os.getcwd()))  # add root path
print(sys.path)

from tasks.update_holdernumber import update_holdernumber


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


dag = DAG('update_holdernumber', default_args=default_args,
          schedule_interval=timedelta(minutes=24*60))


task = PythonOperator(
    task_id='update_holdernumber',
    python_callable=update_holdernumber(),
    op_kwargs={},
    dag=dag,
)

task
