from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "Data_Movies"
MOVIES_FILE = DATA_DIR / "netflix_movies_detailed_up_to_2025.csv"
SHOWS_FILE = DATA_DIR / "netflix_tv_shows_detailed_up_to_2025.csv"

COLORS = {
    "navy": "#0B1F4B",
    "blue": "#1769AA",
    "gold": "#F7B718",
    "teal": "#118AB2",
    "green": "#2E8B57",
    "red": "#D1495B",
}

st.set_page_config(
    page_title="StreamView Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_catalog() -> pd.DataFrame:
    movies = pd.read_csv(MOVIES_FILE)
    shows = pd.read_csv(SHOWS_FILE)
    catalog = pd.concat([movies, shows], ignore_index=True, sort=False)
    catalog["date_added"] = pd.to_datetime(catalog["date_added"], errors="coerce")
    for column in ["popularity", "vote_average", "vote_count", "budget", "revenue"]:
        catalog[column] = pd.to_numeric(catalog[column], errors="coerce").fillna(0)
    catalog["release_year"] = pd.to_numeric(
        catalog["release_year"], errors="coerce"
    ).astype("Int64")
    return catalog


def split_values(series: pd.Series) -> pd.Series:
    return (
        series.fillna("No informado")
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
        .replace("", "No informado")
    )


def format_number(value: float, decimals: int = 0) -> str:
    if decimals:
        return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace(
            "X", "."
        )
    return f"{value:,.0f}".replace(",", ".")


def format_currency(value: float) -> str:
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    return f"${value:,.0f}"


def apply_filters(catalog: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.header("Filtros")
        content_types = st.multiselect(
            "Tipo de contenido",
            options=sorted(catalog["type"].dropna().unique()),
            default=sorted(catalog["type"].dropna().unique()),
        )
        min_year, max_year = int(catalog["release_year"].min()), int(
            catalog["release_year"].max()
        )
        years = st.slider("Año de estreno", min_year, max_year, (min_year, max_year))
        languages = st.multiselect(
            "Idioma principal",
            sorted(split_values(catalog["language"]).unique()),
            default=[],
        )
        countries = st.multiselect(
            "País productor",
            sorted(split_values(catalog["country"]).unique()),
            default=[],
        )

    filtered = catalog[
        catalog["type"].isin(content_types)
        & catalog["release_year"].between(years[0], years[1])
    ].copy()
    if languages:
        filtered = filtered[filtered["language"].fillna("No informado").isin(languages)]
    if countries:
        filtered = filtered[
            filtered["country"]
            .fillna("No informado")
            .apply(lambda value: any(item.strip() in countries for item in str(value).split(",")))
        ]
    return filtered


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <div>
                <div class="eyebrow">STREAMVIEW ANALYTICS · VISUAL ANALYTICS</div>
                <h1>Catálogo audiovisual para decisiones estratégicas</h1>
                <p>Explora composición, popularidad, valoración y desempeño financiero del catálogo.</p>
            </div>
            <div class="author">Autor y desarrollador<br><strong>Eduardo Lizama</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi(label: str, value: str, help_text: str | None = None) -> None:
    st.metric(label, value, help=help_text)


def page_executive(catalog: pd.DataFrame) -> None:
    st.subheader("Dashboard ejecutivo")
    st.caption("Lectura rápida para Directorio y Gerencia General.")
    total = len(catalog)
    movies = int((catalog["type"] == "Movie").sum())
    shows = int((catalog["type"] == "TV Show").sum())
    countries = split_values(catalog["country"]).nunique()
    languages = split_values(catalog["language"]).nunique()
    cols = st.columns(5)
    for col, label, value in zip(
        cols,
        ["Contenidos", "Películas", "Series", "Países", "Idiomas"],
        [total, movies, shows, countries, languages],
    ):
        with col:
            render_kpi(label, format_number(value))

    left, right = st.columns(2)
    with left:
        type_counts = catalog["type"].value_counts().rename_axis("Tipo").reset_index(
            name="Contenidos"
        )
        fig = px.pie(
            type_counts,
            names="Tipo",
            values="Contenidos",
            hole=0.55,
            color="Tipo",
            color_discrete_map={"Movie": COLORS["blue"], "TV Show": COLORS["gold"]},
            title="Composición del catálogo",
        )
        fig.update_layout(margin=dict(t=55, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        by_year = (
            catalog.groupby(["release_year", "type"], as_index=False)
            .size()
            .rename(columns={"size": "Contenidos"})
        )
        fig = px.line(
            by_year,
            x="release_year",
            y="Contenidos",
            color="type",
            markers=True,
            title="Evolución de estrenos por año",
            labels={"release_year": "Año", "type": "Tipo"},
            color_discrete_map={"Movie": COLORS["blue"], "TV Show": COLORS["gold"]},
        )
        fig.update_layout(margin=dict(t=55, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    top_genres = (
        split_values(catalog["genres"])
        .value_counts()
        .head(10)
        .rename_axis("Género")
        .reset_index(name="Contenidos")
    )
    fig = px.bar(
        top_genres.sort_values("Contenidos"),
        x="Contenidos",
        y="Género",
        orientation="h",
        title="Géneros con mayor presencia",
        color="Contenidos",
        color_continuous_scale=["#DDEBFA", COLORS["blue"]],
    )
    fig.update_layout(coloraxis_showscale=False, margin=dict(t=55, l=10, r=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.info(
        "**Lectura ejecutiva:** la evolución temporal, la mezcla entre películas y series "
        "y la concentración por género permiten priorizar contenidos y mercados. "
        "La popularidad es un índice relativo TMDB, no representa reproducciones."
    )


def page_catalog(catalog: pd.DataFrame) -> None:
    st.subheader("Análisis del catálogo")
    st.caption("Comparación de géneros, países, idiomas y contenidos destacados.")
    left, right = st.columns(2)
    with left:
        genre_df = (
            split_values(catalog["genres"])
            .value_counts()
            .head(12)
            .rename_axis("Género")
            .reset_index(name="Contenidos")
        )
        fig = px.bar(
            genre_df.sort_values("Contenidos"),
            x="Contenidos",
            y="Género",
            orientation="h",
            title="Distribución por género",
            color="Contenidos",
            color_continuous_scale=["#E4F3F7", COLORS["teal"]],
        )
        fig.update_layout(coloraxis_showscale=False, margin=dict(t=55, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        country_df = (
            split_values(catalog["country"])
            .value_counts()
            .head(12)
            .rename_axis("País")
            .reset_index(name="Contenidos")
        )
        fig = px.bar(
            country_df.sort_values("Contenidos"),
            x="Contenidos",
            y="País",
            orientation="h",
            title="Países con mayor representación",
            color="Contenidos",
            color_continuous_scale=["#FFF1C7", COLORS["gold"]],
        )
        fig.update_layout(coloraxis_showscale=False, margin=dict(t=55, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    quality = pd.DataFrame(
        {
            "Indicador": [
                "Registros analizados",
                "IDs duplicados",
                "Directores informados",
                "Países informados",
                "Géneros informados",
            ],
            "Valor": [
                len(catalog),
                int(catalog.duplicated("show_id").sum()),
                int(catalog["director"].notna().sum()),
                int(catalog["country"].notna().sum()),
                int(catalog["genres"].notna().sum()),
            ],
        }
    )
    st.dataframe(quality, hide_index=True, use_container_width=True)
    st.markdown("#### Contenidos destacados")
    display = catalog.nlargest(15, "popularity")[
        ["title", "type", "release_year", "genres", "language", "popularity", "vote_average"]
    ].copy()
    display.columns = [
        "Título",
        "Tipo",
        "Año",
        "Géneros",
        "Idioma",
        "Popularidad",
        "Calificación",
    ]
    st.dataframe(display, hide_index=True, use_container_width=True)


def page_popularity(catalog: pd.DataFrame) -> None:
    st.subheader("Popularidad y valoración")
    st.caption(
        "La valoración está en escala 0–10. La popularidad es un índice relativo TMDB."
    )
    cols = st.columns(3)
    with cols[0]:
        render_kpi("Popularidad promedio", format_number(catalog["popularity"].mean(), 1))
    with cols[1]:
        render_kpi("Calificación promedio", format_number(catalog["vote_average"].mean(), 2))
    with cols[2]:
        render_kpi("Votos acumulados", format_number(catalog["vote_count"].sum()))

    left, right = st.columns(2)
    with left:
        scatter = catalog[catalog["vote_count"] > 0]
        fig = px.scatter(
            scatter,
            x="vote_average",
            y="popularity",
            size="vote_count",
            color="type",
            hover_name="title",
            opacity=0.65,
            title="Relación entre valoración y popularidad",
            labels={"vote_average": "Calificación", "popularity": "Popularidad"},
            color_discrete_map={"Movie": COLORS["blue"], "TV Show": COLORS["gold"]},
        )
        fig.update_yaxes(type="log")
        fig.update_layout(margin=dict(t=55, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        top = catalog.nlargest(10, "popularity").sort_values("popularity")
        fig = px.bar(
            top,
            x="popularity",
            y="title",
            orientation="h",
            color="type",
            title="Top 10 contenidos por popularidad",
            labels={"popularity": "Índice TMDB", "title": ""},
            color_discrete_map={"Movie": COLORS["blue"], "TV Show": COLORS["gold"]},
        )
        fig.update_layout(margin=dict(t=55, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    genre_scores = catalog[["genres", "popularity", "vote_average"]].rename(
        columns={
            "genres": "Género",
            "popularity": "Popularidad",
            "vote_average": "Calificación",
        }
    )
    genre_scores["Género"] = genre_scores["Género"].fillna("No informado").str.split(",")
    genre_scores = genre_scores.explode("Género")
    genre_scores["Género"] = genre_scores["Género"].str.strip().replace(
        "", "No informado"
    )
    genre_scores = (
        genre_scores.groupby("Género", as_index=False)
        .agg(Popularidad=("Popularidad", "mean"), Calificación=("Calificación", "mean"))
        .query("Género != 'No informado'")
        .nlargest(12, "Popularidad")
    )
    fig = px.bar(
        genre_scores.sort_values("Popularidad"),
        x="Popularidad",
        y="Género",
        orientation="h",
        color="Calificación",
        title="Popularidad media por género",
        color_continuous_scale=["#FDE2E4", COLORS["red"]],
    )
    fig.update_layout(margin=dict(t=55, l=10, r=10, b=10))
    st.plotly_chart(fig, use_container_width=True)


def page_finance(catalog: pd.DataFrame) -> None:
    st.subheader("Análisis financiero de películas")
    st.caption(
        "Solo se consideran películas con presupuesto e ingresos positivos disponibles."
    )
    movies = catalog[catalog["type"] == "Movie"].copy()
    financial = movies[(movies["budget"] > 0) & (movies["revenue"] > 0)].copy()
    if financial.empty:
        st.warning("No existen registros financieros válidos con los filtros actuales.")
        return
    financial["roi"] = financial["revenue"] / financial["budget"]
    cols = st.columns(4)
    for col, label, value in zip(
        cols,
        ["Películas evaluables", "Presupuesto total", "Ingresos totales", "ROI ponderado"],
        [
            format_number(len(financial)),
            format_currency(financial["budget"].sum()),
            format_currency(financial["revenue"].sum()),
            f"{financial['revenue'].sum() / financial['budget'].sum():.2f}x",
        ],
    ):
        with col:
            render_kpi(label, value)

    left, right = st.columns(2)
    with left:
        fig = px.scatter(
            financial,
            x="budget",
            y="revenue",
            size="vote_count",
            color="vote_average",
            hover_name="title",
            log_x=True,
            log_y=True,
            title="Relación entre presupuesto e ingresos",
            labels={"budget": "Presupuesto", "revenue": "Ingresos"},
            color_continuous_scale=["#DDEBFA", COLORS["blue"]],
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        top = financial.nlargest(10, "roi").sort_values("roi")
        fig = px.bar(
            top,
            x="roi",
            y="title",
            orientation="h",
            title="Top 10 películas por ROI aproximado",
            labels={"roi": "Revenue / Budget", "title": ""},
            color="roi",
            color_continuous_scale=["#E4F3F7", COLORS["green"]],
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    st.info(
        "El ROI aproximado no es rentabilidad contable: no incluye costos de distribución, "
        "marketing ni temporalidad de los flujos."
    )


def page_quality(catalog: pd.DataFrame) -> None:
    st.subheader("Calidad y trazabilidad de datos")
    st.caption("Controles mínimos realizados antes de construir las visualizaciones.")
    checks = []
    for column in catalog.columns:
        missing = int(catalog[column].isna().sum())
        checks.append(
            {
                "Variable": column,
                "Nulos": missing,
                "% nulos": round(missing / len(catalog) * 100, 2),
                "Tipo": str(catalog[column].dtype),
            }
        )
    st.dataframe(
        pd.DataFrame(checks).sort_values(["Nulos", "Variable"], ascending=[False, True]),
        hide_index=True,
        use_container_width=True,
    )
    st.markdown(
        """
        **Decisiones de preparación**

        - Se unificaron películas y series en un catálogo analítico común, preservando sus columnas originales.
        - Se excluyeron del análisis financiero los registros sin presupuesto o ingresos positivos.
        - Países y géneros se separan únicamente al agregar para evitar perder representatividad.
        - Los 9 IDs duplicados detectados en TV Shows se reportan, pero no se eliminan automáticamente.
        - `budget` y `revenue` se interpretan solo para `Movie`, tal como exige el caso.
        - La fuente no presenta una clasificación etaria consistente; no se inventan categorías.
        """
    )


def main() -> None:
    catalog = load_catalog()
    render_header()
    with st.sidebar:
        st.markdown("---")
        page = st.radio(
            "Navegación",
            [
                "Dashboard ejecutivo",
                "Análisis del catálogo",
                "Popularidad y valoración",
                "Finanzas · Películas",
                "Calidad de datos",
            ],
        )
    filtered = apply_filters(catalog) if page != "Calidad de datos" else catalog
    st.caption(
        f"Alcance actual: {len(filtered):,} registros · Estrenos "
        f"{filtered['release_year'].min()}–{filtered['release_year'].max()}".replace(
            ",", "."
        )
    )
    if page == "Dashboard ejecutivo":
        page_executive(filtered)
    elif page == "Análisis del catálogo":
        page_catalog(filtered)
    elif page == "Popularidad y valoración":
        page_popularity(filtered)
    elif page == "Finanzas · Películas":
        page_finance(filtered)
    else:
        page_quality(catalog)


st.markdown(
    """
    <style>
    .hero { background: linear-gradient(120deg, #0B1F4B 0%, #123C78 100%);
            color: white; padding: 1.6rem 2rem; border-radius: 0.8rem;
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 1.2rem; }
    .hero h1 { margin: 0.25rem 0; font-size: 2.15rem; }
    .hero p { margin: 0; color: #DDEBFA; }
    .eyebrow { color: #F7B718; font-weight: 700; letter-spacing: .08em; font-size: .78rem; }
    .author { text-align: right; color: #DDEBFA; font-size: .85rem; }
    .author strong { color: white; font-size: 1rem; }
    [data-testid="stMetricValue"] { color: #0B1F4B; }
    </style>
    """,
    unsafe_allow_html=True,
)


if __name__ == "__main__":
    main()
