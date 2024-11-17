import datetime
import numpy as np  # Importa numpy para usar np.random.normal
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

# Define el DAG
with DAG(
    dag_id='test',
    schedule=None,
    start_date=datetime.datetime(2024, 11, 5),
    catchup=False,
) as dag:
    # Tarea BashOperator
    sleep = BashOperator(
        task_id='sleep',
        bash_command='sleep 3',
    )

    # Función PythonOperator
    def sample_normal(mean, std):
        return np.random.normal(loc=mean, scale=std)

    # Tarea PythonOperator
    random_height = PythonOperator(
        task_id='height',
        python_callable=sample_normal,
        op_kwargs={"mean": 170, "std": 15},
    )

    # Tareas BashOperator
    first = BashOperator(task_id='first', bash_command='sleep 3 && echo First')
    last = BashOperator(task_id='last', bash_command='sleep 3 && echo Last')

    # Definición de dependencias
    first >> sleep
    first >> random_height
    [sleep, random_height] >> last

    # TaskGroup para tareas de post-proceso
    with TaskGroup(group_id="post_process") as post_process_group:
        for i in range(5):
            EmptyOperator(task_id=f"dummy_task_{i}")

    # Dependencia del grupo
    last >> post_process_group