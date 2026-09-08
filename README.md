# StreamView Analytics

Dashboard de Visual Analytics para explorar el catálogo audiovisual de StreamView
Analytics, desarrollado por Eduardo Lizama a partir de los datasets entregados en el
caso semestral de ADY1104.

## Ejecutar localmente

Desde esta carpeta:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

La aplicación carga automáticamente los dos CSV ubicados en `Data_Movies/`.

## Vistas incluidas

- **Dashboard ejecutivo:** KPIs generales, composición y evolución temporal.
- **Análisis del catálogo:** géneros, países, calidad de campos y contenidos destacados.
- **Popularidad y valoración:** relación entre métricas, rankings y análisis por género.
- **Finanzas · Películas:** presupuesto, ingresos y ROI aproximado, excluyendo datos no disponibles.
- **Calidad de datos:** nulos, tipos, duplicados detectados y decisiones de preparación.

La aplicación no modifica los datasets originales. La popularidad se interpreta como
índice relativo TMDB y el análisis financiero se limita a películas con presupuesto e
ingresos positivos, de acuerdo con las reglas de negocio del caso.
