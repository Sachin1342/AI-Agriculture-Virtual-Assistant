"""Crop yield regression training script (local-laptop friendly).

Steps:
- Load dataset (CSV if available, otherwise synthetic fallback)
- Preprocess
- Train
- Evaluate
- Save model
- Print metrics
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "production_model.pkl"


def _candidate_csv_paths() -> list[Path]:
    root = BASE_DIR.parents[1]
    return [
        root / "crop production" / "crop_production.csv",
        root / "data" / "crop_yield.csv",
        root / "datasets" / "crop_yield.csv",
    ]


def _build_synthetic(rows: int = 1600) -> pd.DataFrame:
    rng = np.random.default_rng(7)
    df = pd.DataFrame(
        {
            "crop_type": rng.choice(["rice", "wheat", "corn", "tomato", "potato"], rows),
            "area": rng.uniform(0.5, 10, rows),
            "rainfall": rng.normal(950, 250, rows).clip(50),
            "temperature": rng.normal(26, 5, rows),
            "humidity": rng.normal(60, 10, rows).clip(20, 100),
            "soil_nutrients": rng.normal(55, 15, rows).clip(5, 100),
            "fertilizer_amount": rng.normal(100, 25, rows).clip(10, 300),
        }
    )
    crop_factor = df["crop_type"].map({"rice": 1.2, "wheat": 1.0, "corn": 1.1, "tomato": 0.9, "potato": 1.05})
    yield_per_hectare = (
        1500
        + crop_factor * 900
        + 0.3 * df["rainfall"]
        - 14 * np.abs(df["temperature"] - 25)
        + 8 * df["soil_nutrients"]
        + 1.5 * df["fertilizer_amount"]
        + rng.normal(0, 180, rows)
    ).clip(500, 8000)
    df["yield_per_hectare_kg"] = yield_per_hectare
    return df


def load_dataset() -> pd.DataFrame:
    for path in _candidate_csv_paths():
        if path.exists():
            df = pd.read_csv(path)
            # Normalize likely column variants if using generic crop_production.csv
            rename_map = {
                "Crop": "crop_type",
                "crop": "crop_type",
                "Area": "area",
                "area": "area",
                "Rainfall": "rainfall",
                "Temperature": "temperature",
                "Humidity": "humidity",
                "SoilNutrients": "soil_nutrients",
                "Fertilizer": "fertilizer_amount",
                "Productivity": "yield_per_hectare_kg",
                "yield": "yield_per_hectare_kg",
            }
            df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
            required = {"crop_type", "area", "rainfall", "temperature", "humidity", "soil_nutrients", "fertilizer_amount", "yield_per_hectare_kg"}
            if required.issubset(df.columns):
                print(f"Loaded dataset: {path}")
                return df
            print(f"Dataset found at {path} but missing required columns, using synthetic fallback.")
    print("No suitable crop yield CSV found, using synthetic dataset.")
    return _build_synthetic()


def main() -> None:
    df = load_dataset().dropna()

    X = df[["crop_type", "area", "rainfall", "temperature", "humidity", "soil_nutrients", "fertilizer_amount"]]
    y = df["yield_per_hectare_kg"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(
        [
            ("num", StandardScaler(), ["area", "rainfall", "temperature", "humidity", "soil_nutrients", "fertilizer_amount"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["crop_type"]),
        ]
    )

    model = Pipeline(
        [
            ("prep", preprocessor),
            ("reg", RandomForestRegressor(n_estimators=220, max_depth=20, random_state=42, n_jobs=-1)),
        ]
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    rmse = mean_squared_error(y_test, preds, squared=False)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    joblib.dump(model, MODEL_PATH)

    print("\n=== Crop Yield Training Metrics ===")
    print(f"Rows: {len(df)}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE : {mae:.4f}")
    print(f"R2  : {r2:.4f}")
    print(f"Saved model: {MODEL_PATH}")


if __name__ == "__main__":
    main()
