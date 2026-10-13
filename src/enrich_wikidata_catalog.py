"""Enrich catalog records with duration claims linked by exact TMDB ID in Wikidata."""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "research_wikidata_enrichment.csv"
PARTIAL_FILE = DATA_DIR / "research_wikidata_enrichment.partial.csv"
SOURCES = [
    ("Movie", "netflix_movies_detailed_up_to_2025.csv", "P4947"),
    ("TV Show", "netflix_tv_shows_detailed_up_to_2025.csv", "P4983"),
]
SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
WIKIDATA_ROOT = "https://www.wikidata.org/wiki/"
ENTITY_BATCH_SIZE = 50
PIPELINE_VERSION = 5
TERMINAL_STATUSES = {
    "verified",
    "verified_metadata_difference",
    "verified_no_runtime",
    "multiple_runtime_values",
    "unsupported_unit",
    "ambiguous_external_id",
    "not_found",
    "query_incomplete",
}
UNIT_TO_MINUTES = {
    "Q7727": 1.0,
    "Q11574": 1.0 / 60.0,
    "Q25235": 60.0,
}


def normalize_title(value: Any) -> str:
    if pd.isna(value):
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(character for character in text if not unicodedata.combining(character))
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


def make_row_key(
    source_type: str, source_row_number: int, source_row: pd.Series
) -> str:
    title = "" if pd.isna(source_row["title"]) else str(source_row["title"]).strip()
    return (
        f"{source_type}:{source_row_number}:{int(source_row['show_id'])}:"
        f"{source_row['release_year']}:{title.casefold()}"
    )


def load_catalog_rows() -> list[tuple[str, str, pd.DataFrame]]:
    sources = []
    for source_type, filename, property_id in SOURCES:
        path = DATA_DIR / filename
        if not path.is_file():
            raise FileNotFoundError(f"No se encontró el archivo de origen: {path}")
        frame = pd.read_csv(path)
        required = {"show_id", "title", "release_year"}
        missing = required.difference(frame.columns)
        if missing:
            raise ValueError(
                f"Faltan columnas en {filename}: {', '.join(sorted(missing))}"
            )
        numeric_ids = pd.to_numeric(frame["show_id"], errors="raise")
        if numeric_ids.isna().any() or (numeric_ids <= 0).any():
            raise ValueError(f"{filename} contiene show_id vacío o no positivo.")
        if ((numeric_ids % 1) != 0).any():
            raise ValueError(f"{filename} contiene show_id que no es entero.")
        frame["show_id"] = numeric_ids.astype("int64")
        frame["research_tmdb_id"] = frame["show_id"].astype(str)
        frame["research_source_type"] = source_type
        frame["research_source_row"] = range(1, len(frame) + 1)
        frame["research_row_key"] = [
            make_row_key(source_type, row_number, row)
            for row_number, (_, row) in enumerate(frame.iterrows(), start=1)
        ]
        sources.append((source_type, property_id, frame))
    return sources


def build_query(property_id: str, external_ids: list[str] | None) -> str:
    values_clause = ""
    if external_ids is not None:
        values = " ".join(f'"{int(external_id)}"' for external_id in external_ids)
        values_clause = f"VALUES ?tmdb {{ {values} }}"
    return f"""
SELECT ?tmdb ?item ?duration ?unit WHERE {{
  {values_clause}
  ?item wdt:{property_id} ?tmdb; wdt:P2047 ?duration; p:P2047 ?statement.
  ?statement ps:P2047 ?duration; psv:P2047 ?quantity.
  OPTIONAL {{ ?quantity wikibase:quantityUnit ?unit. }}
}}
"""


