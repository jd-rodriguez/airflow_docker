def run_process(process_name,*args):
    from airflow.operators.python_operator import PythonOperator

    def run(task_instance,process_name):
        import random
        task_instance.xcom_push(key='process_name',value=process_name),
        task_instance.xcom_push(key='pause',value=random.randint(1,10))
    
    def status_check(task_instance,process_name):
        import time
        process=task_instance.xcom_pull("run_"+process_name, key='process_name')
        print(process)
        pause=task_instance.xcom_pull("run_"+process_name, key='pause')
        print(pause)
        time.sleep(int(pause))


    execute_process=PythonOperator(
        task_id="run_"+process_name,
        python_callable=run,
        op_kwargs={"process_name":process_name}
    )

    process_status=PythonOperator(
        task_id="check_status_of_"+process_name,
        python_callable=status_check,
        op_kwargs={"process_name":process_name}
    )

    execute_process >> process_status >> args

    return execute_process

def import_process(cdn_daily_configuration,source):

    from airflow.operators.python_operator import PythonOperator
    from airflow.utils.task_group import TaskGroup

    import_files={}

    def files_check(task_instance,filename,folder_name):
        task_instance.xcom_push(key='filename',value=filename),
        task_instance.xcom_push(key='folder_name',value=folder_name)

    with TaskGroup("import_"+source,prefix_group_id=False) as task_group:

        process = run_process(cdn_daily_configuration['imports'][source]['process_name'])

        for filename in cdn_daily_configuration['imports'][source]['filenames']:
            import_files[filename]=PythonOperator(
            task_id="check_presence_of_"+filename,
            python_callable=files_check,
            op_kwargs={ "filename":filename,
                        "folder_name":cdn_daily_configuration['imports'][source]['folder_name']})
            import_files[filename] >> process

    return task_group

def run_scenarios(cdn_daily_configuration,source):

    from airflow.operators.dummy_operator import DummyOperator
    from airflow.utils.task_group import TaskGroup

    with TaskGroup("run_scenarios_"+source,prefix_group_id=False) as task_group:

        scenario_control=DummyOperator(
            task_id='scenario_control_for_'+source
        )
        for scenario in cdn_daily_configuration['scenarios'][source].keys():
            run_process(cdn_daily_configuration['scenarios'][source][scenario]['process_name'],scenario_control)


    return task_group