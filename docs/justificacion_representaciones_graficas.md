# Justificación de las representaciones gráficas y evaluación crítica

- **Proyecto:** StreamView Analytics
- **Autor:** Eduardo Lizama
- **Fecha de revisión visual:** 13 de octubre de 2026
- **Alcance:** dashboard interactivo y archivos de catálogo disponibles en el proyecto.

## Propósito y alcance de la lectura

El dashboard integra 32.000 registros de catálogo: 16.000 películas y 16.000
series. Sus visualizaciones describen la oferta y los metadatos incluidos en los
archivos; no describen directamente suscriptores ni actividad de clientes. Los
filtros de tipo, año, género y valoración permiten acotar la selección, y los
KPI principales se recalculan con ella.

Las capturas enlazadas corresponden a las siete secciones y conservan la
interfaz, los filtros, los KPI y las visualizaciones de cada vista:

1. [Resumen ejecutivo](../images/dashboard/01_resumen_ejecutivo.png)
2. [Catálogo y tendencias](../images/dashboard/02_catalogo_tendencias.png)
3. [Popularidad y valoración](../images/dashboard/03_popularidad_valoracion.png)
4. [Finanzas de películas](../images/dashboard/04_finanzas_peliculas.png)
5. [Contexto y reglas](../images/dashboard/05_contexto_reglas.png)
6. [Fuentes y calidad](../images/dashboard/06_fuentes_calidad.png)
7. [Investigación complementaria (en construcción)](../images/dashboard/07_investigacion_complementaria.png)

## Justificación de las representaciones gráficas

### Indicadores y filtros compartidos

- **Títulos seleccionados:** conteo de filas que pasan los filtros. Es una
  medida directa del tamaño de la selección, no de usuarios o reproducciones.
- **Calificación promedio:** media de `vote_average` en escala de 0 a 10. Se
  muestra en escala explícita para que la magnitud sea interpretable. En los
  archivos, `rating` coincide con `vote_average`; no se interpreta como
  clasificación por edad.
- **Popularidad promedio:** se conserva como indicador separado porque es un
  índice externo de popularidad, no un conteo de visualizaciones de StreamView.
- **Filtros:** tipo, intervalo de años, géneros y calificación limitan las
  comparaciones al mismo subconjunto. La selección de varios géneros puede
  incluir títulos que tengan cualquiera de los géneros elegidos.

### Resumen ejecutivo

- **Líneas de estrenos por año:** una línea permite comparar la evolución
  temporal entre películas y series y conserva el orden de los años. En la
  fuente actual el gráfico muestra exactamente 1.000 registros por tipo y año
  entre 2010 y 2025; esta regularidad produce una línea plana y debe validarse
  antes de interpretarla como una tendencia real.
- **Gráfico de dona de composición:** resume en una proporción sencilla la
  cantidad de películas y series. El resultado 50/50 refleja que los archivos
  entregados contienen 16.000 filas de cada tipo; no prueba que el catálogo de
  una plataforma tenga esa composición.
- **Barras horizontales de géneros:** facilitan comparar y ordenar categorías
  por cantidad de títulos, con las etiquetas en español y el valor más alto
  fácilmente localizable. Un mismo registro puede pertenecer a varios géneros,
  por lo que los conteos por género no suman necesariamente el total de filas.
- **Tarjetas adicionales de películas, series, países, idiomas y géneros:**
  condensan el tamaño y diversidad informada del catálogo antes de entrar a
  los detalles.

### Catálogo, geografía y producción

- **Barras horizontales por género, país e idioma:** son adecuadas para
  comparar varias categorías con etiquetas de longitud desigual. Se muestran
  los grupos principales, no todas las categorías de alta cardinalidad.
- **Barras por país:** el campo puede contener varios países por título; al
  desglosarlo, una fila contribuye a cada país informado. Por ello, los valores
  representan apariciones declaradas y no particiones excluyentes.
- **Área de incorporaciones por año:** comunica el volumen anual y permite
  contrastar las dos series por tipo. En esta fuente hay exactamente 2.000
  registros por año en el periodo observado, por lo que la forma constante
  requiere corroboración antes de atribuirla a crecimiento, estrategia de
  lanzamientos o actividad de la plataforma.
- **Barras de directores y actores:** presentan apariciones en los créditos de
  cada título. No constituyen una medida de audiencia, calidad artística ni
  impacto causal; además, los créditos faltantes limitan su cobertura.

### Popularidad y valoración

- **Barras horizontales de los 10 títulos principales por popularidad y por
  votos:** exponen rankings independientes y facilitan comparar los valores
  sin solapar nombres extensos. Popularidad y número de votos son medidas
  distintas y ambas son externas al comportamiento observado de StreamView.
- **Dispersión de valoración frente a popularidad:** muestra simultáneamente
  dos métricas numéricas por título. El tamaño codifica la cantidad de votos,
  lo que da contexto al volumen de observaciones. La asimetría y los extremos
  de popularidad pueden comprimir visualmente la nube principal; conviene
  leerla junto con el índice y la nota sobre sus límites.
