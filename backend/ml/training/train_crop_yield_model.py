from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "production_model.pkl"


def build_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(7)
    rows = 1200
    df = pd.DataFrame({
        "crop_type": rng.choice(["rice", "wheat", "corn", "tomato", "potato"], rows),
        "area": rng.uniform(0.5, 10, rows),
        "rainfall": rng.normal(950, 250, rows).clip(50),
        "temperature": rng.normal(26, 5, rows),
        "humidity": rng.normal(60, 10, rows).clip(20, 100),
        "soil_nutrients": rng.normal(55, 15, rows).clip(5, 100),
        "fertilizer_amount": rng.normal(100, 25, rows).clip(10, 300),
    })
    crop_factor = df["crop_type"].map({"rice": 1.2, "wheat": 1.0, "corn": 1.1, "tomato": 0.9, "potato": 1.05})
    yield_per_hectare = (
        1500 + crop_factor * 900 + 0.3 * df["rainfall"] - 14 * np.abs(df["temperature"] - 25) + 8 * df["soil_nutrients"] + 1.5 * df["fertilizer_amount"] + np.random.normal(0, 180, rows)
    ).clip(500, 8000)
    df["yield_per_hectare_kg"] = yield_per_hectare
    return df


def main() -> None:
    df = build_dataset()
    X = df[["crop_type", "area", "rainfall", "temperature", "humidity", "soil_nutrients", "fertilizer_amount"]]
    y = df["yield_per_hectare_kg"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), ["area", "rainfall", "temperature", "humidity", "soil_nutrients", "fertilizer_amount"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["crop_type"]),
    ])
    model = Pipeline([
        ("prep", preprocessor),
        ("reg", RandomForestRegressor(n_estimators=300, random_state=42)),
    ])
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    r2 = r2_score(y_test, preds)

    joblib.dump(model, MODEL_PATH)
    print(f"Saved crop yield model to {MODEL_PATH}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2: {r2:.4f}")


if __name__ == "__main__":
    main()
