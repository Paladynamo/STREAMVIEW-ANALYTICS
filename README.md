# StreamView Analytics

Dashboard de Visual Analytics para explorar el catálogo de películas y series
del caso académico StreamView. Desarrollado por **Eduardo Lizama** para
ADY1104 – Visualización de Datos.

## Propósito y contexto del caso

El caso plantea a StreamView como una plataforma internacional de suscripción
audiovisual con foco en Latinoamérica. Su problema es la falta de una vista
consolidada del catálogo: los reportes separados dificultan comparar géneros y
países y producen indicadores inconsistentes; además, las vistas existentes se
describen como sobrecargadas y con poca interacción. El objetivo del proyecto es
comunicar información relevante del catálogo mediante visualizaciones,
storytelling y vistas interactivas que apoyen decisiones de contenidos,
adquisición, marketing y producto.

La misión, visión y valores que se resumen en el dashboard pertenecen al caso
académico; no se presentan como una verificación de una empresa real. El alcance
de esta entrega utiliza exclusivamente los dos archivos de catálogo
proporcionados. No incluye predicción, inteligencia artificial, ETL operacional
ni cambios en sistemas de producción.

## Correspondencia con las Partes I y II del caso

| Requisito del caso | Implementación / evidencia |
|---|---|
| **Parte I — Contexto, empresa y problema** | Sección **Contexto y reglas** del dashboard y contexto de este README. |
| Objetivo, alcance, audiencias y necesidades de decisión | Sección **Contexto y reglas**; las vistas y sus audiencias se describen en las secciones del dashboard. |
| **Parte II — Arquitectura y fuentes** | Dos CSV de catálogo, anexados en una vista analítica y distinguidos por tipo de contenido. |
| Modelo y grano | Una fila por registro de la fuente. La llave técnica `_content_row` diferencia filas durante el análisis; no es un identificador de cliente ni una llave de negocio. |
| Diccionario de datos | Tabla de variables originales en **Contexto y reglas**. Se conservan los nombres originales para trazabilidad. |
| Calidad, integración y supuestos | Sección **Fuentes y calidad**, con faltantes, duplicados, límites de llaves y distribuciones temporales observadas. |
| KPI y reglas de negocio | Tabla de definiciones operativas y reglas en **Contexto y reglas**; los KPI principales se recalculan con los filtros. |
| Preguntas de negocio y recomendaciones | Secciones **Resumen ejecutivo**, **Catálogo y tendencias**, **Popularidad y valoración** y **Finanzas de películas**. |
| Limitaciones y datos requeridos | Sección **Fuentes y calidad** y notas visibles junto a las métricas afectadas. |

## Fuentes, modelo y límites de interpretación

Los archivos se encuentran en `data/`:

- `netflix_movies_detailed_up_to_2025.csv`: 16.000 filas y 18 columnas.
- `netflix_tv_shows_detailed_up_to_2025.csv`: 16.000 filas y 16 columnas.

La integración es una anexión de registros. Cada fila se trata como un registro
de contenido y se añade el tipo (película o serie). Los campos que solo existen
para películas, como presupuesto e ingresos, no se imputan a las series. Los
países y géneros pueden contener más de un valor por registro; al desglosarlos
para contar, un título puede aparecer en varias categorías.

Se comparó el ZIP de datos entregado con los CSV del repositorio mediante
SHA-256: ambos archivos son idénticos byte por byte. El ZIP no agrega una fuente
de actividad de clientes ni datos que habiliten métricas de uso.

## Investigación complementaria (en construcción)

La pestaña **Investigación complementaria (en construcción)** usa únicamente
los dos CSV adicionales preparados para este análisis y guardados en
`data/research_inputs/`:

- `netflix_movies_completed_estimates.csv`: 16.000 filas y 46 columnas.
- `netflix_tv_shows_completed_estimates.csv`: 16.000 filas y 45 columnas.

Los archivos se mantienen separados de los CSV oficiales de `data/`; no
reemplazan sus valores ni intervienen en los KPI, filtros o visualizaciones del
resto del dashboard. La pestaña investigativa anexa ambos archivos de forma
temporal para permitir filtros por tipo, género, año y valoración, muestra el
proxy interno por género y permite descargar los archivos completos o la
selección filtrada. La tabla y las descargas conservan los campos originales de
procedencia, método y estado, además de identificar archivo y fila de origen.

