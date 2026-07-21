# Data access

Raw inputs are intentionally excluded from the public repository because the archived course materials do not contain complete redistribution terms.

To reproduce the analyses locally, place the following inputs under `data/raw/`:

```text
data/raw/
├── estuary/
│   └── station-*.csv
└── climate/
    └── era5_bangladesh_2000.csv
```

The estuary files require the schema documented in `docs/data-and-ethics.md`. The climate file requires columns `time`, `t2m`, `u10`, `v10`, `e`, `ssr`, `sp`, and `tp`.

Before a fully public reproducibility release, add authoritative download instructions and exact source citations after confirming the original providers and licenses.
