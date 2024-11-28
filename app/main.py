from fastapi import FastAPI
from typing import Dict, List
import psycopg2

app = FastAPI()

# Conexión a la base de datos
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "grupo4mlops",
    "host": "grupo-4-rds.cf4i6e6cwv74.us-east-1.rds.amazonaws.com",
    "port": 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Endpoint: /recommendations/<ADV>/<Modelo>
@app.get("/recommendations/{adv}/{model}")
def get_recommendations(adv: str, model: str) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT product_id, score 
        FROM recommendations 
        WHERE advertiser_id = %s AND model = %s
        """
        cursor.execute(query, (adv, model))
        rows = cursor.fetchall()
        recommendations = [{"product_id": row[0], "score": row[1]} for row in rows]
        return {"advertiser": adv, "model": model, "recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

# Endpoint: /stats/
@app.get("/stats/")
def get_stats() -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        stats = {}

        # Cantidad de advertisers
        cursor.execute("SELECT COUNT(DISTINCT advertiser_id) FROM recommendations")
        stats["advertisers_count"] = cursor.fetchone()[0]

        # Ejemplo: estadísticas adicionales
        cursor.execute("SELECT advertiser_id, COUNT(*) FROM recommendations GROUP BY advertiser_id")
        stats["recommendations_per_advertiser"] = cursor.fetchall()

        return stats
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

# Endpoint: /history/<ADV>/
@app.get("/history/{adv}")
def get_history(adv: str) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT model, product_id, date 
        FROM recommendations 
        WHERE advertiser_id = %s 
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