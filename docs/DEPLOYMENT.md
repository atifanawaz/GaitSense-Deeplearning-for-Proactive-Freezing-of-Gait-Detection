# Deployment

## Azure App Service backend

Deploy the contents of `clinical_portal/azure_package` as a zip package, with `requirements.txt` and `backend/` at the archive root. The package uses CPU-only PyTorch 2.2.2 from the PyTorch CPU index:

```text
--extra-index-url https://download.pytorch.org/whl/cpu
torch==2.2.2+cpu
```

Configure these App Service settings:

```text
SCM_DO_BUILD_DURING_DEPLOYMENT=true
WEBSITES_PORT=8000
DB_PATH=/home/data/fog_portal.db
PYTHONUTF8=1
WEBSITES_CONTAINER_START_TIME_LIMIT=600
ALLOWED_ORIGINS=https://gaitsense-fogtrack.netlify.app
```

Use this startup command:

```text
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

The backend may be stopped or slow on the first request after idle.

## Netlify frontend

Set the build environment variable:

```text
REACT_APP_API_URL=https://fogtrack-backend-gsb2ezcwdehscee6.centralindia-01.azurewebsites.net
```

Build the frontend from `clinical_portal/frontend` with `npm run build`, then deploy the resulting `build` folder. The `public/_redirects` file is copied into the build and contains:

```text
/*  /index.html  200
```
