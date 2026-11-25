# Telangana product roadmap — solar climate intelligence and carbon MRV

## Phase 1 — map and asset intelligence
- Provide an interactive Telangana map with public substation context and registered solar-project pins.
- Preserve source attribution, layer version, refresh time and data limitations.
- Support project registration with district, coordinates, capacity, technology, owner and substation reference.
- Distinguish public GIS, synthetic, owner-provided and utility-provided records.
- Never treat substation proximity as proof of electrical connection or hosting capacity.

## Phase 2 — generation evidence and data quality
- Support secure meter CSV ingestion and, when authorised, API/telemetry integrations.
- Capture generation, export, self-consumption, auxiliary use, outages and curtailment where available.
- Detect duplicate intervals, gaps, outliers, meter resets and meter replacements.
- Reconcile plant generation and export to utility statements within configured tolerances.
- Retain raw files, source metadata, meter identity, timezone, units and audit events.

## Phase 3 — emissions accounting and carbon-credit readiness
- Select and document an applicable carbon-crediting methodology for each project.
- Implement methodology-specific baseline, project-emissions, leakage and monitoring rules only after review.
- Record emission-factor source, geography, vintage and methodology version.
- Track environmental-attribute ownership, renewable energy certificates and double-counting risks.
- Generate reproducible monitoring reports and evidence packs for independent review.
- Keep estimates, methodology-screened potential, verified reductions and issued credits as separate statuses.

## Phase 4 — production qualification and utility integrations
- Move demo storage to managed PostgreSQL/PostGIS with backups, migrations and access controls.
- Add authentication, organisation/project roles, encryption, retention policies and secure secrets.
- Integrate authorised DISCOM/TGTRANSCO and project-owner data where access is formally granted.
- Add monitoring, alerting, deployment checks and disaster recovery.
- Run documented end-to-end acceptance tests with real, authorised solar-project data.

## TRL 8 target — exit criteria

TRL 8 is a target, not a current certification or achievement claim. Before making the claim, demonstrate and document all of the following:

1. An integrated, deployable SolAI system with map, project registration, meter ingestion, QA/QC, MRV calculations, reporting and audit history.
2. At least one real Telangana solar project onboarded using authorised project and meter records.
3. Meter data validation and generation/export reconciliation demonstrated against source statements.
4. A named, applicable methodology selected and calculations independently checked against reference calculations.
5. Reproducible evidence pack with raw inputs, provenance, assumptions, factor vintage, calculation version and exception log.
6. Security, reliability, recovery and user-acceptance tests completed with documented results.
7. Demonstration accepted by the relevant project owner or operational stakeholder; independent technical assessment retained.
8. Clear separation between SolAI's monitoring outputs and third-party validation, verification and registry issuance.

Carbon-credit issuance is not a TRL 8 prerequisite for the software product, and TRL 8 does not imply that a project is eligible for credits.

## Acceptance criteria for the current demo

- Telangana is the only selectable state and non-Telangana districts are rejected by the API.
- Public substation map layer and SolAI project pins are distinguishable.
- A project can be registered with location and capacity.
- CSV meter readings can be uploaded, with duplicate records skipped and counted.
- Dashboard totals reflect records ingested in the active demo instance.
- Indicative MRV output displays its factor source, vintage, energy basis and limitations.
- Audit events are retrievable for a project.
- Demo storage limitations are visible; no demo result is described as independently verified.
