import datetime
import logging
import pandas as pd
from io import StringIO
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Configuración por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

# Conexión a la base de datos PostgreSQL en AWS RDS
CONNECTION_ID = "postgres_aws_rds"
S3_BUCKET = "grupo-4-mlops"
RAW_DATA_PREFIX = "raw/" # Prefijo de los datos crudos en S3
PROCESSED_DATA_PREFIX = "processed/" # Prefijo de los datos procesados en S3

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
        s3_hook = S3Hook()

        # Cargar datos crudos desde S3
        active_clients_data = s3_hook.read_key(key=f"{RAW_DATA_PREFIX}advertiser_ids.csv", bucket_name=S3_BUCKET)
        product_views_data = s3_hook.read_key(key=f"{RAW_DATA_PREFIX}product_views.csv", bucket_name=S3_BUCKET)
        ads_views_data = s3_hook.read_key(key=f"{RAW_DATA_PREFIX}ads_views.csv", bucket_name=S3_BUCKET)
        
        # Leer los archivos como DataFrames
        active_clients = pd.read_csv(StringIO(active_clients_data))
        product_views = pd.read_csv(StringIO(product_views_data))
        ads_views = pd.read_csv(StringIO(ads_views_data))
        
        # Filtrar datos por advertisers activos
        active_clients_list = active_clients['advertiser_id'].tolist()
        filtered_product_views = product_views[product_views['advertiser_id'].isin(active_clients_list)]
        filtered_ads_views = ads_views[ads_views['advertiser_id'].isin(active_clients_list)]
        
        # Guardar resultados en S3
        filtered_product_csv = filtered_product_views.to_csv(index=False)
        filtered_ads_csv = filtered_ads_views.to_csv(index=False)

        s3_hook.load_string(
            string_data=filtered_product_csv,
            key=f"{PROCESSED_DATA_PREFIX}filtered_product_views.csv",
            bucket_name=S3_BUCKET,
            replace=True
        )
        s3_hook.load_string(
            string_data=filtered_ads_csv,
            key=f"{PROCESSED_DATA_PREFIX}filtered_ads_views.csv",
            bucket_name=S3_BUCKET,
            replace=True
        )

        logging.info("Datos filtrados guardados en S3.")
        return True

    filter_task = PythonOperator(
        task_id='filter_data',
        python_callable=filter_data,
    )

    # Calcular TopCTR
    def calculate_top_ctr():
        """
        Calcula los 20 productos con mejor click-through-rate (CTR) por cliente activo.
        """
        logging.info("Calculando TopCTR...")
        s3_hook = S3Hook()

        # Leer logs procesados desde S3
        filtered_ads_views_data = s3_hook.read_key(
            key=f"{PROCESSED_DATA_PREFIX}filtered_ads_views.csv", bucket_name=S3_BUCKET
        )
        ads_views_df = pd.read_csv(StringIO(filtered_ads_views_data))
        
        # Calcular CTR
        clicks = ads_views_df[ads_views_df['type'] == 'click'].groupby(['advertiser_id', 'product_id']).size().reset_index(name='clicks')
        impressions = ads_views_df[ads_views_df['type'] == 'impression'].groupby(['advertiser_id', 'product_id']).size().reset_index(name='impressions')
        ctr_data = pd.merge(clicks, impressions, on=['advertiser_id', 'product_id'], how='left')
        ctr_data['ctr'] = ctr_data['clicks'] / ctr_data['impressions']
        top_ctr = ctr_data.sort_values(['advertiser_id', 'ctr'], ascending=[True, False]).groupby('advertiser_id').head(20)

        # Guardar resultado en S3
        top_ctr_csv = top_ctr.to_csv(index=False)
        s3_hook.load_string(
            string_data=top_ctr_csv,
            key=f"{PROCESSED_DATA_PREFIX}top_ctr.csv",
            bucket_name=S3_BUCKET,
            replace=True
        )
        logging.info("TopCTR calculado y guardado en S3.")
        return True

    top_ctr_task = PythonOperator(
        task_id='calculate_top_ctr',
        python_callable=calculate_top_ctr,
    )

    # Calcular TopProduct
    def calculate_top_products():
        """
        Calcula los 20 productos más vistos en la web por cliente activo.
        """
        logging.info("Calculando TopProduct...")
        s3_hook = S3Hook()

        # Leer logs procesados desde S3
        filtered_product_views_data = s3_hook.read_key(
            key=f"{PROCESSED_DATA_PREFIX}filtered_product_views.csv", bucket_name=S3_BUCKET
        )
        product_views_df = pd.read_csv(StringIO(filtered_product_views_data))

        # Calcular productos más vistos
        top_products = (
            product_views_df.groupby(['advertiser_id', 'product_id'])
            .size()
            .reset_index(name='views')
            .sort_values(['advertiser_id', 'views'], ascending=[True, False])
            .groupby('advertiser_id')
            .head(20)
        )

        # Guardar resultado en S3
        top_products_csv = top_products.to_csv(index=False)
        s3_hook.load_string(
            string_data=top_products_csv,
            key=f"{PROCESSED_DATA_PREFIX}top_products.csv",
            bucket_name=S3_BUCKET,
            replace=True
        )
        logging.info("TopProduct calculado y guardado en S3.")
        return True

    top_product_task = PythonOperator(
        task_id='calculate_top_products',
        python_callable=calculate_top_products,
    )

    # Escribir en la base de datos
    def db_writing():
        """
        Escribe los resultados en la base de datos PostgreSQL.
        """
        logging.info("Escribiendo en la base de datos...")
        s3_hook = S3Hook()
        top_ctr_csv = s3_hook.read_key(key=f"{PROCESSED_DATA_PREFIX}top_ctr.csv", bucket_name=S3_BUCKET)
        top_products_csv = s3_hook.read_key(key=f"{PROCESSED_DATA_PREFIX}top_products.csv", bucket_name=S3_BUCKET)

        top_ctr = pd.read_csv(StringIO(top_ctr_csv))
        top_products = pd.read_csv(StringIO(top_products_csv))
        
        # Conectar a PostgreSQL
        hook = PostgresHook(postgres_conn_id=CONNECTION_ID)
        conn = hook.get_conn()
        cursor = conn.cursor()

        # Verificar y crear las tablas si no existen
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_ctr (
            advertiser_id VARCHAR NOT NULL,
            product_id VARCHAR NOT NULL,
            ctr FLOAT NOT NULL,
            PRIMARY KEY (advertiser_id, product_id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_products (
            advertiser_id VARCHAR NOT NULL,
            product_id VARCHAR NOT NULL,
            views INT NOT NULL,
            PRIMARY KEY (advertiser_id, product_id)
        );
        """)

        # Escribir en las tablas
        for _, row in top_ctr.iterrows():
            cursor.execute(
                "INSERT INTO top_ctr (advertiser_id, product_id, ctr) VALUES (%s, %s, %s) ON CONFLICT (advertiser_id, product_id) DO NOTHING",
                (row['advertiser_id'], row['product_id'], row['ctr']),
            )

        for _, row in top_products.iterrows():
            cursor.execute(
                "INSERT INTO top_products (advertiser_id, product_id, views) VALUES (%s, %s, %s) ON CONFLICT (advertiser_id, product_id) DO NOTHING",
                (row['advertiser_id'], row['product_id'], row['views']),
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