- **Barras de popularidad por género con color de valoración:** combinan una
  comparación de popularidad promedio por grupo y una codificación cromática
  de otra métrica. Los grupos pequeños se excluyen mediante el umbral vigente
  de 20 títulos. Aun con ese umbral, los promedios no tienen el mismo tamaño
  muestral ni son evidencia causal.
- **Barras de popularidad/calificación por país e idioma:** comparan resúmenes
  agregados entre grupos. El desglose de países es múltiple, y los promedios
  pueden ser sensibles al número de registros y a la composición de cada
  grupo.
- **Tabla de títulos mejor evaluados:** permite consultar título, tipo,
  valoración y cantidad de votos. La advertencia de la interfaz es importante:
  una calificación alta con muy pocos votos no debe interpretarse como una
  estimación robusta ni equipararse a alta audiencia.

### Finanzas de películas

- **Dispersión de presupuesto frente a ingresos con ejes logarítmicos:** los
  valores financieros abarcan varios órdenes de magnitud; la escala logarítmica
  permite ver tanto los valores relativamente bajos como los altos. Solo se
  incluyen películas con presupuesto e ingresos positivos y el tamaño del
  punto representa votos. La escala transforma distancias: debe leerse según
  sus marcas y no como una diferencia lineal.
- **Barras de mayores ingresos:** ordenan las películas con mayores valores de
  `revenue` reportados y permiten comparar nombres y montos. No muestran
  beneficio neto.
- **Barras de ROI aproximado:** presentan `revenue / budget` para comparar
  razones descriptivas. Valores extremos pueden estar dominados por
  presupuestos pequeños o datos atípicos; el cociente no es ROI contable.
- **KPI y tabla de películas con menor presupuesto:** restringen la
  interpretación al subconjunto evaluable y hacen explícito el criterio del
  cuartil inferior. Se informa que la moneda no está especificada en los CSV
  originales; los nombres de columnas USD en los CSV complementarios no
  constituyen validación independiente de moneda o valor.

### Contexto, calidad e investigación complementaria

- **Tablas del contexto y reglas:** se usan porque el modelo, el diccionario,
  las definiciones de KPI y las reglas requieren texto preciso y trazabilidad,
  no una codificación gráfica que pueda ocultar excepciones.
- **Tabla de calidad, faltantes y hallazgos:** comunica conteos y porcentajes
  de forma verificable. Separar fuente por tipo ayuda a distinguir los
  faltantes de películas de los de series y a mostrar identificadores
  repetidos sin deduplicar arbitrariamente.
- **Proxy investigativo por género:** se presenta como barras horizontales
  para comparar una señal incluida en los CSV complementarios. El texto
  explícito de la vista aclara que es un proxy calculado con percentiles de
  popularidad y votos, no engagement observado.
- **Duración estimada y tabla complementaria:** se separan de los indicadores
  oficiales. La duración estimada de una película y la duración estimada por
  episodio de una serie tienen alcances distintos; las temporadas y la
  duración total comprobada de las series no están disponibles.

## Evaluación crítica: fortalezas, limitaciones, mejoras

### Fortalezas

1. **Recorrido por audiencia y pregunta:** navegación separada entre resumen,
   catálogo, popularidad, finanzas, contexto, calidad e investigación facilita
   pasar de una lectura ejecutiva a una exploración más detallada.
2. **Interacción coherente:** los filtros del catálogo son comunes a las vistas
   principales y los KPI se recalculan sobre la selección. La vista de
   investigación mantiene sus propios filtros y fuente, evitando mezclar
   datos provisionales con el análisis oficial.
3. **Codificación reconocible:** películas y series conservan colores
   consistentes en comparaciones; las barras horizontales reducen problemas
   de lectura en etiquetas largas y los valores numéricos importantes se
   muestran en KPI o tablas.
4. **Limitaciones visibles:** las advertencias acompañan las visualizaciones
   afectadas. El dashboard diferencia popularidad externa, proxy, estimación y
   actividad real de clientes, en lugar de presentarlos como equivalentes.
5. **Trazabilidad:** las tablas mantienen nombres de variables originales y
   las descargas de investigación conservan procedencia y estados disponibles.

### Limitaciones

1. **La fuente temporal requiere corroboración.** Hay exactamente 2.000 filas
   por año en `release_year` y también en `date_added`. Las líneas y áreas
   resultantes describen esa estructura del archivo, pero no bastan para
   afirmar una tendencia real de la industria o de la plataforma.
2. **La composición 50/50 está condicionada por el muestreo entregado.** Se
   dispone del mismo número de filas por tipo, de modo que la dona puede
   sugerir una distribución real que la fuente no demuestra.
3. **Cobertura incompleta y claves problemáticas.** Hay 9 `show_id` repetidos
   en el CSV de series y 397 identificadores compartidos entre tipos. Además,
   hay faltantes de país, director y género. Los recuentos de personas,
   países y categorías deben leerse con estas limitaciones.
