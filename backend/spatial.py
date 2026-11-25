"""Read-only Hyderabad/Telangana spatial API backed by the imported public GIS tables."""
from __future__ import annotations

import json
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
            detail="Spatial database is not configured. Set DATABASE_URL in the SolAI API deployment.",
        )
    try:
        return psycopg.connect(database_url, connect_timeout=5, row_factory=dict_row)
    except Exception as exc:
        # Do not expose connection strings or credentials in API errors.
        raise HTTPException(status_code=503, detail="Spatial database connection failed.") from exc


@router.get("/health")
def spatial_health():
    """Check PostGIS connectivity and report imported layer counts."""
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT PostGIS_Version() AS postgis_version")
                version = cur.fetchone()["postgis_version"]
                counts: dict[str, int] = {}
                for key, layer in LAYERS.items():
                    cur.execute(f'SELECT COUNT(*) AS n FROM public."{layer["table"]}"')
                    counts[key] = cur.fetchone()["n"]
        return {
            "status": "ok",
            "database": "connected",
            "postgis_version": version,
            "layers": counts,
            "total_features": sum(counts.values()),
            "crs": "EPSG:4326",
            "notice": "Counts reflect the imported public GIS tables; source completeness and utility status are not implied.",
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Spatial database health check failed; verify that all eight public GIS tables exist.") from exc


@router.get("/layers")
def list_spatial_layers():
    """Return layer metadata, row counts, geometry SRID and geometry type."""
    result = []
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                for key, layer in LAYERS.items():
                    table = layer["table"]
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
            "total_features": sum(item["feature_count"] for item in result),
            "notice": "Open-data screening layers only. They are not cadastral, statutory or utility-certified records.",
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Could not read spatial layer metadata; verify the imported table names and geom columns.") from exc


@router.get("/nearby")
def nearby_features(
    lat: float = Query(..., ge=15.0, le=20.5),
    lon: float = Query(..., ge=77.0, le=82.0),
    radius_m: int = Query(2000, ge=50, le=50000),
    layers: str = Query("all", description="Comma-separated layer IDs or 'all'."),
    limit: int = Query(100, ge=1, le=500),
):
    """Return nearby GIS features as GeoJSON, ordered by straight-line distance."""
    requested = list(LAYERS) if layers.strip().lower() == "all" else [
        item.strip() for item in layers.split(",") if item.strip()
    ]
    if not requested or any(item not in LAYERS for item in requested):
        raise HTTPException(
            status_code=422,
            detail={"message": "Unknown layer selection.", "available_layers": list(LAYERS)},
        )

    per_layer_limit = max(1, min(limit, 500))
    features: list[dict[str, Any]] = []
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
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
                        (lon, lat, lon, lat, radius_m, per_layer_limit),
                    )
                    for row in cur.fetchall():
                        geometry = row["geometry"]
                        properties = row["properties"] or {}
                        features.append({
                            "type": "Feature",
                            "id": f"{key}.{row['gid']}",
                            "geometry": geometry,
                            "properties": {
                                **properties,
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
        raise HTTPException(status_code=503, detail="Spatial query failed; verify PostGIS geography support and imported layer schemas.") from exc
