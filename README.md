# Reker SolAI

**Solar Substation Potential Assessment** — a decision-support prototype for screening candidate solar sites around electricity substations.

SolAI is being developed as a separate product repository while retaining compatibility with Reker's existing platform architecture.

## Current status

This repository is an initial engineering scaffold. It does **not** yet contain Telangana utility-validated data, live utility integrations, or validated solar-site results. Any included example inputs are illustrative and must be labelled as sample/synthetic.

## Product workflow

1. Register a project and substation.
2. Ingest candidate-site features from documented geospatial datasets.
3. Screen sites using transparent criteria: land availability, shading, slope, flood risk and grid proximity.
4. Rank candidates using configurable weights.
5. Estimate indicative DC capacity and annual generation from usable area and specific yield.
6. Calculate indicative avoided emissions using an explicitly supplied grid emission factor.
7. Preserve inputs, assumptions, methodology version and validation status for an auditable assessment.

## Technology direction

- API: Python, FastAPI, Pydantic
- Persistence: PostgreSQL; PostGIS is a planned spatial extension
- Frontend: React / Next.js planned; a lightweight prototype UI will be added first
- Cloud: AWS planned
- Geospatial processing: GDAL, Rasterio, GeoPandas and Shapely are proposed additions, not yet integrated

## Run the API locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000/docs for the API documentation.

## Important methodology boundaries

- Suitability scores are screening indicators, not engineering approvals.
- Grid proximity is not electrical hosting capacity. Transformer loading, feeder constraints, voltage and interconnection studies require utility data.
- Solar generation is an estimate until validated against site design and operational metering.
- Avoided emissions are estimates, not issued or verified carbon credits.
- A hash can demonstrate record integrity; it does not prove that source data is true.

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md), [docs/ROADMAP.md](docs/ROADMAP.md) and [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md).
