# Investing Scraper & ADR Analyzer

Este proyecto es una aplicación web interactiva construida con [Streamlit](https://streamlit.io/) que permite:
1. Explorar el calendario de días festivos de mercados bursátiles (bolsas) alrededor del mundo (2024 y 2025).
2. Analizar el impacto en el precio de los "ADR" (empresas extranjeras listadas en EE. UU.) cuando su bolsa local original está cerrada por festivo.

## Requisitos Previos

Para ejecutar este proyecto en cualquier ordenador (Windows, Mac o Linux), necesitas tener instalado [Python](https://www.python.org/downloads/) (versión 3.9 o superior recomendada).

## Instalación y Ejecución

Sigue estos 4 sencillos pasos para instalar y arrancar la aplicación:

### 1. Abre la Terminal (Símbolo del sistema o PowerShell en Windows)
Navega hasta la carpeta donde se encuentra este proyecto:
```bash
cd ruta/a/esta/carpeta
```

### 2. Instala las dependencias
Ejecuta el siguiente comando para instalar todas las librerías necesarias con las que funciona la app:
```bash
pip install -r requirements.txt
```

### 3. Descarga los precios de Yahoo Finance a CSV
Antes de abrir la app, genera el fichero local `price_history.csv` con los históricos que usa la pestaña de ADR:
```bash
python3 download_price_history.py
```

Por defecto se descargan precios diarios desde `2023-12-01` hasta `2026-01-31` para los ADR y tickers locales definidos en el catálogo. Ese CSV queda guardado junto a `holidays_data.csv`.

### 4. Arranca la Aplicación
Una vez instaladas las dependencias, inicia Streamlit:
```bash
streamlit run app.py
```
*(Si no se abre automáticamente, copia la URL local que aparecerá en tu terminal, por ejemplo `http://localhost:8501`, y pégala en tu navegador).*

---

## Estructura de Archivos
* `app.py`: El núcleo de la aplicación de Streamlit (Interfaz y Lógica).
* `download_price_history.py`: Script para descargar y refrescar el CSV local de precios desde Yahoo Finance.
* `scraper.py`: Archivo usado para generar los festivos (Playwright).
* `holidays_data.csv`: Base de datos de los días festivos ya descargada.
* `price_history.csv`: Base de datos local de precios diarios usada por el análisis ADR.
* `requirements.txt`: Documento que lista las dependencias Python (`streamlit`, `pandas`, `yfinance`, etc.) necesarias para compartir el proyecto fácilmente.
