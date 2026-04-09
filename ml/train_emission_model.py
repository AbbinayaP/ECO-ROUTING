from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def generate_synthetic_data(n_samples: int = 5000):
    rng = np.random.default_rng(42)

    distance_km = rng.uniform(0.5, 50.0, size=n_samples)
    avg_speed_kmh = rng.uniform(5.0, 100.0, size=n_samples)
    vehicle_type = rng.integers(0, 7, size=n_samples) # 0-6: car, bike, ev, walk, metro, bus, auto
    fuel_type = rng.integers(0, 5, size=n_samples)    # 0-4: petrol, diesel, electric, none, cng
    traffic_delay_min = rng.uniform(0.0, 45.0, size=n_samples)
    elevation_gain_m = rng.uniform(0.0, 200.0, size=n_samples)

    # Base emission factor per fuel type
    fuel_factor = np.select(
        [
            fuel_type == 0, # petrol
            fuel_type == 1, # diesel
            fuel_type == 2, # electric
            fuel_type == 3, # none
            fuel_type == 4, # cng
        ],
        [0.18, 0.20, 0.05, 0.0, 0.12],
    )

    # Vehicle specific multiplier
    vehicle_multiplier = np.select(
        [
            vehicle_type == 0, # car
            vehicle_type == 1, # bike
            vehicle_type == 2, # ev
            vehicle_type == 3, # walking
            vehicle_type == 4, # metro
            vehicle_type == 5, # bus
            vehicle_type == 6, # auto
        ],
        [1.0, 0.1, 1.0, 0.0, 0.0, 0.5, 0.8],
    )

    co2_kg = (
        distance_km * fuel_factor * vehicle_multiplier
        + 0.01 * traffic_delay_min
        + 0.0005 * elevation_gain_m
        + rng.normal(0, 0.02, size=n_samples)
    )
    co2_kg = np.clip(co2_kg, 0.0, None)

    X = np.column_stack(
        [
            distance_km,
            avg_speed_kmh,
            vehicle_type,
            fuel_type,
            traffic_delay_min,
            elevation_gain_m,
        ]
    )
    y = co2_kg
    return X, y


def main():
    X, y = generate_synthetic_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # --- Train Random Forest ---
    print("\nTraining Random Forest Regressor...")
    rf_model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )
    rf_model.fit(X_train, y_train)

    rf_pred = rf_model.predict(X_test)

    rf_mse = mean_squared_error(y_test, rf_pred)
    rf_rmse = rf_mse ** 0.5
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_r2 = r2_score(y_test, rf_pred)

    print("Random Forest Metrics:")
    print(f"RMSE: {rf_rmse:.4f}")
    print(f"MAE: {rf_mae:.4f}")
    print(f"R2: {rf_r2:.4f}")

    # --- Train XGBoost ---
    print("\nTraining XGBoost Regressor...")
    xgb_model = XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
    )
    xgb_model.fit(X_train, y_train)

    xgb_pred = xgb_model.predict(X_test)

    xgb_mse = mean_squared_error(y_test, xgb_pred)
    xgb_rmse = xgb_mse ** 0.5
    xgb_mae = mean_absolute_error(y_test, xgb_pred)
    xgb_r2 = r2_score(y_test, xgb_pred)

    print("XGBoost Metrics:")
    print(f"RMSE: {xgb_rmse:.4f}")
    print(f"MAE: {xgb_mae:.4f}")
    print(f"R2: {xgb_r2:.4f}")
    
    # --- Ensemble ---
    print("\nEnsemble (Average) Metrics:")
    ensemble_pred = (rf_pred + xgb_pred) / 2.0
    ens_rmse = (mean_squared_error(y_test, ensemble_pred)) ** 0.5
    ens_mae = mean_absolute_error(y_test, ensemble_pred)
    ens_r2 = r2_score(y_test, ensemble_pred)
    print(f"RMSE: {ens_rmse:.4f}")
    print(f"MAE: {ens_mae:.4f}")
    print(f"R2: {ens_r2:.4f}")

    models_dir = Path(__file__).resolve().parents[1] / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    rf_path = models_dir / "rf_emission_model.pkl"
    xgb_path = models_dir / "xgb_emission_model.pkl"

    joblib.dump(rf_model, rf_path)
    joblib.dump(xgb_model, xgb_path)
    
    # Optional: Keep the old filename for backwards compatibility if needed, using best model
    best_model = xgb_model if xgb_rmse < rf_rmse else rf_model
    joblib.dump(best_model, models_dir / "emission_model.pkl")

    print(f"\nSaved Random Forest model to {rf_path}")
    print(f"Saved XGBoost model to {xgb_path}")


if __name__ == "__main__":
    main()

