# AI Hospital Resource Management (Demo)

This repository contains a demo Python project showing multiple AI-driven modules for hospital resource management.

Project layout (final)

```
ai-hospital-resource-management/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   ├── patients.csv
│   ├── beds.csv
│   ├── staff.csv
│   └── medical_rules.json
├── modules/        # core library modules (importable)
│   ├── bed_allocation.py
│   ├── scheduling_csp.py
│   ├── expert_system.py
│   ├── fuzzy_triage.py
│   ├── genetic_optimizer.py
│   ├── ml_predictor.py
│   ├── nn_classifier.py
│   └── nlp_chatbot.py
├── app/            # UI and API entrypoints
│   ├── dashboard_streamlit.py
│   └── api_flask.py
├── tests/
│   └── test_modules.py
└── docs/
	├── project_report.md
	└── implementation_guide.md
```

Quick start (Windows PowerShell)

1. Create and activate a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the demo runner (exercises modules with small examples):

```powershell
python run_demo.py
```

3. Run the Streamlit dashboard (optional):

```powershell
streamlit run app/dashboard_streamlit.py
```

4. Run the Flask API (development, optional):

```powershell
flask run --app app.api_flask
```

Tests

Run the simple import tests:

```powershell
python -m pytest -q
```

Notes

- The repository uses a clean, single source-of-truth layout: library code is under `modules/` and app entrypoints live in `app/`.
- The ML modules use scikit-learn. To avoid heavy test dependencies, the project tolerates scikit-learn being absent at import time and raises a clear error if you attempt to train/predict without it. Install scikit-learn via `pip install scikit-learn` to use ML features.
- This is an educational demo; algorithms are intentionally simple.

Continuous Integration

A GitHub Actions workflow is included to run the test suite on push and pull requests. See `.github/workflows/ci.yml`.

Next steps

- Improve scheduling CSP with OR-Tools or python-constraint.
- Replace the regex chatbot with an embeddings + semantic search solution.
- Add more realistic sample datasets and unit tests for algorithm outputs.

