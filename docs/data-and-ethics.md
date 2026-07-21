# Data, limitations, and responsible use

## Delaware Estuary monitoring data

The station files were supplied for MAST 638 and appear to derive from Delaware Estuary water-quality monitoring records (the course files use CEMA naming). The archived course directory does not contain a definitive public-download citation or redistribution license. Before publishing this repository publicly, confirm the authoritative provider, citation, and redistribution terms. If redistribution is not permitted, remove `data/raw/estuary` and provide a documented acquisition script or access instructions.

## ERA5 climate data

The capstone file contains ERA5 variables for Bangladesh during 2000, including 2 m temperature, wind components, evaporation, surface solar radiation, surface pressure, and precipitation. ERA5 is produced by ECMWF’s Copernicus Climate Change Service. A public release should add the exact CDS request, dataset version, retrieval date, and Copernicus attribution associated with the original download.

## Analytical limitations

- The estuary split is observation-level; repeated measurements from a station may occur in both training and test sets. A station-held-out design would be needed to claim transfer to unseen stations.
- Environmental sampling is irregular and missingness may not be random.
- Region labels are station-derived, so classification performance partly reflects stable spatial gradients rather than causal ecological mechanisms.
- The clustering uses station medians and therefore compresses event-scale and seasonal variability.
- The climate exercise covers one year and one spatial grid, limiting claims about interannual or spatial generalization.
- No result should be treated as an operational water-quality or weather forecast.

## Responsible interpretation

Metrics document technical competence and comparative model behavior. They do not establish causality, regulatory compliance, or deployment readiness. Any operational use would require source verification, stronger spatial/temporal validation, uncertainty calibration, monitoring for distribution shift, and domain-expert review.