### Advertencias y calidad de los datos complementarios

- **Duraciones no verificadas:** las 32.000 filas tienen
  `runtime_is_estimate = True` y un estado que declara la duración como
  estimada. La duración de películas aproxima la obra completa; la de series
  se expresa por episodio. Los archivos no aportan temporadas, cantidad de
  episodios ni duración total comprobada de una serie.
- **Proxy, no uso observado:** `engagement_proxy_score` es un índice interno
  calculado con percentiles de popularidad, cantidad de votos y valoración
  externa. No representa reproducciones, usuarios únicos, minutos vistos ni
  engagement real de Netflix.
- **Sin métricas de clientes:** los archivos declaran que churn, retención y
  clientes activos no son calculables con estas fuentes. No se deben derivar
  estas métricas a partir del proxy ni de popularidad.
- **Estimaciones financieras:** los campos estimados de utilidad y ROI de
  películas requieren verificación y no equivalen a resultados contables.
  Aunque algunos nombres de columna declaran USD, esa moneda no se ha validado.
- **Revisión de fuentes:** cada archivo conserva las columnas de método,
  estado, notas y enlaces de búsqueda/ficha disponibles. Un enlace a IMDb o
  TMDB no significa que la estimación haya sido contrastada con esa fuente.
- **IDs de series repetidos:** el CSV complementario de series contiene 9
  `show_id` duplicados. Se preservan las filas y se identifica su archivo y
  número de fila; el ID por sí solo no se usa para deduplicar.

Los CSV fueron proporcionados por el autor para uso investigativo. La
visualización es descriptiva y exploratoria, no una validación independiente
de cada estimación. No se requiere una API ni conexión a internet para
consultarlos; deben estar presentes en `data/research_inputs/` para que la
pestaña pueda cargarlos.

### KPI disponibles y definiciones

| Indicador | Definición utilizada | Alcance |
|---|---|---|
| Títulos seleccionados | Conteo de registros que cumplen los filtros activos. | Tamaño de la selección de catálogo; no es número de clientes. |
| Calificación promedio | Media de `vote_average`, en escala 0–10. | Valoración reportada en la fuente; no equivale a satisfacción de usuarios de StreamView. |
| Popularidad promedio | Media del índice `popularity`. | Índice de referencia de la fuente; no es cantidad de reproducciones. |
| ROI aproximado de películas | `revenue / budget`, solo cuando ambos campos son positivos. | Relación descriptiva, no rentabilidad contable. La moneda no está especificada en los archivos. |

También se exploran la oferta por género, país, idioma y tipo, las fechas de
estreno e incorporación, los créditos informados, los votos y las relaciones
entre métricas disponibles. Para comparaciones por grupo se muestran categorías
con al menos 20 títulos; un título con varios países puede contribuir a cada
país declarado.

### Hallazgos y calidad de datos verificados

- Los dos archivos suman 32.000 filas: 16.000 películas y 16.000 series.
- `show_id` no es una llave única global: hay 9 valores repetidos dentro del
  archivo de series y 397 identificadores compartidos entre películas y series.
  Al anexar los archivos se observan 406 filas duplicadas respecto de ese
  identificador. No se eliminaron registros porque no existe una regla de
  identidad confirmada.
- `rating` es numérico en los CSV y coincide exactamente con `vote_average` en
  todas las filas. El PDF describe `rating` como clasificación por edad (por
  ejemplo, TV-MA, PG-13 o R), pero esas categorías no están disponibles en los
  archivos; por tanto, ese análisis no es calculable con estas fuentes.
- `duration` está vacío en las 16.000 películas; no se calcula ni imputa una
  duración para ellas.
- Las duraciones complementarias se mantienen en CSV separados, son
  estimaciones no verificadas y no reemplazan el valor faltante de la fuente
  oficial del caso.
- `country` tiene 2.263 valores nulos en el catálogo y `director` está vacío en
  10.965 registros de series. Los análisis de geografía y créditos son
  descriptivos de los valores informados, no un censo completo.
- Las fechas `date_added` se convierten correctamente en las 32.000 filas.
  Entre 2010 y 2025 hay exactamente 2.000 registros por año en `release_year`;
  `date_added` también presenta exactamente 2.000 registros por año. Esta
  regularidad requiere validación con quien entregó la fuente antes de
  interpretarla como una tendencia real.
