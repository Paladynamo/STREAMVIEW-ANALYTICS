from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MOVIES_FILE = DATA_DIR / "netflix_movies_detailed_up_to_2025.csv"
SHOWS_FILE = DATA_DIR / "netflix_tv_shows_detailed_up_to_2025.csv"
RESEARCH_DIR = DATA_DIR / "research_inputs"
RESEARCH_MOVIES_FILE = RESEARCH_DIR / "netflix_movies_completed_estimates.csv"
RESEARCH_SHOWS_FILE = RESEARCH_DIR / "netflix_tv_shows_completed_estimates.csv"

TYPE_LABELS = {"Movie": "Película", "TV Show": "Serie"}
GENRE_LABELS = {
    "Action": "Acción",
    "Action & Adventure": "Acción y aventura",
    "Adventure": "Aventura",
    "Animation": "Animación",
    "Comedy": "Comedia",
    "Crime": "Crimen",
    "Documentary": "Documental",
    "Drama": "Drama",
    "Family": "Familiar",
    "Fantasy": "Fantasía",
    "History": "Historia",
    "Horror": "Terror",
    "Kids": "Infantil",
    "Music": "Música",
    "Mystery": "Misterio",
    "News": "Noticias",
    "Reality": "Telerrealidad",
    "Romance": "Romance",
    "Sci-Fi & Fantasy": "Ciencia ficción y fantasía",
    "Science Fiction": "Ciencia ficción",
    "Soap": "Telenovela",
    "TV Movie": "Película para televisión",
    "Talk": "Conversación",
    "Thriller": "Suspenso",
    "Unknown": "No informado",
    "War": "Bélico",
    "War & Politics": "Guerra y política",
    "Western": "Wéstern",
}
LANGUAGE_LABELS = {
    "af": "Afrikáans", "am": "Amhárico", "ar": "Árabe", "as": "Asamés",
    "az": "Azerí", "bg": "Búlgaro", "bn": "Bengalí", "bs": "Bosnio",
    "ca": "Catalán", "cn": "Cantonés (código cn de la fuente)", "cs": "Checo",
    "cy": "Galés", "da": "Danés", "de": "Alemán", "dz": "Dzongkha",
    "el": "Griego", "en": "Inglés", "es": "Español", "et": "Estonio",
    "eu": "Euskera", "fa": "Persa", "fi": "Finés", "fr": "Francés",
    "ga": "Irlandés", "gl": "Gallego", "he": "Hebreo", "hi": "Hindi",
    "hr": "Croata", "ht": "Criollo haitiano", "hu": "Húngaro",
    "hy": "Armenio", "id": "Indonesio", "is": "Islandés", "it": "Italiano",
    "ja": "Japonés", "ka": "Georgiano", "kk": "Kazajo", "kl": "Groenlandés",
    "km": "Jemer", "kn": "Canarés", "ko": "Coreano", "ku": "Kurdo",
    "ky": "Kirguís", "la": "Latín", "lb": "Luxemburgués", "lt": "Lituano",
    "lv": "Letón", "mi": "Maorí", "mk": "Macedonio", "ml": "Malayalam",
    "mn": "Mongol", "mr": "Maratí", "ms": "Malayo", "mt": "Maltés",
    "nb": "Noruego bokmål", "ne": "Nepalí", "nl": "Neerlandés",
    "no": "Noruego", "or": "Odia", "pa": "Punyabí", "pl": "Polaco",
    "ps": "Pastún", "pt": "Portugués", "ro": "Rumano", "ru": "Ruso",
    "si": "Cingalés", "sk": "Eslovaco", "sl": "Esloveno", "sr": "Serbio",
    "sv": "Sueco", "ta": "Tamil", "te": "Telugu", "th": "Tailandés",
    "tl": "Tagalo", "tr": "Turco", "uk": "Ucraniano", "ur": "Urdu",
    "vi": "Vietnamita", "xx": "Sin código de idioma conocido", "yo": "Yoruba",
    "za": "Zhuang", "zh": "Chino", "zu": "Zulú",
    "Unknown": "No informado",
}
COUNTRY_LABELS = {
    "Unknown": "No informado",
    "Argentina": "Argentina", "Australia": "Australia", "Belgium": "Bélgica",
    "Brazil": "Brasil", "Canada": "Canadá", "Chile": "Chile", "China": "China",
    "Colombia": "Colombia", "France": "Francia", "Germany": "Alemania",
    "India": "India", "Italy": "Italia", "Japan": "Japón", "Mexico": "México",
    "South Africa": "Sudáfrica", "South Korea": "Corea del Sur", "Spain": "España",
    "United Kingdom": "Reino Unido", "United States of America": "Estados Unidos",
    "Afghanistan": "Afganistán", "Albania": "Albania", "Algeria": "Argelia",
    "Angola": "Angola", "Armenia": "Armenia", "Aruba": "Aruba", "Austria": "Austria",
    "Azerbaijan": "Azerbaiyán", "Bahamas": "Bahamas", "Bangladesh": "Bangladés",
    "Belarus": "Bielorrusia", "Bhutan": "Bután", "Bolivia": "Bolivia",
    "Bosnia and Herzegovina": "Bosnia y Herzegovina", "Botswana": "Botsuana",
    "Brunei Darussalam": "Brunéi", "Bulgaria": "Bulgaria", "Cambodia": "Camboya",
    "Cameroon": "Camerún", "Cayman Islands": "Islas Caimán",
    "Central African Republic": "República Centroafricana", "Congo": "Congo",
    "Cote D'Ivoire": "Costa de Marfil", "Croatia": "Croacia", "Cuba": "Cuba",
    "Cyprus": "Chipre", "Czech Republic": "República Checa", "Denmark": "Dinamarca",
    "Dominican Republic": "República Dominicana", "Ecuador": "Ecuador", "Egypt": "Egipto",
    "Estonia": "Estonia", "Ethiopia": "Etiopía", "Faeroe Islands": "Islas Feroe",
    "Fiji": "Fiyi", "Finland": "Finlandia", "French Polynesia": "Polinesia Francesa",
    "Georgia": "Georgia", "Ghana": "Ghana", "Greece": "Grecia", "Greenland": "Groenlandia",
    "Guadaloupe": "Guadalupe", "Guatemala": "Guatemala", "Hong Kong": "Hong Kong",
    "Hungary": "Hungría", "Iceland": "Islandia", "Indonesia": "Indonesia", "Iran": "Irán",
    "Iraq": "Irak", "Ireland": "Irlanda", "Israel": "Israel", "Jordan": "Jordania",
    "Kazakhstan": "Kazajistán", "Kenya": "Kenia", "Kosovo": "Kosovo", "Kuwait": "Kuwait",
    "Kyrgyz Republic": "Kirguistán", "Lao People's Democratic Republic": "Laos",
    "Latvia": "Letonia", "Lebanon": "Líbano", "Liechtenstein": "Liechtenstein",
    "Lithuania": "Lituania", "Luxembourg": "Luxemburgo", "Macao": "Macao",
    "Macedonia": "Macedonia", "Malawi": "Malaui", "Malaysia": "Malasia", "Malta": "Malta",
    "Mauritania": "Mauritania", "Mauritius": "Mauricio", "Monaco": "Mónaco",
    "Mongolia": "Mongolia", "Montenegro": "Montenegro", "Morocco": "Marruecos",
    "Myanmar": "Myanmar", "Namibia": "Namibia", "Nepal": "Nepal", "Netherlands": "Países Bajos",
    "Netherlands Antilles": "Antillas Neerlandesas", "New Caledonia": "Nueva Caledonia",
    "New Zealand": "Nueva Zelanda", "Nicaragua": "Nicaragua", "Nigeria": "Nigeria",
    "Norway": "Noruega", "Pakistan": "Pakistán", "Palau": "Palaos",
    "Palestinian Territory": "Territorio Palestino", "Panama": "Panamá",
    "Paraguay": "Paraguay", "Peru": "Perú", "Philippines": "Filipinas",
    "Poland": "Polonia", "Portugal": "Portugal", "Puerto Rico": "Puerto Rico",
    "Qatar": "Catar", "Romania": "Rumania", "Russia": "Rusia", "Rwanda": "Ruanda",
    "Saudi Arabia": "Arabia Saudita", "Senegal": "Senegal", "Serbia": "Serbia",
    "Singapore": "Singapur", "Slovakia": "Eslovaquia", "Slovenia": "Eslovenia",
    "Solomon Islands": "Islas Salomón", "Sri Lanka": "Sri Lanka",
    "St. Kitts and Nevis": "San Cristóbal y Nieves", "St. Lucia": "Santa Lucía",
    "St. Pierre and Miquelon": "San Pedro y Miquelón", "Sweden": "Suecia",
    "Switzerland": "Suiza", "Syrian Arab Republic": "Siria", "Taiwan": "Taiwán",
    "Tanzania": "Tanzania", "Thailand": "Tailandia", "Tunisia": "Túnez",
    "Turkey": "Turquía", "US Virgin Islands": "Islas Vírgenes de los Estados Unidos",
    "Uganda": "Uganda", "Ukraine": "Ucrania", "United Arab Emirates": "Emiratos Árabes Unidos",
    "United States Minor Outlying Islands": "Islas Ultramarinas Menores de Estados Unidos",
    "Uruguay": "Uruguay", "Uzbekistan": "Uzbekistán", "Vanuatu": "Vanuatu",
    "Venezuela": "Venezuela", "Vietnam": "Vietnam", "Zambia": "Zambia",
}
TYPE_COLORS = {"Película": "#3685D3", "Serie": "#E4A92D"}
PLOT_CONFIG = {"displaylogo": False, "responsive": True, "locale": "es"}
MIN_GROUP_SIZE = 20

