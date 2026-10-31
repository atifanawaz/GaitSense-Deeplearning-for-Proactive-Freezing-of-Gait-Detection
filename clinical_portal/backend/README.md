# GaitSense Clinical Portal Backend

The GaitSense backend is a FastAPI service that analyzes gait-recording CSV
files, runs the trained FOG and trigger-classification models, stores clinical
session results in SQLite, and exposes reports and analytics to the React
frontend.

The backend is intended to be started from the `clinical_portal` directory,
not from this directory directly.

## Responsibilities

- Accept recording uploads and medication status.
- Validate and parse gait CSV data.
- Load the trained FOG detection and trigger-classification models.
- Detect FOG windows and summarize FOG episodes.
- Classify episode triggers: Start Hesitation, Turn, and Walking.
- Store subjects, sessions, episodes, and window results in SQLite.
- Support episode annotations.
- Generate PDF reports and CSV exports.
- Provide subject progression and population statistics.

## Backend layout

```text
backend/
├── main.py                 # FastAPI application and lifecycle startup
├── requirements.txt        # Pinned Python dependencies
├── fog_portal.db           # SQLite application database
├── data/
│   ├── subjects.csv        # Subject demographic and clinical metadata
│   └── tdcsfog_metadata.csv
├── db/
│   └── database.py         # SQLAlchemy engine, models, and DB sessions
├── models/
│   ├── architectures.py   # Model architecture definitions
│   └── loader.py           # Model registry and weight loading
├── model_weights/
│   ├── dl_fog_model_best.pth
│   └── trigger_dl_model.pth
├── routers/
│   ├── upload.py
│   ├── sessions.py
│   ├── subjects.py
│   └── statistics.py
└── services/
    ├── inference.py
    ├── metadata_parser.py
    ├── report.py
    └── crud.py
```

## Requirements

The pinned dependency list is maintained in
[`requirements.txt`](./requirements.txt). It includes:

- FastAPI and Uvicorn
- Python multipart upload support
- SQLAlchemy and aiosqlite
- PyTorch
- NumPy, pandas, scikit-learn, and joblib
- Pillow
- ReportLab for PDF generation
- python-dotenv

## Installation

From the `clinical_portal` directory, create the local virtual environment
and install the backend dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

The virtual environment belongs inside `clinical_portal` and is ignored by
Git. Do not install these dependencies into the global Python installation.

## Start the API

From `clinical_portal`:

```powershell
.\venv\Scripts\python.exe -m uvicorn backend.main:app --port 8000
```

The API is available at:

```text
http://127.0.0.1:8000
```

On Windows consoles using a `cp1252` encoding, configure UTF-8 output before
starting the server because model-loader startup messages contain checkmark
characters:

```powershell
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
.\venv\Scripts\python.exe -m uvicorn backend.main:app --port 8000
```

The frontend development proxy targets the same address:
`http://127.0.0.1:8000`.

## Health check

```powershell
curl.exe -sS -i http://127.0.0.1:8000/api/health
```

Successful response:

```json
{
  "status": "ok",
  "models_loaded": true,
  "device": "cpu"
}
```

The API initializes the SQLite database and loads both model registries
during application startup. If model loading fails, the startup log reports
the missing or invalid weight file.

## Model weights

The loader reads weights from:

```text
backend/model_weights/dl_fog_model_best.pth
backend/model_weights/trigger_dl_model.pth
```

The files must remain in this directory unless the paths in
[`models/loader.py`](./models/loader.py) are intentionally changed and
verified. The model architectures in
[`models/architectures.py`](./models/architectures.py) must remain compatible
with the saved state dictionaries.

Verified SHA256 values:

```text
dl_fog_model_best.pth
875F18D5D0E71890C8A29CF67DAFDE82AB778D5C7C9BBD4F56BB03171AC61B9F

trigger_dl_model.pth
5A2A705B5128C8E4A8FF22085F4BA2DC28127954DCF01690200F77C72A5F05E9
```

To verify a local copy:

```powershell
Get-FileHash backend\model_weights\*.pth -Algorithm SHA256
```

## Metadata and database

The upload router loads metadata from:

```text
backend/data/subjects.csv
backend/data/tdcsfog_metadata.csv
```

The SQLite database is:

```text
backend/fog_portal.db
```

The database path is resolved relative to the backend package by
[`db/database.py`](./db/database.py). Database tables are initialized during
application startup. The database may change after uploads, annotations, or
other API operations, so preserve a backup before replacing it.

## API routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/api/health` | Report API and model readiness |
| `POST` | `/api/upload` | Analyze a gait CSV upload |
| `GET` | `/api/sessions/{session_id}` | Retrieve session analysis |
| `PATCH` | `/api/sessions/{session_id}/episodes/{episode_id}/annotate` | Save an episode annotation |
| `GET` | `/api/sessions/{session_id}/report` | Download a PDF session report |
| `GET` | `/api/sessions/{session_id}/export-csv` | Download episode results |
| `GET` | `/api/subjects/` | List subjects |
| `GET` | `/api/subjects/{subject_id}` | Retrieve a subject profile |
| `GET` | `/api/subjects/{subject_id}/progression` | Retrieve visit progression |
| `GET` | `/api/subjects/{subject_id}/report` | Download a progression report |
| `GET` | `/api/stats/` | Retrieve population statistics |

Interactive API documentation is available when the server is running:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Upload requirements

The upload endpoint expects:

- A gait recording CSV file.
- `medication_status` set to `on` or `off`.
- An optional clinical note.

The uploaded filename is used when matching recording metadata. The
corresponding metadata and subject records must be available in the backend
CSV files for complete demographic and medication information.

## Frontend integration

The React frontend is in [`../frontend/`](../frontend/). Its API client keeps
requests under `/api`, and the frontend development proxy forwards them to
port `8000`.

Start the frontend separately:

```powershell
cd ..\frontend
npm install
npm start
```

The frontend normally runs on `http://localhost:3000`.

## Verification commands

From `clinical_portal`:

```powershell
.\venv\Scripts\python.exe -c "import backend.main"
.\venv\Scripts\python.exe -m uvicorn backend.main:app --port 8000
curl.exe http://127.0.0.1:8000/api/health
```

The import command verifies module loading. The health check verifies that
the application can initialize the database and load the model weights.

## Troubleshooting

### `ModuleNotFoundError`

Confirm that the project virtual environment is being used:

```powershell
.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### Model files not found

Confirm both `.pth` files exist under `backend\model_weights` and verify
their SHA256 values. Do not substitute weights from a different architecture
without retraining or validating compatibility.

### Windows console encoding error

Set `PYTHONUTF8` and `PYTHONIOENCODING` to `utf-8` before starting Uvicorn,
as shown above.

### Port already in use

Start the API on another port for local testing:

```powershell
.\venv\Scripts\python.exe -m uvicorn backend.main:app --port 8001
```

If the port changes, update the frontend proxy or use the corresponding
development configuration.

## Security and data handling

This backend processes potentially sensitive clinical data. Before sharing
the application or its outputs:

- Follow institutional and dataset-specific data-governance requirements.
- Do not expose the API publicly without authentication and transport
  security.
- Protect the SQLite database, uploaded recordings, reports, and model files.
- Avoid committing private recordings, credentials, or generated reports.
- Treat model predictions as decision-support output, not a diagnosis.
