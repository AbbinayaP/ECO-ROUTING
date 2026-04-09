from pathlib import Path
from typing import Literal

import joblib
import numpy as np

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "emission_model.pkl"
RF_MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "rf_emission_model.pkl"
XGB_MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "xgb_emission_model.pkl"

class EmissionModelNotTrained(Exception):
    pass


def load_emission_model():
    models = {}
    if RF_MODEL_PATH.exists() and XGB_MODEL_PATH.exists():
        models['rf'] = joblib.load(RF_MODEL_PATH)
        models['xgb'] = joblib.load(XGB_MODEL_PATH)
        models['type'] = 'ensemble'
    elif MODEL_PATH.exists():
        # Fallback to single model
        models['single'] = joblib.load(MODEL_PATH)
        models['type'] = 'single'
    else:
        raise EmissionModelNotTrained(
            f"Emission models not found in {RF_MODEL_PATH.parent}. Train via ml/train_emission_model.py"
        )
    return models


def predict_co2_kg(
    model,
    *,
    distance_km: float,
    avg_speed_kmh: float,
    vehicle_type: Literal["car", "bike", "ev", "walking", "metro", "bus", "auto"],
    fuel_type: Literal["petrol", "diesel", "electric", "none", "cng"],
    traffic_delay_min: float,
    elevation_gain_m: float,
) -> float:
    vehicle_type_map = {
        "car": 0,
        "bike": 1,
        "ev": 2,
        "walking": 3,
        "metro": 4,
        "bus": 5,
        "auto": 6,
    }
    fuel_type_map = {
        "petrol": 0,
        "diesel": 1,
        "electric": 2,
        "none": 3,
        "cng": 4,
    }

    vt = vehicle_type_map.get(vehicle_type, 0)
    ft = fuel_type_map.get(fuel_type, 0)

    features = np.array(
        [
            [
                distance_km,
                avg_speed_kmh,
                vt,
                ft,
                traffic_delay_min,
                elevation_gain_m,
            ]
        ]
    )

    if model.get('type') == 'ensemble':
        rf_co2 = float(model['rf'].predict(features)[0])
        xgb_co2 = float(model['xgb'].predict(features)[0])
        co2_kg = (rf_co2 + xgb_co2) / 2.0
    else:
        co2_kg = float(model['single'].predict(features)[0])
        
    return max(co2_kg, 0.0)

