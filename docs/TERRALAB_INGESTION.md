# TerraLab GIS ingestion — Hyderabad pilot

This runbook imports the TerraLab vector extracts into the five public PostGIS tables queried by `backend/spatial.py`. It does not upload files to Vercel and does not claim the data are statewide or authoritative.

## Source extracts

- Combined GeoPackage: landuse, waterways, water_areas, protected_areas; Hyderabad centre 17.360588 N, 78.474061 E; 15 km radius.
- Roads GeoPackage: same centre; 2.5 km radius.
- Sources: OpenStreetMap planet 2026-11-16 for land/water/protected layers; Overture Maps 2026-11-18 for roads, via TerraLab.
- Licence/attribution: ODbL 1.0. Retain © OpenStreetMap contributors; modified by TerraLab. Roads attribution also includes Overture Maps Foundation and TomTom. A database published from OSM-derived data must remain under ODbL.

Download the GeoPackages from the TerraLab extraction result shown in the ChatGPT conversation and place them on a machine with network access to the managed PostGIS instance. Do not commit raw extracts or database credentials to Git.

## Prerequisites

- PostgreSQL with PostGIS enabled.
- GDAL/OGR command-line tools (`ogrinfo`, `ogr2ogr`) and `psql`.
- A database role allowed to create/replace the target public tables and indexes.
- The existing `DATABASE_URL` secret, supplied only through the shell environment or a secure secret manager.

## Import

First inspect layer names:

```bash
ogrinfo -ro -so "$CONTEXT_GPKG"
ogrinfo -ro -so "$ROADS_GPKG"
```

Then run:

```bash
export DATABASE_URL='postgresql://…'
export CONTEXT_GPKG='/secure/path/landuse-waterways-water_areas-protected_areas-extract.gpkg'
export ROADS_GPKG='/secure/path/roads-extract.gpkg'
bash scripts/import_terralab_gpkg.sh
```

The script expects GeoPackage layer names `landuse`, `waterways`, `water_areas`, `protected_areas`, and `roads`. If `ogrinfo` reports different names, change the source layer argument in the script to the exact reported name. It writes the table names expected by the current spatial API: `public.landuse`, `public.waterways`, `public.water_areas`, `public.protected_areas`, `public.roads_hyderabad`.

The script uses `-overwrite`: it replaces these five pilot tables. Run it only against the intended SolAI PostGIS database.

## Verify

```bash
curl -fsS "$SOLAI_API_URL/api/v1/spatial/health"
curl -fsS "$SOLAI_API_URL/api/v1/spatial/layers"
```

Expected extraction counts from the recorded source run: landuse 2,893; waterways 309; water_areas 343; protected_areas 5; roads 16,172. Counts can vary if a new extraction is generated. The API's nearby endpoint returns at most 500 features per request, so the dashboard shows a local context sample around the current map centre, not the entire dataset.

## Important limitations

- The initial extracts cover Hyderabad only; roads cover a smaller radius than the other four layers.
- OpenStreetMap/Overture mapping is incomplete. Missing mapped features do not prove absence on the ground.
- The five mapped protected-area features are not sufficient for statutory exclusion screening.
- Land-use tags are not parcel ownership, title or statutory zoning.
- Roads are proximity context, not surveyed access or transmission right-of-way.
- A mapped power feature is not utility-confirmed and does not establish voltage, feeder connectivity or hosting capacity.
- Preserve the original source, release, feature IDs, retrieval date, licence, attribution and raw attributes.