DATA_DICTIONARY = [
    ("show_id", "Texto/identificador", "Identificador del contenido; hay ID repetidos en la fuente de series y colisiones entre tipos."),
    ("type", "Categoría", "Tipo de contenido: película o serie; valores originales conservados en la fuente."),
    ("title", "Texto", "Nombre del título."),
    ("director", "Texto", "Director o directores informados."),
    ("cast", "Texto", "Actores informados."),
    ("country", "Texto", "Uno o más países de producción separados por coma."),
    ("date_added", "Fecha", "Fecha de incorporación a la plataforma según el archivo."),
    ("release_year", "Entero", "Año de estreno."),
    ("rating", "Numérico en los CSV", "El diccionario del caso lo define como clasificación etaria, pero en estos archivos es numérico y coincide exactamente con vote_average; no se usa como edad."),
    ("duration", "Texto", "Duración; en el archivo de películas está vacío en los 16.000 registros."),
    ("genres", "Texto", "Uno o más géneros separados por coma."),
    ("language", "Código/Texto", "Código de idioma en la fuente."),
    ("description", "Texto", "Sinopsis; el caso indica que no se requiere análisis textual."),
    ("popularity", "Decimal", "Índice relativo TMDB; no equivale a reproducciones."),
    ("vote_count", "Entero", "Cantidad de evaluaciones externas informadas."),
    ("vote_average", "Decimal 0–10", "Promedio de calificación; métrica comparable entre tipos según el caso."),
    ("budget", "Moneda", "Presupuesto; disponible en el archivo de películas."),
    ("revenue", "Moneda", "Ingresos reportados; disponible en el archivo de películas."),
]

st.set_page_config(
    page_title="StreamView Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_source(path: Path, content_type: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo requerido: {path}")
    source = pd.read_csv(path)
    source["type"] = content_type
    return source


@st.cache_data
def load_catalog() -> pd.DataFrame:
    movies = load_source(MOVIES_FILE, "Movie")
    shows = load_source(SHOWS_FILE, "TV Show")
    catalog = pd.concat([movies, shows], ignore_index=True, sort=False)

    required = {
        "show_id", "type", "title", "release_year", "rating", "vote_average",
        "vote_count", "genres", "country", "language", "date_added", "popularity",
    }
    missing = required.difference(catalog.columns)
    if missing:
        raise ValueError("Faltan columnas requeridas: " + ", ".join(sorted(missing)))

    for column in [
        "release_year", "rating", "vote_average", "vote_count", "popularity",
        "budget", "revenue",
    ]:
        if column in catalog:
            catalog[column] = pd.to_numeric(catalog[column], errors="coerce")
    catalog["date_added"] = pd.to_datetime(catalog["date_added"], errors="coerce")
    catalog["genres"] = catalog["genres"].fillna("Unknown")
    catalog["type_label"] = catalog["type"].map(TYPE_LABELS).fillna("No informado")
    catalog["_content_row"] = range(len(catalog))
    return catalog


@st.cache_data
def load_research_catalog() -> pd.DataFrame:
    sources = [
        (RESEARCH_MOVIES_FILE, "Movie"),
        (RESEARCH_SHOWS_FILE, "TV Show"),
    ]
    required = {
        "show_id",
        "type",
        "title",
        "release_year",
        "rating",
        "genres",
        "engagement_proxy_score",
        "runtime_is_estimate",
        "runtime_verification_status",
        "runtime_source",
        "customer_metrics_status",
    }
    frames = []
    for path, expected_type in sources:
        if not path.is_file():
            raise FileNotFoundError(
                f"No se encontró el CSV complementario requerido: {path}"
            )
        frame = pd.read_csv(path, low_memory=False)
        missing = required.difference(frame.columns)
        if missing:
            raise ValueError(
                f"Faltan columnas requeridas en {path.name}: "
                + ", ".join(sorted(missing))
            )
        if not frame["type"].eq(expected_type).all():
            raise ValueError(
                f"El archivo {path.name} contiene valores inesperados en la columna type."
            )
        frame["_research_source_file"] = path.name
        frame["_research_source_row"] = range(1, len(frame) + 1)
        frames.append(frame)

    research = pd.concat(frames, ignore_index=True, sort=False)
    for column in [
        "release_year",
        "rating",
        "vote_average",
        "vote_count",
        "popularity",
        "engagement_proxy_score",
        "runtime_minutes",
        "runtime_minutes_estimated",
        "runtime_minutes_per_episode",
        "estimated_gross_profit_usd",
        "estimated_roi_pct",
    ]:
        if column in research:
            research[column] = pd.to_numeric(research[column], errors="coerce")

    movie_runtime = research.get("runtime_minutes_estimated")
    if movie_runtime is None:
        movie_runtime = research.get("runtime_minutes")
    series_runtime = research.get("runtime_minutes_per_episode")
    research["investigation_runtime_minutes"] = pd.NA
    if movie_runtime is not None:
        movie_mask = research["type"].eq("Movie")
        research.loc[movie_mask, "investigation_runtime_minutes"] = movie_runtime[
            movie_mask
        ]
    if series_runtime is not None:
        series_mask = research["type"].eq("TV Show")
        research.loc[series_mask, "investigation_runtime_minutes"] = series_runtime[
            series_mask
        ]
    research["investigation_runtime_minutes"] = pd.to_numeric(
        research["investigation_runtime_minutes"], errors="coerce"
    )
    research["investigation_runtime_scope"] = research["type"].map(
        {
            "Movie": "Duración total de película (estimada)",
            "TV Show": "Duración por episodio (estimada)",
        }
    )
    research["type_label"] = research["type"].map(TYPE_LABELS)
    research["genres"] = research["genres"].fillna("Unknown")
    return research


