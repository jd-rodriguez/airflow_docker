from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import time
from textwrap import dedent

sources = {'bsre','cat','pre','eaeaz','fsqfqf','wcccw','dqsdqsd','gdgfg','hfghfg','yryrty','jghjg','xsxsxqc'}
etapes = {'get_data','proccess_data','print_proccesed_data'}
groups={}
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

def task_pause():
    time.sleep(60)

with DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
    concurrency=10,
) as dag:

    for source in sources :
        with TaskGroup(source) as groups[source]:
        
            task_get_data=PythonOperator(
                task_id=source+'_get_data',
                python_callable=task_pause
            )

            task_proccess_data=PythonOperator(
                task_id=source+'_proccess_data',
                python_callable=task_pause
            )

            task_print_proccesed_data=PythonOperator(
                task_id=source+'_print_proccesed_data',
                python_callable=task_pause
            )
            task_get_data>>task_proccess_data>>task_print_proccesed_data        

