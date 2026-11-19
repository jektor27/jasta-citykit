# Demo data

This folder contains a tiny synthetic export for an offline demonstration.
Names, addresses and phones are invented. It is not a real city directory.

Run:

```bash
python -m citykit dedupe --in examples/gusev-open-data/shops.json --out data/unique.json
python -m citykit build --in data/unique.json --out site/ --base-url https://example.org
python -m citykit audit site/ --json report.json
```
