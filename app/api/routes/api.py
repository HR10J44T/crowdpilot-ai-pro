from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.data import store

router = APIRouter(prefix="/api", tags=["api"])


class AlertCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    message: str = Field(min_length=5, max_length=300)
    severity: str = Field(pattern="^(low|medium|high)$")


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "crowdpilot-ai-pro"}


@router.get("/dashboard")
def dashboard_data() -> dict:
    return {
        "kpis": store.kpis(),
        "recommended_gate": store.recommended_gate(True),
        "recommended_food": store.recommended_queue("food"),
        "zones": store.snapshot()["zones"],
        "alerts": store.snapshot()["alerts"],
        "ai": store.ai_summary(),
    }


@router.get("/gates")
def get_gates() -> list[dict]:
    return store.snapshot()["gates"]


@router.get("/gates/recommendation")
def gate_recommendation(accessible: bool = False) -> dict:
    return store.recommended_gate(accessible)


@router.get("/queues")
def get_queues() -> list[dict]:
    return store.snapshot()["facilities"]


@router.get("/queues/recommendation")
def queue_recommendation(facility_type: str = "food") -> dict:
    return store.recommended_queue(facility_type)


@router.get("/zones")
def get_zones() -> list[dict]:
    return store.snapshot()["zones"]


@router.get("/alerts")
def get_alerts() -> list[dict]:
    return store.snapshot()["alerts"]


@router.post("/alerts")
def create_alert(payload: AlertCreate) -> dict:
    return store.create_alert(payload.title, payload.message, payload.severity)


@router.get("/ai/summary")
def ai_summary() -> dict:
    return store.ai_summary()


@router.post("/simulate")
def simulate() -> dict:
    return store.tick()
