# Guia para crear la presentacion ejecutiva de StreamView Analytics

## Instrucciones para el agente

Actua como disenyador de presentaciones ejecutivas y especialista en visualizacion de datos. Crea una presentacion clara, sobria y defendible para el profesor de ADY1104. El producto debe ser un archivo PPTX orientado a una exposicion grupal de 10 minutos, con hasta 5 minutos adicionales de preguntas.

No inventes datos ni presentar como reales los datos que el caso describe como corporativos. En todas las diapositivas distingue:

- Catalogo oficial entregado.
- Analisis descriptivo.
- Estimaciones complementarias.
- Datos que faltan.
- Decision de negocio recomendada como hipotesis.

## Identidad visual recomendada

- Orientacion: 16:9.
- Fondo principal: blanco o gris muy claro.
- Azul oscuro: `#18324A`.
- Teal: `#188C9E`.
- Dorado: `#E4A92D`.
- Morado: `#8A63C7`.
- Azul: `#3685D3`.
- Tipografia sin serifas: Aptos, Calibri o similar.
- Usar iconos Material Symbols si la herramienta los admite.
- Evitar emojis, sombras excesivas, textos largos y diapositivas recargadas.
- Mantener maximo dos ideas por diapositiva.
- Cada grafico debe incluir titulo, unidad, fuente, alcance y limitacion visible cuando corresponda.
- El texto pequeno debe ser legible desde la proyeccion.

## Secuencia sugerida

### Diapositiva 1: Portada

Contenido:

- StreamView Analytics.
- Dashboard interactivo para analisis de catalogo audiovisual.
- ADY1104 - Visualizacion de Datos.
- Autor: Eduardo Lizama.
- Fecha: noviembre de 2026.
- Subtitulo: evolucion desde la consolidacion inicial hasta la entrega final.

No agregar decoracion no vinculada al proyecto.

### Diapositiva 2: Contexto del caso

Explicar:

- StreamView es un caso academico de una plataforma internacional de streaming.
- Problema: falta de una vista consolidada del catalogo.
- Los reportes separados dificultaban comparar generos y paises.
- El objetivo era comunicar informacion util para decisiones de contenidos, adquisicion, marketing y producto.

Mensaje verbal sugerido:

> Convertimos datos de catalogo dispersos en una vista unica que permite pasar de la descripcion general a la exploracion detallada.

### Diapositiva 3: Audiencias y objetivos

Mostrar cuatro audiencias:

- Directorio y Gerencia General.
- Gerencia de Contenidos y Adquisicion.
- Marketing y Producto.
- Equipo de Datos y Finanzas.

Mostrar objetivos:

- Consolidar.
- Filtrar.
- Analizar.
- Mostrar limites.
- Recomendar con evidencia.

Usar una matriz audiencia-necesidad-decision.

### Diapositiva 4: Fuentes y arquitectura

Mostrar:

- `netflix_movies_detailed_up_to_2025.csv`: 16.000 filas y 18 columnas.
- `netflix_tv_shows_detailed_up_to_2025.csv`: 16.000 filas y 16 columnas.
- 32.000 filas totales.
- Anexion por tipo de contenido.
- `_content_row` como llave tecnica interna.
- Dos CSV complementarios de 32.000 filas separados del analisis oficial.

Nota obligatoria:

> La llave `show_id` no se usa como identificador unico global.

### Diapositiva 5: Modelo de datos y variables relevantes

Presentar solo las variables principales:

- Identidad: `show_id`, `title`, `type`.
- Tiempo: `release_year`, `date_added`.
- Contenido: `genres`, `country`, `language`, `director`, `cast`.
- Valoracion: `rating`, `vote_average`, `vote_count`, `popularity`.
- Finanzas oficiales: `budget`, `revenue`.
- Investigacion complementaria: `engagement_proxy_score`, duracion estimada, estado y procedencia.

Explicar el grano:

> Una fila representa un registro de contenido; no representa un usuario, una sesion ni una reproduccion.

### Diapositiva 6: Hitos de construccion

Esta diapositiva debe ser central para demostrar mejora progresiva.

Secuencia:

1. Analisis inicial de los archivos oficiales.
2. Construccion del modelo integrado y validacion de columnas.
3. Desarrollo de KPI y filtros comunes.
4. Creacion de seis o siete vistas ejecutivas y analiticas.
5. Incorporacion de datos complementarios separados.
6. Evaluacion critica de representaciones y calidad.
7. Reduccion de rigidez visual mediante solapas principales.
8. Incorporacion de subsolapas por familia de grafico.
9. Correccion del renderizado para que cada solapa muestre exclusivamente su contenido.
10. Empaquetado final con informe, presentacion, codigo y estructura profesional.

