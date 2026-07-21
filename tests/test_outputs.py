from pathlib import Path
import json, pandas as pd
root=Path(__file__).resolve().parents[1]
s=json.loads((root/"results/tables/project_summary.json").read_text())
assert s["records"] > 1000 and s["stations"] >= 15
assert 0 <= s["classification"]["test_balanced_accuracy"] <= 1
assert s["regression"]["RMSE"] > 0 and s["climate"]["RMSE_C"] > 0
assert s["robust_validation"]["station_cv_RMSE_mean"] > 0
assert len(list((root/"results/figures").glob("*.png"))) >= 9
for f in (root/"results/tables").glob("*.csv"): assert len(pd.read_csv(f)) > 0
print("All enviroML smoke tests passed.")
