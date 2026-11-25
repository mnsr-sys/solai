-- Metadata only: records current TerraLab extraction provenance and counts.
-- This does NOT import GeoPackage features. Set binary_imported=true only after
-- the matching source file has been ingested and validated.
INSERT INTO solai.source_datasets
(source_name, source_provider, source_release, source_url, licence, attribution,
 coverage_name, coverage_geom, feature_count, is_truncated, metadata)
VALUES
('Land use — Hyderabad 15 km','OpenStreetMap via TerraLab','planet-2026-11',
 'https://www.openstreetmap.org/','ODbL 1.0',
 '© OpenStreetMap contributors; modified by TerraLab',
 'Hyderabad centre 17.360588,78.474061; radius 15 km',
 ST_Multi(ST_MakeEnvelope(78.3329245356,17.2250529255,78.6151974644,17.4961212397,4326)),
 2893,false,'{"layer":"landuse","retrieved_on":"2026-11-25","binary_imported":false,"source_snapshot":"OpenStreetMap planet 2026-11-16"}'::jsonb),
('Waterways — Hyderabad 15 km','OpenStreetMap via TerraLab','planet-2026-11',
 'https://www.openstreetmap.org/','ODbL 1.0',
 '© OpenStreetMap contributors; modified by TerraLab',
 'Hyderabad centre 17.360588,78.474061; radius 15 km',
 ST_Multi(ST_MakeEnvelope(78.3329245356,17.2250529255,78.6151974644,17.4961212397,4326)),
 309,false,'{"layer":"waterways","retrieved_on":"2026-11-25","binary_imported":false,"source_snapshot":"OpenStreetMap planet 2026-11-16"}'::jsonb),
('Water areas — Hyderabad 15 km','OpenStreetMap via TerraLab','planet-2026-11',
 'https://www.openstreetmap.org/','ODbL 1.0',
 '© OpenStreetMap contributors; modified by TerraLab',
 'Hyderabad centre 17.360588,78.474061; radius 15 km',
 ST_Multi(ST_MakeEnvelope(78.3329245356,17.2250529255,78.6151974644,17.4961212397,4326)),
 343,false,'{"layer":"water_areas","retrieved_on":"2026-11-25","binary_imported":false,"source_snapshot":"OpenStreetMap planet 2026-11-16"}'::jsonb),
('Protected areas — Hyderabad 15 km','OpenStreetMap via TerraLab','planet-2026-11',
 'https://www.openstreetmap.org/','ODbL 1.0',
 '© OpenStreetMap contributors; modified by TerraLab',
 'Hyderabad centre 17.360588,78.474061; radius 15 km',
 ST_Multi(ST_MakeEnvelope(78.3329245356,17.2250529255,78.6151974644,17.4961212397,4326)),
 5,false,'{"layer":"protected_areas","retrieved_on":"2026-11-25","binary_imported":false,"source_snapshot":"OpenStreetMap planet 2026-11-16","warning":"Not sufficient for statutory exclusion screening"}'::jsonb),
('Roads — Hyderabad 2.5 km','Overture Maps via TerraLab','2026-11-18',
 'https://overturemaps.org/','ODbL 1.0',
 '© OpenStreetMap contributors, Overture Maps Foundation and TomTom',
 'Hyderabad centre 17.360588,78.474061; radius 2.5 km',
 ST_Multi(ST_MakeEnvelope(78.4505382518,17.3379989480,78.4975837482,17.3831770010,4326)),
 16172,false,'{"layer":"roads","retrieved_on":"2026-11-25","binary_imported":false,"source_snapshot":"Overture Maps 2026-11-18"}'::jsonb),
('Power features — Hyderabad 20 km','OpenStreetMap via TerraLab','planet-2026-11',
 'https://www.openstreetmap.org/','ODbL 1.0',
 '© OpenStreetMap contributors; modified by TerraLab',
 'Hyderabad centre 17.360588,78.474061; radius 20 km',
 ST_Multi(ST_MakeEnvelope(78.2858790738,17.1798741618,78.6622429262,17.5412985764,4326)),
 2889,false,'{"layer":"power","retrieved_on":"2026-11-25","binary_imported":false,"source_snapshot":"OpenStreetMap planet 2026-11-16","tagged_substation_count":171,"warning":"OSM records, not utility-verified inventory"}'::jsonb)
ON CONFLICT DO NOTHING;
