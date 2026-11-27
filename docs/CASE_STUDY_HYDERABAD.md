# Hyderabad solar site intelligence case study — demo protocol

## Status and purpose

This is the first end-to-end SolAI demonstration protocol for the Hyderabad GIS extract. It is **not yet a verified real-project case study**: no cadastral parcel, landowner-authorised project boundary, utility-approved interconnection, or operating solar plant has been supplied for this location.

The initial GIS extract is centred at **17.360588° N, 78.474061° E** with a 15 km radius. This coordinate is a data-extract reference point, not a proposed project parcel or selected solar site.

## Demonstration workflow

1. Select a candidate parcel supplied by a developer/landowner or identify a candidate polygon from mapped land-cover data.
2. Record the parcel boundary, source, retrieval date, licence, area and confidence. Do not treat an OSM land-use polygon as title or statutory land-use proof.
3. Run nearby PostGIS queries for land use, waterways, water areas, protected-area context, roads and mapped power infrastructure.
4. Obtain authoritative forest, wildlife, wetlands, flood, cadastral and land-use restrictions before assigning an exclusion status.
5. Obtain authorised utility records for substation identity, voltage, transformer/feeder capacity, load, existing connections, evacuation options and cost. A nearby mapped point is not proof of grid access.
6. Fetch daily NASA POWER `ALLSKY_SFC_SW_DWN` resource data for the candidate coordinate and a completed historical period. Record the exact coordinate, dates, valid-day count and data vintage.
7. Generate an indicative specific-yield screen using an explicitly stated performance-ratio assumption. This is a coarse resource screen, not a bankable PV yield simulation.
8. Estimate capacity only from a surveyed/validated usable area and an explicit layout density assumption.
9. Compare the resulting indicative capacity/yield with engineering design, utility feasibility and owner-provided project economics.
10. If the project is operational, replace planning estimates with calibrated generation/export meter data and utility reconciliation before any MRV claim.

## NASA POWER resource method

- Provider: NASA POWER.
- Daily point endpoint: `https://power.larc.nasa.gov/api/temporal/daily/point`.
- Parameter: `ALLSKY_SFC_SW_DWN` (all-sky surface shortwave downward irradiation).
- Community: `RE` (renewable energy).
- Time standard: UTC.
- API documentation: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- SolAI's current screening calculation: sum valid daily horizontal irradiation (kWh/m²/day) over the requested period, then multiply by an explicit performance ratio (default 0.78) to produce an indicative MWh/MW/year proxy.

This simplified calculation does not transpose horizontal irradiation to a tilted plane or model array tilt/azimuth, shading, module temperature, clipping, soiling, degradation, downtime or curtailment. It must not be presented as an independently validated PV simulation or lender-grade yield assessment.

## Required case-study evidence

| Evidence | Required input | Current position |
|---|---|---|
| Candidate parcel | Polygon, area, source, rights/owner permission | Awaiting real site |
| Land-use / land cover | Official records plus dated imagery | Public GIS context available; incomplete |
| Environmental exclusions | Authoritative protected-area, forest, wetland and flood layers | Not yet complete |
| Terrain | Site DEM/slope and field survey | Regional Copernicus DEM extract exists; site validation pending |
| Solar resource | NASA POWER history and preferably site measurement | API integration added; live point result pending |
| Grid feasibility | Utility-authorised feeder/substation/hosting data | Public substation context only |
| Plant design | Layout, module/inverter, DC/AC ratio, losses | Awaiting engineering inputs |
| Generation | Calibrated generation/export meter data | No real project data supplied |
| Carbon/MRV | Applicable methodology and evidence | Framework only; not credit eligibility or issuance |

## What can be demonstrated now

- Eight imported Hyderabad spatial layers and their PostGIS metadata.
- Nearby-feature query and map display.
- Candidate-site weighted scoring API (with manually supplied factor values).
- NASA POWER daily solar-resource retrieval endpoint.
- Capacity/yield planning calculator.
- Project registration, meter CSV ingestion, indicative emissions calculation and audit-event view.

## Pitch-safe statement

"SolAI has built a Hyderabad geospatial screening foundation and is integrating satellite-derived solar-resource context into a traceable site-assessment workflow. The current prototype supports preliminary screening and planning estimates; parcel rights, statutory exclusions, utility hosting capacity, engineering yield and measured generation require authoritative project-specific evidence."

## Gate to call this a real project case study

Do not label the demonstration a real project until a real candidate parcel and its owner/developer authorisation are supplied, its boundary is documented, and at least the relevant land, environmental and utility evidence is collected. Keep all synthetic inputs visibly labelled as synthetic.
