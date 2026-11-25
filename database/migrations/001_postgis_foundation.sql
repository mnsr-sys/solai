-- Reker SolAI PostGIS foundation
-- Apply with: psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f database/migrations/001_postgis_foundation.sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS solai;

CREATE TABLE IF NOT EXISTS solai.source_datasets (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_name text NOT NULL,
    source_provider text NOT NULL,
    source_release text,
    source_url text,
    licence text NOT NULL,
    attribution text NOT NULL,
    retrieved_at timestamptz NOT NULL DEFAULT now(),
    coverage_name text,
    coverage_geom geometry(MultiPolygon, 4326),
    feature_count integer,
    is_truncated boolean NOT NULL DEFAULT false,
    checksum_sha256 text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS source_datasets_coverage_gix
    ON solai.source_datasets USING gist (coverage_geom);

-- Normalised landing table for OSM, Overture, TGRAC and other vector layers.
-- Preserve original tags/attributes and dataset lineage; never treat OSM as official utility data.
CREATE TABLE IF NOT EXISTS solai.spatial_features (
    id bigserial PRIMARY KEY,
    dataset_id uuid NOT NULL REFERENCES solai.source_datasets(id),
    layer_name text NOT NULL,
    source_feature_key text,
    source_feature_type text,
    name text,
    feature_class text,
    attributes jsonb NOT NULL DEFAULT '{}'::jsonb,
    geom geometry(Geometry, 4326) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (dataset_id, layer_name, source_feature_key)
);
CREATE INDEX IF NOT EXISTS spatial_features_geom_gix
    ON solai.spatial_features USING gist (geom);
CREATE INDEX IF NOT EXISTS spatial_features_layer_idx
    ON solai.spatial_features (layer_name, feature_class);
CREATE INDEX IF NOT EXISTS spatial_features_attributes_gin
    ON solai.spatial_features USING gin (attributes);

CREATE TABLE IF NOT EXISTS solai.substations (
    id bigserial PRIMARY KEY,
    dataset_id uuid REFERENCES solai.source_datasets(id),
    source_feature_key text NOT NULL,
    source_name text NOT NULL,
    source_class text NOT NULL DEFAULT 'public-map-reference',
    name text,
    operator_name text,
    voltage_kv numeric[],
    status text,
    confidence text NOT NULL DEFAULT 'unverified'
        CHECK (confidence IN ('unverified','public-reference','owner-confirmed','utility-confirmed')),
    utility_verified boolean NOT NULL DEFAULT false,
    attributes jsonb NOT NULL DEFAULT '{}'::jsonb,
    geom geometry(Point, 4326) NOT NULL,
    retrieved_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_name, source_feature_key)
);
CREATE INDEX IF NOT EXISTS substations_geom_gix
    ON solai.substations USING gist (geom);
CREATE INDEX IF NOT EXISTS substations_voltage_gin
    ON solai.substations USING gin (voltage_kv);