def display_genre(value: str) -> str:
    return GENRE_LABELS.get(value, value)


def split_column(
    catalog: pd.DataFrame,
    column: str,
    label_map: dict[str, str] | None = None,
) -> pd.DataFrame:
    values = catalog[column].fillna("").astype(str).str.split(",").explode().str.strip()
    result = pd.DataFrame(
        {"valor": values, "_content_row": catalog["_content_row"].reindex(values.index)}
    )
    result = result.loc[result["valor"] != ""].copy()
    if column == "genres":
        result = result.loc[result["valor"].str.casefold() != "unknown"].copy()
    if label_map:
        result["etiqueta"] = result["valor"].map(label_map).fillna(result["valor"])
    else:
        result["etiqueta"] = result["valor"]
    return result


def format_count(value: int | float) -> str:
    return f"{value:,.0f}".replace(",", ".")


def format_decimal(value: float, digits: int = 1) -> str:
    if pd.isna(value):
        return "Sin datos"
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_source_amount(value: float) -> str:
    if value >= 1_000_000_000:
        return (
            f"{format_decimal(value / 1_000_000_000, 1)} mil millones "
            "(moneda no especificada)"
        )
    if value >= 1_000_000:
        return (
            f"{format_decimal(value / 1_000_000, 1)} millones "
            "(moneda no especificada)"
        )
    return f"{format_count(value)} (moneda no especificada)"


def update_figure(figure: object, x_title: str | None = None, y_title: str | None = None) -> object:
    figure.update_layout(
        legend_title_text="",
        margin={"t": 58, "l": 12, "r": 12, "b": 12},
        hoverlabel={"namelength": -1},
    )
    if x_title is not None:
        figure.update_xaxes(title=x_title)
    if y_title is not None:
        figure.update_yaxes(title=y_title)
    return figure


def apply_filters(catalog: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.header("Filtros del catálogo")
        types = sorted(catalog["type"].dropna().unique())
        selected_types = st.multiselect(
            "Tipo de contenido", types, default=types,
            format_func=lambda value: TYPE_LABELS.get(value, value),
        )

        valid_years = catalog["release_year"].dropna()
        if valid_years.empty:
            st.error("Los archivos no contienen años de estreno válidos.")
            st.stop()
        year_min, year_max = int(valid_years.min()), int(valid_years.max())
        selected_years = st.slider(
            "Año de estreno", year_min, year_max, (year_min, year_max), step=1
        )

        genres = sorted({
            display_genre(value.strip())
            for raw in catalog["genres"].dropna().astype(str)
            for value in raw.split(",")
            if value.strip() and value.strip() != "Unknown"
        })
        selected_genres = st.multiselect("Género", genres, default=[])

        scores = catalog["vote_average"].dropna()
        if scores.empty:
            st.error("Los archivos no contienen calificaciones válidas.")
            st.stop()
        selected_score = st.slider(
            "Calificación promedio (0–10)",
            min_value=0.0,
            max_value=10.0,
            value=(max(0.0, float(scores.min())), min(10.0, float(scores.max()))),
            step=0.1,
        )

    selected = catalog[
        catalog["type"].isin(selected_types)
        & catalog["release_year"].between(*selected_years)
        & catalog["vote_average"].between(*selected_score)
    ].copy()
    if selected_genres:
        selected["_genres_es"] = selected["genres"].map(
            lambda raw: {display_genre(value.strip()) for value in str(raw).split(",")}
        )
        selected = selected[
            selected["_genres_es"].map(lambda values: bool(set(selected_genres) & values))
        ]
    return selected


def render_kpis(catalog: pd.DataFrame) -> None:
    score = catalog["vote_average"].mean()
    popularity = catalog["popularity"].mean()
    columns = st.columns(3, gap="medium")
    indicators = [
        ("Títulos seleccionados", format_count(len(catalog)), "Cantidad de títulos según los filtros activos."),
        ("Calificación promedio", f"{format_decimal(score, 2)}/10", "Promedio de vote_average; escala 0 a 10."),
        ("Popularidad promedio", format_decimal(popularity, 1), "Índice TMDB; no equivale a reproducciones."),
    ]
    for column, (label, value, help_text) in zip(columns, indicators):
        with column:
            st.metric(label, value, help=help_text, border=True)


def render_overview(catalog: pd.DataFrame) -> None:
    st.subheader("Resumen ejecutivo")
    st.caption(
        "Audiencia: Directorio y Gerencia General. Orienta decisiones de catálogo y marketing; "
        "no mide comportamiento de suscriptores."
    )
    movie_count = int((catalog["type"] == "Movie").sum())
    show_count = int((catalog["type"] == "TV Show").sum())
    countries = split_column(catalog, "country")["valor"].nunique()
    languages = catalog["language"].nunique()
    genres = split_column(catalog, "genres")["valor"].nunique()
    st.markdown("#### Indicadores del catálogo")
    extra = st.columns(5)
    for column, label, value in zip(
        extra,
        ["Películas", "Series", "Países informados", "Idiomas", "Géneros"],
        [movie_count, show_count, countries, languages, genres],
    ):
        column.metric(label, format_count(value))

    yearly = (
        catalog.groupby(["release_year", "type_label"], as_index=False)
        .size()
        .rename(columns={"release_year": "Año de estreno", "type_label": "Tipo de contenido", "size": "Títulos"})
    )
    left, right = st.columns(2)
    with left:
        figure = px.line(
            yearly, x="Año de estreno", y="Títulos", color="Tipo de contenido",
            markers=True, title="Estrenos por año", color_discrete_map=TYPE_COLORS,
        )
        update_figure(figure, "Año", "Cantidad de títulos")
        st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)
    with right:
        type_counts = catalog["type_label"].value_counts().rename_axis(
            "Tipo de contenido"
        ).reset_index(name="Títulos")
        figure = px.pie(
            type_counts, names="Tipo de contenido", values="Títulos", hole=0.58,
            title="Composición del catálogo", color="Tipo de contenido",
            color_discrete_map=TYPE_COLORS,
        )
        update_figure(figure)
        st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)

    genre_counts = split_column(catalog, "genres", GENRE_LABELS).groupby(
        "etiqueta"
    )["_content_row"].nunique().nlargest(10).sort_values().rename("Títulos").reset_index()
    figure = px.bar(
        genre_counts, x="Títulos", y="etiqueta", orientation="h",
        title="Géneros con más títulos", color_discrete_sequence=["#188C9E"],
        labels={"etiqueta": "Género"},
    )
    update_figure(figure, "Cantidad de títulos", "")
    st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)

    release_counts = catalog["release_year"].value_counts()
    if not release_counts.empty and release_counts.nunique() == 1:
        st.warning(
            f"En esta selección hay exactamente {int(release_counts.iloc[0]):,} "
            "títulos por año de estreno. La distribución uniforme debe validarse "
            "antes de interpretarla como tendencia de producción."
        )

    st.markdown("### Narrativa y decisiones")
    most_common_genre = genre_counts.iloc[-1]["etiqueta"] if not genre_counts.empty else "sin información"
    type_rating = catalog.groupby("type_label")["vote_average"].mean().dropna()
    highest_rated_type = type_rating.idxmax() if not type_rating.empty else "sin datos"
    highest_score = type_rating.max() if not type_rating.empty else float("nan")
    st.markdown(
        f"""
        **Qué ocurre:** {most_common_genre} concentra más títulos en la selección;
        el promedio de calificación más alto corresponde a **{highest_rated_type}**
        ({format_decimal(highest_score, 2)}/10).

        **Qué hacer:** usar estos patrones para formular hipótesis de adquisición y
        promoción. Antes de asignar presupuesto o tomar decisiones de retención,
        contrastarlos con reproducciones, finalizaciones, búsquedas y cancelaciones
        anonimizadas por cohorte, que no vienen en estas fuentes.
        """
    )


