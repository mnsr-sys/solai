#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_URL:?Set DATABASE_URL to the managed PostGIS connection string}"
: "${CONTEXT_GPKG:?Set CONTEXT_GPKG to the TerraLab combined GeoPackage path}"
: "${ROADS_GPKG:?Set ROADS_GPKG to the TerraLab roads GeoPackage path}"

echo "Inspecting TerraLab GeoPackage layers. Confirm names before import:"
ogrinfo -ro -so "$CONTEXT_GPKG"
ogrinfo -ro -so "$ROADS_GPKG"

# TerraLab theme layer names are expected to be landuse, waterways,
# water_areas and protected_areas. Confirm with ogrinfo above.
for layer in landuse waterways water_areas protected_areas; do
  echo "Importing $layer..."
  ogr2ogr -f PostgreSQL "$DATABASE_URL" "$CONTEXT_GPKG" "$layer" \
    -nln "public.$layer" -lco GEOMETRY_NAME=geom -lco FID=gid \
    -t_srs EPSG:4326 -overwrite -progress
done

# Roads are kept in their own, smaller extract and mapped to the API's
# existing table name roads_hyderabad.
echo "Importing roads..."
ogr2ogr -f PostgreSQL "$DATABASE_URL" "$ROADS_GPKG" roads \
  -nln public.roads_hyderabad -lco GEOMETRY_NAME=geom -lco FID=gid \
  -t_srs EPSG:4326 -overwrite -progress

psql "$DATABASE_URL" -v ON_ERROR_STOP=1 <<'SQL'
CREATE INDEX IF NOT EXISTS landuse_geom_gix ON public.landuse USING GIST (geom);
CREATE INDEX IF NOT EXISTS waterways_geom_gix ON public.waterways USING GIST (geom);
CREATE INDEX IF NOT EXISTS water_areas_geom_gix ON public.water_areas USING GIST (geom);
CREATE INDEX IF NOT EXISTS protected_areas_geom_gix ON public.protected_areas USING GIST (geom);
CREATE INDEX IF NOT EXISTS roads_hyderabad_geom_gix ON public.roads_hyderabad USING GIST (geom);
ANALYZE public.landuse;
ANALYZE public.waterways;
ANALYZE public.water_areas;
ANALYZE public.protected_areas;
ANALYZE public.roads_hyderabad;
SQL

echo "Import complete. Verify with:"
echo 'curl -fsS "$SOLAI_API_URL/api/v1/spatial/health"'
