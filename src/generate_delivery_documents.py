from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
OUT.mkdir(exist_ok=True)

NAVY = "18324A"
TEAL = "188C9E"
GOLD = "E4A92D"
LIGHT = "F7FAFC"


def generate_pdf():
    path = OUT / "Informe_Ejecutivo_StreamView.pdf"
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Informe Ejecutivo - StreamView Analytics",
        author="Eduardo Lizama",
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleES", parent=styles["Title"], textColor=colors.HexColor("#18324A"), alignment=TA_LEFT if False else 0, fontSize=22, leading=26))
    styles.add(ParagraphStyle(name="HeadingES", parent=styles["Heading2"], textColor=colors.HexColor("#188C9E"), fontSize=14, leading=17, spaceBefore=10))
    styles.add(ParagraphStyle(name="BodyES", parent=styles["BodyText"], fontSize=9.2, leading=13, textColor=colors.HexColor("#243B53")))

    story = [
        Paragraph("StreamView Analytics", styles["TitleES"]),
        Paragraph("Informe ejecutivo de visualización de datos", styles["BodyES"]),
        Spacer(1, 8),
        Paragraph("Autor: Eduardo Lizama · ADY1104 · Noviembre de 2026", styles["BodyES"]),
        Spacer(1, 14),
        Paragraph("Resumen ejecutivo", styles["HeadingES"]),
        Paragraph(
            "Dashboard interactivo que integra 32.000 registros de catálogo: 16.000 películas y "
            "16.000 series. El proyecto comunica oferta, géneros, territorios, popularidad, valoración "
            "y finanzas mediante filtros, KPI, navegación lateral y solapas. Los datos describen "
            "catálogo y atributos externos; no permiten afirmar comportamiento real de clientes.",
            styles["BodyES"],
        ),
        Paragraph("Problema de negocio y objetivos", styles["HeadingES"]),
        Paragraph(
            "StreamView necesita una vista consolidada para apoyar decisiones de contenidos, adquisición, "
            "marketing y producto. Los objetivos son integrar las fuentes, identificar patrones verificables, "
            "facilitar la interacción y separar explícitamente datos oficiales de estimaciones.",
            styles["BodyES"],
        ),
        Paragraph("Audiencias", styles["HeadingES"]),
        Table(
            [
                ["Audiencia", "Propósito"],
                ["Directorio / Gerencia", "Prioridades y validación de riesgos"],
                ["Contenidos / Adquisición", "Hipótesis de portafolio y territorios"],
                ["Marketing / Producto", "Promoción basada en señales externas"],
                ["Finanzas / Datos", "Subconjunto financiero y calidad"],
            ],
            colWidths=[4.5 * cm, 10.5 * cm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#188C9E")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
            ]),
        ),
        Paragraph("Fuentes y calidad", styles["HeadingES"]),
        Paragraph(
            "Los CSV oficiales contienen 32.000 filas. Se preservan los nombres originales y se anexa "
            "por tipo. Se encontraron 406 filas afectadas por colisiones o repeticiones de show_id; no "
            "se eliminan registros sin una regla de identidad acordada. Country tiene 2.263 faltantes y "
            "director está vacío en 10.965 registros de series.",
            styles["BodyES"],
        ),
        PageBreak(),
        Paragraph("Hallazgos principales", styles["HeadingES"]),
        Paragraph(
            "La composición entregada es 16.000 películas y 16.000 series. Los periodos observados contienen "
            "exactamente 2.000 registros por año, lo que requiere validación antes de atribuir tendencias. "
            "Rating es numérico y coincide con vote_average; no representa clasificación por edad.",
            styles["BodyES"],
        ),
        Paragraph(
            "Solo 3.540 películas tienen presupuesto e ingresos positivos. De ellas, 1.298 tienen ingresos "
            "menores que el presupuesto, 6 iguales y 2.236 mayores. Revenue / Budget es una relación "
            "descriptiva: no incorpora marketing, distribución ni flujos contables.",
            styles["BodyES"],
        ),
        Paragraph("Diseño visual e interacción", styles["HeadingES"]),
        Paragraph(
            "Se justifican líneas para tiempo, barras horizontales para categorías largas, dona para "
            "composición, dispersión para relaciones y escala logarítmica para finanzas. Los gráficos se "
            "disponen en solapas dentro de cada sección, mejorando legibilidad y reduciendo desplazamiento.",
            styles["BodyES"],
        ),
        Paragraph("Evaluación crítica", styles["HeadingES"]),
        Paragraph(
            "Fortalezas: navegación clara, filtros recalculados, advertencias visibles, trazabilidad y "
            "separación de datos estimados. Riesgos: claves no únicas, datos temporales uniformes, rankings "
            "con pocos votos, extremos de popularidad y moneda financiera no especificada.",
            styles["BodyES"],
        ),
        Paragraph("Recomendaciones", styles["HeadingES"]),
        Paragraph(
            "1) Validar periodos y muestreo. 2) Corregir el diccionario de rating. 3) Definir llave de "
            "registro y reconciliación. 4) Incorporar suscripciones y eventos de reproducción. 5) Aplicar "
            "umbral mínimo de votos. 6) Confirmar moneda y fuentes financieras.",
            styles["BodyES"],
        ),
        Paragraph("Conclusión", styles["HeadingES"]),
        Paragraph(
            "El proyecto entrega una solución reproducible que transforma el catálogo en evidencia ejecutiva "
            "sin exceder las capacidades de las fuentes. Su siguiente fase debe integrar datos longitudinales "
            "de usuarios para medir retención y engagement con evidencia real.",
            styles["BodyES"],
        ),
    ]
    doc.build(story)
    return path


