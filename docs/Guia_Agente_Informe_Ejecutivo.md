# Guia para crear el informe ejecutivo detallado de StreamView Analytics

## Objetivo

Crear un informe ejecutivo profesional en PDF o Markdown para entregar al profesor y al equipo directivo del caso. Debe documentar el problema, objetivos, audiencia, fuentes, analisis, representaciones, dashboard, critica, recomendaciones y hitos del proyecto.

El informe debe ser trazable, tecnico y prudente. Cada afirmacion cuantitativa debe indicar alcance y fuente. No debe confundir metadatos externos o estimaciones con actividad real de usuarios.

## Estructura obligatoria

### 1. Portada

Incluir:

- StreamView Analytics.
- Informe ejecutivo.
- Visualizacion de datos.
- Eduardo Lizama.
- ADY1104.
- Fecha.
- Nombre del equipo si corresponde.
- Version final.

### 2. Resumen ejecutivo

Redactar uno o dos parrafos con:

- Objetivo del proyecto.
- Alcance de 32.000 registros.
- Tecnologia usada: StreamLit, Python, Pandas y Plotly.
- Solucion entregada.
- Principales limitaciones.
- Conclusion relevante.

Ejemplo de formula:

> StreamView Analytics consolida 32.000 registros de catalogo y ofrece navegacion modular, filtros, KPI y visualizaciones para apoyar decisiones exploratorias de contenidos, adquisicion y marketing.

### 3. Contexto organizacional

Explicar el caso academico:

- Plataforma internacional de streaming digital.
- Foco en Latino Latinoamerica.
- Necesidad de comprender catalogo y comportamiento de usuarios.
- Los datos disponibles no contienen actividad real de clientes.

No presentar la empresa como verificada ni atribuirle informacion no incluida en el caso.

### 4. Problema de negocio

Documentar:

- Informacion distribuida.
- Comparaciones dificiles.
- Riesgo de indicadores inconsistentes.
- Vistas sobrecargadas.
- Falta de una narrativa visual integrada.

Relacionar el problema con decisiones:

- Contenidos.
- Adquisicion.
- Marketing.
- Producto.
- Datos.

### 5. Objetivos del proyecto

Incluir objetivos generales y especificos:

- Integrar catalogo.
- Identificar composicion y tendencias.
- Calcular KPI sobre una seleccion filtrada.
- Comparar popularidad y valoracion.
- Analizar presupuesto e ingresos.
- Mostrar calidad y limitaciones.
- Separar estimaciones.
- Entregar codigo reproducible.

### 6. Audiencia objetivo

Usar una tabla con audiencia, necesidad, decision y visualizacion relacionada.

| Audiencia | Necesidad | Uso |
|---|---|---|
| Directorio | Panorama y riesgos | Prioridades |
| Contenidos | Generos y territorios | Hipotesis de adquisicion |
| Marketing | Popularidad y votos | Pruebas de promocion |
| Finanzas | Presupuesto e ingresos | Revision del subconjunto evaluable |
| Datos | Calidad y claves | Validacion de fuentes |

### 7. Alcance

Indicar que esta entrega utiliza:

- Dos CSV oficiales.
- Dos CSV complementarios separados.
- Analisis descriptivo.
- Dashboard interactivo.
- Informe y presentacion.

Indicar que no incluye:

- Prediccion.
- IA de recomendacion.
- ETL operativo.
- Cambios en sistemas de produccion.
- Churn real.
- Retencion real.
- Engagement observado.
- Reproducciones o minutos vistos.

### 8. Fuentes y descripcion

Presentar una tabla:

| Fuente | Filas | Columnas | Uso |
|---|---:|---:|---|
| Peliculas oficial | 16.000 | 18 | Catalogo y finanzas |
| Series oficial | 16.000 | 16 | Catalogo y valoracion |
| Peliculas complementario | 16.000 | 46 | Investigacion estimada |
| Series complementario | 16.000 | 45 | Investigacion estimada |