def render_catalog_analysis(catalog: pd.DataFrame) -> None:
    st.subheader("Catálogo, geografía y producción")
    st.caption(
        "Audiencia: Gerencia de Contenidos y Adquisición. Los países múltiples se "
        "desglosan al contar y un título puede contribuir a más de un país."
    )
    genre = split_column(catalog, "genres", GENRE_LABELS)
    genre_counts = (
        genre.groupby("etiqueta")["_content_row"].nunique().nlargest(12)
        .sort_values().rename("Títulos").reset_index()
    )
    countries = split_column(catalog, "country", COUNTRY_LABELS)
    country_counts = (
        countries.groupby("etiqueta")["_content_row"].nunique().nlargest(12)
        .sort_values().rename("Títulos").reset_index()
    )
    languages = split_column(catalog, "language", LANGUAGE_LABELS)
    language_counts = (
        languages.groupby("etiqueta")["_content_row"].nunique().nlargest(12)
        .sort_values().rename("Títulos").reset_index()
    )
    first, second = st.columns(2)
    with first:
        figure = px.bar(
            genre_counts, x="Títulos", y="etiqueta", orientation="h",
            title="Títulos por género", color_discrete_sequence=["#188C9E"],
            labels={"etiqueta": "Género"},
        )
        update_figure(figure, "Cantidad de títulos", "")
        st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)
    with second:
        figure = px.bar(
            country_counts, x="Títulos", y="etiqueta", orientation="h",
            title="Títulos por país de producción", color_discrete_sequence=["#8A63C7"],
            labels={"etiqueta": "País"},
        )
        update_figure(figure, "Cantidad de títulos", "")
        st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)
    figure = px.bar(
        language_counts, x="Títulos", y="etiqueta", orientation="h",
        title="Títulos por idioma principal", color_discrete_sequence=["#E4A92D"],
        labels={"etiqueta": "Idioma"},
    )
    update_figure(figure, "Cantidad de títulos", "")
    st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)

    date_rows = catalog.dropna(subset=["date_added"]).copy()
    if not date_rows.empty:
        date_rows["Año de incorporación"] = date_rows["date_added"].dt.year
        added_counts = (
            date_rows.groupby(["Año de incorporación", "type_label"], as_index=False)
            .size().rename(columns={"type_label": "Tipo de contenido", "size": "Títulos"})
        )
        figure = px.area(
            added_counts, x="Año de incorporación", y="Títulos",
            color="Tipo de contenido", title="Incorporaciones por año",
            color_discrete_map=TYPE_COLORS,
        )
        update_figure(figure, "Año", "Cantidad de incorporaciones")
        st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)
        counts_per_year = date_rows["Año de incorporación"].value_counts()
        if counts_per_year.nunique() == 1:
            st.warning(
                f"La fuente contiene exactamente {int(counts_per_year.iloc[0]):,} "
                "registros por año de incorporación en el periodo observado. "
                "La distribución uniforme requiere validación con el responsable de "
                "la fuente antes de interpretar la tendencia como crecimiento real."
            )

    st.markdown("#### Directores y actores con más apariciones")
    people_cols = st.columns(2)
    for column, source_col, label in [
        (people_cols[0], "director", "Directores"),
        (people_cols[1], "cast", "Actores"),
    ]:
        people = split_column(catalog, source_col)
        people = people.loc[people["valor"].str.casefold() != "unknown"]
        top_people = (
            people.groupby("valor")["_content_row"].nunique().nlargest(10)
            .sort_values().rename("Títulos").reset_index()
        )
        with column:
            figure = px.bar(
                top_people, x="Títulos", y="valor", orientation="h",
                title=f"{label} con mayor presencia",
                labels={"valor": label[:-1] if label.endswith("s") else label},
                color_discrete_sequence=["#3685D3" if source_col == "director" else "#8A63C7"],
            )
            update_figure(figure, "Cantidad de títulos", "")
            st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)
    st.caption(
        "Los conteos de personas son apariciones en listas de créditos, no medidas "
        "de audiencia, calidad causal o valor de mercado."
    )


