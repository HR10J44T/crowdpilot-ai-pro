from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes.api import router as api_router
from app.services.data import store

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="CrowdPilot AI Pro", version="1.0.0")
app.include_router(api_router)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


PAGES = {
    "dashboard": "Dashboard",
    "gates": "Gates",
    "queues": "Queues",
    "zones": "Zones",
    "alerts": "Alerts",
    "insights": "AI Insights",
    "settings": "Settings",
}


def _context(page: str) -> dict:
    snapshot = store.snapshot()
    return {
        "page": page,
        "pages": PAGES,
        "kpis": store.kpis(),
        "gates": snapshot["gates"],
        "facilities": snapshot["facilities"],
        "zones": snapshot["zones"],
        "alerts": snapshot["alerts"],
        "recommended_gate": store.recommended_gate(True),
        "recommended_food": store.recommended_queue("food"),
        "ai": store.ai_summary(),
    }


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", _context("dashboard") | {"request": request})


@app.get("/{page}", response_class=HTMLResponse)
async def render_page(request: Request, page: str):
    if page not in PAGES:
        return templates.TemplateResponse(request, "404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse(request, "index.html", _context(page) | {"request": request})
