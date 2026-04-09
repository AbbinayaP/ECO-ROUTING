from dataclasses import dataclass


@dataclass
class EcoScoreWeights:
    w_co2: float = 0.5
    w_traffic_delay: float = 0.3
    w_distance: float = 0.2


def compute_eco_score(
    co2_kg: float,
    traffic_delay_min: float,
    distance_km: float,
    weights: EcoScoreWeights | None = None,
) -> float:
    if weights is None:
        weights = EcoScoreWeights()

    norm_co2 = co2_kg
    norm_delay = traffic_delay_min
    norm_distance = distance_km

    raw_score = (
        weights.w_co2 * norm_co2
        + weights.w_traffic_delay * norm_delay
        + weights.w_distance * norm_distance
    )

    return max(0.0, min(100.0, 100.0 - raw_score))

