import datetime
import logging
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

# Configuración por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

# Define el DAG
with DAG(
    dag_id='product_recommendation_pipeline',
    default_args=default_args,
    description='Este DAG implementa un pipeline para procesar y filtrar datos, calcular métricas clave como el click-through rate (CTR) y productos más vistos, y escribir los resultados en una base de datos PostgreSQL en AWS RDS. Es parte del sistema de recomendación, diseñado para identificar los productos más relevantes para los usuarios basándose en datos actualizados y clientes activos.',
    start_date=datetime.datetime(2024, 11, 5),
    schedule_interval="0 0 * * *",
    catchup=False,
    tags=['MLOps 2024 - UTDT'],
) as dag:

    # Función de inicio
    def start():
        logging.info("Started")
        return True

    # Tarea de inicio
    start_task = PythonOperator(
        task_id='start',
        python_callable=start,
    )

    # Función para filtrar datos
    def filter_data():
        """
        FiltrarDatos: Los logs crudos contienen datos sobre advertisers que ya no se encuentran
        activos en nuestra plataforma. Esta primera tarea debe limpiar los logs del día, dejando
        solamente las líneas que se refieran a clientes activos.
        """
        logging.info("Filtrando datos...")
        return True

    filter_task = PythonOperator(
        task_id='filter_data',
        python_callable=filter_data,
    )

    # Función para calcular TopCTR
    def top_ctr():
        """
        TopCTR: Esta tarea computa el modelo TopCTR. Por cada advertirser activo debe
        devolver los 20 (o menos) productos con mejor click-through-rate.
        """
        logging.info("Calculando TopCTR...")
        return True

    top_ctr_task = PythonOperator(
        task_id='top_ctr',
        python_callable=top_ctr,
    )

    # Función para calcular TopProduct
    def top_product():
        """
        TopProduct: Esta tarea computa el modelo TopProduct. Por cada advertirser activo debe
        devolver los 20 (o menos) productos más vistos en la web del cliente.
        """
        logging.info("Calculando TopProduct...")
        return True

    top_product_task = PythonOperator(
        task_id='top_product',
        python_callable=top_product,
    )

    # Función para escribir en la base de datos
    def db_writing():
        """
        DBWriting: Esta tarea debe tomar los resultados de los modelos y los debe escribir en la
        base de datos PostgreSQL disponible en AWS RDS.
        """
        logging.info("Escribiendo en la base de datos...")
        return True

    db_writing_task = PythonOperator(
        task_id='db_writing',
        python_callable=db_writing,
    )

    # Función de finalización
    def finish():
        logging.info("Finished")
        return True

    finish_task = PythonOperator(
        task_id='finish',
        python_callable=finish,
    )

    # Definición de dependencias
    start_task >> filter_task >> top_ctr_task >> top_product_task >> db_writing_task >> finish_task