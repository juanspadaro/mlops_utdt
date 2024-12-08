# Imagen base
FROM python:3.9.21-slim-bullseye

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instala dependencias sin apache-airflow primero (esto lo hago así para evitar problemas de dependencias entre librerías)
RUN pip install --no-cache-dir email-validator fastapi uvicorn pandas sqlalchemy psycopg2-binary boto3 numpy

# Luego, instala apache-airflow
RUN pip install --no-cache-dir apache-airflow

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
