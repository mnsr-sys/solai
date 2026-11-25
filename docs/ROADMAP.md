# Engineering roadmap

## Phase 0 — prototype foundation
- FastAPI project and health endpoint.
- Project registration endpoint.
- Explainable five-criteria site scoring.
- Indicative solar capacity, generation and emissions calculator.
- Explicit validation and data-status labels.

## Phase 1 — Telangana demonstration
- Select one district and a small, documented sample of substations.
- Add public geospatial layers with attribution and provenance.
- Add map UI and candidate parcel overlays.
- Add result export and methodology note.
- Keep synthetic and public data visibly distinguished.

## Phase 2 — utility feasibility
- Ingest utility-approved transformer, feeder and load-profile data.
- Add electrical hosting-capacity and interconnection checks.
- Add field validation records for 3–5 shortlisted sites.
- Add uncertainty ranges and reviewer sign-off.

## Phase 3 — operational product
- PostgreSQL/PostGIS persistence and tenant/project access controls.
- Asynchronous raster processing and object storage.
- Monitoring, audit logs, backups and automated tests.
- Utility integration and role-based reporting.

## Jury demo acceptance criteria
1. Select a sample Telangana district and substation.
2. Show candidate sites and data provenance.
3. Explain every score and weight.
4. Calculate MW, MWh/year and estimated tCO₂e/year with visible assumptions.
5. Flag missing utility data and electrical checks.
6. Export a report whose figures match the dashboard.
7. Have an offline backup recording.