Explicar que los ZIP o fuentes originales se compararon mediante SHA-256 cuando corresponda y que no aportaron datos de clientes.

### 9. Diccionario y grano

Definir las variables principales y el grano:

- Una fila por registro de catalogo.
- `_content_row` evita colisiones tecnicas en el proceso.
- `show_id` no es llave unica.
- Las variables multivaluadas pueden contar un titulo en varias categorias.

Lista minima:

- `show_id`.
- `title`.
- `type`.
- `release_year`.
- `date_added`.
- `genres`.
- `country`.
- `language`.
- `director`.
- `cast`.
- `rating`.
- `vote_average`.
- `vote_count`.
- `popularity`.
- `budget`.
- `revenue`.

### 10. Reglas de integracion y filtros

Documentar:

- Anexion de peliculas y series.
- Tipo agregado como etiqueta analitica.
- Filtros por tipo, ano, genero y calificacion.
- Generos seleccionados con criterio OR.
- Paises multiples desglosados.
- Grupos con al menos 20 registros para comparaciones agregadas.
- Solo peliculas con budget y revenue positivos en finanzas.
- Datos oficiales separados de los complementarios.

### 11. KPI y definiciones

| KPI | Formula o definicion | Alcance |
|---|---|---|
| Titulos seleccionados | Conteo de filas filtradas | Catalogo |
| Calificacion promedio | Media de `vote_average` | 0 a 10, no satisfaccion |
| Popularidad promedio | Media de `popularity` | Indice externo |
| ROI aproximado | `revenue / budget` | Solo peliculas evaluables |

No llamar rentabilidad al ROI aproximado.

### 12. Analisis exploratorio

### 12.1 Volumen

Mencionar:

- 32.000 registros totales.
- 16.000 por tipo.
- Composicion 50/50 en la muestra.
- No demostrar composicion real de una plataforma.

### 12.2 Tiempo

Mencionar:

- 2.000 registros por ano entre 2010 y 2025 en `release_year`.
- 2.000 registros por ano en `date_added`.
- La regularidad requiere validacion.
- No atribuir crecimiento real de produccion o incorporacion.

### 12.3 Calidad de identidad

Mencionar:

- 9 `show_id` repetidos en series.
- 397 identificadores compartidos entre tipos.
- 406 filas afectadas al revisar colisiones.
- No se deduplicaron sin una regla acordada.

### 12.4 Faltantes

Mencionar:

- `country`: 2.263 faltantes.
- `director`: 10.965 faltantes en series.
- `duration`: vacia en 16.000 peliculas.
- `genre`: 107 faltantes en peliculas y 974 en series segun la tabla oficial integrada.

Explicar como afectan geografia, creditos y duracion.

### 12.5 Valoracion y popularidad

- `rating` coincide con `vote_average`.
- No es clasificacion por edad.
- Popularidad tiene mediana 10,9135 y maximo 3.876,006.
- Rankings deben incluir votos y umbral minimo.

### 12.6 Finanzas

- 3.540 peliculas evaluables.
- 1.298 con ingresos menores que presupuesto.
- 6 con valores iguales.
- 2.236 con ingresos mayores.
- Moneda no especificada.
- Revenue / Budget no incluye costos ni flujos contables.

### 13. Hitos del proyecto

Esta seccion es esencial para demostrar la evolucion hasta la entrega final.

