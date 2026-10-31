# GaitSense Frontend

This React application is the GaitSense clinical portal UI for uploading gait recordings, reviewing FoG sessions, browsing subjects, and viewing statistics. It uses the development proxy at `http://127.0.0.1:8000` for local `/api` requests.

## Run locally

```powershell
npm install
npm start
```

For a deployed backend, set `REACT_APP_API_URL` before `npm run build`.

## Routes

- `/` - Landing page
- `/portal` - Portal home
- `/upload` - Recording upload
- `/subjects` - Subject list
- `/subjects/:subjectId` - Subject profile
- `/sessions/:sessionId` - Session analysis
- `/stats` - Population statistics
