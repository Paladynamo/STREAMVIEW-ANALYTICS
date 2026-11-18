# Informe ejecutivo: StreamView Analytics

**Proyecto:** Visualización de datos para toma de decisiones  
**Autor:** Eduardo Lizama  
**Asignatura:** ADY1104 – Visualización de Datos  
**Fecha:** noviembre de 2026

## 1. Resumen ejecutivo

StreamView Analytics es un dashboard interactivo desarrollado en StreamLit que integra 32.000 registros de catálogo: 16.000 películas y 16.000 series. La solución organiza el análisis en navegación lateral, indicadores KPI y solapas temáticas para reducir desplazamientos y facilitar la exploración individual de tendencias, géneros, territorios, popularidad y finanzas.

Los datos permiten describir la oferta disponible y atributos externos de los títulos. No permiten medir suscriptores, reproducciones, cancelaciones, retención, satisfacción ni engagement real. Por ello, todas las recomendaciones son hipótesis verificables y no afirmaciones causales.

## 2. Problema de negocio

StreamView requiere comprender su catálogo para apoyar decisiones de contenidos, adquisición, marketing y producto. La información estaba distribuida en reportes separados y podía presentar indicadores inconsistentes. El proyecto busca consolidar una vista trazable que distinga datos oficiales de estimaciones complementarias y comunique los límites de interpretación.

## 3. Objetivos

- Consolidar películas y series en una vista analítica de 32.000 registros.
- Identificar composición, géneros, países, idiomas, estrenos, popularidad y valoración.
- Analizar presupuesto e ingresos solo en películas con valores positivos y comprobables en los archivos.
- Facilitar filtros compartidos y exploración mediante navegación y solapas.
- Diferenciar hallazgos descriptivos de métricas reales de clientes.
- Entregar una solución reproducible con documentación profesional y trazabilidad.

## 4. Audiencia y propósito comunicacional

| Audiencia | Necesidad | Uso esperado |
|---|---|---|
| Directorio y Gerencia General | Panorama ejecutivo, riesgos y prioridades | Definir agenda de adquisición y validar información faltante |
| Gerencia de Contenidos y Adquisición | Géneros, territorios, créditos y incorporaciones | Formular hipótesis de portafolio |
| Marketing y Producto | Popularidad, valoración y votos externos | Diseñar pruebas de promoción sin confundir índice con uso |
| Finanzas | Presupuesto e ingresos disponibles | Analizar magnitudes y no rentabilidad contable |
| Equipo de Datos | Calidad, claves y supuestos | Priorizar validaciones y nuevas fuentes |

## 5. Fuentes y modelo

Los archivos oficiales son `netflix_movies_detailed_up_to_2025.csv` y `netflix_tv_shows_detailed_up_to_2025.csv`. La integración usa anexión por tipo de contenido y conserva una fila por registro. `_content_row` es una llave técnica local, no una llave de negocio.

Los CSV oficiales contienen entre otros: `show_id`, `title`, `type`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `genres`, `language`, `popularity`, `vote_count`, `vote_average`, `budget` y `revenue`.

Los dos CSV complementarios tienen 32.000 filas y se mantienen separados. Incluyen duración estimada, método, estado y un `engagement_proxy_score`. Este índice no representa engagement observado y no interviene en KPI ni filtros oficiales.

## 6. Hallazgos exploratorios

- Los archivos suman exactamente 16.000 películas y 16.000 series.
- `release_year` y `date_added` presentan exactamente 2.000 registros por año en los rangos observados. Esa regularidad puede corresponder a muestreo sintético o generado y debe validarse antes de interpretarla como una tendencia real.
- Hay 9 `show_id` repetidos dentro de series y 397 identificadores compartidos entre películas y series. Se conservan las filas y no se deduplican de forma arbitraria.
- `country` tiene 2.263 valores nulos y `director` está vacío en 10.965 registros de series.
- `rating` coincide exactamente con `vote_average` y es numérico; no se interpreta como clasificación por edad.
- Solo 3.540 películas tienen presupuesto e ingresos positivos.
- Entre esas películas, 1.298 tienen ingresos inferiores al presupuesto, 6 iguales y 2.236 superiores. Los campos no especifican moneda y no permiten calcular rentabilidad neta.
- `popularity` tiene cola extrema: mediana 10,9135 y máximo 3.876,006. Debe mostrarse junto con el contexto de medidad externa y no como reproducciones.
- El ranking de valoración es sensible a pocos votos. No debe usarse sin considerar el volumen de evaluaciones.