def request_runtime_rows(
    property_id: str, external_ids: list[str] | None
) -> tuple[list[dict[str, str]], bool]:
    query = build_query(property_id, external_ids)
    url = f"{SPARQL_ENDPOINT}?{urlencode({'query': query})}"
    request = Request(
        url,
        headers={
            "Accept": "text/csv",
            "User-Agent": (
                "StreamViewAnalytics/1.0 "
                "(academic research; github.com/Paladynamo/STREAMVIEW-ANALYTICS)"
            ),
        },
    )
    for attempt in range(5):
        try:
            with urlopen(request, timeout=60) as response:
                content = response.read().decode("utf-8")
            raw_rows = list(csv.DictReader(io.StringIO(content)))
            valid_rows = []
            incomplete = "SPARQL-QUERY:" in content
            for row in raw_rows:
                if (
                    not re.fullmatch(r"\d+", row.get("tmdb") or "")
                    or not re.fullmatch(
                        r"https?://www\.wikidata\.org/entity/Q\d+",
                        row.get("item") or "",
                    )
                ):
                    incomplete = True
                    continue
                valid_rows.append(row)
            return valid_rows, incomplete
        except HTTPError as error:
            if error.code == 429 or 500 <= error.code < 600:
                if attempt < 4:
                    retry_after = error.headers.get("Retry-After")
                    try:
                        delay = float(retry_after) if retry_after else 2**attempt
                    except ValueError:
                        delay = 2**attempt
                    time.sleep(min(delay, 60))
                    continue
            raise RuntimeError(
                f"Wikidata respondió HTTP {error.code} al consultar duraciones."
            ) from error
        except (URLError, TimeoutError) as error:
            if attempt < 4:
                time.sleep(2**attempt)
                continue
            raise RuntimeError(
                "No se pudo consultar Wikidata tras cinco intentos."
            ) from error
        except UnicodeDecodeError as error:
            raise RuntimeError("Wikidata devolvió una respuesta que no es UTF-8.") from error
    raise RuntimeError("Se agotaron los reintentos de consulta a Wikidata.")


def request_entities(qids: list[str]) -> dict[str, dict[str, Any]]:
    entities: dict[str, dict[str, Any]] = {}
    for offset in range(0, len(qids), ENTITY_BATCH_SIZE):
        batch = qids[offset : offset + ENTITY_BATCH_SIZE]
        parameters = {
            "action": "wbgetentities",
            "ids": "|".join(batch),
            "props": "labels|claims",
            "languages": "en",
            "format": "json",
            "maxlag": "5",
        }
        url = f"{WIKIDATA_API}?{urlencode(parameters)}"
        request = Request(
            url,
            headers={
                "User-Agent": (
                    "StreamViewAnalytics/1.0 "
                    "(academic research; github.com/Paladynamo/STREAMVIEW-ANALYTICS)"
                )
            },
        )
        for attempt in range(5):
            try:
                with urlopen(request, timeout=60) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                batch_entities = payload.get("entities")
                if not isinstance(batch_entities, dict):
                    raise RuntimeError("Wikidata devolvió entidades en formato inesperado.")
                entities.update(batch_entities)
                break
            except HTTPError as error:
                if error.code == 429 or 500 <= error.code < 600:
                    if attempt < 4:
                        retry_after = error.headers.get("Retry-After")
                        try:
                            delay = float(retry_after) if retry_after else 2**attempt
                        except ValueError:
                            delay = 2**attempt
                        time.sleep(min(delay, 60))
                        continue
                raise RuntimeError(
                    f"Wikidata respondió HTTP {error.code} al consultar entidades."
                ) from error
            except (URLError, TimeoutError) as error:
                if attempt < 4:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(
                    "No se pudieron consultar entidades de Wikidata tras cinco intentos."
                ) from error
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise RuntimeError(
                    "Wikidata devolvió JSON inválido al consultar entidades."
                ) from error
        time.sleep(0.25)
    return entities


def parse_number(value: str | None) -> float | None:
    if not value:
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def qid_from_uri(value: str) -> str:
    return value.rsplit("/", 1)[-1]


