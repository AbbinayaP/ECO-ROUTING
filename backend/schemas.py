from typing import List, Literal, Optional

from pydantic import BaseModel, Field


TransportMode = Literal["car", "bike", "ev", "walking", "metro", "bus", "auto"]
FuelType = Literal["petrol", "diesel", "electric", "none", "cng"]


class RouteRequest(BaseModel):
    origin: str
    destination: str
    modes: List[TransportMode] = Field(
        default_factory=lambda: ["car", "bike", "ev", "walking", "metro", "bus", "auto"]
    )
    vehicle_type: TransportMode = "car"
    fuel_type: FuelType = "petrol"
    elevation_gain_m: float = 0.0
    user_email: Optional[str] = None
    algorithm: Literal["google", "dijkstra", "astar", "multi_objective"] = "google"


class StepDetail(BaseModel):
    instruction: str
    distance: str
    duration: str
    mode: str
    transit_line: Optional[str] = None
    departure_stop: Optional[str] = None
    arrival_stop: Optional[str] = None


class RouteOption(BaseModel):
    mode: TransportMode
    distance_km: float
    duration_min: float
    duration_in_traffic_min: float
    traffic_delay_min: float
    polyline: str
    co2_kg: float
    eco_score: float
    steps: List[StepDetail] = Field(default_factory=list)


class RouteComparison(BaseModel):
    fastest: RouteOption
    eco_optimized: RouteOption
    emission_saved_pct: float
    extra_travel_time_min: float


class RouteResponse(BaseModel):
    origin: str
    destination: str
    options: List[RouteOption]
    comparison: RouteComparison


class EmissionHistoryItem(BaseModel):
    id: int
    mode: TransportMode
    distance_km: float
    duration_min: float
    traffic_delay_min: float
    co2_kg: float
    eco_score: float

    class Config:
        orm_mode = True


class EmissionHistoryResponse(BaseModel):
    items: List[EmissionHistoryItem]


from typing import Dict, Any

class XAIChatRequest(BaseModel):
    message: str
    route_context: Dict[str, Any]

class XAIChatResponse(BaseModel):
    response: str

