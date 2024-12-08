from fastapi import FastAPI, Path, Query, HTTPException
from typing import Dict, List
import psycopg2

app = FastAPI()


# Conexión a la base de datos
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "rdsgrupo4",
    "host": "grupo-4-rds2.cf4i6e6cwv74.us-east-1.rds.amazonaws.com",
    "port": 5432
}

def db_query(query, params=None):
    """
    Esta función sería la génerica. Dsp habría que ver si hay algunas dependencias adicionales a sumar
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")

# def get_db_connection():
#     return psycopg2.connect(**DB_CONFIG)

# Endpoint: /recommendations/<ADV>/<Modelo>
@app.get("/recommendations/{adv}/{model}")
def recommendations(
    adv: str = Path(..., title="Advertiser ID", description="ID del advertiser"),
    model: str = Path(..., title="Model", description="Modelo de recomendación (e.g., TopCTR, TopProduct)")
):
    """
    Endpoint para obtener las recomendaciones del día para un advertiser y modelo específicos.
    """
    if model not in ["TopCTR", "TopProduct"]:
        raise HTTPException(status_code=400, detail="Modelo no válido. Por favor usa TopCTR o TopProduct")

    if model=="TopProduct":
        query_top_product = """
            SELECT product_id
            FROM top_products_model
            WHERE advertiser_id = %s AND date = CURRENT_DATE
        """
        recommendations = db_query(query_top_product,(adv,))

    if model=="TopCTR":
        query_top_ctr = """
            SELECT product_id
            FROM top_ctr_model
            WHERE advertiser_id = %s AND date = CURRENT_DATE
        """
        recommendations = db_query(query_top_ctr,(adv,))

    if not recommendations:
        raise HTTPException(status_code=404, detail="No se encontraron recomendaciones para este advertiser.")

    return {"advertiser": adv, "model": model, "recommendations": [row[0] for row in recommendations]}

@app.get("/stats/")
def stats():
    """
    Endpoint para devolver estadísticas sobre las recomendaciones.
    """
    stats_data = {}

    # Cantidad de advertisers activos
    query_advertisers_count = """
        SELECT COUNT(DISTINCT advertiser_id)
        FROM (
            SELECT advertiser_id FROM top_ctr_model
            UNION
            SELECT advertiser_id FROM top_products_model
        ) AS active_advertisers
    """
    stats_data["advertisers_count"] = db_query(query_advertisers_count)[0][0]

    # Advertisers con mayor variación diaria en recomendaciones
    query_variation = """
        SELECT advertiser_id, COUNT(DISTINCT product_id)
        FROM (
            SELECT advertiser_id, product_id, date FROM top_ctr_model
            UNION ALL
            SELECT advertiser_id, product_id, date FROM top_products_model
        ) AS all_recommendations
        WHERE date = CURRENT_DATE
        GROUP BY advertiser_id
        ORDER BY COUNT(DISTINCT product_id) DESC
        LIMIT 5
    """
    stats_data["top_advertisers_variation"] = db_query(query_variation)

    # Estadísticas de coincidencia entre TopCTR y TopProduct
    query_overlap = """
        SELECT r1.advertiser_id, COUNT(*) AS overlapping_products
        FROM top_ctr_model r1
        INNER JOIN top_products_model r2
        ON r1.advertiser_id = r2.advertiser_id
        AND r1.product_id = r2.product_id
        AND r1.date = r2.date
        WHERE r1.date = CURRENT_DATE
        GROUP BY r1.advertiser_id
        ORDER BY overlapping_products DESC
    """
    stats_data["model_overlap"] = db_query(query_overlap)

    return stats_data

# Endpoint: /history/<ADV>/
# TODO Este no lo hice, me falta
@app.get("/history/{adv}")
def get_history(
    adv: str = Path(..., title="Advertiser ID", description="ID del advertiser")
):
    """
    Endpoint para obtener las recomendaciones de los últimos 7 días para un advertiser específico.
    """
    try:
        # Query para obtener recomendaciones de los últimos 7 días
        query = """
            SELECT date, 'TopCTR' AS model, product_id
            FROM top_ctr_model
            WHERE advertiser_id = %s AND date >= CURRENT_DATE - INTERVAL '7 days'
            UNION ALL
            SELECT date, 'TopProduct' AS model, product_id
            FROM top_products_model
            WHERE advertiser_id = %s AND date >= CURRENT_DATE - INTERVAL '7 days'
            ORDER BY date DESC
        """
        results = db_query(query, (adv, adv))

        # Si no hay resultados, que tire una excepción
        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron recomendaciones para este advertiser en los últimos 7 días.")

        # Agrupar resultados por fecha y modelo
        history = {}
        for row in results:
            date, model, product_id = row
            if date not in history:
                history[date] = {}
            if model not in history[date]:
                history[date][model] = []
            history[date][model].append(product_id)

        return {"advertiser": adv, "history": history}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el historial: {e}")
