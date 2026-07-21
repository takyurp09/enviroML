# Contributing

Contributions that improve reproducibility, documentation, tests, or environmental interpretation are welcome.

## Development setup

```bash
git clone https://github.com/takyurp09/enviroML.git
cd enviroML
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Raw inputs must be staged locally according to `data/README.md`; do not commit restricted or unverified datasets.

## Before opening a pull request

```bash
ruff check src tests
python src/run_pipeline.py   # requires local source data
python tests/test_outputs.py
git diff --check
```

Update generated tables and figures whenever an analytical change affects results. Explain changes to methods, validation, or reported metrics in the pull-request description.

## Scope and conduct

- Keep analytical claims traceable to generated outputs.
- Distinguish observed results from interpretation.
- Document data provenance and redistribution terms.
- Never commit credentials, private records, or course materials without permission.
