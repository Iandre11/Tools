# Investing Scraper & ADR Analyzer

Este proyecto es una aplicación web interactiva construida con [Streamlit](https://streamlit.io/) que permite:
1. Explorar el calendario de días festivos de mercados bursátiles (bolsas) alrededor del mundo (2024 y 2025).
2. Analizar el impacto en el precio de los "ADR" (empresas extranjeras listadas en EE. UU.) cuando su bolsa local original está cerrada por festivo.

## Requisitos Previos

Para ejecutar este proyecto en cualquier ordenador (Windows, Mac o Linux), necesitas tener instalado [Python](https://www.python.org/downloads/) (versión 3.9 o superior recomendada).

## Instalación y Ejecución

Sigue estos 3 sencillos pasos para instalar y arrancar la aplicación:

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

### 3. Arranca la Aplicación
Una vez instaladas las dependencias, inicia Streamlit:
```bash
streamlit run app.py
```
*(Si no se abre automáticamente, copia la URL local que aparecerá en tu terminal, por ejemplo `http://localhost:8501`, y pégala en tu navegador).*

---

## Estructura de Archivos
* `app.py`: El núcleo de la aplicación de Streamlit (Interfaz y Lógica).
* `scraper.py`: Archivo usado para generar los festivos (Playwright).
* `holidays_data.csv`: Base de datos de los días festivos ya descargada.
* `requirements.txt`: Documento que lista las dependencias Python (`streamlit`, `pandas`, `yfinance`, etc.) necesarias para compartir el proyecto fácilmente.
