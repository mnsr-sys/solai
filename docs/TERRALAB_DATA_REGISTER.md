# Telangana geospatial data register and extraction log

## Product purpose

SolAI is a substation-first geospatial intelligence platform for solar deployment planning across Telangana. This register preserves the initial Hyderabad-area extract and records the statewide layers and official datasets needed to expand coverage. The initial extraction area is a data-coverage starting point, not a limit on the product geography.

The geospatial intelligence layer is the core product. Generation monitoring and carbon MRV are downstream extensions for projects that move from candidate-site screening to development and operation.

## Initial extracted coverage

The initial land, water and protected-feature extract is centred at **17.360588° N, 78.474061° E** in Hyderabad, Telangana, with a **15 km radius** (approximately 900 km²). Roads were extracted separately at a **2.5 km radius** (approximately 25 km²) because the wider roads query exceeded the 20,000-feature extraction limit.

| Layer | Features extracted | Source / release | Coverage |
|---|---:|---|---|
| Land use | 2,893 | OpenStreetMap planet 2026-11-16 | 15 km radius |
| Waterways | 309 | OpenStreetMap planet 2026-11-16 | 15 km radius |
| Water areas | 343 | OpenStreetMap planet 2026-11-16 | 15 km radius |
| Protected areas | 5 | OpenStreetMap planet 2026-11-16 | 15 km radius |
| Roads | 16,172 | Overture Maps 2026-11-18 | 2.5 km radius |

The combined land/water/protected extract was not truncated. The roads extract was not truncated. These counts describe the saved extraction result, not completeness of real-world features.

## Elevation extract

- Source: Copernicus DEM GLO-30 surface model.
- Returned grid: approximately 31 m.
- Extent: approximately 900 km².
- Elevation range: 458–633 m.
- Mean elevation: 542 m.
- Vertical reference: EGM2008 geoid.
- Derived outputs generated: DEM, hillshade and slope GeoTIFFs.

Required notice: Produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. The organisations in charge of the Copernicus programme by law or by delegation do not incur any liability for any use of this product.

## Substation and grid context

Two distinct sources/approaches must remain visible in SolAI:

1. **TGRAC public ArcGIS electric-transmission substation layer.** The dashboard fetches all object IDs exposed by the published RRR electric-transmission `Sub Stations` layer (MapServer layer 8), then retrieves features in batches. This layer belongs to the Regional Ring Road (RRR) service and is corridor/project-context coverage—not a certified statewide inventory of every Telangana substation. The interactive map queries:
   `https://tgrac.telangana.gov.in/arcgis/rest/services/RRR_Folder/RRR/MapServer/8`
   The dashboard displays its mapped point records and published attributes. This is a public GIS reference, not a certified exhaustive TSTRANSCO/DISCOM inventory.
2. **Earlier 20 km Hyderabad-area OSM power-feature extract.** This extract contains 2,889 mapped power features. It is useful as a secondary discovery layer, but is not a verified/exhaustive TSTRANSCO inventory and does not establish voltage, operational status, feeder connectivity or hosting capacity.

Do not silently merge these into one “official substation inventory”. Preserve source, layer ID, feature ID, attributes, geometry, retrieval date and confidence for every record. De-duplicate only with documented matching rules and retain source lineage.

## Data-quality limitations

- OSM/Overture completeness varies. A missing mapped feature does not prove absence on the ground.
- Only five protected-area features were mapped in the initial 15 km extract. This is inadequate for statutory exclusion screening; obtain authoritative forest, wildlife, wetlands, eco-sensitive-zone and other government boundaries.
- Land-use tags and water features are not cadastral/title evidence. Verify ownership, encumbrances, access, permitted use and water/flood buffers with authoritative records.
- Roads support preliminary proximity/corridor analysis, not surveyed transmission right-of-way.
- Public substation points do not provide feeder load curves, transformer ratings, protection settings, voltage limits, existing generation register, evacuation cost schedule or spare hosting capacity.
- DEM is for regional terrain screening, not detailed grading, drainage or geotechnical design.
- A nearby substation does not prove that a candidate parcel can connect to it or export power.

## Licensing and attribution

- OSM-derived data: ODbL 1.0; commercial use is allowed with attribution. A database published from OSM-derived data must remain under ODbL; maps, images and reports may use another licence. Attribution: © OpenStreetMap contributors, modified by TerraLab.
- Overture Maps extract: TerraLab reports ODbL 1.0 and attribution to OpenStreetMap contributors, Overture Maps Foundation and TomTom. Review the source release terms before redistribution.
- Copernicus DEM: reproduction, distribution and modification are allowed subject to retaining the required notice above.
- Retain the actual licence and attribution text with each source release; do not assume every layer has identical terms.

## Next-stage Telangana extraction

Expand district by district across Telangana, not by assuming that the initial Hyderabad-area extent represents statewide coverage.

1. Extract and catalogue land use, land cover, water bodies, waterways, roads, settlements and constraints by district.
2. Obtain official TSTRANSCO/DISCOM substation, transformer and feeder records, including voltage, ratings, load curves and existing solar connections where access is authorised.
3. Add authoritative parcel/cadastral, forest, wildlife, wetlands, flood, irrigation and statutory exclusion boundaries.
4. Add Sentinel-2 land classification with product IDs, dates, cloud masking, class definitions and validation samples.
5. Extend Copernicus DEM terrain screening and derive slope, aspect and drainage indicators.
6. Build a PostgreSQL/PostGIS database with source lineage, geometry validation, spatial indexes, dataset vintages and refresh logs.
7. Generate candidate land polygons and rank them against land availability, land-cover constraints, water/flood exposure, slope, shading, solar resource and grid proximity.
8. Add evacuation and hosting-capacity assessment only when official utility engineering data is available.

## How MRV extends the geospatial product

The geospatial engine discovers and ranks candidate sites. Once a project is selected, developed and operational, the MRV layer attaches to the same project and asset records:

- planning: estimated capacity and annual yield from screened usable area and explicit assumptions;
- development: project boundary, ownership/rights, permits, interconnection and commissioning evidence;
- operations: actual generation/export meter readings, calibration, outages, curtailment and utility reconciliation;
- climate accounting: methodology-specific eligible electricity, baseline, project emissions and leakage;
- reporting: traceable monitoring reports and evidence packages for independent validation/verification.

Keep planning estimates separate from metered generation, indicative avoided emissions, verified reductions and issued credits. SolAI does not itself issue carbon credits.
