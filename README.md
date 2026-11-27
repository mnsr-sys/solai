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

## Working demo — single dashboard and same-origin API

The user-facing application is one Vercel project: **REKER SolAI**. The dashboard is served from `frontend/dashboard/index.html`; the root `vercel.json` routes `/api/*` to the FastAPI entrypoint at `api/index.py`. The browser calls the API on the same origin. Users should open the dashboard URL only; the separate API Vercel project is not a second user interface.

The dashboard follows one guided workflow:

1. **Select geography and site:** choose a Telangana district, inspect the map, click a location to set candidate coordinates, and view distinct map symbols for public TGRAC substations, SolAI projects, selected candidate and context GIS layers.
2. **Enter site evidence:** provide usable area and the five screening inputs (land availability, low shading, slope suitability, flood safety and grid proximity), identify the evidence class, and record source notes.
3. **Assess and generate report:** calculate a weighted preliminary screening score; retrieve NASA POWER resource data; estimate planning-stage capacity/yield; print/save a site screening report or download the assessment JSON.
4. **Register project and track MRV:** create a project record, upload generation/export meter CSV, calculate an indicative emissions result using a supplied factor, and inspect the project audit events and MRV milestones.

Current demo endpoints include:

- `GET /health`
- `GET /api/v1/dashboard`
- `GET/POST /api/v1/projects`
- `POST /api/v1/projects/{project_id}/meter-readings`
- `POST /api/v1/projects/{project_id}/meter-csv`
- `GET /api/v1/projects/{project_id}/meter-readings`
- `POST /api/v1/sites/score`
- `GET /api/v1/solar/resource`
- `POST /api/v1/solar/potential`
- `POST /api/v1/projects/{project_id}/mrv`
- `GET /api/v1/projects/{project_id}/audit`
- `GET /api/v1/map/layers`
- `GET /api/v1/map/substations`
- `GET /api/v1/spatial/health`
- `GET /api/v1/spatial/layers`
- `GET /api/v1/spatial/nearby`

**Important demo limitations:** project and meter records remain in application memory, not durable storage across restarts/serverless instances. The public TGRAC GIS layer is contextual, not utility-verified. Candidate scoring uses supplied factor values and is a screening aid, not automated parcel/title approval. NASA POWER is gridded resource context, not an on-site measurement or bankable PV simulation. Meter uploads are not independently verified. The MRV result is indicative; the prototype does not independently verify reductions or issue carbon credits. Connect managed PostgreSQL/PostGIS, authentication, secure evidence storage, backups and authorised utility/project data before production onboarding.

## Carbon accounting and claims boundaries

- Renewable generation is not itself proof that carbon credits can be issued.
- Avoided emissions are estimates until calculated under an applicable methodology with verified project and monitoring data.
- Carbon-credit eligibility depends on methodology requirements, including additionality where applicable, baseline, project boundary, ownership/rights, monitoring, leakage, safeguards and double counting.
- Metered generation must be distinguished from capacity, modelled generation, grid export and self-consumption.
- Substation proximity does not prove grid connection, dispatch, export or hosting capacity.
- SolAI must label estimated reductions, methodology-screened potential, validated reductions and issued credits as distinct statuses.
- Independent validation and verification, registry approval and issuance are performed by the relevant authorised bodies—not by SolAI.

See [docs/CASE_STUDY_HYDERABAD.md](docs/CASE_STUDY_HYDERABAD.md) for the first end-to-end site-screening demo protocol. See [docs/TERRALAB_DATA_REGISTER.md](docs/TERRALAB_DATA_REGISTER.md) for the initial geospatial extract, substation sources and Telangana expansion requirements. See [docs/METHODOLOGY.md](docs/METHODOLOGY.md), [docs/ROADMAP.md](docs/ROADMAP.md), [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) and [docs/CARBON_MRV_FRAMEWORK.md](docs/CARBON_MRV_FRAMEWORK.md).

## PostGIS foundation

The initial durable spatial schema and controlled GIS ingestion procedure are in:

- [PostGIS migration](database/migrations/001_postgis_foundation.sql)
- [PostGIS setup and ingestion guide](docs/POSTGIS_SETUP.md)

The migration is ready to apply to a managed PostgreSQL/PostGIS instance. The current hosted API still uses in-memory demo persistence until a database provider is selected, credentials are configured, and the imported layers are validated. Do not treat the new SQL schema as a live database connection.
