# Model card

## Intended use

enviroML is an educational and research demonstration of environmental machine-learning workflows. It is intended for methodological review, skills assessment, and reproducible comparison—not operational forecasting or regulatory decision-making.

## Tasks and leading models

| Task | Leading evaluated model | Primary test design |
|---|---|---|
| Chlorophyll-a regression | Random forest | Observation holdout; station-grouped CV; later-year holdout |
| Estuary-region classification | Multinomial logistic regression | Repeated stratified CV plus untouched test set |
| Water-quality regime discovery | K-means, k=2 | Silhouette selection plus feature-bootstrap stability |
| ERA5 temperature prediction | Seasonal ridge regression | Chronological final-quarter holdout plus expanding-window CV |

## Inputs and outputs

Estuary models use temperature, pH, salinity, nitrogen, phosphorus, suspended solids, and dissolved oxygen. Outputs are chlorophyll-a predictions, region probabilities/classes, or station-regime assignments. The climate model uses location, wind, evaporation, solar radiation, pressure, precipitation, and cyclic time features to predict 2 m air temperature.

## Performance

The authoritative metrics are generated in `results/tables/`. Headline results and confidence intervals are summarized in the README and connected to evidence in `docs/validation.md`.

## Limitations

- The dataset is modest, observational, irregularly sampled, and potentially affected by non-random missingness.
- Station labels encode location; classification does not imply causal ecological attribution.
- Station-grouped validation is stronger than random splitting but covers the same estuarine system.
- The climate case study contains one year of ERA5 data and does not establish interannual generalization.
- Prediction intervals for individual observations are not calibrated.

## Prohibited interpretation

Do not use these models to issue environmental alerts, determine compliance, allocate resources, or make safety-critical decisions without new data governance, external validation, uncertainty calibration, monitoring, and expert review.