CREATE TABLE IF NOT EXISTS solai.candidate_sites (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    site_code text UNIQUE,
    state_code text NOT NULL DEFAULT 'TS' CHECK (state_code = 'TS'),
    district text NOT NULL,
    label text,
    source_dataset_ids uuid[] NOT NULL DEFAULT '{}',
    land_area_m2 numeric,
    usable_area_m2 numeric,
    land_cover_class text,
    slope_mean_deg numeric,
    flood_exposure text,
    nearest_substation_id bigint REFERENCES solai.substations(id),
    substation_distance_m numeric,
    indicative_capacity_mw numeric,
    indicative_annual_yield_mwh numeric,
    suitability_score numeric CHECK (suitability_score BETWEEN 0 AND 100),
    scoring_version text,
    confidence text NOT NULL DEFAULT 'screening-only'
        CHECK (confidence IN ('screening-only','field-checked','owner-confirmed','utility-reviewed')),
    constraints jsonb NOT NULL DEFAULT '{}'::jsonb,
    attributes jsonb NOT NULL DEFAULT '{}'::jsonb,
    geom geometry(MultiPolygon, 4326) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS candidate_sites_geom_gix
    ON solai.candidate_sites USING gist (geom);
CREATE INDEX IF NOT EXISTS candidate_sites_district_score_idx
    ON solai.candidate_sites (district, suitability_score DESC);

CREATE TABLE IF NOT EXISTS solai.solar_projects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_code text UNIQUE,
    name text NOT NULL,
    state_code text NOT NULL DEFAULT 'TS' CHECK (state_code = 'TS'),
    district text NOT NULL,
    asset_type text NOT NULL,
    owner_name text,
    capacity_mw numeric NOT NULL CHECK (capacity_mw > 0),
    commissioning_date date,
    candidate_site_id uuid REFERENCES solai.candidate_sites(id),
    substation_id bigint REFERENCES solai.substations(id),
    location geometry(Point, 4326) NOT NULL,
    boundary geometry(MultiPolygon, 4326),
    status text NOT NULL DEFAULT 'registered-unverified',
    data_status text NOT NULL DEFAULT 'owner-provided',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS solar_projects_location_gix
    ON solai.solar_projects USING gist (location);
CREATE INDEX IF NOT EXISTS solar_projects_boundary_gix
    ON solai.solar_projects USING gist (boundary);

CREATE TABLE IF NOT EXISTS solai.meter_readings (
    id bigserial PRIMARY KEY,
    project_id uuid NOT NULL REFERENCES solai.solar_projects(id),
    meter_id text NOT NULL,
    reading_at timestamptz NOT NULL,
    energy_mwh numeric NOT NULL CHECK (energy_mwh >= 0),
    reading_type text NOT NULL CHECK (reading_type IN ('generation','grid-export')),
    source text NOT NULL,
    raw_record jsonb NOT NULL DEFAULT '{}'::jsonb,
    ingested_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, meter_id, reading_at, reading_type)
);
CREATE INDEX IF NOT EXISTS meter_readings_project_time_idx
    ON solai.meter_readings (project_id, reading_at DESC);

CREATE TABLE IF NOT EXISTS solai.audit_events (
    id bigserial PRIMARY KEY,
    entity_type text NOT NULL,
    entity_id text NOT NULL,
    action text NOT NULL,
    details jsonb NOT NULL DEFAULT '{}'::jsonb,
    event_at timestamptz NOT NULL DEFAULT now(),
    event_hash text
);
CREATE INDEX IF NOT EXISTS audit_events_entity_idx
    ON solai.audit_events (entity_type, entity_id, event_at DESC);

-- Proximity is a screening measure only. It does not establish feeder connectivity
-- or spare hosting capacity; those require authorised TSTRANSCO/DISCOM engineering data.
CREATE OR REPLACE VIEW solai.v_candidate_site_substation_context AS
SELECT
    c.id AS candidate_site_id,
    c.district,
    c.suitability_score,
    s.id AS substation_id,
    s.name AS substation_name,
    s.source_name AS substation_source,
    s.confidence AS substation_confidence,
    CASE WHEN s.id IS NULL THEN NULL
         ELSE ST_Distance(c.geom::geography, s.geom::geography) END AS straight_line_distance_m
FROM solai.candidate_sites c
LEFT JOIN LATERAL (
    SELECT ss.*
    FROM solai.substations ss
    ORDER BY c.geom <-> ss.geom
    LIMIT 1
) s ON true;

COMMENT ON SCHEMA solai IS 'Telangana-first solar geospatial intelligence and downstream generation MRV';
COMMENT ON TABLE solai.spatial_features IS 'Source-preserving vector feature store. Retain source attribution and raw attributes.';
COMMENT ON TABLE solai.substations IS 'Public-map and utility records kept distinct through source_name, source_class and confidence.';
COMMENT ON TABLE solai.candidate_sites IS 'Candidate polygons and screening scores; not land-title, statutory or grid-feasibility approval.';