| Hito | Cambio realizado | Problema que resolvio | Evidencia |
|---|---|---|---|
| 1. Diagnostico | Revision de archivos y caso | Definir alcance y variables | README y diccionario |
| 2. Integracion | Anexion de peliculas y series | Vista consolidada | `_content_row`, tipo y filtros |
| 3. KPI inicial | Titulos, calificacion y popularidad | Respuesta ejecutiva rapida | Recalculo por seleccion |
| 4. Analisis oficial | Generos, paises, tiempos y creditos | Comparacion por audiencias | Secciones y graficos |
| 5. Finanzas | Filtro de presupuesto e ingresos positivos | Evitar sumar series o datos faltantes | Cuatro KPI y visualizaciones |
| 6. Calidad | Tabla de faltantes e IDs | Hacer visibles sesgos y llaves | Vista de calidad |
| 7. Investigacion | CSV complementarios separados | Evitar confundir estimaciones con hechos | Descargas y filtros propios |
| 8. Critica visual | Justificacion de graficos | Mejorar seleccion segun dato y objetivo | Documento de representaciones |
| 9. Tema profesional | Configuracion StreamLit | Jerarquia visual coherente | `.streamlit/config.toml` |
| 10. Subsolapas | Separacion por familias de grafico | Menos deslizamiento vertical | st.tabs en resumen, catalogo, popularidad y finanzas |
| 11. Solapas principales | Navegacion superior | Reemplazo de menu lateral rigido | st.tabs en main |
| 12. Correccion de renderizado | Eliminacion de `.open` manual | Evitar informacion pegada entre apartados | Bloques with tab_* |
| 13. Restablecimiento | Boton de filtros iniciales | Volver rapidamente al universo completo | Sesion de StreamLit |
| 14. Comparacion | Segundo periodo configurable | Analizar cambios entre rangos | Tabla y grafico de variacion |
| 15. Ranking ponderado | Ajuste por volumen de votos | Reducir sesgo de rankings con poca evidencia | Calificacion ponderada configurable |
| 16. Distribucion | Mediana, cuartiles, percentiles e histograma | Explicar extremos de popularidad | KPI y grafico interactivo |
| 17. Descarga | CSV de seleccion oficial | Reutilizar resultados y auditar | Boton en sidebar |
| 18. Trazabilidad | Llave con archivo, fila y tipo | Identificar registros sin deduplicar arbitrariamente | `_content_key` |
| 19. Narrativa y cobertura | Conclusion ejecutiva y cobertura | Explicar alcance de cada seleccion | Resumen y KPI |
| 20. Entregables | Informe, PDF y PPT | Cumplir EP5 y EP6 | Carpetas de deliverables |

El texto no debe presentarse como una lista meramente cosmetica. Destacar que las mejoras finales mejoraron navegacion, legibilidad, responsividad y correccion tecnica.

### 14. Justificacion de representaciones

Explicar para cada tipo:

- Linea: evolucion temporal.
- Dona: composicion.
- Barras horizontales: categorias con nombres largos.
- Area: incorporaciones por periodo.
- Dispersion: relacion entre variables.
- Escala logaritmica: rangos financieros heterogeneos.
- Tabla: precision de claves y variables.
- KPI: resumen inmediato.
- Solapas: exploracion individual sin perder contexto.

Incluir una evaluacion de percepcion visual:

- Jerarquia.
- Accesibilidad.
- Consistencia cromatica.
- Longitud de etiquetas.
- Escalas.
- Advertencias.
- No codificar dos mediciones con atributos confusos.

### 15. Design and implementation

Describir:

- StreamLit como herramienta autorizado por el profesor.
- Python 3.14 validado.
- StreamLit 1.63.0.
- Pandas 3.0.5.
- Plotly 7.0.0.
- Cache de carga.
- Filtrado fuera del codigo de carga pesada.
- Configuracion de tema.
- Solapas principales y secundarias.
- Exportacion de CSV en investigacion.

No agregar dependencias que no sean parte final sin verificar.

### 16. Narrativa visual

Organizar el recorrido:

1. Dimension de la seleccion.
2. Composicion y evolucion.
3. Catalogo por categoria.
4. Popularidad y calificacion.
5. Dimension financiera.
6. Calidad.
7. Datos faltantes y siguiente fase.

Explicar que la narrativa es secuencial y no causal.

### 17. Fortalezas

Fundamentar cada fortaleza:

