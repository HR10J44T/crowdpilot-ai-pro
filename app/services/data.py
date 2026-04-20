from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, List
import random


@dataclass
class Gate:
    gate_id: str
    name: str
    wait_time: int
    status: str
    accessible: bool
    crowd_level: str
    recommendation_score: float


@dataclass
class Facility:
    facility_id: str
    name: str
    type: str
    zone_id: str
    wait_time: int
    trend: str


@dataclass
class Zone:
    zone_id: str
    name: str
    crowd_count: int
    risk_level: str
    trend: str
    occupancy_pct: int


@dataclass
class Alert:
    alert_id: str
    title: str
    message: str
    severity: str
    active: bool
    created_at: str


class VenueStore:
    """Simple in-memory venue store for demo and hackathon use."""

    def __init__(self) -> None:
        self.gates: List[Gate] = [
            Gate("gate_1", "Gate 1", 14, "open", True, "high", 0.44),
            Gate("gate_2", "Gate 2", 11, "open", True, "medium", 0.58),
            Gate("gate_3", "Gate 3", 8, "open", False, "medium", 0.71),
            Gate("gate_4", "Gate 4", 4, "open", True, "low", 0.92),
        ]
        self.facilities: List[Facility] = [
            Facility("food_a", "North Bites", "food", "zone_b", 17, "increasing"),
            Facility("food_b", "Arena Express", "food", "zone_d", 6, "stable"),
            Facility("food_c", "Quick Grill", "food", "zone_f", 9, "decreasing"),
            Facility("wash_a", "Washroom A", "washroom", "zone_c", 8, "stable"),
            Facility("wash_b", "Washroom B", "washroom", "zone_e", 4, "decreasing"),
        ]
        self.zones: List[Zone] = [
            Zone("zone_a", "North Entry", 220, "medium", "rising", 68),
            Zone("zone_b", "Food Court", 305, "high", "rising", 88),
            Zone("zone_c", "East Corridor", 156, "low", "stable", 42),
            Zone("zone_d", "South Seating", 244, "medium", "stable", 71),
            Zone("zone_e", "Merch Zone", 128, "low", "decreasing", 35),
            Zone("zone_f", "West Exit", 198, "medium", "rising", 63),
        ]
        self.alerts: List[Alert] = [
            Alert(
                "alert_1",
                "Zone B congestion",
                "Food Court density is rising. Suggest redirecting fans to Arena Express in Zone D.",
                "high",
                True,
                datetime.now(timezone.utc).isoformat(),
            )
        ]

    def snapshot(self) -> Dict[str, List[dict]]:
        return {
            "gates": [asdict(g) for g in self.gates],
            "facilities": [asdict(f) for f in self.facilities],
            "zones": [asdict(z) for z in self.zones],
            "alerts": [asdict(a) for a in self.alerts],
        }

    def recommended_gate(self, accessible_required: bool = False) -> dict:
        candidates = [g for g in self.gates if (g.accessible or not accessible_required) and g.status == "open"]
        best = max(candidates, key=lambda g: g.recommendation_score)
        return asdict(best)

    def recommended_queue(self, facility_type: str = "food") -> dict:
        candidates = [f for f in self.facilities if f.type == facility_type]
        best = min(candidates, key=lambda f: f.wait_time)
        return asdict(best)

    def kpis(self) -> dict:
        total_attendees = sum(z.crowd_count for z in self.zones)
        avg_wait = round(sum(g.wait_time for g in self.gates) / len(self.gates))
        high_risk = sum(1 for z in self.zones if z.risk_level == "high")
        active_alerts = sum(1 for a in self.alerts if a.active)
        return {
            "total_attendees": total_attendees,
            "avg_wait": avg_wait,
            "high_risk": high_risk,
            "active_alerts": active_alerts,
        }

    def ai_summary(self) -> dict:
        high_zones = [z for z in self.zones if z.risk_level == "high"]
        best_gate = self.recommended_gate(True)
        shortest_food = self.recommended_queue("food")
        if high_zones:
            hot = high_zones[0]
            summary = (
                f"{hot.name} is currently the highest-risk zone due to rising crowd density. "
                f"Recommend redirecting attendees toward {best_gate['name']} for entry flow and promoting "
                f"{shortest_food['name']} as the fastest nearby food option."
            )
        else:
            summary = "Venue flow is stable. Continue current routing and monitor queue conditions."
        return {
            "summary": summary,
            "confidence": 0.89,
            "recommended_gate": best_gate["name"],
            "recommended_food": shortest_food["name"],
        }

    def create_alert(self, title: str, message: str, severity: str) -> dict:
        alert = Alert(
            f"alert_{len(self.alerts) + 1}",
            title,
            message,
            severity,
            True,
            datetime.now(timezone.utc).isoformat(),
        )
        self.alerts.insert(0, alert)
        return asdict(alert)

    def tick(self) -> dict:
        """Small simulator for demo refreshes."""
        for gate in self.gates:
            gate.wait_time = max(2, min(18, gate.wait_time + random.choice([-1, 0, 1])))
            gate.crowd_level = "low" if gate.wait_time <= 5 else "medium" if gate.wait_time <= 10 else "high"
            gate.recommendation_score = round((20 - gate.wait_time) / 20 + (0.1 if gate.accessible else 0), 2)

        for fac in self.facilities:
            fac.wait_time = max(3, min(22, fac.wait_time + random.choice([-2, -1, 0, 1, 2])))
            fac.trend = "decreasing" if fac.wait_time <= 6 else "stable" if fac.wait_time <= 12 else "increasing"

        for zone in self.zones:
            zone.crowd_count = max(80, min(340, zone.crowd_count + random.choice([-18, -10, -4, 4, 10, 18])))
            zone.occupancy_pct = max(20, min(95, zone.occupancy_pct + random.choice([-5, -2, 0, 2, 5])))
            zone.risk_level = "low" if zone.occupancy_pct <= 45 else "medium" if zone.occupancy_pct <= 75 else "high"
            zone.trend = random.choice(["rising", "stable", "decreasing"])

        if self.alerts and random.random() > 0.6:
            self.alerts[0].message = self.ai_summary()["summary"]
        return self.snapshot()


store = VenueStore()
