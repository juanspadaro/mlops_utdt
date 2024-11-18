import datetime
import logging
import pandas as pd
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Configuración por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

# Conexión a la base de datos PostgreSQL en AWS RDS
CONNECTION_ID = "postgres_aws_rds"

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
        logging.info("Pipeline iniciado.")
        return True

    start_task = PythonOperator(
        task_id='start',
        python_callable=start,
    )

    # Filtrar datos
    def filter_data():
        """
        Filtra los logs del día, dejando solo líneas que correspondan a clientes activos.
        """
        logging.info("Filtrando datos...")
        # Simula la carga de logs y clientes activos
        logs = pd.DataFrame({'client_id': [1, 2, 3], 'activity': ['click', 'view', 'click']})
        active_clients = [1, 3]
        filtered_logs = logs[logs['client_id'].isin(active_clients)]
        filtered_logs.to_csv('/tmp/filtered_logs.csv', index=False)
        logging.info("Datos filtrados y guardados en /tmp/filtered_logs.csv")
        return True

    filter_task = PythonOperator(
        task_id='filter_data',
        python_callable=filter_data,
    )

    # Calcular TopCTR
    def top_ctr():
        """
        Calcula los 20 productos con mejor click-through-rate (CTR) por cliente activo.
        """
        logging.info("Calculando TopCTR...")
        logs = pd.read_csv('/tmp/filtered_logs.csv')
        # Simula cálculo de CTR
        ctr_data = pd.DataFrame({'client_id': [1, 3], 'top_ctr': ['product_a', 'product_b']})
        ctr_data.to_csv('/tmp/top_ctr.csv', index=False)
        logging.info("TopCTR calculado y guardado en /tmp/top_ctr.csv")
        return True

    top_ctr_task = PythonOperator(
        task_id='top_ctr',
        python_callable=top_ctr,
    )

    # Calcular TopProduct
    def top_product():
        """
        Calcula los 20 productos más vistos en la web por cliente activo.
        """
        logging.info("Calculando TopProduct...")
        logs = pd.read_csv('/tmp/filtered_logs.csv')
        # Simula cálculo de productos más vistos
        product_data = pd.DataFrame({'client_id': [1, 3], 'top_products': ['product_x', 'product_y']})
        product_data.to_csv('/tmp/top_product.csv', index=False)
        logging.info("TopProduct calculado y guardado en /tmp/top_product.csv")
        return True

    top_product_task = PythonOperator(
        task_id='top_product',
        python_callable=top_product,
    )

    # Escribir en la base de datos
    def db_writing():
        """
        Escribe los resultados en la base de datos PostgreSQL.
        """
        logging.info("Escribiendo en la base de datos...")
        top_ctr = pd.read_csv('/tmp/top_ctr.csv')
        top_product = pd.read_csv('/tmp/top_product.csv')

        # Conectar a PostgreSQL
        hook = PostgresHook(postgres_conn_id=CONNECTION_ID)
        conn = hook.get_conn()
        cursor = conn.cursor()

        # Escribe los datos en las tablas
        for _, row in top_ctr.iterrows():
            cursor.execute(
                "INSERT INTO top_ctr (client_id, top_ctr) VALUES (%s, %s)",
                (row['client_id'], row['top_ctr']),
            )

        for _, row in top_product.iterrows():
            cursor.execute(
                "INSERT INTO top_product (client_id, top_products) VALUES (%s, %s)",
                (row['client_id'], row['top_products']),
            )

        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Datos escritos en la base de datos.")
        return True

    db_writing_task = PythonOperator(
        task_id='db_writing',
        python_callable=db_writing,
    )

    # Finalizar pipeline
    def finish():
        logging.info("Pipeline finalizado.")
        return True

    finish_task = PythonOperator(
        task_id='finish',
        python_callable=finish,
    )

    # Definir dependencias
    start_task >> filter_task >> top_ctr_task >> top_product_task >> db_writing_task >> finish_task