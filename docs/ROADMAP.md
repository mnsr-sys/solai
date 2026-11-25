# Telangana product roadmap — solar climate intelligence and carbon MRV

## Phase 1 — Telangana data foundation
- Organise open geospatial layers for solar assets, substations, roads, land cover, terrain and water features.
- Build a provenance register with licences, dates, resolution, coverage and limitations.
- Separate mapped public assets from owner-submitted and utility-verified records.
- Establish the Telangana project/asset data model.

## Phase 2 — solar asset and generation MRV
- Register solar projects and associated substations/grid connection points.
- Support secure meter-data upload and API ingestion.
- Capture generation, export, self-consumption, auxiliary use, outages and curtailment where available.
- Add meter QA/QC, missing-data detection, reconciliation and exception review.
- Produce traceable monthly and annual generation reports.

## Phase 3 — emissions accounting and carbon-credit readiness
- Select and document applicable carbon-crediting methodologies for each project type.
- Implement methodology-specific baseline, project-emissions, leakage and monitoring calculations only after methodology review.
- Track ownership of environmental attributes, renewable energy certificates and double-counting risks.
- Generate evidence packages and monitoring reports for independent review.
- Clearly distinguish estimated reductions, verified reductions and registry-issued credits.

## Phase 4 — utility and project integrations
- Integrate authorised DISCOM/TGTRANSCO or other utility data where access is formally granted.
- Reconcile plant meters with utility export/import statements and interconnection records.
- Add secure telemetry, role-based access, audit logs and operational monitoring.
- Extend coverage across Telangana with verified project and utility participation.

## Acceptance criteria
1. A Telangana solar project and associated grid/substation context can be registered.
2. Every mapped asset and dataset has visible provenance and validation status.
3. Meter files can be ingested with units, timezone, meter identity and source retained.
4. QA/QC flags missing intervals, duplicates, abnormal values and meter changes.
5. Generation and export totals reconcile to source records within configured tolerances.
6. Emissions estimates show the exact baseline method, factor, vintage and assumptions.
7. The system prevents an estimate from being labelled as verified reductions or issued credits.
8. A monitoring/evidence report can be exported with a complete audit trail.