def render_popularity(catalog: pd.DataFrame) -> None:
    st.subheader("Popularidad y valoración")
    st.caption(
        "Audiencia: Marketing y Producto. El índice de popularidad, las calificaciones y los votos "
        "son metadatos externos y no describen reproducciones de StreamView."
    )

    top_popular = catalog.nlargest(10, "popularity").sort_values("popularity")
    top_popular = top_popular.assign(Tipo=top_popular["type_label"])
    left, right = st.columns(2)
    with left:
        figure = px.bar(
            top_popular, x="popularity", y="title", color="Tipo", orientation="h",
            title="10 títulos con mayor popularidad",
            labels={"popularity": "Índice TMDB", "title": "Título"},
            color_discrete_map=TYPE_COLORS,
        )
        update_figure(figure, "Popularidad (índice TMDB)", "")
        st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)
    with right:
        most_voted = catalog.nlargest(10, "vote_count").sort_values("vote_count")
        figure = px.bar(
            most_voted, x="vote_count", y="title", color="type_label", orientation="h",
            title="10 títulos con más votos externos",
            labels={"vote_count": "Cantidad de votos", "title": "Título", "type_label": "Tipo"},
            color_discrete_map=TYPE_COLORS,
        )
        update_figure(figure, "Votos externos", "")
        st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)

    valid_votes = catalog[catalog["vote_count"].fillna(0) > 0]
    figure = px.scatter(
        valid_votes, x="vote_average", y="popularity", size="vote_count",
        color="type_label", hover_name="title", opacity=0.68,
        title="Relación entre calificación, popularidad y votos",
        labels={
            "vote_average": "Calificación promedio (0–10)",
            "popularity": "Popularidad TMDB",
            "vote_count": "Votos externos",
            "type_label": "Tipo de contenido",
        },
        color_discrete_map=TYPE_COLORS,
    )
    update_figure(figure, "Calificación promedio (0–10)", "Popularidad (índice TMDB)")
    st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)

    genre = split_column(catalog, "genres", GENRE_LABELS)
    scored = genre.merge(
        catalog[["_content_row", "popularity", "vote_average"]],
        on="_content_row",
        how="left",
        validate="many_to_one",
    )
    genre_metrics = (
        scored.groupby("etiqueta", as_index=False)
        .agg(
            Títulos=("_content_row", "nunique"),
            **{
                "Popularidad promedio": ("popularity", "mean"),
                "Calificación promedio": ("vote_average", "mean"),
            },
        )
        .query("Títulos >= @MIN_GROUP_SIZE")
        .nlargest(12, "Popularidad promedio")
        .sort_values("Popularidad promedio")
    )
    figure = px.bar(
        genre_metrics, x="Popularidad promedio", y="etiqueta", orientation="h",
        color="Calificación promedio", title="Popularidad y calificación promedio por género",
        labels={"etiqueta": "Género"},
        color_continuous_scale=["#56B4E9", "#E69F00"],
    )
    update_figure(figure, "Popularidad promedio (TMDB)", "")
    st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)
    st.caption(f"Para comparar grupos, se muestran categorías con al menos {MIN_GROUP_SIZE} títulos.")

    st.markdown("#### Popularidad y valoración por territorio e idioma")
    for column_name, source_column, label_map, dimension in [
        ("País", "country", COUNTRY_LABELS, "país"),
        ("Idioma", "language", LANGUAGE_LABELS, "idioma"),
    ]:
        expanded = split_column(catalog, source_column, label_map).merge(
            catalog[["_content_row", "popularity", "vote_average"]],
            on="_content_row",
            how="left",
            validate="many_to_one",
        )
        dimension_metrics = (
            expanded.groupby("etiqueta", as_index=False)
            .agg(
                Títulos=("_content_row", "nunique"),
                **{
                    "Popularidad promedio": ("popularity", "mean"),
                    "Calificación promedio": ("vote_average", "mean"),
                },
            )
            .query("Títulos >= @MIN_GROUP_SIZE")
        )
        if dimension_metrics.empty:
            st.info(
                f"No hay grupos de {dimension} con al menos "
                f"{MIN_GROUP_SIZE} títulos en la selección."
            )
            continue
        popularity_figure = px.bar(
            dimension_metrics.nlargest(12, "Popularidad promedio").sort_values(
                "Popularidad promedio"
            ),
            x="Popularidad promedio",
            y="etiqueta",
            orientation="h",
            title=f"Índice de popularidad promedio por {dimension}",
            labels={"etiqueta": column_name},
            color_discrete_sequence=["#188C9E"],
        )
        update_figure(popularity_figure, "Índice TMDB promedio", "")
        st.plotly_chart(
            popularity_figure, width="stretch", config=PLOT_CONFIG
        )
        if source_column == "country":
            rating_figure = px.bar(
                dimension_metrics.nlargest(12, "Calificación promedio").sort_values(
                    "Calificación promedio"
                ),
                x="Calificación promedio",
                y="etiqueta",
                orientation="h",
                title="Calificación promedio por país",
                labels={"etiqueta": "País"},
                color_discrete_sequence=["#8A63C7"],
            )
            update_figure(rating_figure, "Calificación promedio (0–10)", "")
            st.plotly_chart(rating_figure, width="stretch", config=PLOT_CONFIG)
    st.caption(
        f"Solo se muestran grupos con al menos {MIN_GROUP_SIZE} títulos. "
        "Un título con varios países se cuenta en cada país informado."
    )

    st.markdown("#### Títulos mejor evaluados")
    st.warning(
        "El ranking ordena el promedio informado, sin corregir por cantidad de votos. "
        "Interprételo junto con el volumen de votos; una calificación basada en pocas "
        "evaluaciones tiene mayor incertidumbre."
    )
    best_rated = catalog.nlargest(10, "vote_average")[
        ["title", "type_label", "vote_average", "vote_count"]
    ].rename(
        columns={
            "title": "Título",
            "type_label": "Tipo",
            "vote_average": "Calificación promedio",
            "vote_count": "Cantidad de votos",
        }
    )
    st.dataframe(best_rated, hide_index=True, width="stretch")


def render_finance(catalog: pd.DataFrame) -> None:
    st.subheader("Finanzas de películas")
    st.caption(
        "Solo se consideran películas con budget y revenue positivos; las series "
        "se excluyen de este análisis conforme a las reglas del caso."
    )
    movies = catalog.loc[catalog["type"] == "Movie"].copy()
    financial = movies[
        (movies["budget"].fillna(0) > 0) & (movies["revenue"].fillna(0) > 0)
    ].copy()
    if financial.empty:
        st.warning("No hay películas con presupuesto e ingresos positivos en esta selección.")
        return

    financial["roi_aproximado"] = financial["revenue"] / financial["budget"]
    kpis = st.columns(4)
    values = [
        ("Películas evaluables", format_count(len(financial))),
        ("Presupuesto promedio", format_source_amount(financial["budget"].mean())),
        ("Presupuesto total", format_source_amount(financial["budget"].sum())),
        ("Ingresos totales", format_source_amount(financial["revenue"].sum())),
    ]
    for column, (label, value) in zip(kpis, values):
        column.metric(label, value)
    weighted_roi = financial["revenue"].sum() / financial["budget"].sum()
    st.metric(
        "ROI aproximado agregado (ingresos / presupuesto)",
        f"{format_decimal(weighted_roi, 2)}×",
    )

    left, right = st.columns(2)
    with left:
        figure = px.scatter(
            financial, x="budget", y="revenue", color="vote_average",
            size="vote_count", hover_name="title", log_x=True, log_y=True,
            title="Presupuesto e ingresos (escala logarítmica)",
            labels={
                "budget": "Presupuesto (moneda según fuente)",
                "revenue": "Ingresos (moneda según fuente)",
                "vote_average": "Calificación promedio",
                "vote_count": "Votos externos",
            },
            color_continuous_scale=["#56B4E9", "#E69F00"],
        )
        update_figure(figure, "Presupuesto (escala logarítmica)", "Ingresos (escala logarítmica)")
        st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)
    with right:
        top_revenue = financial.nlargest(10, "revenue").sort_values("revenue")
        figure = px.bar(
            top_revenue, x="revenue", y="title", orientation="h",
            title="10 películas con mayores ingresos",
            labels={"revenue": "Ingresos (moneda según fuente)", "title": "Título"},
            color_discrete_sequence=["#188C9E"],
        )
        update_figure(figure, "Ingresos reportados", "")
        st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)

    top_roi = financial.nlargest(10, "roi_aproximado").sort_values("roi_aproximado")
    figure = px.bar(
        top_roi, x="roi_aproximado", y="title", orientation="h",
        title="10 películas con mayor ROI aproximado",
        labels={"roi_aproximado": "Ingresos / presupuesto", "title": "Título"},
        color_discrete_sequence=["#8A63C7"],
    )
    update_figure(figure, "ROI aproximado (veces)", "")
    st.plotly_chart(figure, width="stretch", config=PLOT_CONFIG)

    budget_cutoff = financial["budget"].quantile(0.25)
    low_budget = financial.loc[financial["budget"] <= budget_cutoff].nlargest(10, "revenue")
    st.markdown("#### Mayores ingresos entre las películas de menor presupuesto")
    st.caption(
        f"“Menor presupuesto” se define aquí como el cuartil inferior del grupo "
        f"evaluable (budget ≤ {format_source_amount(budget_cutoff)}); es un criterio "
        "descriptivo de este análisis, no una categoría definida por el caso."
    )
    st.dataframe(
        low_budget[["title", "budget", "revenue", "roi_aproximado"]].rename(
            columns={
                "title": "Título",
                "budget": "Presupuesto",
                "revenue": "Ingresos",
                "roi_aproximado": "ROI aproximado",
            }
        ),
        hide_index=True,
        width="stretch",
    )
    st.warning(
        "Revenue / Budget no es rentabilidad contable: no incorpora costos de "
        "distribución, marketing ni calendario de flujos. Los presupuestos e ingresos "
        "son valores según fuente; extremos y magnitudes requieren validación."
    )