- Navegacion clara.
- Recorrido por audiencia.
- KPI recalculados.
- Codificacion coherente.
- Advertencias visibles.
- Trazabilidad.
- Separacion de datos.
- Exportacion.
- Codigo documentado.

### 18. Limitaciones y riesgos

La seccion debe incluir riesgos, impacto y mitigacion:

| Riesgo | Impacto | Mitigacion |
|---|---|---|
| show_id no unico | Conteos ambiguos | Definir llave |
| Periodos uniformes | Tendencia falsa | Validar muestreo |
| rating mal descrito | Clasificacion inexistente | Reconciliar diccionario |
| Pocos votos | Ranking extremo | Umbral y ponderacion |
| Popularidad extrema | Promedios distorsionados | Mediana y sensibilidad |
| Moneda desconocida | Conclusion financiera invalida | Verificar fuente |
| Sin usuarios | No medir churn ni UX | Agregar eventos |
| Estimaciones | No validar consumo real | Separar y marcar |

### 19. Oportunidades de mejora

Clasificar:

**Inmediatas**

- Validar periodos.
- Corregir diccionario.
- Definir llave.
- Confirmar moneda.
- Mostrar mediana y rangos.
- Agregar umbral de votos.

**Siguiente fase**

- Suscripciones con altas y bajas.
- Reproducciones y minutos vistos.
- Finalizaciones.
- Busquedas e impresiones.
- Dispositivos.
- Fecha y cohorte.
- Privacidad y pseudonimizacion.
- Reglas de churn acordadas.

**Evolucion del dashboard**

- Guardar filtros en URL.
- Permitir comparacion de cohortes.
- Anadir exportacion de seleccion general.
- Incorporar descarga de resultados de popularidad y finanzas.
- Mantener filtros comparables compartibles mediante URL.
- Anadir filtros dinamicos por pais o idioma.
- Agregar indicadores de calidad junto a KPI.

No prometer mejoras que no esten implementadas en esta entrega.

### 20. Conclusiones

Redactar conclusiones separadas de recomendaciones:

- El dashboard entrega una vista integrada y trazable.
- Las visualizaciones son apropiadas al tipo de dato.
- Las solapas reducen rigidez y desplazamiento.
- Los resultados son descriptivos.
- El principal riesgo es extrapolar datos de catalogo a conducta real.
- La siguiente fase debe incorporar datos de usuarios.

### 21. Recomendaciones

Priorizar recomendaciones con evidencia:

1. Validar el muestreo temporal.
2. Reconciliar la definicion de rating.
3. Crear regla de identidad.
4. Confirmar moneda financiera.
5. Incorporar volumen de votos.
6. Incorporar datos de suscripcion.
7. Incorporar eventos de reproduccion.
8. Mantener separacion de estimaciones.

### 22. Anexos

Incluir:

- Diccionario resumido.
- Tabla de calidad.
- Capturas del dashboard.
- Ejemplos de filtros.
- Tabla de KPI.
- Resultado de ejecucion.
- Lista de archivos reproducibles.
- Comando de ejecucion.

## Comando de reproducibilidad

```powershell
streamlit run dashboard/app.py
```

## Requisitos formales EP5

Confirmar que el informe contiene:

- Problema de negocio.
- Objetivos.
- Audiencia.
- Fuentes.
- Analisis exploratorio.
- Justificacion grafica.
- Data storytelling.
- Dashboard.
- Evaluacion critica.
- Conclusiones y recomendaciones.

## Nivel de detalle esperado

El informe debe incluir una explicacion suficiente para que el profesor pueda reproducir:

- Donde entra cada fuente.
- Como se integra.
- Como se filtra.
- Que se calcula.
- Que grafico representa cada dato.
- Que limite afecta cada conclusion.
- Que cambio fue agregado en la entrega final.

Evitar texto decorativo. Cada seccion debe relacionarse con una decision, una evidencia o una mejora.
