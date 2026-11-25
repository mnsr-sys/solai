# Reker SolAI

**Solar Substation Potential Assessment** — a multi-state decision-support prototype for screening candidate solar sites around electricity substations.

**Geographic rollout:** Telangana is the first implementation and demo priority. Karnataka is included as the next expansion state, using the same assessment engine with state-specific datasets and utility criteria.

## Current status

This repository is an engineering prototype. It does **not** yet contain Telangana or Karnataka utility-validated substation inventories, live utility integrations, or validated solar-site results. District selectors are geographic scaffolding only. Example site inputs are synthetic unless explicitly labelled otherwise.

## Product workflow

1. Select a state and district (Telangana first; Karnataka next).
2. Register a project and substation.
3. Ingest candidate-site features from documented geospatial datasets.
4. Screen sites using transparent criteria: land availability, shading, slope, flood risk and grid proximity.
5. Rank candidates using configurable weights.
6. Estimate indicative DC capacity and annual generation from usable area and specific yield.
7. Calculate indicative avoided emissions using an explicitly supplied grid emission factor.
8. Preserve inputs, assumptions, methodology version and validation status for an auditable assessment.

## State rollout

| Priority | State | Current role |
|---|---|---|
| 1 | Telangana | Primary demo and first pilot geography |
| 2 | Karnataka | Next expansion geography; shared engine, separate data and criteria |

The current district lists are starter selectors, not official or complete administrative inventories and not evidence of substation coverage.

## Technology direction

- API: Python, FastAPI, Pydantic
- Persistence: PostgreSQL; PostGIS is a planned spatial extension
- Frontend: React / Next.js planned; a lightweight prototype UI is used first
- Cloud: AWS planned
- Geospatial processing: GDAL, Rasterio, GeoPandas and Shapely are proposed additions, not yet integrated

## Run the API locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000/docs for the API documentation. State and district options are available at `GET /api/v1/states`.

## Important methodology boundaries

- Suitability scores are screening indicators, not engineering approvals.
- Grid proximity is not electrical hosting capacity. Transformer loading, feeder constraints, voltage and interconnection studies require utility data.
- Solar generation is an estimate until validated against site design and operational metering.
- Avoided emissions are estimates, not issued or verified carbon credits.
- A hash can demonstrate record integrity; it does not prove that source data is true.

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md), [docs/ROADMAP.md](docs/ROADMAP.md) and [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md).