def render_business_context() -> None:
    st.subheader("Contexto del caso y reglas de negocio")
    st.caption(
        "Resumen fiel de las Partes I y II del caso académico. La descripción de "
        "StreamView es un supuesto narrativo del encargo, no una verificación de una empresa real."
    )
    st.markdown("#### Empresa, propósito y problema")
    st.markdown(
        """
        El caso presenta a **StreamView Analytics** como una plataforma internacional
        de suscripción audiovisual, fundada en 2018 y disponible en mercados de
        Latinoamérica. Su misión es facilitar el acceso a contenido audiovisual con
        una experiencia personalizada y sustentada en información confiable; su visión
        es liderar el entretenimiento digital en Latinoamérica mediante datos y
        analítica. El caso enumera como valores innovación, orientación al usuario,
        calidad, transparencia, colaboración y decisiones basadas en evidencia.

        El problema de negocio descrito es la falta de una visión consolidada del
        catálogo: reportes independientes producen indicadores inconsistentes,
        dificultan comparar géneros y países y limitan las decisiones de adquisición
        y promoción. Los dashboards actuales se describen como sobrecargados y con
        poca interacción.
        """
    )
    st.markdown("#### Objetivo, alcance y audiencias")
    st.markdown(
        """
        **Objetivo general:** comunicar información relevante del catálogo mediante
        visualizaciones, dashboards interactivos y storytelling para apoyar decisiones.
        Los objetivos específicos son caracterizar la oferta, comparar país, idioma,
        género, popularidad y valoración, analizar tendencias y relaciones financieras
        disponibles, construir vistas por audiencia y formular recomendaciones basadas
        en evidencia.

        **Alcance del caso:** usar exclusivamente los dos datasets entregados. No se
        incluyen modelos predictivos, IA, procesos ETL ni cambios en sistemas
        operacionales. Las audiencias son Directorio, Gerencia General, Contenidos y
        Adquisición, Marketing, Producto y Data & Analytics.
        """
    )
    st.markdown("#### Arquitectura lógica")
    st.code(
        "Fuentes de catálogo\n"
        "├── Películas (16.000 filas, 18 columnas)\n"
        "└── Series (16.000 filas, 16 columnas)\n"
        "    └── integración analítica por registro y tipo de contenido\n"
        "        └── visualizaciones, filtros e indicadores",
        language="text",
    )
    st.markdown("#### Modelo analítico y fuentes")
    st.dataframe(
        pd.DataFrame(
            [
                (
                    "Películas",
                    MOVIES_FILE.relative_to(PROJECT_ROOT).as_posix(),
                    "Una fila de la fuente por registro de película.",
                ),
                (
                    "Series",
                    SHOWS_FILE.relative_to(PROJECT_ROOT).as_posix(),
                    "Una fila de la fuente por registro de serie.",
                ),
            ],
            columns=["Fuente", "Archivo", "Grano"],
        ),
        hide_index=True,
        width="stretch",
    )
    st.caption(
        "Las dos fuentes se anexan para analizar variables comunes; el tipo de "
        "contenido identifica el origen. `_content_row` es una llave técnica de la "
        "integración, no un identificador de negocio ni de cliente."
    )
    st.markdown("#### Diccionario de variables")
    st.dataframe(
        pd.DataFrame(DATA_DICTIONARY, columns=["Variable original", "Tipo observado / esperado", "Descripción y observación"]),
        hide_index=True,
        width="stretch",
    )
    st.warning(
        "Discrepancia importante: el PDF define rating como clasificación por edad "
        "(ejemplos TV-MA, PG-13 y R), pero los CSV entregados contienen rating numérico "
        "0–10 y sus valores coinciden con vote_average en todos los registros. No se "
        "puede analizar distribución por clasificación etaria con estos archivos."
    )
    st.markdown("#### KPI y definiciones operativas")
    st.dataframe(
        pd.DataFrame(
            [
                (
                    "Títulos seleccionados",
                    "Conteo de registros del catálogo después de aplicar filtros.",
                    "No representa suscriptores ni reproducciones.",
                ),
                (
                    "Calificación promedio",
                    "Media de `vote_average` en escala 0–10.",
                    "Valoración externa; no es rating etario ni satisfacción de clientes.",
                ),
                (
                    "Popularidad promedio",
                    "Media del índice `popularity` reportado.",
                    "Índice externo; no equivale a vistas o engagement.",
                ),
                (
                    "ROI aproximado de películas",
                    "Ingresos / presupuesto para películas donde ambos valores son positivos.",
                    "No es rentabilidad contable; la moneda no está especificada en los archivos.",
                ),
            ],
            columns=["Indicador", "Definición", "Interpretación / límite"],
        ),
        hide_index=True,
        width="stretch",
    )
    st.markdown("#### Reglas de negocio aplicadas")
    st.markdown(
        """
        1. Una fila se trata como un registro de contenido, pero `show_id` no es una
           clave única global: hay 9 ID repetidos en series y 397 ID que aparecen en
           ambos tipos. Se conserva el dataset y se distingue por tipo.
        2. Películas y series se comparan solo en variables comunes.
        3. `budget` y `revenue` se usan únicamente para películas y con ambos valores
           positivos en los KPI financieros.
        4. `vote_average` se interpreta en escala 0–10; `popularity` no son vistas.
        5. Cada visualización indica periodo y alcance; los filtros se muestran en
           todas las secciones y los KPI principales se recalculan.
        6. Cuando una variable no está disponible o contradice el diccionario del caso,
           se excluye o se declara la limitación, sin fabricar valores.
        """
    )


