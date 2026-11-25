# Hyderabad pilot geospatial data register

Purpose: record public geospatial screening layers for Reker SolAI. These are preliminary screening inputs, not utility-validated inventory, land-title evidence, statutory exclusion boundaries or engineering approval.

## Cost
TerraLab documentation states 100 free MCP/API calls per month, then pay-per-call from a prepaid balance, with no subscription. Check the current account balance/pricing before scaling. The calls made for this pilot returned `call_usage.state = not_counted`.
Pricing: https://terra-lab.ai/docs/pricing

## Pilot extent
Centre: 17.360588 N, 78.474061 E (Hyderabad, Telangana). Main radius: 15 km (~900 km²). Roads radius: 2.5 km (~25 km²), because the larger road query exceeded the 20,000-feature extract limit.

## Extracts
| Layer | Features | Source/release |
|---|---:|---|
| Land use | 2,893 | OpenStreetMap planet 2026-11-16 |
| Waterways | 309 | OpenStreetMap planet 2026-11-16 |
| Water areas | 343 | OpenStreetMap planet 2026-11-16 |
| Protected areas | 5 | OpenStreetMap planet 2026-11-16 |
| Roads | 16,172 | Overture Maps 2026-11-18 |

Combined land/water/protected extract was not truncated. Roads extract was not truncated.

## Elevation
Copernicus DEM GLO-30 surface model; returned grid approximately 31 m; extent ~900 km². Elevation range 458–633 m, mean 542 m (EGM2008 geoid). DEM, hillshade and slope GeoTIFFs were generated.

Required notice: Produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. The organisations in charge of the Copernicus programme by law or by delegation do not incur any liability for any use of this product.

## Licences and attribution
OSM-derived data: ODbL 1.0; commercial use allowed with attribution. A database published from OSM-derived data must remain under ODbL; maps, images and reports may use another licence. Attribution: © OpenStreetMap contributors, modified by TerraLab.
Overture Maps extract: TerraLab reports ODbL 1.0 and attribution to OpenStreetMap contributors, Overture Maps Foundation and TomTom. Review the source release terms before redistribution.
Copernicus DEM: reproduction, distribution and modification allowed subject to retaining the required notice above.

## Limitations
- OSM/Overture completeness varies. A missing mapped feature does not prove absence on the ground.
- Only five protected-area features were mapped in this pilot extent. This is inadequate for statutory exclusion screening; obtain authoritative forest, wildlife, wetlands, eco-sensitive-zone and other government boundaries.
- Land-use tags and water features are not cadastral/title evidence. Verify ownership, encumbrances, access, permitted use and water/flood buffers with authoritative records.
- Roads support preliminary proximity/corridor analysis, not surveyed transmission right-of-way.
- A separate 20 km Hyderabad OSM power extract contains 2,889 mapped features, but is not a verified/exhaustive TSTRANSCO inventory or evidence of operational status/hosting capacity.
- No feeder load curves, transformer ratings, protection settings, voltage limits, existing generation register, evacuation cost schedule or land-title data are present in these extracts.
- DEM is for regional terrain screening, not detailed grading or drainage design.

## Next data requirements
1. TSTRANSCO/DISCOM verified substation, transformer and feeder data, including interval load curves and existing solar connections.
2. Official Telangana land parcels, land-use, forest, wildlife, wetlands, flood and waterbody boundaries.
3. Sentinel-2 imagery with documented classification and validation.
4. Site visits and revenue-record verification before feasibility claims.
