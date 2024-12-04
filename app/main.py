from fastapi import FastAPI, Path, Query, HTTPException
from typing import Dict, List
import psycopg2

app = FastAPI()

# Conexión a la base de datos
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "rdsgrupo4",
    "host": "grupo-4-rds.cf4i6e6cwv74.us-east-1.rds.amazonaws.com",
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
    adv: int = Path(..., title="Advertiser ID", description="ID del advertiser"),
    model: str = Path(..., title="Model", description="Modelo de recomendación (e.g., TopCTR, TopProduct)")
):
    """
    Endpoint para obtener las recomendaciones del día para un advertiser y modelo específicos.
    """
    if model not in ["TopCTR", "TopProduct"]:
        raise HTTPException(status_code=400, detail="Modelo no válido. Por favor usa TopCTR o TopProduct")

    # TODO Chequear la query
    query = """
        SELECT product_id
        FROM recommendations
        WHERE adv = %s AND model = %s AND date = CURRENT_DATE
    """
    recommendations = db_query(query, (adv, model))

    if not recommendations:
        raise HTTPException(status_code=404, detail="No se encontraron recomendaciones para este advertiser.")

    return {"advertiser": adv, "model": model, "recommendations": [row[0] for row in recommendations]}

@app.get("/stats/")
def stats():
    """
    Esto sería el endpoint para devolver estadísticas de las recomendaciones
    """
    stats_data = {}
    # TODO Chequear query tmb
    query_count = "SELECT COUNT(DISTINCT adv) FROM recommendations WHERE date = CURRENT_DATE"
    stats_data["advertisers_count"] = db_query(query_count)[0][0]

    # Si buscamos los advertisers con mayor variación diaria
    query_variation = """
        SELECT adv, COUNT(DISTINCT product_id)
        FROM recommendations
        WHERE date BETWEEN CURRENT_DATE - INTERVAL '1 day' AND CURRENT_DATE
        GROUP BY adv
        ORDER BY COUNT(DISTINCT product_id) DESC
        LIMIT 5
    """
    stats_data["top_advertisers_variation"] = db_query(query_variation)

    # Estadísticas de coincidencia entre modelos
    query_overlap = """
        SELECT adv, COUNT(*)
        FROM recommendations r1
        JOIN recommendations r2
        ON r1.adv = r2.adv AND r1.product_id = r2.product_id AND r1.date = r2.date
        WHERE r1.model = 'TopCTR' AND r2.model = 'TopProduct'
        GROUP BY adv
    """
    stats_data["model_overlap"] = db_query(query_overlap)

    return stats_data

# TODO --> NO USAR. Lo estoy pisando por uno nuevo
# Endpoint: /stats/
@app.get("/stats/")
def get_stats() -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        stats = {}

        # Cantidad de advertisers
        cursor.execute("SELECT COUNT(DISTINCT adv) FROM recommendations")
        stats["advertisers_count"] = cursor.fetchone()[0]

        # Ejemplo: estadísticas adicionales
        cursor.execute("SELECT adv, COUNT(*) FROM recommendations GROUP BY adv")
        stats["recommendations_per_advertiser"] = cursor.fetchall()

        return stats
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

# Endpoint: /history/<ADV>/
# TODO Este no lo hice, me falta
@app.get("/history/{adv}")
def get_history(adv: str) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT model, product_id, date 
        FROM recommendations 
        WHERE adv = %s 
        ORDER BY date DESC 
        LIMIT 7
        """
        cursor.execute(query, (adv,))
        rows = cursor.fetchall()
        history = [{"model": row[0], "product_id": row[1], "date": row[2]} for row in rows]
        return {"advertiser": adv, "history": history}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()