📊 Dashboard ANS – Control de Pedidos con Streamlit

Autor: Héctor Gaviria
Tecnologías: Python · Streamlit · Pandas · Folium · Plotly

🧩 Descripción

Este proyecto es un Dashboard Web profesional para visualizar y analizar el estado ANS de los pedidos atendidos por Elite Ingenieros S.A.S.
El sistema permite:

Consulta rápida por pedido

Mapa geolocalizado con marcadores personalizados

Visualización rosada con OSM Bright (calles, carreras, barrios muy detallados)

Gráficas por estado, municipio y porcentajes

Filtros dinámicos en tiempo real

Vista general de KPIs

Integración directa con Excel mediante botón macro

Es un dashboard tipo empresarial, accesible desde cualquier navegador.

🚀 Tecnologías utilizadas

Streamlit (frontend web)

Pandas (procesamiento de datos)

Plotly (gráficas interactivas)

Folium + Streamlit-Folium (mapas dinámicos)

Openpyxl (lectura de Excel)

Python 3.10+

📂 Estructura del proyecto
control-ans-dashboard/
│
├── app.py              # Archivo principal del dashboard
├── lector_cortes.py    # Lector del archivo más reciente del informe ANS
├── requirements.txt    # Dependencias del proyecto
└── .gitignore          # Archivos ignorados para Git
