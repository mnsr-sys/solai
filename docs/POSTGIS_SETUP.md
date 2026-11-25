# PostGIS setup and GIS ingestion

This is the first durable spatial-data foundation for Reker SolAI. It is designed for Telangana-wide district expansion while preserving the original Hyderabad-area extracts as the first coverage package.

## 1. Database

Provision a managed PostgreSQL instance with the PostGIS extension enabled. Keep credentials in the hosting provider's environment variables; never commit a database URL or password.

Apply the schema:

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f database/migrations/001_postgis_foundation.sql
```

The migration creates the `solai` schema and source registry, source-preserving vector feature store, substations, candidate sites, solar projects, meter readings and audit events. Spatial indexes are created for geometry columns. The metadata seed records the re-extracted Hyderabad coverage and feature counts, explicitly marked `binary_imported=false`; it is not a claim that the actual GIS features are already in PostGIS.

## 2. GIS file ingestion

Download the TerraLab GeoPackage extracts from the download cards shown with the extraction results, then import them from a trusted workstation or controlled ingestion job. Install GDAL/OGR with PostgreSQL support. Use a least-privilege database role restricted to the ingestion schema.

Example (GeoPackage may contain several named layers; inspect first):

```bash
ogrinfo -so -al hyderabad-land-water.gpkg
psql "$DATABASE_URL" -c "CREATE SCHEMA IF NOT EXISTS solai_staging;"
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f database/seeds/001_hyderabad_extract_metadata.sql
ogr2ogr -f PostgreSQL "PG:$DATABASE_URL" hyderabad-land-water.gpkg \
  -nln solai_staging.landuse -lco SCHEMA=solai_staging \
  -lco GEOMETRY_NAME=geom -lco FID=source_feature_id
```

Repeat for each layer, using a stable table name and preserving the source attributes. Import into a staging schema first. Validate SRID, geometry type, feature count, null/empty geometry, duplicate source IDs and spatial extent before promoting to `solai.spatial_features`. Record each source file's release, retrieval time, licence, attribution, extent and SHA-256 checksum in `solai.source_datasets`.

Do not use `-overwrite` on production tables. Use a new dataset/version record and a controlled upsert so historical vintages remain reproducible.

## 3. Initial Hyderabad-area coverage re-extracted 25 November 2026

The current TerraLab extraction run returned the following counts (not a completeness claim):

| Layer | Features | Extent |
|---|---:|---|
| Land use | 2,893 | 15 km radius (~900 km²) |
| Waterways | 309 | 15 km radius (~900 km²) |
| Water areas | 343 | 15 km radius (~900 km²) |
| Protected areas | 5 | 15 km radius (~900 km²) |
| Roads | 16,172 | 2.5 km radius (~25 km²) |
| OSM power features | 2,889 | 20 km radius (~1,600 km²) |

The power extract includes 171 features tagged `power=substation`, alongside towers, lines, generators, transformers and other power features. These are OpenStreetMap map records, **not a utility-verified substation inventory**. The TGRAC ArcGIS public substation layer remains a separate source and should be imported separately with its own provenance.

The land/water/protected layers are from OpenStreetMap planet 2026-11-16 (ODbL 1.0). Roads are from Overture Maps 2026-11-18 (TerraLab reports ODbL 1.0; attribution includes OpenStreetMap contributors, Overture Maps Foundation and TomTom). Retain the licence and attribution supplied with each download.

The earlier register's Copernicus DEM GLO-30 extraction remains a separate raster ingest task. Do not force rasters into the vector feature table; use a raster-capable PostGIS workflow or object storage with a COG catalogue and derived slope/aspect products.

## 4. Source confidence and screening boundaries

- TGRAC published point records: public reference; not automatically utility-confirmed.
- OSM power=substation: open-map reference; not a certified inventory.
- Land use/water/roads: contextual screening layers, not title, right-of-way or statutory records.
- Five mapped protected-area features are not enough for statutory exclusions. Add authoritative forest, wildlife, wetlands, eco-sensitive zone and flood layers.
- Nearest-substation distance is straight-line proximity only. Do not infer feeder connection, spare hosting capacity, transformer headroom or evacuation cost without authorised TSTRANSCO/DISCOM data.

## 5. Candidate-site scoring

Only score a candidate polygon after its geometry and source lineage are present. Keep the scoring version and all component metrics. Initial factors may include usable land, land-cover exclusions, slope, water/flood exposure, shading, solar resource and straight-line substation distance. Missing evidence must reduce confidence or block a score; do not silently substitute synthetic values.

## 6. Next implementation sequence

1. Provision managed PostGIS and set `DATABASE_URL` in the API environment.
2. Import the GeoPackages into a staging schema and validate counts/extents.
3. Import TGRAC substation points as a separate provenance class; retain original attributes.
4. Add official TSTRANSCO/DISCOM feeder, transformer and load data only with authorised access.
5. Add Sentinel-2 land-cover classification and authoritative constraint layers district by district.
6. Build GIS-derived candidate polygons and scoring from imported geometry.
7. Connect the production API to PostGIS; retire in-memory project/meter persistence only after migration and backup tests.
8. Keep generation monitoring and carbon MRV downstream of the selected, developed project.

**Current boundary:** this repository now contains the schema and ingestion procedure, not the downloaded GeoPackage binaries or a live database connection. The extracts are generated in TerraLab and presented as download files; the binary files must be downloaded and imported into the provisioned database before the map can claim to render those layers from PostGIS.