Destacar que las modificaciones finales no fueron cosmeticas: resolvieron navegacion, carga visual, legibilidad y interpretacion.

### Diapositiva 7: Evolucion de navegacion

Comparacion:

| Antes | Entrega final |
|---|---|
| Navegacion lateral extensa | Solapas superiores principales |
| Muchos graficos en una misma altura | Subsolapas por tipo de informacion |
| Desplazamiento vertical importante | Cada apartado se explora individualmente |
| Riesgo de confundir datos oficiales y estimados | Investigacion separada y advertida |
| Informacion financiera compactada sin lectura clara | Solapas de distribucion, rankings y tabla |
| Filtros sin forma rapida de reinicio | Boton para restablecer la seleccion |
| Sin comparacion temporal | Comparacion configurable con otro periodo |

No decir que la solucion original era mala; usar lenguaje de iteracion y mejora.

### Diapositiva 8: Arquitectura interactiva final

Mostrar solapas:

- Resumen.
- Catalogo.
- Popularidad.
- Finanzas.
- Contexto.
- Calidad.
- Investigacion.

Luego mostrar subsolapas:

- Resumen: evolucion, composicion, generos, lectura ejecutiva.
- Catalogo: mercado, incorporaciones, creditos.
- Popularidad: rankings, relacion, grupos, titulo mejor evaluado.
- Finanzas: distribucion, rankings y menor presupuesto.

Explicar:

- Los filtros compartidos afectan las vistas oficiales.
- La investigacion conserva sus propios filtros.
- Los bloques se renderizan dentro de su contexto correcto.

### Diapositiva 9: Representaciones y justificacion

Relacion tipo de dato/grafico:

- Tiempo: lineas o areas.
- Composicion: dona.
- Categorias largas: barras horizontales.
- Dos variables numericas: dispersion.
- Varias magnitudes financieras: escala logaritmica.
- Diccionario y calidad: tablas.
- Metricas: KPI.

Justificar no solo que existe el grafico, sino por que mejora la lectura.

### Diapositiva 10: Hallazgos principales

Incluir solo hallazgos robustos:

- 16.000 peliculas y 16.000 series.
- 2.000 registros por ano tanto en `release_year` como en `date_added`.
- Esta regularidad requiere validacion.
- 406 apariciones repetidas o colisiones de `show_id`.
- `country`: 2.263 faltantes.
- `director`: 10.965 faltantes en series.
- `duration`: vacia en las 16.000 peliculas.
- `rating`: numerico y coincide con `vote_average`; no es clasificacion por edad.
- Solo 3.540 peliculas tienen presupuesto e ingresos positivos.
- De esas: 1.298 inferiores, 6 iguales y 2.236 superiores.

Durante la demostracion, tambien mostrar:

- Mediana y percentiles de popularidad.
- Ranking ponderado por votos.
- Descarga del catalogo filtrado.
- Cobertura visible de calificacion, popularidad y pais.

No usar reproducciones, churn o retencion como hallazgos directos.

### Diapositiva 11: Hallazgos que requieren cautela

- Popularidad: mediana 10,9135 y maximo 3.876,006.
- Ranking de calificaciones sensible a pocos votos.
- Grupos 50/50 condicionados por el muestreo.
- Tendencias uniformes no verificadas como comportamiento real.
- Presupuesto e ingresos sin moneda especificada.
- Datos complementarios estimados y proxy no observado.

Usar colores amarillo o rojo solo para advertencias, no para sugerir culpa.

### Diapositiva 12: Hallazgos o recomendaciones de decision

Proponer decisiones como pruebas:

1. Validar distribucion anual antes de atribuir tendencias.
2. Priorizar generos y territorios solo como hipotesis de adquisicion.
3. Usar popularidad externa junto con numero de votos.
4. No interpretar un aumento financiero sin confirmar moneda y costos.
5. Obtener datos de suscripcion y reproduccion antes de decidir retencion.

Cada recomendacion debe mencionar evidencia y siguiente accion.

### Diapositiva 13: Fortalezas de la solucion

- Cohesion entre visualizaciones y objetivos.
- Navegacion modular.
- Interaccion por filtros y KPI.
- Advertencias visibles.
- Separacion de estimaciones.
- Trazabilidad de variables y descargas.
- Codigo reproducible.

Incluir al menos una evidencia concreta por fortaleza.

### Diapositiva 14: Limitaciones y oportunidades de mejora

