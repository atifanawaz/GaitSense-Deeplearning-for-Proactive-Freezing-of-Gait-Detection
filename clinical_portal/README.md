# GaitSense Clinical Portal

The portal combines a FastAPI backend for FoG analysis with a React frontend for clinical review.

## Backend

From `clinical_portal` in PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
$env:PYTHONUTF8="1"
python -m uvicorn backend.main:app --port 8000
```

The API is available at `http://127.0.0.1:8000`. Interactive docs are at `/docs`.

## Frontend

In a second terminal:

```powershell
cd clinical_portal\frontend
npm install
npm start
```

The React development server runs on port 3000 and its proxy sends `/api` requests to `http://127.0.0.1:8000`.

## API routes

- `GET /api/health`
- `POST /api/upload`
- `GET /api/sessions/{session_id}`
- `PATCH /api/sessions/{session_id}/episodes/{episode_id}/annotate`
- `GET /api/sessions/{session_id}/report`
- `GET /api/sessions/{session_id}/export-csv`
- `GET /api/subjects/`
- `GET /api/subjects/{subject_id}`
- `GET /api/subjects/{subject_id}/progression`
- `GET /api/subjects/{subject_id}/report`
- `GET /api/stats/`

## Environment variables

- `DB_PATH`: SQLite file path. Defaults to the backend's current `fog_portal.db` location.
- `ALLOWED_ORIGINS`: comma-separated CORS origins. Defaults to the local React origins.
- `REACT_APP_API_URL`: frontend API origin. The frontend appends `/api`; unset uses the local `/api` path and proxy.
- `PYTHONUTF8`: set to `1` for UTF-8 Python output.