- Solo 3.540 películas tienen presupuesto e ingresos positivos. En esos
  registros, 1.298 tienen ingresos inferiores al presupuesto, 6 iguales y 2.236
  superiores. Los campos no especifican moneda y pueden incluir valores
  extremos; no se afirma rentabilidad neta.
- El índice `popularity` tiene mediana 10,9135 y máximo 3.876,006. Se conserva
  el extremo y se advierte sobre la cola de la distribución en lugar de
  eliminarlo sin una regla de negocio acordada.

### Lo que estos datos no permiten concluir

Los CSV no incluyen identificadores de suscriptores, altas o cancelaciones,
sesiones, búsquedas, impresiones, reproducciones, minutos vistos ni
finalizaciones. En consecuencia, **no permiten calcular churn, retención,
engagement real, reproducciones ni experiencia de usuario observada**. La
popularidad y los votos son atributos externos de los títulos y no deben
presentarse como métricas de uso de StreamView.

Para medir churn y retención se necesitarían registros anonimizados de
suscripción con fechas de alta/cancelación y una definición de churn. Para
engagement y UX se requerirían eventos de exposición, búsqueda y reproducción,
minutos vistos, finalizaciones, fecha y dispositivo, vinculados mediante un
identificador seudonimizado. Estos datos serían una nueva fuente, no una
transformación de los CSV actuales.

## Requisitos

- Git
- Python 3.11 o superior
- `pip`

Las dependencias directas y sus versiones están fijadas en `requirements.txt`.
`.venv/` es un entorno local excluido de Git: no se descarga al clonar y cada
usuario debe crearlo.

## Clonar, instalar y ejecutar

### Windows (PowerShell)

```powershell
git clone https://github.com/Paladynamo/STREAMVIEW-ANALYTICS.git
cd STREAMVIEW-ANALYTICS

# Crear una sola vez
py -m venv .venv

# Activar
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar desde la raíz
streamlit run dashboard/app.py
```

Si PowerShell bloquea la activación, permite scripts solo para la sesión actual
y vuelve a activar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
git clone https://github.com/Paladynamo/STREAMVIEW-ANALYTICS.git
cd STREAMVIEW-ANALYTICS
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run dashboard/app.py
```

Streamlit informa la dirección local, normalmente
`http://localhost:8501`. Para detener el servidor, presione `Ctrl+C`.

## Secciones del dashboard

- **Resumen ejecutivo:** tres KPI principales, composición y tendencias del
  catálogo, más una narrativa de decisiones y sus límites.
- **Catálogo y tendencias:** oferta por género, país e idioma; estrenos,
  incorporaciones y apariciones en créditos.
- **Popularidad y valoración:** títulos destacados, votos externos,
  calificaciones y comparaciones por género, país e idioma.
- **Finanzas de películas:** presupuesto, ingresos y ROI aproximado solo para
  los registros con ambos valores positivos.
- **Contexto y reglas:** resumen del caso, modelo, fuentes, diccionario, KPI y
  reglas aplicadas.
- **Fuentes y calidad:** faltantes, identificadores repetidos, controles,
  cobertura de preguntas del caso y datos que faltan para responderlas.
- **Investigación complementaria (en construcción):** análisis separado de los
  dos CSV estimados, filtros por tipo/año/género/valoración y descarga de las
  fuentes completas o de la selección. No interviene en el análisis principal.

Los filtros compartidos incluyen tipo de contenido, año de estreno, género y
calificación. La interfaz está en español y respeta el tema claro u oscuro
configurado en Streamlit. Los nombres originales de variables y títulos se
conservan cuando es necesario para la trazabilidad de la fuente.

## Estructura

```text
STREAMVIEW-ANALYTICS/
├── .venv/                 # Entorno local, excluido de Git
├── data/                  # CSV oficiales del caso
│   └── research_inputs/   # CSV complementarios, provisionales y separados
├── dashboard/
│   └── app.py             # Aplicación Streamlit
├── notebooks/             # Análisis exploratorio
├── images/
├── src/                   # Código fuente auxiliar
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Licencia

Consulte el archivo `LICENSE`.
