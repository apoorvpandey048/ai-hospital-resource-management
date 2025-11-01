# Implementation Guide

This guide documents file layout, coding style, and where to extend modules.

Key locations:
- `modules/` — library code for algorithms and models
- `app/` — UI and API entrypoints
- `data/` — sample CSV/JSON datasets
- `tests/` — small test suite

When changing package layout, update import paths in `run_demo.py` and tests.
