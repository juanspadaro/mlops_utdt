# Trabajo Práctico Final - Ciencia de Datos en Ambientes Productivos (MLOps)

### Materia: Ciencia de Datos en Ambientes Productivos (MLOps)
**Master in Management + Analytics, 2024**  
**Profesores:** Federico Pousa, Agustín Mosteiro  
**Horario:** Miércoles, 19:15 - 22:15


**Alumnos:** Juan Spadaro, Tomás Gonzalez Danna, Rocío Palacín y Jaime Sempértegui 


---

## Tabla de Contenidos
- [Descripción](#descripción)
- [Objetivos del Trabajo Práctico](#objetivos-del-trabajo-práctico)
- [Contenido del Proyecto](#contenido-del-proyecto)
- [Requisitos](#requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
- [Despliegue en Producción](#despliegue-en-producción)
- [Evaluación](#evaluación)
- [Referencias y Recursos](#referencias-y-recursos)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

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

## Estructura del Proyecto

```plaintext
├── src/                   # Código fuente del proyecto
│   ├── data_pipeline/     # Pipelines de procesamiento de datos
│   ├── model/             # Definición y entrenamiento del modelo
│   ├── deployment/        # Scripts para el despliegue en producción
│   └── utils/             # Funciones auxiliares y herramientas
├── notebooks/             # Notebooks para el análisis y experimentación
├── config/                # Archivos de configuración
├── docker/                # Archivos y configuración de Docker
├── airflow/               # Workflows de Apache Airflow
└── README.md              # Documentación del proyecto
