# Trabajo Práctico Final - Ciencia de Datos en Ambientes Productivos (MLOps)

### Materia: Ciencia de Datos en Ambientes Productivos (MLOps)
**Master in Management + Analytics, 2024**  
**Profesores:** Federico Pousa, Agustín Mosteiro  
**Horario:** Miércoles, 19:15 - 22:15


**Alumnos:** Juan Spadaro, Tomás Gonzalez Danna y Rocío Palacín


---

## Tabla de Contenidos
- [Descripción](#descripción)
- [Objetivos del Trabajo Práctico](#objetivos-del-trabajo-práctico)
- [Contenido del Proyecto](#contenido-del-proyecto)
- [Requisitos](#requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Configuración](#instalación-y-configuración)
- [Pipelines de Procesamiento de Datos](#pipelines-de-procesamiento-de-datos)
- [API y Endpoints](#api-y-endpoints)
- [Despliegue en Producción](#despliegue-en-producción)
- [Referencias y Recursos](#referencias-y-recursos)


---

## Descripción

Este repositorio contiene el trabajo práctico final del curso *Ciencia de Datos en Ambientes Productivos (MLOps)*. En este curso, se estudian y aplican prácticas clave para llevar soluciones de ciencia de datos a producción de manera efectiva, utilizando herramientas y técnicas ampliamente empleadas en la industria. El enfoque es mayormente práctico, alentando la participación activa y el desarrollo de soluciones implementables.

## Objetivos del Trabajo Práctico

El objetivo de este trabajo práctico es aplicar los conceptos y herramientas vistas en clase para desarrollar una solución de ciencia de datos lista para producción, integrando prácticas y herramientas de MLOps. Esto incluye:

- Diseño de pipelines de datos
- Automatización de procesos
- Despliegue de modelos de Machine Learning en ambientes productivos
- Uso de contenedores (Docker)
- Implementación en plataformas de nube como AWS

## Contenido del Proyecto

1. **Preparación del Entorno de Desarrollo**
   - Configuración de sistemas operativos y manejo de terminal
   - Uso de herramientas de control de versiones como Git
   - Configuración de Docker para el empaquetado y despliegue de modelos

2. **Automatización de Tareas**
   - Implementación de workflows mediante herramientas de orquestación (e.g., Apache Airflow)

3. **Desarrollo y Despliegue en la Nube**
   - Configuración e interacción con servicios en la nube de AWS (EC2, RDS, S3)
   - Despliegue de modelos en servicios como HuggingFace o Streamlit Cloud

4. **Evaluación y Disponibilización de Modelos**
   - Diseño y despliegue de endpoints para la inferencia de modelos
   - Evaluación de rendimiento y monitoreo en producción

## Requisitos

- **Python** (versión 3.7 o superior)
- **Docker** para contenedores
- **Apache Airflow** para la orquestación de workflows
- **AWS CLI** para la interacción con servicios en la nube de AWS
- **Git** para el control de versiones
- **PostgreSQL** como base de datos


## Estructura del Proyecto

```plaintext
├── .github/workflows/     # Archivos para configurar GitHub Actions
├── .ssh/                  # Claves RSA para acceso seguro
├── AdTech/                # Generación y manejo de datos de publicidad
├── Enunciado/             # Documentos con los lineamientos del proyecto final
├── Programa/              # Silabo del curso de MLOps
├── app/                   # Código fuente principal de la aplicación
│   ├── main.py            # Punto de entrada de la aplicación
├── dags/                  # Pipelines de Apache Airflow
├── .gitignore             # Archivos y carpetas a ignorar por Git
├── README.md              # Documentación del proyecto
├── rds.py                 # Conexión y configuración de la base de datos RDS
└── s3.py                  # Scripts para interacción con S3
```

## Instalación y Configuración

### Crear Ambiente Virtual

Para configurar el entorno virtual llamado `mlops_utdt`, sigue estos pasos:

1. **Asegúrate de tener `python3-venv` instalado**:
   
   Si estás en Linux y no tienes instalado el módulo `venv`, instálalo con:
   ```bash
   sudo apt-get install python3-venv

3. **Crea el ambiente virtual**:

   Ejecuta el siguiente comando:
   ```bash
   python3 -m venv mlops_utdt

4. **Activa el ambiente virtual**:

   En Linux/macOS:
   ```bash
   source mlops_utdt/bin/activate
   ```
   En Windows:
   ```bash
   .\mlops_utdt\Scripts\activate
   ```

5. **Instala las dependencias necesarias (opcional)**:

   Si tienes un archivo `requirements.txt`, puedes instalar las dependencias con:
   ```bash
   pip install -r requirements.txt
   ```

Este ambiente virtual permitirá gestionar las dependencias de Python necesarias para el proyecto de manera aislada.

 ## Pipelines de Procesamiento de Datos

El pipeline de datos incluye las siguientes tareas:

1. **Filtrado de Datos**
   - Filtra logs crudos para mantener solo clientes activos.

2. **Cálculo de Métricas**
   - Calcula TopCTR y TopProduct basados en eventos.

3. **Escritura en Base de Datos**
   - Guarda resultados en tablas PostgreSQL (`top_ctr_model`, `top_products_model`)
  
![image](https://github.com/user-attachments/assets/128ca21c-68a0-4670-9ad5-c670ce300130)



 ## API y Endpoints
 
1. `/recommendations/<ADV>/<Modelo>`
   - Devuelve recomendaciones del día para un advertiser y un modelo (TopCTR o TopProduct)
2. `stats`
   - Devuelve estadísticas globales:
      - Cantidad de advertisers activos.
      - Los 5 Advertisers de mayor variación diaria de recomendaciones.
      - Coincidencia de productos recomendados entre `TopCTR` y `TopProduct` de un mismo Advertiser.
3. `/history/<ADV>/`
   - Devuelve historial de recomendaciones para un advertiser en los últimos 7 días.
  
![image](https://github.com/user-attachments/assets/37f98e96-ed58-408a-a365-167df743a3e0)


 ## Despliegue en Producción

 TBD

 ## Referencias y Recursos

 - [FastAPI Documentation](https://fastapi.tiangolo.com/)
 - [Apache Airflow Documentation](https://airflow.apache.org/docs/)
 - [PostgreSQL Documentation](https://www.postgresql.org/docs/)
