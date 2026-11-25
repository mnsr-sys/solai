# Reker SolAI

**Solar Asset Intelligence & Carbon MRV for Telangana**

Reker SolAI is a climate-infrastructure intelligence and measurement, reporting and verification (MRV) platform focused on quantifying renewable electricity generation and tracking the evidence needed to assess carbon-credit potential from solar projects associated with substations and the wider electricity network in Telangana.

## Objective

Help solar project developers, asset owners, utilities and climate stakeholders answer four questions:

1. Where are existing and potential solar assets in Telangana, and how are they spatially related to substations and grid infrastructure?
2. How much renewable electricity is actually generated and delivered, based on reliable meter and operational data?
3. What emissions are avoided compared with a documented grid-electricity baseline?
4. Which projects may qualify for carbon-credit issuance under an applicable methodology, and what monitoring evidence, safeguards and third-party validation are required?

SolAI aims to make solar generation and its climate impact measurable, traceable and auditable—not simply map solar potential.

## What SolAI builds

- **Solar and substation intelligence:** geospatial inventory of solar installations, substations and relevant infrastructure using open data and verified asset records.
- **Generation MRV:** ingest inverter, generation-meter and export-meter data; validate time series, meter identity, gaps, anomalies and reconciliation.
- **Emissions accounting:** calculate net renewable electricity supplied and estimated avoided grid emissions using a documented, applicable baseline and emission factor.
- **Carbon-credit readiness:** map project evidence to the requirements of an applicable carbon-crediting methodology, including additionality, project boundary, baseline, monitoring, ownership, safeguards and double-counting checks.
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
- `POST /api/v1/projects/{project_id}/mrv`
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

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md), [docs/ROADMAP.md](docs/ROADMAP.md), [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) and [docs/CARBON_MRV_FRAMEWORK.md](docs/CARBON_MRV_FRAMEWORK.md).