Priorizar:

1. Definir una llave confiable de contenido.
2. Corregir el diccionario de `rating`.
3. Validar regularidad temporal.
4. Confirmar moneda y fuentes financieras.
5. Incorporar churn, retencion, reproduccion y finalizacion.
6. Agregar umbral minimo de votos.
7. Mostrar mediana y sensibilidad de extremos.
8. Conectar calidad con reglas automaticas.

Diferenciar mejora inmediata de mejora futura.

### Mejora final incorporada

Mencionar explicitamente las funcionalidades agregadas al cerrar el proyecto:

- Restablecimiento de filtros.
- Comparacion entre periodos.
- Ranking ponderado por votos.
- Mediana, cuartiles, percentiles e histograma de popularidad.
- Descarga del catalogo filtrado.
- Llave tecnica compuesta de trazabilidad.
- Lectura ejecutiva, cobertura visible y conclusiones de seleccion.

### Diapositiva 15: Impacto esperado

Explicar:

- Reduce tiempo para revisar catalogo.
- Permite explorar el mismo subconjunto desde distintos criterios.
- Dispone advertencias antes de tomar decisiones.
- Convierte la informacion fragmentada en una agenda de validacion.
- Facilita una siguiente etapa basada en comportamiento real.

No afirmar mejoras medibles de negocio que no puedan derivarse de las fuentes.

### Diapositiva 16: Demostracion

Plan para exponer el dashboard:

1. Mostrar seleccion completa.
2. Cambiar tipo de contenido.
3. Reducir rango de ano.
4. Elegir un genero.
5. Visitar resumen.
6. Navegar a popularidad.
7. Cambiar a finanzas.
8. Abrir calidad.
9. Abrir investigacion y explicar que esta aislada.

Esta secuencia demuestra interaccion sin recorrer toda la aplicacion.

### Diapositiva 17: Conclusiones

Sintesis:

- El proyecto cumple una etapa integral de visualizacion.
- La solucion comunica oportunidades sin convertir correlaciones en causalidad.
- La principal mejora final fue la navegacion modular por solapas.
- La siguiente prioridad es incorporar datos longitudinales de usuarios.

### Diapositiva 18: Preguntas y cierre

Agregar:

- Nombre del proyecto.
- Repositorio o ruta.
- Indicacion para ejecutar: `streamlit run dashboard/app.py`.
- Agradecimiento.

## Preguntas probables del profesor

Preparar respuestas para:

1. ¿Por que Streamlit en lugar de Power BI?
2. ¿Que significa la seleccion filtrada?
3. ¿`rating` representa edad?
4. ¿Puede calcular churn?
5. ¿Que mide `engagement_proxy_score`?
6. ¿Por que no se eliminan los `show_id` repetidos?
7. ¿Por que la distribucion temporal es uniforme?
8. ¿Revenue / Budget es rentabilidad?
9. ¿Que representa la popularidad?
10. ¿Que graficos cambiaron en la entrega final?
11. ¿Como funcionan las solapas y subsolapas?
12. ¿Que falta para una fase siguiente?

### Respuestas modelo

- Se uso StreamLit por autorizacion del profesor y por poder implementar una solucion reproducible en Python.
- Una fila representa un titulo o registro, no un usuario.
- `rating` no representa clasificacion por edad en estos archivos.
- No se puede calcular churn sin altas, bajas y fechas.
- El proxy no representa reproducciones ni consumo real.
- Se conservaron los registros porque no existe una regla de deduplicacion acordada.
- La regularidad temporal debe validarse con el responsable de datos.
- Revenue / Budget es una relacion descriptiva, no ROI contable.
- Popularidad es un indice externo TMDB.
- La mejora final hizo mas modular la navegacion y corrigio el renderizado de solapas.
- La siguiente fase requiere datos seudonimizados de suscripcion y eventos.

## Criterios de rubrica a reflejar

La presentacion debe demostrar explicitamente:

- IE26: fundamentacion tecnica de graficos.
- IE31: fortalezas mediante evidencia.
- IE32: limitaciones, sesgos y riesgos con mitigacion.
- IE33: mejoras viables y priorizadas.
- IE35: recomendaciones justificadas con hallazgos.
- IE36: impacto esperado en toma de decisiones sin sobredimensionarlo.

## Archivos utiles para disenar

- Capturas: `images/dashboard/`.
- Justificacion: `docs/justificacion_representaciones_graficas.md`.
- Informe: `docs/Informe_Ejecutivo_StreamView.md`.
- README: `README.md`.
- Dashboard: `dashboard/app.py`.
