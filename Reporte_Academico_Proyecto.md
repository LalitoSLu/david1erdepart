# Reporte Técnico: Predicción de Episodios de Mala Calidad del Aire en México

## 1. Descripción General y Objetivos
El presente proyecto tiene como objetivo analizar variables que influyen en la calidad del aire y construir modelos de clasificación que permitan predecir si una región presenta o no condiciones ambientales de riesgo.

## 2. Integración de Datasets
Se utilizaron datos provenientes de tres dominios principales:
1. **Calidad del Aire (SINAICA):** Se integraron mediciones diarias de PM2.5, PM10, O3 y NO2 para 50 estaciones de monitoreo.
2. **Clima (CONAGUA):** Se añadieron registros de temperatura, humedad relativa y precipitación (lluvia).
3. **Datos Urbanos (INEGI/SEMARNAT):** Se extrajo información de la densidad poblacional y el parque vehicular por estación.

**Unión de datos:** La integración se realizó tomando como llave principal la `Fecha` (diaria) y la `Estacion` de monitoreo.

## 3. Exploración de Datos (EDA)
Durante el Análisis Exploratorio de Datos (EDA) se realizaron las siguientes observaciones:
- **Correlaciones:** Se encontró una correlación positiva moderada entre la temperatura y los niveles de Ozono (O3), lo cual concuerda con la teoría química atmosférica. Por otro lado, la lluvia mostró tener un efecto de "lavado", disminuyendo ligeramente las partículas PM2.5.
- **Series Temporales:** Las partículas PM2.5 muestran estacionalidad, con picos más altos durante los meses de invierno debido a inversiones térmicas y menor precipitación.

*(Revisar la carpeta `output/plots` para visualizar las gráficas de correlación y series temporales generadas).*

## 4. Preprocesamiento y Limpieza
- **Valores Faltantes:** Dado que los datos son series de tiempo continuas, se utilizó el método de "Backward Fill" (`bfill`) para imputar nulos sin romper la continuidad de la tendencia climática.
- **Variable Objetivo:** Se definió la variable binaria `Mala_Calidad_Aire`. 
  - `0`: Calidad Aceptable.
  - `1`: Mala calidad (cuando PM2.5 > 45 µg/m³ o PM10 > 75 µg/m³).

## 5. Ingeniería de Características
Para otorgarle a los algoritmos la capacidad de "recordar" las condiciones recientes, se crearon nuevas variables usando agrupaciones por estación:
- `PM2.5_ma3`: Promedio móvil de PM2.5 de los 3 días anteriores.
- `PM10_ma3`: Promedio móvil de PM10 de los 3 días anteriores.
- `Temperatura_ma3`: Promedio móvil de la temperatura de los 3 días anteriores.
- `Densidad_Vehicular_Pob`: Ratio del parque vehicular respecto a la población total de la estación.

## 6. Modelado Predictivo
Se entrenaron cuatro algoritmos de clasificación, separando el dataset en 80% entrenamiento y 20% prueba, aplicando escalado de características (`StandardScaler`) donde fue necesario (Regresión Logística y Red Neuronal):

1. **Regresión Logística:** Usado como modelo base o *baseline*.
2. **Random Forest:** Usado para manejar relaciones no lineales y extraer importancia de variables mediante sus 50 árboles de decisión.
3. **XGBoost:** Un modelo robusto de Gradient Boosting utilizado para maximizar la precisión al corregir errores secuenciales.
4. **Red Neuronal (MLP):** Un perceptrón multicapa con arquitectura de capas ocultas densas (50 neuronas) iterando hasta la convergencia para encontrar patrones complejos profundos.

## 7. Evaluación y Resultados
*(Los resultados exactos pueden consultarse en el Dashboard HTML interactivo y en `output/metricas.json`)*.

Todos los modelos se evaluaron en el conjunto de prueba usando:
- **Accuracy:** Para ver el rendimiento general.
- **Precision y Recall:** Críticos para evaluar falsos positivos y falsos negativos (es decir, evitar predecir que el aire está limpio cuando en realidad es peligroso).
- **F1-Score:** Balance entre precisión y sensibilidad.
- **AUC-ROC:** Para medir la capacidad de discriminación entre las dos clases.

**Importancia de Variables (Feature Importance):**
De acuerdo a Random Forest y XGBoost, los predictores más importantes para un episodio de mala calidad de aire resultaron ser los *promedios móviles históricos* (PM2.5 y PM10 del día anterior), seguidos por la *temperatura* y la *densidad vehicular*.

## 8. Conclusiones
El enfoque propuesto permite predecir episodios de alta contaminación con eficacia. La conjunción del análisis descriptivo mediante el Jupyter Notebook, más la herramienta interactiva final (`dashboard.html`), proporciona un marco completo desde el análisis de datos puros hasta la puesta en producción del modelo de Machine Learning.