def normalize_claims(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    claims = []
    seen = set()
    for row in rows:
        amount = parse_number(row.get("amount"))
        duration = parse_number(row.get("duration"))
        unit_uri = row.get("unit", "")
        unit_id = qid_from_uri(unit_uri) if unit_uri else ""
        factor = UNIT_TO_MINUTES.get(unit_id)
        lower = parse_number(row.get("lower"))
        upper = parse_number(row.get("upper"))
        claim = {
            "amount": amount,
            "unit_id": unit_id or None,
            "unit_uri": unit_uri or None,
            "statement_id": row.get("statement_id") or None,
            "rank": row.get("rank") or None,
            "qualifiers": (
                json.loads(row["qualifiers_json"])
                if row.get("qualifiers_json")
                else None
            ),
            "duration_minutes": (
                round(amount * factor, 3) if amount is not None and factor else None
            ),
            "lower_bound_minutes": (
                round(lower * factor, 3) if lower is not None and factor else None
            ),
            "upper_bound_minutes": (
                round(upper * factor, 3) if upper is not None and factor else None
            ),
        }
        if claim["duration_minutes"] is None and duration is not None and factor:
            claim["duration_minutes"] = round(duration * factor, 3)
        fingerprint = (
            claim["amount"],
            claim["unit_id"],
            claim["lower_bound_minutes"],
            claim["upper_bound_minutes"],
            claim["statement_id"],
        )
        if fingerprint not in seen:
            seen.add(fingerprint)
            claims.append(claim)
    return claims


def build_entity_rows(
    runtime_rows: list[dict[str, str]],
    entities: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, str]]]:
    results: dict[str, list[dict[str, str]]] = {}
    for runtime_row in runtime_rows:
        external_id = str(int(runtime_row["tmdb"]))
        qid = qid_from_uri(runtime_row["item"])
        entity = entities.get(qid)
        if entity is None:
            raise RuntimeError(f"Wikidata no devolvió el elemento solicitado {qid}.")
        label = entity.get("labels", {}).get("en", {}).get("value", "")
        statements = entity.get("claims", {}).get("P2047", [])
        active_statements = [
            statement for statement in statements
            if statement.get("rank") != "deprecated"
        ]
        preferred_statements = [
            statement for statement in active_statements
            if statement.get("rank") == "preferred"
        ]
        selected_statements = preferred_statements or active_statements
        claim_rows = []
        for statement in selected_statements:
            datavalue = (
                statement.get("mainsnak", {})
                .get("datavalue", {})
                .get("value", {})
            )
            if not isinstance(datavalue, dict) or "amount" not in datavalue:
                continue
            claim_rows.append(
                {
                    "tmdb": external_id,
                    "item": f"{WIKIDATA_ROOT}{qid}",
                    "label": label,
                    "duration": str(datavalue.get("amount", "")).lstrip("+"),
                    "amount": str(datavalue.get("amount", "")).lstrip("+"),
                    "unit": str(datavalue.get("unit", "")),
                    "lower": str(datavalue.get("lowerBound", "")).lstrip("+"),
                    "upper": str(datavalue.get("upperBound", "")).lstrip("+"),
                    "statement_id": str(statement.get("id", "")),
                    "rank": str(statement.get("rank", "")),
                    "qualifiers_json": json.dumps(
                        statement.get("qualifiers", {}),
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                }
            )
        if not claim_rows:
            claim_rows.append(
                {
                    "tmdb": external_id,
                    "item": f"{WIKIDATA_ROOT}{qid}",
                    "label": label,
                }
            )
        results.setdefault(external_id, []).extend(claim_rows)
    return results


def number_label(value: float) -> str:
    return f"{value:g}"


def build_research_record(
    source_row: pd.Series,
    source_type: str,
    external_id: str,
    rows: list[dict[str, str]],
    retrieved_at: str,
    query_complete: bool,
) -> dict[str, Any]:
    property_id = "P4947" if source_type == "Movie" else "P4983"
    entities: dict[str, dict[str, str]] = {}
    for row in rows:
        item_uri = row.get("item", "")
        if item_uri:
            entities[qid_from_uri(item_uri)] = row

    record: dict[str, Any] = {
        "research_pipeline_version": PIPELINE_VERSION,
        "research_query_complete": query_complete,
        "research_tmdb_id": external_id,
        "research_status": "",
        "research_confidence": "",
        "research_notes": "",
        "research_source": "Wikidata (datos estructurados CC0)",
        "research_source_property": property_id,
        "research_api_url": SPARQL_ENDPOINT,
        "research_title_url": "",
        "research_retrieved_at_utc": retrieved_at,
        "research_verified_external_id": "",
        "research_external_title": "",
        "research_duration_claims_json": "[]",
        "research_movie_runtime_minutes": pd.NA,
        "research_episode_runtime_minutes": "[]",
        "research_runtime_lower_bound_minutes": pd.NA,
        "research_runtime_upper_bound_minutes": pd.NA,
        "research_duration_display": "",
    }
    if not entities:
        if query_complete:
            record.update(
                research_status="not_found",
                research_confidence="Sin duración P2047 vinculada por ID exacto",
                research_notes=(
                    "No se halló una afirmación de duración P2047 asociada a este ID; "
                    "esto no demuestra que no exista una entidad Wikidata sin duración."
                ),
            )
        else:
            record.update(
                research_status="query_incomplete",
                research_confidence="Consulta incompleta; ausencia no confirmada",
                research_notes=(
                    "Wikidata devolvió una respuesta parcial/no interpretable; "
                    "no se puede concluir que este ID carezca de duración."
                ),
            )
        return record
    if len(entities) > 1:
        record.update(
            research_status="ambiguous_external_id",
            research_confidence="Ambiguo",
            research_external_title="; ".join(
                sorted({row.get("label", "") for row in entities.values() if row.get("label")})
            ),
            research_duration_claims_json=json.dumps(
                [
                    {
                        "wikidata_id": qid,
                        "wikidata_url": f"{WIKIDATA_ROOT}{qid}",
                        "english_label": entity.get("label") or None,
                    }
                    for qid, entity in sorted(entities.items())
                ],
                ensure_ascii=False,
            ),
            research_notes=(
                "El identificador se vincula a más de un elemento Wikidata; "
                "no se asigna ninguna duración."
            ),
        )
        return record

    qid, entity = next(iter(entities.items()))
    title = entity.get("label", "")
    title_matches = bool(title) and normalize_title(source_row["title"]) == normalize_title(title)
    claims = normalize_claims(
        [
            row
            for row in rows
            if row.get("item", "").rsplit("/", 1)[-1] == qid and row.get("amount")
        ]
    )
    record["research_verified_external_id"] = qid
    record["research_external_title"] = title
    record["research_title_url"] = f"{WIKIDATA_ROOT}{qid}"
    record["research_duration_claims_json"] = json.dumps(claims, ensure_ascii=False)

    usable_claims = [
        claim for claim in claims if claim["duration_minutes"] is not None
    ]
    unique_values = sorted({claim["duration_minutes"] for claim in usable_claims})
    lower_bounds = [
        claim["lower_bound_minutes"]
        for claim in usable_claims
        if claim["lower_bound_minutes"] is not None
    ]
    upper_bounds = [
        claim["upper_bound_minutes"]
        for claim in usable_claims
        if claim["upper_bound_minutes"] is not None
    ]
    if lower_bounds:
        record["research_runtime_lower_bound_minutes"] = min(lower_bounds)
    if upper_bounds:
        record["research_runtime_upper_bound_minutes"] = max(upper_bounds)
    if source_type == "Movie" and len(unique_values) == 1:
        record["research_movie_runtime_minutes"] = unique_values[0]
    elif source_type == "TV Show":
        record["research_episode_runtime_minutes"] = json.dumps(
            unique_values, ensure_ascii=False
        )

    duration_labels = []
    for claim in usable_claims:
        minutes = claim["duration_minutes"]
        label = f"{number_label(minutes)} min"
        lower = claim["lower_bound_minutes"]
        upper = claim["upper_bound_minutes"]
        if lower is not None or upper is not None:
            lower_label = number_label(lower) if lower is not None else "?"
            upper_label = number_label(upper) if upper is not None else "?"
            label += f" (rango {lower_label}–{upper_label})"
        duration_labels.append(label)
    if duration_labels and source_type == "TV Show":
        duration_labels = [f"{label}/episodio" for label in duration_labels]
    record["research_duration_display"] = "; ".join(sorted(set(duration_labels)))

    unsupported_claims = [
        claim for claim in claims if claim["duration_minutes"] is None
    ]
    if not claims:
        status = "verified_no_runtime"
        notes = "El elemento está enlazado, pero no informa duración P2047."
    elif unsupported_claims:
        status = "unsupported_unit"
        notes = (
            "Hay valores P2047 con unidades que no se pudieron convertir; "
            "se preservan junto con los valores convertibles."
        )
    elif len(unique_values) > 1:
        status = "multiple_runtime_values"
        notes = "Wikidata informa más de un valor de duración; se conservan por separado."
    else:
        status = "verified"
        notes = ""
    if not title_matches:
        status = "verified_metadata_difference"
        notes = (
            (notes + " " if notes else "")
            + (
                "El título de la etiqueta inglesa difiere del título del catálogo; "
                "revisar antes de utilizarlo."
                if title
                else "Wikidata no aporta una etiqueta inglesa para comparar el título."
            )
        )
    if title_matches:
        confidence = "Alta: ID externo y título normalizado coinciden"
    elif title:
        confidence = "ID enlazado; diferencia de título pendiente de revisión"
    else:
        confidence = "ID enlazado; Wikidata no aporta etiqueta inglesa"
    record.update(
        research_status=status,
        research_confidence=confidence,
        research_notes=notes,
    )
    return record


def initial_output_rows(
    sources: list[tuple[str, str, pd.DataFrame]],
) -> list[dict[str, Any]]:
    output = []
    for _, _, frame in sources:
        for _, row in frame.iterrows():
            record = row.to_dict()
            record.update(
                research_pipeline_version=PIPELINE_VERSION,
                research_query_complete=pd.NA,
                research_status="pending",
                research_confidence="No consultado",
                research_notes="Pendiente de consulta a Wikidata.",
                research_source="Wikidata (datos estructurados CC0)",
                research_source_property=(
                    "P4947" if row["type"] == "Movie" else "P4983"
                ),
                research_api_url=SPARQL_ENDPOINT,
                research_title_url="",
                research_retrieved_at_utc="",
                research_verified_external_id="",
                research_external_title="",
                research_duration_claims_json="[]",
                research_movie_runtime_minutes=pd.NA,
                research_episode_runtime_minutes="[]",
                research_runtime_lower_bound_minutes=pd.NA,
                research_runtime_upper_bound_minutes=pd.NA,
                research_duration_display="",
            )
            output.append(record)
    return output


def write_partial(rows: list[dict[str, Any]]) -> None:
    pd.DataFrame(rows).to_csv(PARTIAL_FILE, index=False, encoding="utf-8-sig")


def run_enrichment(limit: int | None = None) -> None:
    sources = load_catalog_rows()
    output_rows = initial_output_rows(sources)
    row_positions = {
        row["research_row_key"]: position for position, row in enumerate(output_rows)
    }
    resume_file = PARTIAL_FILE if PARTIAL_FILE.is_file() else OUTPUT_FILE
    if resume_file.is_file():
        previous = pd.read_csv(
            resume_file, dtype={"research_row_key": str}, low_memory=False
        )
        if {
            "research_row_key",
            "research_status",
            "research_pipeline_version",
        }.issubset(previous.columns):
            for _, previous_row in previous.iterrows():
                key = str(previous_row["research_row_key"])
                previous_version = str(previous_row["research_pipeline_version"])
                if (
                    key not in row_positions
                    or previous_version
                    not in {str(PIPELINE_VERSION), str(PIPELINE_VERSION - 1)}
                    or str(previous_row["research_status"]) not in TERMINAL_STATUSES
                ):
                    continue
                previous_record = previous_row.to_dict()
                if previous_version == str(PIPELINE_VERSION - 1):
                    if str(previous_row["research_status"]) == "not_found":
                        previous_record.update(
                            research_status="query_incomplete",
                            research_confidence=(
                                "Consulta global no exhaustiva; ausencia no confirmada"
                            ),
                            research_notes=(
                                "La extracción global no puede demostrar que no haya "
                                "una afirmación P2047 asociada a este ID; requiere "
                                "una consulta exacta."
                            ),
                        )
                    previous_record["research_query_complete"] = False
                previous_record["research_pipeline_version"] = PIPELINE_VERSION
                output_rows[row_positions[key]].update(previous_record)

    retrieved_at = datetime.now(timezone.utc).isoformat()
    write_partial(output_rows)
    processed = 0
    for source_type, property_id, frame in sources:
        source_rows = [
            row for _, row in frame.iterrows()
            if output_rows[row_positions[row["research_row_key"]]]["research_status"]
            not in TERMINAL_STATUSES
        ]
        source_rows_by_id: dict[str, list[pd.Series]] = {}
        for row in source_rows:
            external_id = str(int(row["show_id"]))
            source_rows_by_id.setdefault(external_id, []).append(row)
        ids = list(dict.fromkeys(str(int(row["show_id"])) for row in source_rows))
        if limit is not None:
            ids = ids[:limit]
        if not ids:
            continue
        response_rows, query_complete = request_runtime_rows(
            property_id,
            ids if limit is not None else None,
        )
        if limit is None:
            query_complete = False
        relevant_rows = [
            result
            for result in response_rows
            if str(int(result["tmdb"])) in source_rows_by_id
            and result.get("item", "").startswith(
                "http://www.wikidata.org/entity/"
            )
        ]
        qids = list(
            dict.fromkeys(qid_from_uri(row["item"]) for row in relevant_rows)
        )
        entity_payloads = request_entities(qids)
        claims_by_id = build_entity_rows(relevant_rows, entity_payloads)
        for external_id in ids:
            for row in source_rows_by_id[external_id]:
                additions = build_research_record(
                    row,
                    source_type,
                    external_id,
                    claims_by_id.get(external_id, []),
                    retrieved_at,
                    query_complete,
                )
                additions["research_row_key"] = row["research_row_key"]
                output_rows[row_positions[row["research_row_key"]]].update(additions)
        processed += len(ids)
        write_partial(output_rows)
        if not query_complete:
            print(
                f"Advertencia: Wikidata devolvió resultados parciales para "
                f"{source_type}; los IDs sin resultado quedaron como "
                "'query_incomplete', no como ausentes.",
                flush=True,
            )
        print(
            f"Consultados {processed} identificadores únicos en esta ejecución; "
            f"{sum(row['research_status'] in TERMINAL_STATUSES for row in output_rows)} "
            "registros con estado guardado.",
            flush=True,
        )

    pending_count = sum(
        row["research_status"] not in TERMINAL_STATUSES for row in output_rows
    )
    if pending_count:
        write_partial(output_rows)
        print(
            f"Ejecución limitada/incompleta: quedan {pending_count} registros "
            f"pendientes. El progreso está en {PARTIAL_FILE}; no se publica como final.",
            flush=True,
        )
        return

    output = pd.DataFrame(output_rows)
    output.to_csv(PARTIAL_FILE, index=False, encoding="utf-8-sig")
    PARTIAL_FILE.replace(OUTPUT_FILE)
    status_counts = output["research_status"].value_counts().to_dict()
    print(
        f"Enriquecimiento completo: {OUTPUT_FILE} "
        f"({len(output)} filas; estados: {status_counts}; originales sin modificar).",
        flush=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Enriquece los catálogos con duraciones P2047 de Wikidata, "
            "mediante los IDs externos ya presentes en los CSV."
        )
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limita los IDs consultados para una prueba; no publica el CSV final.",
    )
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit debe ser un entero positivo.")
    try:
        run_enrichment(args.limit)
    except (FileNotFoundError, ValueError, RuntimeError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
