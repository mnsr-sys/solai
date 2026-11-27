"""Read-only Hyderabad/Telangana spatial API backed by imported public GIS tables."""
from __future__ import annotations

import os
from typing import Any

import psycopg
from psycopg.rows import dict_row
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/v1/spatial", tags=["spatial"])

# Strict allow-list: request values are never interpolated as SQL identifiers.
LAYERS: dict[str, dict[str, str]] = {
    "landuse": {"table": "landuse", "label": "Land use", "geometry": "MultiPolygon"},
    "waterways": {"table": "waterways", "label": "Waterways", "geometry": "LineString"},
    "water_areas": {"table": "water_areas", "label": "Water areas", "geometry": "MultiPolygon"},
    "protected_areas": {"table": "protected_areas", "label": "Protected areas", "geometry": "MultiPolygon"},
    "roads_hyderabad": {"table": "roads_hyderabad", "label": "Roads", "geometry": "LineString"},
    "power_hyderabad_polygons": {"table": "power_hyderabad_polygons", "label": "Power infrastructure polygons", "geometry": "MultiPolygon"},
    "power_hyderabad_points": {"table": "power_hyderabad_points", "label": "Power infrastructure points", "geometry": "Point"},
    "power_hyderabad_lines": {"table": "power_hyderabad_lines", "label": "Power infrastructure lines", "geometry": "LineString"},
}


def _connect():
    database_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
    if not database_url:
        raise HTTPException(
            status_code=503,
            detail="Spatial database is not configured. Set DATABASE_URL in the SolAI deployment.",
        )
    try:
        return psycopg.connect(database_url, connect_timeout=5, row_factory=dict_row)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Spatial database connection failed.") from exc


def _existing_tables(cur) -> set[str]:
    cur.execute(
        "SELECT tablename FROM pg_catalog.pg_tables "
        "WHERE schemaname = 'public' AND tablename = ANY(%s)",
        ([layer["table"] for layer in LAYERS.values()],),
    )
    return {row["tablename"] for row in cur.fetchall()}


@router.get("/health")
def spatial_health():
    """Check PostGIS connectivity and report counts for tables that are present."""
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT PostGIS_Version() AS postgis_version")
                version = cur.fetchone()["postgis_version"]
                existing = _existing_tables(cur)
                counts: dict[str, int] = {}
                for key, layer in LAYERS.items():
                    if layer["table"] not in existing:
                        continue
                    cur.execute(f'SELECT COUNT(*) AS n FROM public."{layer["table"]}"')
                    counts[key] = cur.fetchone()["n"]
        missing = [key for key, layer in LAYERS.items() if layer["table"] not in existing]
        return {
            "status": "ok" if not missing else "degraded",
            "database": "connected",
            "postgis_version": version,
            "layers": counts,
            "missing_layers": missing,
            "total_features": sum(counts.values()),
            "crs": "EPSG:4326",
            "notice": "Only existing imported tables are counted. Missing layers are reported separately; source completeness and utility status are not implied.",
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Spatial database health check failed; verify PostGIS is enabled and imported tables have the expected schema.",
        ) from exc


@router.get("/layers")
def list_spatial_layers():
    """Return metadata only for imported tables, including data-quality indicators."""
    result = []
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                existing = _existing_tables(cur)
                for key, layer in LAYERS.items():
                    table = layer["table"]
                    if table not in existing:
                        continue
                    cur.execute(
                        f"""
                        SELECT COUNT(*) AS feature_count,
                               COUNT(*) FILTER (WHERE geom IS NULL) AS null_geometries,
                               COUNT(DISTINCT ST_SRID(geom)) AS srid_count,
                               MIN(ST_SRID(geom)) AS srid,
                               COUNT(*) FILTER (WHERE NOT ST_IsValid(geom)) AS invalid_geometries
                        FROM public."{table}"
                        """
                    )
                    stats = cur.fetchone()
                    result.append({
                        "id": key,
                        "table": table,
                        "label": layer["label"],
                        "expected_geometry": layer["geometry"],
                        **stats,
                    })
        return {
            "city": "Hyderabad",
            "state": "Telangana",
            "crs": "EPSG:4326",
            "layers": result,
            "missing_layers": [key for key, layer in LAYERS.items() if layer["table"] not in existing],
            "total_features": sum(item["feature_count"] for item in result),
            "notice": "Only imported public GIS layers are listed. They are not cadastral, statutory or utility-certified records.",
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Could not read spatial layer metadata; verify imported table names, geom columns and PostGIS functions.",
        ) from exc


@router.get("/nearby")
def nearby_features(
    lat: float = Query(..., ge=15.0, le=20.5),
    lon: float = Query(..., ge=77.0, le=82.0),
    radius_m: int = Query(2000, ge=50, le=50000),
    layers: str = Query("all", description="Comma-separated layer IDs or 'all'."),
    limit: int = Query(100, ge=1, le=500),
):
    """Return nearby imported GIS features as GeoJSON, ordered by straight-line distance."""
    requested = list(LAYERS) if layers.strip().lower() == "all" else [
        item.strip() for item in layers.split(",") if item.strip()
    ]
    if not requested or any(item not in LAYERS for item in requested):
        raise HTTPException(
            status_code=422,
            detail={"message": "Unknown layer selection.", "available_layers": list(LAYERS)},
        )

    features: list[dict[str, Any]] = []
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                existing = _existing_tables(cur)
                missing = [key for key in requested if LAYERS[key]["table"] not in existing]
                if missing:
                    raise HTTPException(
                        status_code=404,
                        detail={"message": "Selected GIS layer is not imported.", "missing_layers": missing},
                    )
                for key in requested:
                    table = LAYERS[key]["table"]
                    cur.execute(
                        f"""
                        SELECT gid,
                               (to_jsonb(f) - 'geom') AS properties,
                               ST_AsGeoJSON(f.geom)::jsonb AS geometry,
                               ST_Distance(
                                   f.geom::geography,
                                   ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
                               ) AS distance_m
                        FROM public."{table}" AS f
                        WHERE f.geom IS NOT NULL
                          AND ST_DWithin(
                              f.geom::geography,
                              ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                              %s
                          )
                        ORDER BY distance_m
                        LIMIT %s
                        """,
                        (lon, lat, lon, lat, radius_m, limit),
                    )
                    for row in cur.fetchall():
                        features.append({
                            "type": "Feature",
                            "id": f"{key}.{row['gid']}",
                            "geometry": row["geometry"],
                            "properties": {
                                **(row["properties"] or {}),
                                "layer": key,
                                "distance_m": round(float(row["distance_m"]), 1),
                            },
                        })

        features.sort(key=lambda feature: feature["properties"]["distance_m"])
        features = features[:limit]
        return {
            "type": "FeatureCollection",
            "query": {"lat": lat, "lon": lon, "radius_m": radius_m, "layers": requested},
            "numberReturned": len(features),
            "features": features,
            "notice": "Distances are straight-line proximity only. They do not establish road travel time, land rights, statutory clearance, electrical connection or grid hosting capacity.",
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Spatial query failed; verify PostGIS geography support and imported layer schemas.",
        ) from exc
