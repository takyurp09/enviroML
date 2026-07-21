# Data card

## Delaware Estuary observations

- **Unit:** station-time water-quality observation
- **Coverage in analysis:** 3,346 records across 22 station files
- **Variables:** timestamps, station identifiers, water temperature, pH, salinity, nutrients, suspended solids, dissolved oxygen, and chlorophyll-a
- **Spatial metadata:** 22 station coordinates derived from the course-provided `DE_stations.mat`
- **Processing:** numeric coercion, broad physical screens, and model-pipeline median imputation
- **Known constraints:** irregular frequency, missing values, differing measurement conditions, and incomplete public redistribution metadata

## Bangladesh ERA5 data

- **Unit:** six-hourly grid-cell observation
- **Coverage:** 200 grid cells (18 longitudes × 22 latitudes with land-mask gaps), 732 time steps during 2000
- **Variables:** 2 m temperature, wind components, evaporation, surface solar radiation, surface pressure, precipitation, latitude, longitude, and time
- **Processing:** Celsius conversion, cyclic temporal features, chronological separation, and grid-cell error aggregation
- **Known constraints:** one year, reanalysis rather than direct station observations, and no external observational validation

## Access and rights

Raw inputs are not committed. Public redistribution requires confirmation of the estuary provider and exact Copernicus/ECMWF retrieval metadata. The included coordinate table is non-sensitive metadata used for visualization. See `data/README.md` and `docs/data-and-ethics.md`.
