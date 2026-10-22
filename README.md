# CoSight

Grounded marketing analytics for CBS Marketing & Communications. CoSight aggregates social, web, search, and email metrics, streams AI briefs with citations, and runs an agentic chat that may only cite figures returned by data connectors.

This repository was split from [Cowork](https://github.com/przhevalskiy/Cowork) as a standalone deployable app.

## Stack

- **Frontend:** React 19, Vite, TypeScript (`frontend/`)
- **Backend:** FastAPI (`backend/`)
- **Database:** Supabase (`backend/supabase_schema.sql`)

## Local development

### Prerequisites

- Python 3.11+
- Node.js 20+

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in credentials
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
echo 'VITE_API_URL=http://localhost:8000' > .env
npm run dev
```

Open http://localhost:5173 (Vite proxies `/api` to the backend in dev).

### One command (macOS)

From the repo root:

```bash
./start.sh
```

## Deploy (Render)

1. Push this repo to GitHub.
2. In Render, create a **Blueprint** from `render.yaml`.
3. Set environment variables on the backend service (see `backend/.env.example`).
4. Set `VITE_API_URL` on the frontend static site to your backend URL (e.g. `https://cosight-backend.onrender.com`).
5. Set `CORS_ORIGINS` on the backend to your frontend URL.

## API

All routes are under `/api/cosight/*` (metrics, chat, reports, brief). Health check: `GET /health`.

## License

See `NOTICE` for third-party acknowledgments.