## 7. Justificación de representaciones

- Líneas para evolución temporal entre tipos.
- Dona para mostrar composición, con advertencia sobre la muestra 50/50.
- Barras horizontales para géneros, países, idiomas y créditos con etiquetas largas.
- Dispersión con tamaño de votos para relacionar calificación y popularidad.
- Escala logarítmica para presupuesto e ingresos debido a varios órdenes de magnitud.
- Tablas para diccionarios, calidad y rankings donde el texto preciso tiene más valor que la codificación gráfica.
- Solapas para separar visualizaciones relacionadas y reducir desplazamiento vertical.

## 8. Diseño e implementación del dashboard

La interfaz utiliza un tema claro coherente, KPI con borde, navegación lateral y contenedores responsivos. Los filtros compartidos recalculan los análisis principales por tipo, año, género y calificación. Las secciones se organizan en solapas:

- Resumen: evolución, composición, géneros y lectura ejecutiva.
- Catálogo: mercado, incorporaciones y créditos.
- Popularidad: rankings, relación, agrupaciones, territorios y tabla.
- Finanzas: KPI, dispersión, rankings y cuartil inferior.

La investigación complementaria mantiene filtros propios y queda separada de los datos oficiales. Esta separación evita que estimaciones se presenten como hechos.

## 9. Data storytelling y decisiones

La narrativa sigue un recorrido ejecutivo:

1. Medir la dimensión de la selección mediante KPI.
2. Revisar composición y evolución del catálogo.
3. Identificar categorías y territorios relevantes.
4. Interpretar popularidad y valoración como señales externas.
5. Aplicar restricciones financieras a un subconjunto evaluable.
6. Explicar calidad, límites y datos necesarios.

La decisión recomendada no es comprar o promocionar automáticamente por el ranking de una métrica. Debe utilizarse como priorización de hipótesis que será contrastada con datos de clientes.

## 10. Fortalezas

- Navegación clara y consistente.
- Filtros comunes y KPI recalculados.
- Separación visible entre datos oficiales y estimaciones.
- Advertencias junto a cada métrica sensible.
- Trazabilidad de variables y descargas investigativas.
- Código reproducible y estructura profesional del proyecto.

## 11. Limitaciones y riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Identificadores no únicos | Conteos o integraciones incorrectas | Definir clave de registro y reconciliación por tipo/título/año |
| Periodos uniformes | Tendencia falsa | Validar muestreo, generación y cobertura con el responsable |
| Falta de variables de clientes | No se puede medir retención/engagement | Incorporar eventos seudonimizados y suscripción |
| Ranking sin volumen mínimo | Valoraciones basadas en pocos votos | Agregar umbral y calificación ponderada |
| Extremos de popularidad y finanzas | Visualización y promedios distorsionados | Mostrar mediana, colas y métodos de sensibilidad |
| Moneda no especificada | Interpretación financiera inválida | Confirmar moneda y validación título por título |

## 12. Recomendaciones priorizadas

1. Validar la regularidad temporal y el significado de `release_year` y `date_added`.
2. Corregir el diccionario de `rating` y reconciliarlo con clasificación por edad si existe.
3. Crear una llave técnica por archivo y establecer una regla de integración sin deduplicar arbitrariamente.
4. Incorporar fuentes de suscripciones y reproducción: altas, bajas, sesiones, búsquedas, reproducciones, minutos vistos y finalizaciones.
5. Añadir métricas por cohorte: retención, churn, frecuencia y finalización.
6. Aplicar umbral mínimo de votos y ponderación a rankings.
7. Registrar moneda, fuente y estado de verificación de valores financieros.
8. Mantener la narrativa visible junto a KPI y gráficos para evitar interpretaciones fuera de contexto.

## 13. Conclusiones

El dashboard entrega una solución integral de visualización que convierte un catálogo heterogéneo en una vista ejecutiva y exploratoria. Su principal valor no es pronosticar el comportamiento de clientes, sino ordenar evidencias, reducir ambigüedad y facilitar preguntas verificables. La próxima fase debe integrar datos longitudinales de usuarios y productos para transformar hallazgos descriptivos en decisiones de retención y engagement.
