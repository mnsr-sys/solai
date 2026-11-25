# Telangana data sources and provenance

## Open geospatial context

Use free/open sources for discovery and spatial context, retaining licence and attribution:

- **OpenStreetMap:** roads, mapped land-use tags, waterways and mapped infrastructure. ODbL obligations and attribution apply.
- **Overture Maps:** supplementary geospatial features where its release terms fit the use case.
- **Copernicus Sentinel-2:** optical imagery for land-cover and change context. Record scene/product ID, sensing date, processing level, cloud cover, resolution and licence/attribution.
- **Copernicus DEM GLO-30:** regional elevation, slope and terrain context; retain the required product notice.
- **ESA WorldCover:** reference land-cover layer; not a cadastral or statutory land-use record.
- **NASA POWER / PVGIS:** optional solar-resource context; not a substitute for plant meter readings.

## Authoritative project and energy evidence

For carbon MRV, geospatial context is not enough. Obtain authorised, project-specific evidence as applicable:
- solar project registration, capacity, technology and commissioning documents;
- project boundary, land rights and ownership of environmental attributes;
- inverter and calibrated generation-meter records;
- export/import meters and utility energy statements;
- interconnection approval and relevant grid/settlement records;
- meter calibration certificates, replacements and maintenance logs;
- applicable grid emission factor and methodology references;
- records of renewable energy certificates or other environmental-attribute claims.

Utility or owner data must only be accessed with appropriate permission. Do not represent public map features as verified substations, operating assets or connected solar projects.

## Free/open processing stack

- QGIS, GDAL, Rasterio, GeoPandas and Shapely for geospatial preparation.
- PostgreSQL + PostGIS for spatial data.
- Python + FastAPI for APIs and calculation services.
- CSV ingestion initially; secure APIs/telemetry when authorised and available.

## Provenance fields

For each dataset or evidence record retain publisher/source, stable identifier, licence or access authority, retrieval date, data vintage, spatial resolution, CRS, extent, units, timezone, processing steps, validation status and known limitations.

## Key boundaries

- Open mapping is incomplete and is not land-title evidence.
- A mapped substation does not establish its operational status, spare capacity or electrical relationship to a solar plant.
- Installed capacity and satellite imagery do not prove actual electricity generation.
- Modelled generation is not a substitute for meter data in an MRV calculation unless the applicable methodology expressly permits it.
- Grid emission factors must be appropriate to the selected methodology, geography, period and electricity boundary.
- Estimated avoided emissions are not verified reductions or issued credits.
