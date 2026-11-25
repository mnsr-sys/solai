# Telangana geospatial data register

## Purpose

This register describes public and open geospatial context layers that may support solar-asset discovery and preliminary infrastructure screening across Telangana. It is not an official asset inventory, statutory land-use register, grid-capacity assessment or project verification record.

## Public infrastructure context

- **TGRAC public ArcGIS electric-transmission substation layer:** the dashboard queries the published RRR electric-transmission substation service at `https://tgrac.telangana.gov.in/arcgis/rest/services/RRR_Folder/RRR/MapServer/8`. Treat the layer as a discovery reference only. Validate asset identity, voltage, operational status, ownership, feeder association and electrical connection with the relevant utility before use in project decisions.
- **OpenStreetMap:** roads, waterways, land-use tags and mapped infrastructure. Attribute the source and comply with ODbL obligations.
- **Overture Maps:** supplementary features where the release terms and source attribution are suitable.
- **Copernicus Sentinel-2:** imagery for land-cover and change context. Record product ID, acquisition date, processing level, cloud cover and resolution.
- **Copernicus DEM GLO-30:** regional elevation/slope context, not detailed engineering survey.
- **ESA WorldCover:** reference land-cover classification, not cadastral or statutory land-use evidence.
- **NASA POWER / PVGIS:** optional solar-resource context, not a substitute for actual plant meter readings.

## Required provenance fields

For every layer retain: publisher, dataset/service name, stable layer ID, URL, licence/terms, retrieval date, data vintage, coordinate reference system, spatial extent, resolution/scale, attribute schema, processing steps, validation status and known limitations.

## Project and energy evidence still required

Public map layers do not provide the evidence required for carbon MRV. Obtain authorised, project-specific records as applicable:

1. Project registration, ownership/rights, capacity, technology and commissioning records.
2. Project boundary, land rights, permits and ownership of environmental attributes.
3. Calibrated generation and export meter records, meter IDs and replacement/calibration history.
4. Utility interconnection approval, energy statements and settlement records.
5. Authoritative land, forest, wildlife, wetlands, flood and other statutory boundaries.
6. Applicable methodology and official grid emission factor with geography and vintage.
7. Renewable energy certificate and other environmental-attribute claims.

## Limitations and safe use

- Public GIS coverage can be incomplete, stale or misclassified; missing features do not prove absence on the ground.
- A mapped substation does not establish available capacity, feeder load, voltage constraints, dispatch or a project's electrical connection.
- Land-use tags and satellite classification are not title or statutory approvals.
- A proximity analysis is not an evacuation study or engineering approval.
- Modelled generation is not metered generation.
- Do not publish a statewide completeness percentage without a reconciled authoritative reference inventory.
- Record each data refresh and preserve the exact source version used in a screening or MRV report.

## Licensing and attribution

Retain each provider's current licence and attribution requirements with the dataset. For OSM-derived data, attribution must include © OpenStreetMap contributors and ODbL obligations apply. Review Overture and Copernicus terms for the exact release used. Do not assume every layer has the same redistribution terms.
