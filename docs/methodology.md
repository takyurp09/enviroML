# Methodology and validation

## Estuary data preparation

Station CSV files are concatenated into a common schema and timestamps are parsed explicitly. Eight analysis variables are converted to numeric form. Broad physical screens flag implausible values as missing; median imputation is learned inside each model pipeline, preventing information from the test set from determining training transformations.

The principal predictors are water temperature, pH, salinity, nitrogen, phosphorus, total suspended solids, and dissolved oxygen. Chlorophyll-a is the regression target. Station identifiers supply the course-defined ecological-region labels.

## Regression

Linear regression, ridge regression, and random forest regression are compared on the same held-out quarter of observations. RMSE is the primary selection measure, supported by MAE and R². This extension replaces visual-only fit assessment with directly comparable out-of-sample metrics.

## Classification

The training partition is assessed with repeated stratified five-fold cross-validation. Logistic regression, a grid-searched RBF-SVM, random forest, and gradient boosting are compared using balanced accuracy, which gives equal importance to each ecological region. The final score comes from a stratified 25% test partition not used for model fitting. A row-normalized confusion matrix exposes region-specific errors.

Permutation importance is computed on held-out data, not training data. It therefore estimates how much predictive performance is lost when each feature’s information is disrupted.

## Clustering

Station-level medians summarize multivariate water quality. Variables are standardized before K-means. Candidate solutions from k=2 through k=6 are compared by silhouette score. Robustness is assessed through 200 feature-bootstrap refits and summarized with the adjusted Rand index (ARI), which measures agreement while correcting for chance.

## Climate prediction

The ERA5 case study predicts 2 m temperature from wind components, evaporation, solar radiation, surface pressure, precipitation, and cyclic hour/day-of-year encodings. Because observations are temporal, the first 75% of the series trains the models and the final 25% is held out. This chronological design is stricter—and more realistic—than randomly mixing past and future records.

The dense sub-daily grid is regularly thinned by a factor of four for portable runtime while preserving temporal order. Seasonal ridge and random forest models are compared by MAE, RMSE, and R².

## Reproducibility

All stochastic models use a fixed seed. Every reported metric is written to CSV or JSON, and every principal claim in the README can be traced to a generated table. Smoke tests check record coverage, metric bounds, figure creation, and non-empty outputs.