4. **`rating` no coincide con la definición del caso.** En estos archivos es
   numérico, coincide con `vote_average` y no aporta clasificación etaria.
   Mostrarlo como tal no responde preguntas sobre adecuación por edad.
5. **Rankings de valoración sensibles a pocos votos.** Un título con una
   valoración de 10 y uno o pocos votos puede aparecer en los primeros lugares.
   Sin ponderación o un mínimo de votos, no es comparable con títulos con
   muchas evaluaciones.
6. **Extremos de popularidad y finanzas.** La popularidad presenta una cola
   extrema (mediana reportada de 10,9135 y máximo de 3.876,006). Solo 3.540
   películas tienen presupuesto e ingresos positivos, y el ROI más alto es
   particularmente sensible al denominador. La moneda de la fuente no está
   especificada.
7. **No hay conducta de clientes.** Los catálogos no incluyen altas, bajas,
   sesiones, búsquedas, reproducciones, minutos vistos ni finalizaciones.
   Por ello no permiten medir churn, retención, engagement real o experiencia
   de usuario observada.
8. **Los datos complementarios son estimaciones.** Las 32.000 filas de los
   CSV complementarios marcan `runtime_is_estimate = True`. El score de
   engagement es un proxy, no consumo, y los indicadores financieros
   complementarios también necesitan validación independiente.
9. **Legibilidad a escala de captura.** Las vistas extensas agrupan varios
   gráficos y tablas en una página alta. En una pantalla pequeña el lector
   necesita desplazarse y algunas tablas anchas pueden requerir desplazamiento
   horizontal; las capturas completas sirven como evidencia, pero no reemplazan
   la exploración interactiva.

### Mejoras recomendadas

**Prioridad alta — calidad, definiciones y datos necesarios**

- Confirmar con el responsable de los datos por qué cada periodo contiene el
  mismo número de filas y si los campos representan una muestra, una
  generación sintética o un catálogo completo.
- Obtener un diccionario corregido y reconciliar `rating` con la clasificación
  etaria esperada. Hasta entonces, rotularlo siempre como valoración numérica.
- Documentar una clave de registro y una regla de deduplicación por tipo,
  identificador, título y año antes de sumar filas o integrar nuevas fuentes.
- Para churn y retención, solicitar datos longitudinales seudonimizados de
  suscripción, fechas de altas/bajas y una definición de cancelación, periodo
  de gracia y población elegible. Para engagement/UX, solicitar eventos de
  impresión, búsqueda, reproducción, minutos vistos, finalización, fecha y
  dispositivo con controles de privacidad.
- Verificar duraciones, presupuesto, ingresos y moneda en una fuente
  identificada título por título. Registrar fuente, enlace, fecha de consulta,
  método, confianza y si el valor es estimado o comprobado; no sobrescribir
  los archivos originales.

**Prioridad media — comparación estadística y robustez**

- Mantener el conteo de filas, pero acompañar tendencias por año con cobertura
  de la fuente y, si existe una población comparable, una tasa o proporción
  calculada sobre un denominador conocido.
- Para rankings de valoración, mostrar siempre `vote_count`, establecer una
  regla de mínimo de votos justificada por análisis y ofrecer una vista sin
  umbral para transparentar el efecto. Evitar presentarlos como ranking de
  audiencia.
- Para popularidad sesgada, agregar una vista con escala logarítmica o
  percentiles y conservar los valores originales accesibles en hover/tabla.
- En finanzas, mostrar distribución y sensibilidad a presupuestos bajos,
  diferenciar explícitamente magnitudes originales de cocientes y no etiquetar
  `revenue / budget` como rentabilidad contable.
- Acompañar los promedios de país, idioma y género con tamaño muestral y
  medida de dispersión; revisar cómo el desglose múltiple cambia los
  denominadores.

**Prioridad de experiencia — legibilidad y validación con usuarios**

- Probar tareas concretas con representantes de Dirección, Contenidos,
  Marketing y Data: por ejemplo, comparar oferta por país o encontrar títulos
  con determinada combinación de popularidad y valoración.
- Considerar una página ejecutiva más compacta y páginas de detalle con
  selectores de visualizaciones o pestañas para evitar que cada lectura
  requiera mucho desplazamiento.
- Revisar contraste y lectura en los temas claro y oscuro, etiquetas de
  valores, formatos de moneda tras validar la divisa y accesibilidad de
  colores para usuarios con deficiencias de percepción cromática.
- Registrar para cada KPI su fórmula, población incluida, periodo, filtros,
  unidad, exclusiones y fuente en una ficha breve accesible desde la interfaz.

## Conclusión

El diseño actual funciona como explorador descriptivo del catálogo y comunica
con claridad varios límites importantes. Sus visualizaciones ayudan a comparar
registros y a formular preguntas de negocio, pero no convierten estas fuentes
en evidencia de consumo, retención o churn. La prioridad para fortalecer las
conclusiones es validar el origen y la estructura temporal de los datos y
obtener fuentes de actividad de clientes; las cifras investigativas deben
continuar separadas y marcadas como provisionales.
