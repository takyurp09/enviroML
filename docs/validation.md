# Validation and evidence map

This page connects each scientific claim to its evaluation design, metric, output table, and diagnostic figure.

## Evaluation safeguards

- Transformations and imputers are fitted inside model pipelines.
- Classification splits preserve class proportions.
- Hyperparameter tuning occurs within training data.
- Final classification and regression metrics use untouched test observations.
- Climate records use a chronological split instead of random shuffling.
- Cluster robustness is tested with 200 feature-bootstrap refits.
- A fixed seed (`638`) makes stochastic results repeatable.

## Evidence map

| Claim | Metric | Generated table | Diagnostic |
|---|---|---|---|
| Random forest improves chlorophyll prediction over linear baselines | Test RMSE, MAE, R² | [`02_regression_comparison.csv`](../results/tables/02_regression_comparison.csv) | [`02_regression_validation.png`](../results/figures/02_regression_validation.png) |
| Ecological regions are distinguishable from water quality | Repeated-CV and test balanced accuracy | [`03_classification_comparison.csv`](../results/tables/03_classification_comparison.csv) | [`03_confusion_matrix.png`](../results/figures/03_confusion_matrix.png) |
| Predictor relevance can be evaluated outside training data | Test-set permutation importance | [`04_permutation_importance.csv`](../results/tables/04_permutation_importance.csv) | [`04_feature_importance.png`](../results/figures/04_feature_importance.png) |
| Two station regimes receive the strongest silhouette support | Silhouette coefficient | [`05_cluster_selection.csv`](../results/tables/05_cluster_selection.csv) | [`05_clustering_diagnostics.png`](../results/figures/05_clustering_diagnostics.png) |
| Regime assignments are moderately robust | Bootstrap adjusted Rand index | [`06_cluster_stability.csv`](../results/tables/06_cluster_stability.csv) | [`05_clustering_diagnostics.png`](../results/figures/05_clustering_diagnostics.png) |
| Seasonal linear structure generalizes better than the tested forest to the final quarter | Chronological test RMSE, MAE, R² | [`07_climate_time_split.csv`](../results/tables/07_climate_time_split.csv) | [`06_climate_time_validation.png`](../results/figures/06_climate_time_validation.png) |

## Metric definitions

- **MAE:** mean absolute prediction error in the target’s original units.
- **RMSE:** square root of mean squared error; penalizes large errors more heavily than MAE.
- **R²:** proportion of test-set variance explained relative to a mean-prediction baseline. Negative values indicate performance worse than that baseline.
- **Balanced accuracy:** mean recall across classes, used because ecological regions are not equally represented.
- **Silhouette coefficient:** within-cluster cohesion relative to nearest-cluster separation; higher is better.
- **Adjusted Rand index (ARI):** chance-adjusted agreement between two cluster assignments; 1 indicates identical partitions.

## Interpretation boundary

The observation-level estuary holdout evaluates interpolation among recorded stations and periods. It does not establish transfer to an unseen station. The one-year climate split evaluates later-period prediction within 2000, not interannual forecasting. These boundaries are stated so model metrics are not interpreted more broadly than the design supports.
