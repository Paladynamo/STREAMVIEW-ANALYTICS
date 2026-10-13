"""Enrich the local catalog from TMDB using its existing numeric content IDs."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "research_tmdb_enrichment.csv"
PARTIAL_FILE = DATA_DIR / "research_tmdb_enrichment.partial.csv"
SOURCES = [
    ("Movie", "netflix_movies_detailed_up_to_2025.csv", "movie"),
    ("TV Show", "netflix_tv_shows_detailed_up_to_2025.csv", "tv"),
]
API_ROOT = "https://api.themoviedb.org/3"
TMDB_ROOT = "https://www.themoviedb.org"
TERMINAL_STATUSES = {
    "verified",
    "verified_metadata_difference",
    "verified_no_runtime",
    "not_found",
}
EXTERNAL_COLUMNS = [
    "research_row_key",
    "research_source_type",
    "research_source_row",
    "research_status",
    "research_confidence",
    "research_notes",
    "research_source",
    "research_api_url",
    "research_title_url",
    "research_retrieved_at_utc",
    "research_verified_external_id",
    "research_external_title",
    "research_external_year",
    "research_movie_runtime_minutes",
    "research_episode_runtime_minutes",
    "research_episode_count",
    "research_season_count",
]


def normalize_title(value: Any) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def make_row_key(
    source_type: str, source_row_number: int, source_row: pd.Series
) -> str:
    return (
        f"{source_type}:{source_row_number}:{int(source_row['show_id'])}:"
        f"{source_row['release_year']}:{normalize_title(source_row['title'])}"
    )


def request_details(content_type: str, external_id: int, token: str) -> dict[str, Any] | None:
    endpoint = f"{API_ROOT}/{content_type}/{external_id}?language=en-US"
    request = Request(
        endpoint,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "StreamViewAnalytics/1.0 (academic research)",
        },
    )
    for attempt in range(5):
        try:
            with urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload
        except HTTPError as error:
            if error.code == 404:
                return None
            if error.code == 401:
                raise RuntimeError(
                    "TMDB rechazó el token (HTTP 401). Verifica el token de lectura "
                    "configurado localmente; no lo incluyas en el repositorio."
                ) from error
            if error.code == 429 or 500 <= error.code < 600:
                if attempt < 4:
                    retry_after = error.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else 2**attempt
                    time.sleep(min(delay, 60))
                    continue
            raise RuntimeError(
                f"Error HTTP {error.code} al consultar TMDB para ID {external_id}."
            ) from error
        except (URLError, TimeoutError) as error:
            if attempt < 4:
                time.sleep(2**attempt)
                continue
            raise RuntimeError(
                f"No se pudo consultar TMDB para ID {external_id} tras 5 intentos."
            ) from error
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RuntimeError(
                f"TMDB devolvió una respuesta no JSON para ID {external_id}."
            ) from error
    raise RuntimeError(f"Se agotaron los reintentos para el ID {external_id}.")


def build_research_record(
    source_row: pd.Series,
    source_type: str,
    api_type: str,
    source_row_number: int,
    details: dict[str, Any] | None,
) -> dict[str, Any]:
    external_id = int(source_row["show_id"])
    api_url = f"{API_ROOT}/{api_type}/{external_id}?language=en-US"
    title_url = f"{TMDB_ROOT}/{api_type}/{external_id}"
    record: dict[str, Any] = {
        "research_row_key": make_row_key(source_type, source_row_number, source_row),
        "research_source_type": source_type,
        "research_source_row": source_row_number,
        "research_status": "not_found" if details is None else "",
        "research_confidence": "Sin coincidencia" if details is None else "",
        "research_notes": (
            "TMDB no encontró el identificador."
            if details is None
            else ""
        ),
        "research_source": "The Movie Database (TMDB) API",
        "research_api_url": api_url,
        "research_title_url": title_url,
        "research_retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "research_verified_external_id": pd.NA,
        "research_external_title": pd.NA,
        "research_external_year": pd.NA,
        "research_movie_runtime_minutes": pd.NA,
        "research_episode_runtime_minutes": pd.NA,
        "research_episode_count": pd.NA,
        "research_season_count": pd.NA,
    }
    if details is None:
        return record

    returned_id = details.get("id")
    if returned_id != external_id:
        raise RuntimeError(
            f"TMDB devolvió el ID {returned_id!r} al consultar {external_id}; "
            "se detuvo para evitar una asociación incorrecta."
        )

    external_title = (
        details.get("title") if api_type == "movie" else details.get("name")
    )
    date_field = "release_date" if api_type == "movie" else "first_air_date"
    external_date = str(details.get(date_field) or "")
    external_year = external_date[:4] if len(external_date) >= 4 else ""
    title_matches = normalize_title(source_row.get("title")) == normalize_title(
        external_title
    )
    try:
        year_matches = bool(external_year) and int(external_year) == int(
            source_row["release_year"]
        )
    except (TypeError, ValueError):
        year_matches = False

    metadata_matches = title_matches and year_matches
    has_runtime = False
    record["research_verified_external_id"] = returned_id
    record["research_external_title"] = external_title or pd.NA
    record["research_external_year"] = external_year or pd.NA
    if api_type == "movie":
        runtime = details.get("runtime")
        if isinstance(runtime, int) and runtime > 0:
            record["research_movie_runtime_minutes"] = runtime
            has_runtime = True
    else:
        episode_runtimes = details.get("episode_run_time") or []
        valid_runtimes = sorted(
            {
                int(value)
                for value in episode_runtimes
                if isinstance(value, (int, float)) and value > 0
            }
        )
        if valid_runtimes:
            record["research_episode_runtime_minutes"] = json.dumps(
                valid_runtimes, ensure_ascii=False
            )
            has_runtime = True
        record["research_episode_count"] = details.get("number_of_episodes", pd.NA)
        record["research_season_count"] = details.get("number_of_seasons", pd.NA)

    if metadata_matches and has_runtime:
        record["research_status"] = "verified"
        record["research_confidence"] = "Alta: ID, título y año coinciden"
    elif metadata_matches:
        record["research_status"] = "verified_no_runtime"
        record["research_confidence"] = "Alta: ID, título y año coinciden"
        record["research_notes"] = "La ficha no informa una duración utilizable."
    else:
        record["research_status"] = "verified_metadata_difference"
        record["research_confidence"] = "Alta para el ID; metadatos por revisar"
        differences = []
        if not title_matches:
            differences.append("el título difiere")
        if external_year and not year_matches:
            differences.append("el año difiere")
        elif not external_year:
            differences.append("TMDB no informa el año")
        record["research_notes"] = (
            "ID TMDB validado, pero " + " y ".join(differences) + "."
        )
    return record


def load_catalog_rows() -> list[tuple[str, str, str, pd.DataFrame]]:
    frames = []
    for source_type, filename, api_type in SOURCES:
        path = DATA_DIR / filename
        if not path.is_file():
            raise FileNotFoundError(f"No se encontró la fuente requerida: {path}")
        frame = pd.read_csv(path)
        required = {"show_id", "title", "release_year"}
        missing = required.difference(frame.columns)
        if missing:
            raise ValueError(
                f"Faltan columnas en {filename}: {', '.join(sorted(missing))}"
            )
        if frame["show_id"].isna().any():
            raise ValueError(f"{filename} contiene show_id vacío.")
        frame["show_id"] = pd.to_numeric(frame["show_id"], errors="raise").astype(int)
        frame["research_row_key"] = [
            make_row_key(source_type, row_number, row)
            for row_number, (_, row) in enumerate(frame.iterrows(), start=1)
        ]
        frame["research_source_type"] = source_type
        frames.append((source_type, api_type, frame))
    return frames


def write_partial(rows: list[dict[str, Any]]) -> None:
    if rows:
        pd.DataFrame(rows).to_csv(PARTIAL_FILE, index=False, encoding="utf-8-sig")


def run_enrichment(limit: int | None = None) -> None:
    token = os.environ.get("TMDB_API_READ_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "Falta TMDB_API_READ_ACCESS_TOKEN. Obtén un token de lectura en "
            "https://www.themoviedb.org/settings/api y configúralo solo en el "
            "entorno local; no lo pegues en el código ni lo subas a Git."
        )

    sources = load_catalog_rows()
    all_source_rows = sum(len(frame) for _, _, frame in sources)
    existing: dict[str, dict[str, Any]] = {}
    resume_file = PARTIAL_FILE if PARTIAL_FILE.is_file() else OUTPUT_FILE
    if resume_file.is_file():
        previous = pd.read_csv(resume_file, dtype={"research_row_key": str})
        if "research_row_key" not in previous or "research_status" not in previous:
            raise ValueError(f"El archivo de progreso no es válido: {resume_file}")
        existing = {
            str(row["research_row_key"]): row.to_dict()
            for _, row in previous.iterrows()
        }

    expected_keys = {
        str(row["research_row_key"])
        for _, _, frame in sources
        for _, row in frame.iterrows()
    }
    result_by_key = {
        key: record for key, record in existing.items() if key in expected_keys
    }
    processed_this_run = 0
    pending = [
        (source_type, api_type, row_number, row)
        for source_type, api_type, frame in sources
        for row_number, (_, row) in enumerate(frame.iterrows(), start=1)
        if str(row["research_row_key"]) not in result_by_key
        or str(result_by_key[str(row["research_row_key"])]["research_status"])
        not in TERMINAL_STATUSES
    ]

    for source_type, api_type, row_number, source_row in pending:
        if limit is not None and processed_this_run >= limit:
            break
        external_id = int(source_row["show_id"])
        details = request_details(api_type, external_id, token)
        result = build_research_record(
            source_row, source_type, api_type, row_number, details
        )
        result_by_key[result["research_row_key"]] = result
        processed_this_run += 1
        if processed_this_run % 25 == 0:
            write_partial(list(result_by_key.values()))
            print(
                f"Consultados {processed_this_run} registros en esta ejecución; "
                f"{len(result_by_key)} con estado guardado.",
                flush=True,
            )
        time.sleep(0.25)

    write_partial(list(result_by_key.values()))
    if limit is not None and (processed_this_run < len(pending)):
        print(
            f"Prueba limitada: se consultaron {processed_this_run} registros. "
            f"El progreso quedó en {PARTIAL_FILE}; no se publica como dataset final.",
            flush=True,
        )
        return
    if len(result_by_key) != all_source_rows:
        raise RuntimeError(
            f"El enriquecimiento está incompleto: {len(result_by_key)} de "
            f"{all_source_rows} filas guardadas en {PARTIAL_FILE}."
        )

    enriched = []
    for source_type, _, source_frame in sources:
        additions = pd.DataFrame(
            [
                result_by_key[str(row_key)]
                for row_key in source_frame["research_row_key"]
            ]
        )
        enriched.append(
            pd.concat(
                [
                    source_frame.drop(columns="research_row_key").reset_index(drop=True),
                    additions.drop(
                        columns=["research_source_type", "research_source_row"],
                        errors="ignore",
                    ).reset_index(drop=True),
                ],
                axis=1,
            )
        )
    output = pd.concat(enriched, ignore_index=True, sort=False)
    output.to_csv(PARTIAL_FILE, index=False, encoding="utf-8-sig")
    os.replace(PARTIAL_FILE, OUTPUT_FILE)
    print(
        f"Enriquecimiento completo: {OUTPUT_FILE} "
        f"({len(output)} filas; original sin modificar).",
        flush=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Consulta metadatos de runtime del API oficial de TMDB mediante los "
            "identificadores existentes en los CSV."
        )
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limita las consultas para una prueba local; no genera el CSV final.",
    )
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit debe ser un entero positivo.")
    try:
        run_enrichment(args.limit)
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