def render_quality(catalog: pd.DataFrame) -> None:
    st.subheader("Calidad de datos y preguntas pendientes")
    st.caption("Auditoría calculada desde los CSV locales; no se modifican los originales.")
    source_stats = []
    for content_type, frame in [
        ("Películas", load_source(MOVIES_FILE, "Movie")),
        ("Series", load_source(SHOWS_FILE, "TV Show")),
    ]:
        source_stats.append(
            {
                "Fuente": content_type,
                "Filas": len(frame),
                "Columnas": len(frame.columns),
                "ID duplicados": int(frame["show_id"].duplicated().sum()),
                "Director nulo": int(frame["director"].isna().sum()),
                "País nulo": int(frame["country"].isna().sum()),
                "Género nulo": int(frame["genres"].isna().sum()),
                "Duración nula": int(frame["duration"].isna().sum()),
            }
        )
    st.dataframe(pd.DataFrame(source_stats), hide_index=True, width="stretch")

    duplicates = int(catalog["show_id"].duplicated().sum())
    missing_rows = []
    for column in catalog.columns:
        if column in {"type_label", "_content_row", "_genres_es"}:
            continue
        count = int(catalog[column].isna().sum())
        if count:
            missing_rows.append(
                {
                    "Variable original": column,
                    "Nulos": count,
                    "Nulos en la integración": format_count(count),
                    "%": format_decimal(count / len(catalog) * 100, 2),
                }
            )
    left, right = st.columns(2)
    with left:
        st.metric("ID repetidos dentro de la selección", format_count(duplicates))
        st.markdown("#### Variables con datos faltantes")
        st.dataframe(
            pd.DataFrame(missing_rows)
            .sort_values("Nulos", ascending=False)
            .drop(columns="Nulos"),
            hide_index=True,
            width="stretch",
        )
    with right:
        st.markdown("#### Hallazgos de validación")
        st.markdown(
            """
            - Hay **16.000 películas** y **16.000 series** (32.000 filas en total).
            - Las películas tienen `duration` nulo en las 16.000 filas; no se puede
              analizar duración de películas con este archivo.
            - Hay 9 ID repetidos en el CSV de series; en una concatenación directa hay
              además colisiones de `show_id` entre los dos tipos. No se deduplicó sin
              una regla de identidad confirmada.
            - `rating` es numérico e idéntico a `vote_average`; no representa edad.
            - Los años de estreno cubren 2010–2025 con exactamente 2.000 filas por año.
              Las fechas `date_added` también suman exactamente 2.000 filas por año;
              validar esta distribución antes de afirmar tendencias reales.
            - `date_added` se pudo convertir a fecha en las 32.000 filas.
            - Hay 2.263 países nulos y 10.965 directores nulos en la fuente de series;
              los créditos y la geografía son incompletos.
            - Los CSV contienen vacíos y ceros en métricas; en finanzas solo se toman
              valores estrictamente positivos para budget y revenue.
            - Solo 3.540 películas tienen presupuesto e ingresos positivos: en 1.298
              el ingreso es menor al presupuesto, en 6 es igual y en 2.236 es mayor.
              Son comparaciones nominales de campos cuya moneda no está especificada.
            - Popularity presenta cola extrema (mediana 10,9135; máximo 3.876,006).
              Se conserva el valor y no se eliminan atípicos sin una regla confirmada.
            """
        )

    st.markdown("#### Preguntas del caso: cobertura y límite de estos datos")
    coverage = pd.DataFrame(
        [
            ("Distribución de películas/series, géneros, países e idiomas", "Calculable", "Conteos del catálogo; país/género pueden ser múltiples por título."),
            ("Popularidad y valoración por título, género, país o idioma", "Calculable con cautela", "Son metadatos/votos externos; no miden consumo."),
            ("Evolución de estrenos e incorporaciones", "Calculable, requiere validación", "La fuente tiene exactamente 2.000 filas por año en ambos campos temporales."),
            ("Directores y actores más frecuentes", "Parcial", "Listas de créditos incompletas y separadas por coma; cuenta apariciones informadas."),
            ("Presupuesto, ingresos y ROI aproximado de películas", "Parcial", "Solo 3.540 películas tienen ambos valores positivos."),
            ("Duración de películas y series", "Investigación complementaria", "Los CSV aparte contienen solo estimaciones no verificadas; para series son por episodio, no duración total."),
            ("Clasificación por edad", "No calculable", "El campo `rating` es numérico y coincide con `vote_average`; no hay categorías etarias en los CSV."),
            ("Churn, retención, reproducciones y engagement de clientes", "No calculable", "No hay clientes, suscripciones, eventos de uso, reproducciones ni cancelaciones."),
        ],
        columns=["Pregunta / análisis", "Estado", "Justificación"],
    )
    st.dataframe(coverage, hide_index=True, width="stretch")
    st.info(
        "Para medir churn y retención se requieren registros anonimizados de suscripción "
        "con fechas de alta/cancelación y una definición de churn. Para engagement/UX: "
        "eventos de impresión, búsqueda, reproducción, minutos vistos, finalización, "
        "dispositivo y fecha, vinculables por identificador seudonimizado. Esto sería "
        "una nueva fuente y queda fuera del alcance de los CSV y de la Parte II."
    )


