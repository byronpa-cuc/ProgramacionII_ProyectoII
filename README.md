# World Cup Insights 🏆

**Colegio Universitario de Cartago (CUC)** **Curso:** BD-143 Programación II — II Cuatrimestre 2026  
**Profesor:** Osvaldo González Chaves  
**Proyecto II**

## 📋 Descripción del Proyecto
Este sistema ha sido desarrollado en Python aplicando rigurosamente el paradigma de **Programación Orientada a Objetos (POO)** y la librería **Pandas**. El objetivo principal es realizar la ingesta, limpieza, análisis exploratorio avanzado (EDA) y visualización interactiva del historial de partidos de la Copa Mundial de la FIFA (1930-2022). 

El sistema es completamente autónomo: descarga los datos brutos de la fuente pública, aísla los partidos mundialistas, computa variables analíticas derivadas (como efectividad de localía y detección de *outliers* mediante IQR) y expone los resultados a través de Notebooks tradicionales y un Dashboard interactivo de última generación.

---

## 🗂️ Arquitectura del Proyecto
El código se encuentra modularizado en paquetes específicos según su responsabilidad:

```text
world_cup_insights/
│
├── data/
│   ├── raw/                  # Datos filtrados originales (partidos-mundial.csv)
│   └── processed/            # Dataset limpio con columnas derivadas (partidos-limpios.csv)
│
├── src/                      # Código fuente bajo el paradigma POO
│   ├── __init__.py
│   ├── ingesta/
│   │   └── cargador.py       # Clase CargadorDatos (Ingesta y persistencia)
│   ├── eda/
│   │   └── procesador.py     # Clase ProcesadorEDA (Métricas avanzadas, IQR, Skewness)
│   ├── gestor/
│   │   └── gestor.py         # Clase GestorPartidos (Consultas de solo lectura)
│   └── visualizacion/
│       └── visualizador.py   # Clase Visualizador (Gráficos Seaborn y objetos Plotly)
│
├── notebooks/                # Documentación y pruebas del análisis
│   ├── 01_EDA.ipynb          # Invoca Ingesta, Limpieza y Estadísticas Avanzadas
│   └── 02_Visualizacion.ipynb # Invoca los métodos de la historia gráfica
│
├── dashboard/
│   └── app.py                # Interfaz Web Interactiva (Streamlit)
│
├── main.py                   # Script principal para ejecución autónoma del Pipeline
├── README.md                 # Guía de usuario y documentación técnica
└── requirements.txt          # Dependencias y librerías del entorno
```


## 🛠️ Requisitos e Instalación
Para asegurar que el proyecto corra perfectamente en el momento de la revisión, sigue estos pasos en tu entorno local (PyCharm / VS Code):

1. Clonar el repositorio u organizar las carpetas
Asegúrate de abrir la terminal en el directorio raíz donde se encuentra este archivo README.md y el archivo main.py.

2. Crear y activar el entorno virtual (Recomendado)
```
# Crear entorno virtual
python -m venv venv

# Activar en Windows (PowerShell / CMD)
.\venv\Scripts\activate

# Activar en Mac/Linux
source venv/bin/activate
```

3. Instalar dependencias requeridas
Instala todas las librerías necesarias con el congelado exacto de versiones:
```
pip install -r requirements.txt
```

## 🚀 Instrucciones de Ejecución
El sistema cuenta con tres vías independientes de visualización y ejecución:

### Opción A: Pipeline Autónomo Principal (main.py)
Ejecuta el ciclo completo de Big Data: descarga los datos de la URL de GitHub, aplica la limpieza de nulos y conversión de tipos, genera las variables derivadas, guarda el archivo en la carpeta processed/ y despliega en la consola un resumen estadístico de asimetría e IQR.
```
python main.py
```
### Opción B: Dashboard Interactivo (Streamlit)
Levanta una plataforma web interactiva dividida en pestañas que incluye KPIs globales, gráficos interactivos con Plotly (con información flotante interactiva), análisis del "Efecto Sede" y un buscador jerárquico por Selección, Año o País Organizador.
```
streamlit run dashboard/app.py
```
### Opción C: Cuadernos de Trabajo (Jupyter Notebooks)
Para revisar el análisis exploratorio formal de forma secuencial, abre los archivos de la carpeta notebooks/ mediante PyCharm o Jupyter:

#### 01_EDA.ipynb: Muestra las matrices de correlación, asimetría de curvas de goles y detección matemática de marcadores atípicos.

#### 02_Visualizacion.ipynb: Despliega las historias de datos con Seaborn y Plotly.

## 📊 Historias Clave Analizadas en el EDA
¿El país sede realmente influye? Evaluamos matemáticamente la efectividad porcentual de los organizadores cuando juegan en estadios no neutrales frente a su afición.

¿Se juega un fútbol más defensivo en la actualidad? Analizamos la evolución cronológica del promedio de anotaciones por partido desde Uruguay 1930 hasta Qatar 2022.

Detección de Anomalías (Outliers): Velamos por la integridad estadística implementando la regla de ±1.5 IQR para extraer de forma puramente matemática los partidos históricamente más inusuales por su abultado marcador.

## 👥 Desarrolladores
Integrante 1:  - Identificación: 304920721

Integrante 2:  - Identififación: 

###### Nota: Este proyecto fue desarrollado con fines académicos estrictamente bajo las pautas de la rúbrica de evaluación de Programación II del CUC.