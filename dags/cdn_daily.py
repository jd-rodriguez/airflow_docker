from airflow import DAG
from commons.cdn_daily_functions import import_process
from commons.cdn_daily_functions import run_scenarios
from datetime import datetime, timedelta
import os
import json

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

with DAG(
    'cdn_daily',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
    concurrency=10,
) as dag:
    import_sources_groups={}
    run_scenarios_groups={}
    my_dir = os.path.dirname(os.path.abspath(__file__))
    cdn_daily_configuration_filename=os.path.join(my_dir,'confs','cdn_daily.json')
    with open(cdn_daily_configuration_filename,'r') as outputfile:
        cdn_daily_configuration = json.load(outputfile)
    
    for import_source in cdn_daily_configuration['imports'].keys() :
        import_sources_groups[import_source] = import_process(cdn_daily_configuration,import_source)

    for source in cdn_daily_configuration['scenarios'].keys() :
        run_scenarios_groups[source] = run_scenarios(cdn_daily_configuration,source)



[import_sources_groups['bsre'],import_sources_groups['cat'],import_sources_groups['pre']] >>import_sources_groups['vol']
import_sources_groups['bsre']>>run_scenarios_groups['bsre']
import_sources_groups['cat']>>run_scenarios_groups['cat']
import_sources_groups['pre']>>run_scenarios_groups['pre']
import_sources_groups['vol']>>run_scenarios_groups['vol']