def render_external_research() -> None:
    st.subheader("Investigación complementaria (en construcción)")
    st.warning(
        "Esta sección usa exclusivamente los dos CSV complementarios preparados "
        "para la investigación; no modifica ni alimenta los indicadores oficiales "
        "del catálogo. Es material provisional, no verificado al 100 %, y requiere "
        "validación antes de citarlo como dato factual."
    )
    st.markdown(
        """
        **Archivos utilizados:** `data/research_inputs/netflix_movies_completed_estimates.csv`
        y `data/research_inputs/netflix_tv_shows_completed_estimates.csv`. Se mantienen
        separados de los archivos oficiales y se anexan únicamente dentro de esta vista
        investigativa. Los CSV incluyen sus propios campos de fuente, método y estado.

        **Duraciones:** todas las filas de ambos archivos están marcadas como estimadas
        y no verificadas externamente. Para películas, la cifra pretende aproximar la
        duración total; para series, es una estimación por episodio. Las temporadas,
        cantidad de episodios y duración total de las series no están informadas.

        **Interacción y clientes:** `engagement_proxy_score` es un proxy interno basado
        en percentiles de popularidad y votos; no representa reproducciones, usuarios
        únicos ni engagement real de Netflix. Los archivos indican que churn, retención
        y clientes activos no son calculables con las fuentes disponibles. Los campos
        financieros estimados de películas también requieren verificación; aunque algunos
        nombres de columna declaran USD, esa moneda no se ha validado.
        """
    )

    try:
        research = load_research_catalog()
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        st.error(f"No se pudo cargar la investigación complementaria: {error}")
        return

    st.caption(
        f"Archivos locales preparados para esta investigación: "
        f"{format_count(len(research))} registros en total. "
        "No se emparejan ni reemplazan registros del análisis principal."
    )
    with st.sidebar:
        st.header("Filtros de investigación")
        st.caption("La valoración es numérica (0–10), no una clasificación por edad.")
        content_types = sorted(research["type"].dropna().unique())
        selected_types = st.multiselect(
            "Tipo de contenido",
            content_types,
            default=content_types,
            format_func=lambda value: TYPE_LABELS.get(value, value),
            key="research_types",
        )
        years = research["release_year"].dropna()
        if years.empty:
            st.error("Los CSV complementarios no contienen años de estreno válidos.")
            return
        year_min, year_max = int(years.min()), int(years.max())
        selected_years = st.slider(
            "Año de estreno",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max),
            key="research_years",
        )
        scores = research["rating"].dropna()
        if scores.empty:
            st.error("Los CSV complementarios no contienen calificaciones válidas.")
            return
        selected_scores = st.slider(
            "Valoración disponible (0–10)",
            min_value=0.0,
            max_value=10.0,
            value=(max(0.0, float(scores.min())), min(10.0, float(scores.max()))),
            step=0.1,
            key="research_ratings",
        )
        available_genres = sorted(
            {
                display_genre(value.strip())
                for raw in research["genres"].astype(str)
                for value in raw.split(",")
                if value.strip() and value.strip().casefold() != "unknown"
            }
        )
        selected_genres = st.multiselect(
            "Género", available_genres, default=[], key="research_genres"
        )

    selected = research[
        research["type"].isin(selected_types)
        & research["release_year"].between(*selected_years)
        & research["rating"].between(*selected_scores)
    ].copy()
    selected["_genres_es"] = selected["genres"].map(
        lambda raw: {display_genre(item.strip()) for item in str(raw).split(",")}
    )
    if selected_genres:
        selected = selected[
            selected["_genres_es"].map(
                lambda values: bool(set(selected_genres) & values)
            )
        ].copy()
    if selected.empty:
        st.warning("No hay títulos que coincidan con los filtros de investigación.")
        return

    estimate_flags = (
        selected["runtime_is_estimate"]
        .astype("string")
        .str.casefold()
        .isin({"true", "1", "yes", "sí"})
    )
    runtime_count = int(
        (selected["investigation_runtime_minutes"].notna() & estimate_flags).sum()
    )
    proxy_count = int(selected["engagement_proxy_score"].notna().sum())
    kpis = st.columns(3)
    kpis[0].metric("Registros en la selección", format_count(len(selected)))
    kpis[1].metric("Duraciones estimadas", format_count(runtime_count))
    kpis[2].metric("Registros con proxy interno", format_count(proxy_count))
    st.caption(
        "La duración estimada de una película y la duración estimada por episodio "
        "son conceptos distintos; no deben compararse como si tuvieran el mismo alcance."
    )

    genre_rows = selected[["genres", "engagement_proxy_score"]].copy()
    genre_rows["Género"] = genre_rows["genres"].astype(str).str.split(",")
    genre_rows = genre_rows.explode("Género")
    genre_rows["Género"] = genre_rows["Género"].str.strip().map(display_genre)
    genre_rows = genre_rows.loc[
        genre_rows["Género"].ne("No informado")
        & genre_rows["engagement_proxy_score"].notna()
    ]
    genre_summary = (
        genre_rows.groupby("Género", as_index=False)
        .agg(
            proxy_promedio=("engagement_proxy_score", "mean"),
            registros=("engagement_proxy_score", "size"),
        )
        .sort_values("registros", ascending=False)
        .head(15)
    )
    if not genre_summary.empty:
        st.markdown("#### Proxy comparativo por género")
        st.caption(
            "Promedio del score interno incluido en los CSV. Es una señal exploratoria "
            "basada en popularidad y votos externos; no mide actividad de clientes."
        )
        figure = px.bar(
            genre_summary.sort_values("proxy_promedio"),
            x="proxy_promedio",
            y="Género",
            orientation="h",
            color="proxy_promedio",
            color_continuous_scale="Blues",
            hover_data={"registros": True, "proxy_promedio": ":.2f"},
            labels={"proxy_promedio": "Proxy promedio", "Género": "Género"},
        )
        st.plotly_chart(
            update_figure(figure, "Proxy promedio (no es engagement real)", ""),
            width="stretch",
            config=PLOT_CONFIG,
        )

    visible_columns = [
        column
        for column in [
            "type_label",
            "title",
            "show_id",
            "release_year",
            "_genres_es",
            "duration",
            "investigation_runtime_minutes",
            "investigation_runtime_scope",
            "runtime_verification_status",
            "runtime_source",
            "runtime_estimation_method",
            "engagement_proxy_score",
            "engagement_proxy_method",
            "customer_metrics_status",
            "estimated_gross_profit_usd",
            "estimated_roi_pct",
            "imdb_search_url",
            "tmdb_record_url",
            "_research_source_file",
            "_research_source_row",
        ]
        if column in selected.columns
    ]
    visible_labels = {
        "type_label": "Tipo",
        "title": "Título",
        "show_id": "ID del archivo complementario",
        "release_year": "Año de estreno",
        "_genres_es": "Género(s)",
        "duration": "Duración declarada en el CSV",
        "investigation_runtime_minutes": "Duración estimada (minutos)",
        "investigation_runtime_scope": "Alcance de la estimación",
        "runtime_verification_status": "Estado de verificación de duración",
        "runtime_source": "Método/fuente declarada de duración",
        "runtime_estimation_method": "Regla de estimación declarada",
        "engagement_proxy_score": "Proxy interno (no engagement real)",
        "engagement_proxy_method": "Método del proxy",
        "customer_metrics_status": "Estado de métricas de clientes",
        "estimated_gross_profit_usd": "Utilidad bruta estimada (USD declarado)",
        "estimated_roi_pct": "ROI estimado (%)",
        "imdb_search_url": "Búsqueda IMDb",
        "tmdb_record_url": "Ficha TMDB",
        "_research_source_file": "Archivo complementario",
        "_research_source_row": "Fila de origen",
    }
    st.markdown("#### Registros complementarios")
    st.dataframe(
        selected[visible_columns].rename(columns=visible_labels).head(200),
        hide_index=True,
        width="stretch",
        column_config={
            "Búsqueda IMDb": st.column_config.LinkColumn(
                "Búsqueda IMDb", display_text="Abrir búsqueda"
            ),
            "Ficha TMDB": st.column_config.LinkColumn(
                "Ficha TMDB", display_text="Abrir ficha"
            ),
        },
    )
    if len(selected) > 200:
        st.caption(
            "Vista previa limitada a 200 filas. Las descargas incluyen todos los "
            "registros filtrados y conservan las columnas originales del archivo."
        )

    st.markdown("#### Descargas de esta investigación")
    downloads = st.columns(3)
    downloads[0].download_button(
        "Películas estimadas (CSV)",
        data=research.loc[research["type"].eq("Movie")]
        .to_csv(index=False)
        .encode("utf-8-sig"),
        file_name="netflix_movies_completed_estimates.csv",
        mime="text/csv",
        help="Descarga las filas de películas con procedencia y columnas complementarias de trazabilidad.",
    )
    downloads[1].download_button(
        "Series estimadas (CSV)",
        data=research.loc[research["type"].eq("TV Show")]
        .to_csv(index=False)
        .encode("utf-8-sig"),
        file_name="netflix_tv_shows_completed_estimates.csv",
        mime="text/csv",
        help="Descarga las filas de series con procedencia y columnas complementarias de trazabilidad.",
    )
    downloads[2].download_button(
        "Selección filtrada (CSV)",
        data=selected.drop(columns=["_genres_es"], errors="ignore")
        .to_csv(index=False)
        .encode("utf-8-sig"),
        file_name="streamview_investigacion_complementaria_filtrada.csv",
        mime="text/csv",
        help="Exporta la selección actual con procedencia, métodos y estados de verificación.",
    )


def main() -> None:
    st.title("StreamView Analytics")
    st.caption(
        "Analítica visual para explorar el catálogo audiovisual · películas y series hasta 2025"
    )

    try:
        catalog = load_catalog()
    except (FileNotFoundError, ValueError) as error:
        st.error(str(error))
        st.stop()

    with st.sidebar:
        st.title("Navegación")
        page = st.radio(
            "Ir a sección",
            [
                "Resumen ejecutivo",
                "Catálogo y tendencias",
                "Popularidad y valoración",
                "Finanzas de películas",
                "Contexto y reglas",
                "Fuentes y calidad",
                "Investigación complementaria (en construcción)",
            ],
            label_visibility="collapsed",
        )
        st.divider()

    if page == "Investigación complementaria (en construcción)":
        render_external_research()
        return

    selected = apply_filters(catalog)
    if selected.empty:
        st.warning("No hay títulos que coincidan con los filtros seleccionados.")
        st.info("Amplía el rango de años o calificación, o cambia género y tipo de contenido.")
        st.stop()

    valid_years = selected["release_year"].dropna()
    year_range = (
        f"{int(valid_years.min())}–{int(valid_years.max())}"
        if not valid_years.empty
        else "sin años informados"
    )
    st.caption(
        f"Selección: {format_count(len(selected))} de {format_count(len(catalog))} títulos"
        f" · Años de estreno: {year_range}"
    )
    render_kpis(selected)
    st.divider()

    if page == "Resumen ejecutivo":
        render_overview(selected)
    elif page == "Catálogo y tendencias":
        render_catalog_analysis(selected)
    elif page == "Popularidad y valoración":
        render_popularity(selected)
    elif page == "Finanzas de películas":
        render_finance(selected)
    elif page == "Contexto y reglas":
        render_business_context()
    else:
        render_quality(catalog)


if __name__ == "__main__":
    main()
