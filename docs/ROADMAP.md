# Telangana product roadmap — substation-first solar intelligence with MRV extension

## Product thesis

SolAI's core product is substation-first geospatial intelligence for solar deployment planning. It helps utilities and developers discover and rank candidate sites using land, water, terrain, land-cover, risk and grid-context data.

Generation monitoring and carbon MRV are extensions of the same project record after a candidate site moves through development and becomes an operating solar asset. MRV must not replace or obscure the original geospatial decision workflow.

## Phase 1 — Telangana geospatial foundation and substation intelligence

- Preserve and catalogue the initial 15 km Hyderabad-area land/water extract and 2.5 km roads extract, including exact feature counts, source releases, licences and limitations.
- Keep TGRAC's published substation GIS and the earlier 20 km OSM power-feature extract as separate sources with provenance.
- Expand land use, land cover, water, roads, settlements, terrain and constraints district by district across Telangana.
- Obtain official TSTRANSCO/DISCOM substation, transformer and feeder records through authorised access.
- Add Sentinel-2 land classification and authoritative government land, forest, wildlife, wetland and flood constraints.
- Build PostgreSQL/PostGIS with source lineage, stable feature IDs, spatial indexes, coordinate validation, data vintages and refresh logs.

## Phase 2 — Candidate-site discovery and ranking

- Generate candidate land polygons around substations and relevant grid corridors using transparent distance and constraint rules.
- Screen land availability, land cover, slope, aspect, shading, water proximity, flood exposure and protected-area constraints.
- Rank sites using configurable, documented weights; show each component score and source confidence.
- Estimate usable area, indicative DC capacity and annual yield using explicit assumptions and solar-resource data.
- Show grid proximity as a screening attribute only; do not infer feeder connection, available capacity or evacuation feasibility.
- Produce ranked candidate lists, map overlays and downloadable site-screening reports.

## Phase 3 — Project development and grid feasibility

- Convert shortlisted candidate sites into project records with boundary, ownership/rights, permits, capacity, technology and commissioning data.
- Attach the relevant substation, feeder and utility records with source IDs.
- Integrate transformer ratings, feeder load curves, existing generation, voltage constraints and evacuation cost inputs when officially supplied.
- Add engineering review workflows, site visits and ground-truthing.
- Maintain explicit gates for land-title verification, statutory exclusions, grid feasibility and project approvals.

## Phase 4 — Operating asset monitoring and carbon MRV extension

- Ingest authorised inverter, generation-meter and export-meter data.
- Validate intervals, meter IDs, calibration, missing readings, duplicates, resets, outages, curtailment and energy balance.
- Reconcile generation and export with utility statements.
- Select an applicable methodology and implement its baseline, eligible energy, project-emissions, leakage and monitoring rules.
- Generate monitoring reports and traceable evidence packs for independent validation/verification.
- Track estimated impact, methodology screening, verified reductions and registry-issued credits as distinct states.

## Phase 5 — Production qualification

- Move demo storage to managed PostgreSQL/PostGIS with backups, migrations and recovery tests.
- Add authentication, organisation/project roles, encryption, secure evidence storage and access controls.
- Add observability, data refresh monitoring, QA alerts and deployment checks.
- Complete documented end-to-end acceptance tests with authorised real project and utility data.

## TRL 8 target — exit criteria

TRL 8 is a target, not a current certification or achievement claim. Before making the claim, demonstrate and document:

1. Integrated geospatial platform with substation map, district datasets, candidate land discovery, suitability ranking and solar planning.
2. Traceable source lineage and documented data-quality validation for each geospatial layer.
3. At least one shortlisted site ground-truthed and assessed against land, statutory and utility requirements.
4. At least one real Telangana solar project onboarded with authorised project and operational meter records.
5. Meter QA/QC and generation/export reconciliation demonstrated against source statements.
6. Methodology-aligned MRV calculations independently checked against reference calculations.
7. Reproducible reports and evidence packs with raw inputs, provenance, assumptions, methodology/factor vintage, calculation version and exceptions.
8. Security, reliability, recovery and user-acceptance tests completed, with demonstration accepted by a relevant developer, utility or operational stakeholder.

Carbon-credit issuance is not a prerequisite for software TRL 8, and TRL 8 does not imply carbon-credit eligibility.

## Current demo acceptance criteria

- Telangana is the only geography selectable.
- Public substation markers are visible, searchable and distinguishable from SolAI project pins.
- Candidate-site ranking endpoint scores sites with transparent inputs and weighted criteria.
- Solar planning endpoint estimates capacity and yield without mislabelling them as metered generation.
- Projects can be registered with coordinates, capacity and substation reference.
- Meter CSV readings can be uploaded with duplicate checks.
- Indicative MRV output displays factor source, vintage, energy basis and limitations.
- Audit events are retrievable for a project.
- Demo storage limitations are visible; no demo result is described as independently verified.
