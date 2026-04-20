# CrowdPilot AI Pro

CrowdPilot AI Pro is a multi-page smart venue dashboard built as a single FastAPI service so it is easier to run locally and deploy to Google Cloud Run without the usual frontend/backend integration issues.

## What it includes
- Multi-page premium SaaS-style UI
- Dashboard, Gates, Queues, Zones, Alerts, AI Insights, Settings pages
- Gate recommendation and shortest queue recommendation
- Zone risk monitoring
- Operator alert creation
- AI-style ops summary endpoint
- Simulated live data refresh
- Cloud Run-ready Dockerfile
- Basic automated tests

## Pages
- `/` Dashboard
- `/gates`
- `/queues`
- `/zones`
- `/alerts`
- `/insights`
- `/settings`

## Local run
```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Open `http://127.0.0.1:8080`

## Run tests
```bash
pytest
```

## Cloud Run deploy
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/crowdpilot-ai-pro

gcloud run deploy crowdpilot-ai-pro \
  --image gcr.io/YOUR_PROJECT_ID/crowdpilot-ai-pro \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated
```

## Why this architecture
This version is intentionally kept as one deployable service so you can avoid common GCP errors around separate frontend hosting, CORS, multiple containers, and realtime infra complexity.
