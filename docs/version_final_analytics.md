# StreamView Analytics — versión definitiva

## Resumen de la evolución

La versión definitiva conserva el dashboard existente y añade análisis complementarios. La navegación principal pasa a un selector horizontal de módulos y la investigación complementaria deja de presentarse como una sección en construcción. Los datos oficiales y los datos estimados permanecen separados.

## Módulos conservados

1. Resumen ejecutivo.
2. Catálogo y tendencias.
3. Popularidad y valoración.
4. Finanzas de películas.
5. Contexto y reglas.
6. Fuentes y calidad.
7. Investigación complementaria.

## Cambios de interfaz

- Navegación horizontal por módulos para reducir el desplazamiento vertical al cambiar de análisis.
- Filtros oficiales comunes en la barra lateral para los seis módulos principales.
- Filtros independientes en investigación complementaria.
- Vistas separadas para proxy, duración estimada, finanzas estimadas y trazabilidad.
- Ajustes de espaciado, ancho del contenido, tarjetas KPI y gráficos responsivos.

## Nuevos análisis

### Valoración ajustada por votos

Para un título con promedio de valoración R y cantidad de votos v, se calcula:

\[
R_{ajustada}=\frac{v}{v+m}R+\frac{m}{v+m}C
\]

Donde C es el promedio global de valoración en la selección y m es la mediana de votos de esa selección. La interfaz informa ambos parámetros y permite fijar un mínimo de votos para participar en el ranking.

Es una regla exploratoria de suavizado: no es una métrica oficial, no representa audiencia y puede variar al cambiar los filtros.

### Distribución de popularidad

Se agrega un histograma con eje X logarítmico para explorar una distribución con cola extrema sin eliminar registros.

### Duración estimada

Las películas se analizan en minutos estimados de duración total; las series se muestran en minutos estimados por episodio. Son magnitudes distintas y no verificadas.

### Finanzas estimadas

Se incorporan vistas exploratorias de ROI y utilidad bruta estimados cuando las columnas están presentes. No deben interpretarse como cifras contables ni como moneda verificada.

## Datos y límites

- Catálogos oficiales: 16.000 películas y 16.000 series.
- Total integrado: 32.000 registros.
- Los catálogos no contienen identificadores de clientes, altas, bajas, reproducciones, sesiones, minutos vistos ni finalizaciones.
- Por tanto, no es posible calcular churn, retención, clientes activos ni engagement real.
- Los CSV complementarios contienen estimaciones y proxies; no reemplazan los originales ni se incorporan a los KPI oficiales.
- La variable `rating` de los archivos es numérica y coincide con `vote_average`; no representa clasificación por edad.
- Los campos financieros originales no especifican moneda.
- La distribución temporal de exactamente 2.000 filas por año requiere validación con el responsable de la fuente antes de interpretarse como tendencia real.

## Correspondencia con EP5

El informe ejecutivo documenta problema de negocio, objetivos, audiencias, fuentes, exploración, justificación de gráficos, storytelling, dashboard, evaluación crítica, conclusiones y recomendaciones. Se mantienen los archivos reproducibles y la estructura profesional del proyecto.

## Correspondencia con EP6

La presentación ejecutiva se organiza para una exposición de hasta 10 minutos, seguida de hasta 5 minutos de preguntas. La defensa es individual: cada integrante debe poder justificar las representaciones, explicar fortalezas y limitaciones, proponer mejoras y defender recomendaciones e impacto esperado.

## Recomendaciones para la organización

1. Validar la estructura temporal y el origen de los registros antes de tomar decisiones de tendencia.
2. Corregir el diccionario de datos y reconciliar el significado de `rating`.
3. Definir una clave de negocio y reglas de deduplicación.
4. Verificar las estimaciones de duración y finanzas, registrando fuente, fecha, método y confianza.
5. Para medir retención y churn, incorporar datos longitudinales seudonimizados de suscripción.
6. Para medir engagement y experiencia, incorporar eventos de exposición, búsqueda y reproducción, con fecha y dispositivo y controles de privacidad.
