# Reker SolAI

**Substation-first Solar Geospatial Intelligence, with Generation MRV and Carbon Impact Tracking — Telangana**

Reker SolAI is a climate-infrastructure intelligence platform that helps utilities and renewable-energy developers discover, assess and rank solar deployment opportunities around substations across Telangana. It combines geospatial data, land and terrain constraints, water/flood context, solar-resource inputs and grid-infrastructure proximity to support better site-screening and project-planning decisions.

Generation MRV and carbon accounting extend this same workflow after a candidate site becomes a developed and operating solar project. MRV does not replace the geospatial product.

## Problem statement

Solar developers and utility teams often assess land availability, terrain, water constraints, proximity to substations, grid access, evacuation feasibility and project economics using fragmented datasets and manual analysis. This slows site discovery and makes candidate-site comparisons difficult.

**SolAI turns those fragmented inputs into a traceable, map-led decision workflow:** identify candidate land, screen constraints, assess substation context, estimate potential capacity and yield, rank sites for detailed feasibility, and then follow selected projects through generation monitoring and climate-impact reporting.

## What decisions SolAI supports

1. Where is potentially suitable land around mapped substations and grid infrastructure?
2. What do land use, water bodies, waterways, terrain, slope, shading, flood exposure and protected-area constraints indicate?
3. Which candidate sites should be prioritised for detailed field and engineering assessment?
4. What indicative solar capacity and annual generation could a screened site support under stated assumptions?
5. What official utility data is still needed to confirm feeder connectivity, hosting capacity, evacuation requirements and cost?
6. Once operational, how much renewable electricity is actually generated/exported, what emissions impact can be estimated under an applicable methodology, and what evidence is needed for independent verification?

## What SolAI builds

- **Substation-first geospatial intelligence:** map substations and grid context; organise land, water, roads, terrain, land-cover and constraint layers; screen candidate parcels around infrastructure.
- **Candidate-site ranking and solar planning:** rank sites using land availability, shading, slope, flood safety and grid proximity; estimate capacity and yield from explicit planning assumptions.
- **Generation MRV extension:** after project development, ingest inverter, generation-meter and export-meter data; validate time series, meter identity, gaps, anomalies and reconciliation.
- **Emissions accounting and carbon-credit readiness:** assess eligible electricity and potential avoided emissions against a documented methodology, including baseline, monitoring, ownership, safeguards and double-counting checks.
- **Audit trail:** preserve source records, timestamps, methodology versions, calculations, review status and cryptographic integrity checks.

## Telangana focus

The product and data model are focused on Telangana. District-level views are for organising analysis; they do not imply complete official coverage or utility validation.

## Data strategy for the demonstration

Use free/open datasets and open-source software wherever possible: OpenStreetMap, Copernicus Sentinel-2, Copernicus DEM, relevant openly licensed reference layers, QGIS, PostgreSQL/PostGIS, Python and FastAPI. Use official utility, project-owner and meter data only when access is authorised. Public geospatial data can support discovery and context; it cannot replace verified generation meters, ownership records or utility confirmation.

## Product workflow

1. Discover and map solar assets and substations from attributed open data and authorised records.
2. Register each project, asset owner, location, commissioning date, capacity and project boundary.
3. Connect or import generation and grid-export meter data.
4. Validate meter readings, data completeness, outages, curtailment and energy balance.
5. Calculate net eligible renewable electricity and baseline emissions using a selected methodology.
6. Generate monitoring reports, evidence packages and carbon-credit readiness status.
7. Track independent validation/verification and issuance status separately from estimated reductions.

## Technology direction

- API: Python, FastAPI, Pydantic
- Spatial database: PostgreSQL + PostGIS
- Geospatial processing: QGIS, GDAL, Rasterio, GeoPandas and Shapely
- Data ingestion: secure CSV/API ingestion initially; telemetry integrations as authorised
- Frontend: existing web application
- Auditability: immutable event history and content hashes; hashes support integrity, not source-data truth

## Run the API locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000/docs for API documentation.

## Working demo

The dashboard is served from `frontend/dashboard/index.html`. It includes the Telangana map, project registration, meter CSV upload, indicative MRV calculation and project audit view. The API endpoints are documented at `/docs` when the FastAPI service is running.

Current demo endpoints:
- `GET /api/v1/dashboard`
- `GET/POST /api/v1/projects`
- `POST /api/v1/projects/{project_id}/meter-readings`
- `POST /api/v1/projects/{project_id}/meter-csv`
- `GET /api/v1/projects/{project_id}/meter-readings`
- `POST /api/v1/sites/score`\n- `POST /api/v1/solar/potential`\n- `POST /api/v1/projects/{project_id}/mrv`
- `GET /api/v1/projects/{project_id}/audit`
- `GET /api/v1/map/layers`

**Demo limitation:** current project and meter records are held in application memory. They are not durable across restarts or serverless instances. Connect managed PostgreSQL/PostGIS, authentication, backups and access controls before production onboarding. The public GIS substation layer is an external contextual source and must be validated with the relevant utility.

## Carbon accounting and claims boundaries

- Renewable generation is not itself proof that carbon credits can be issued.
- Avoided emissions are estimates until calculated under an applicable methodology with verified project and monitoring data.
- Carbon-credit eligibility depends on methodology requirements, including additionality where applicable, baseline, project boundary, ownership/rights, monitoring, leakage, safeguards and double counting.
- Metered generation must be distinguished from capacity, modelled generation, grid export and self-consumption.
- Substation proximity does not prove grid connection, dispatch, export or hosting capacity.
- SolAI must label estimated reductions, methodology-screened potential, validated reductions and issued credits as distinct statuses.
- Independent validation and verification, registry approval and issuance are performed by the relevant authorised bodies—not by SolAI.

See [docs/TERRALAB_DATA_REGISTER.md](docs/TERRALAB_DATA_REGISTER.md) for the initial geospatial extract, substation sources and Telangana expansion requirements. See [docs/METHODOLOGY.md](docs/METHODOLOGY.md), [docs/ROADMAP.md](docs/ROADMAP.md), [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) and [docs/CARBON_MRV_FRAMEWORK.md](docs/CARBON_MRV_FRAMEWORK.md).
