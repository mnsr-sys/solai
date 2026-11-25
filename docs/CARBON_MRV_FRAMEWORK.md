# SolAI carbon MRV framework — Telangana

## Purpose and boundary

SolAI measures renewable electricity generation, supports grid-export reconciliation and prepares traceable evidence for project-level climate-impact assessment in Telangana. A substation is a spatial/grid-context reference; proximity alone does not establish a project's electrical connection, dispatch, export or carbon-credit eligibility.

This is an implementation framework for product design and pre-screening. It is not an approved carbon-credit methodology, validation opinion, verification statement or guarantee of issuance.

## End-to-end evidence chain

1. **Project identity and boundary:** project ID, legal owner/rights holder, coordinates and polygon boundary, technology, installed capacity, commissioning date, permits and grid interconnection evidence.
2. **Methodology screening:** identify an applicable crediting programme and active methodology before selecting monitoring parameters. Record version, effective dates, applicability conditions and deviations.
3. **Baseline:** document the counterfactual electricity source, grid boundary, applicable emission factor, vintage, geography and source publication.
4. **Monitoring:** ingest calibrated generation and export meter readings with timestamp, timezone, meter ID, units, source file and reading type.
5. **QA/QC:** test gaps, duplicates, resets, outliers, unit changes, meter replacement, calibration, outages, curtailment and reconciliation.
6. **Eligible energy:** calculate only the quantity allowed by the selected methodology and project boundary. Keep gross generation, auxiliary consumption, self-consumption and grid export distinct.
7. **Emissions calculation:** apply methodology-prescribed baseline, project emissions, leakage, losses and adjustments. Retain factor source, vintage and calculation version.
8. **Reporting and independent review:** produce monitoring reports and evidence packs for the project owner and an independent validation/verification body.

## Minimum project and meter data

- Project identifier, owner, rights evidence, technology, DC/AC capacity and commissioning date.
- Project boundary geometry and site coordinates.
- Inverter and meter identifiers, meter type, calibration certificate, accuracy class and replacement history.
- Interval timestamp with timezone, energy value, unit, meter ID, reading type and source.
- Generation, grid export, imports, auxiliary use and self-consumption where separately metered.
- Outage, curtailment and missing-data annotations.
- Utility interconnection approvals and settlement/energy statements where applicable.
- Source file hash, ingestion time, transformations, reviewer, exceptions and report version.

## Conceptual calculation

For an illustrative grid-displacement estimate:

- Baseline emissions = eligible electricity (MWh) × applicable baseline factor (tCO2e/MWh).
- Indicative net impact = baseline emissions − project emissions − leakage.

This expression is conceptual only. The eligible electricity boundary, factor, grid loss treatment, temporal resolution, project emissions, leakage and any adjustments must follow the selected methodology. A generic factor multiplied by annual solar generation is not automatically a credit calculation.

## Eligibility gates before a credit claim

Assess the applicable programme and methodology; project start date and registration deadlines; additionality and regulatory surplus where required; baseline; ownership of environmental attributes; renewable energy certificates and other claims; double counting/double issuance; monitoring plan; meter calibration; leakage; safeguards; stakeholder consultation; and independent validation, verification and registry issuance.

## Product status vocabulary

| Status | Meaning |
|---|---|
| Mapped asset | A public or supplied GIS feature; identity and operation not yet confirmed |
| Project registered | Project details entered; not necessarily independently verified |
| Meter data uploaded | Source data ingested; QA/QC still pending |
| Generation measured | Readings passed documented data checks |
| Avoided emissions estimated | Indicative calculation; not verified reductions |
| Methodology screened | Preliminary assessment against a named methodology/version |
| Validation/verification pending | Submitted for independent review |
| Verified reductions | Confirmed through the relevant independent process |
| Credits issued | Credits issued by the relevant registry with serialised records |

Never label an estimate as “credits generated”, “verified” or “issued”.

## Audit and integrity

Preserve raw files, hashes, source references, ingestion logs, meter metadata, data-quality results, calculation inputs, factor vintage, methodology version, assumptions, exceptions, approvals and report versions. A cryptographic hash helps show that a captured file has not changed; it does not prove that the source meter or claim is true.

## SolAI implementation guardrails

- Public GIS layers are discovery/context only; they do not prove land title, asset ownership, grid connection or hosting capacity.
- Synthetic, owner-provided and utility-provided data must be visibly distinguished.
- Do not silently fill missing meter intervals or convert modelled generation into measured generation.
- Store raw data separately from cleaned/derived data and retain a reproducible transformation trail.
- Do not claim TRL 8 until the integrated system has been demonstrated and qualified against documented acceptance criteria.
- SolAI does not issue carbon credits. Independent bodies and registries retain their respective roles.