def generate_ppt():
    path = OUT / "Presentacion_Defensa_StreamView.pptx"
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slides = [
        ("StreamView Analytics", "Dashboard interactivo para decisión de catálogo y comunicación visual", True),
        ("Problema y audiencia", "Catálogo fragmentado; directorio, contenidos, marketing y datos requieren una vista común."),
        ("Objetivos", "Consolidar · explorar · justificar · advertir · recomendar."),
        ("Fuentes y modelo", "32.000 registros oficiales; anexión por tipo; llaves técnicas locales; datos complementarios separados."),
        ("Diseño final", "Navegación lateral, KPI recalculados, tema profesional y solapas por análisis."),
        ("Hallazgos de catálogo", "16.000 películas + 16.000 series; periodos uniformes que requieren validación."),
        ("Popularidad y valoración", "Señales externas, no reproducciones: ranking sensible a pocos votos."),
        ("Finanzas", "3.540 películas evaluables; moneda no especificada; ROI aproximado no contable."),
        ("Limitaciones y mitigación", "Claves, faltantes, sesgos temporales, extremos y ausencia de datos de clientes."),
        ("Recomendaciones", "Validar datos · definir claves · incorporar suscripciones/eventos · ponderar rankings."),
        ("Impacto esperado", "Priorizar hipótesis de adquisición y marketing con trazabilidad y menor riesgo de interpretación."),
        ("Demostración y cierre", "Dashboard reproducible · informe ejecutivo · presentación · estructura profesional."),
    ]

    for index, item in enumerate(slides):
        title = item[0]
        body = item[1]
        title_slide = len(item) > 2 and item[2]
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(247, 250, 252)

        if title_slide:
            accent = slide.shapes.add_shape(1, 0, 0, Inches(0.18), prs.slide_height)
            accent.fill.solid()
            accent.fill.fore_color.rgb = RGBColor(24, 140, 158)
            accent.line.fill.background()

        box = slide.shapes.add_textbox(Inches(0.75), Inches(0.55), Inches(11.8), Inches(0.8))
        frame = box.text_frame
        p = frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(28 if title_slide else 24)
        p.font.bold = True
        p.font.name = "Aptos"
        p.font.color.rgb = RGBColor(24, 50, 74)

        body_box = slide.shapes.add_textbox(Inches(0.75), Inches(1.55), Inches(11.8), Inches(4.9))
        tf = body_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = body
        p.font.size = Pt(22 if title_slide else 18)
        p.font.name = "Aptos"
        p.font.color.rgb = RGBColor(36, 59, 83)
        p.alignment = PP_ALIGN.LEFT

        footer = slide.shapes.add_textbox(Inches(11.9), Inches(7.05), Inches(0.7), Inches(0.25))
        fp = footer.text_frame.paragraphs[0]
        fp.text = f"{index + 1}"
        fp.font.size = Pt(9)
        fp.font.color.rgb = RGBColor(100, 116, 139)
        fp.alignment = PP_ALIGN.RIGHT

    prs.save(path)
    return path


if __name__ == "__main__":
    print(generate_pdf())
    print(generate_ppt())
