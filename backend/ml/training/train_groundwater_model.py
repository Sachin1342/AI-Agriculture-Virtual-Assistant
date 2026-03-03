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
MODEL_PATH = MODEL_DIR / "groundwater_model.pkl"


def load_dataset() -> pd.DataFrame:
    # fallback synthetic data for portability
    rng = np.random.default_rng(42)
    rows = 1000
    df = pd.DataFrame({
        "rainfall": rng.normal(120, 40, rows).clip(0),
        "soil_type": rng.choice(["clay", "sandy", "loamy", "silty"], rows),
        "temperature": rng.normal(27, 6, rows),
        "humidity": rng.normal(65, 12, rows).clip(20, 100),
        "previous_level": rng.normal(5.5, 1.2, rows).clip(1, 12),
    })
    soil_effect = df["soil_type"].map({"clay": 0.3, "sandy": -0.5, "loamy": 0.2, "silty": 0.1})
    df["groundwater_level"] = (
        0.02 * df["rainfall"] + 0.5 * df["previous_level"] - 0.03 * df["temperature"] + 0.01 * df["humidity"] + soil_effect + rng.normal(0, 0.4, rows)
    ).clip(1, 15)
    return df


def main() -> None:
    df = load_dataset()
    X = df[["rainfall", "soil_type", "temperature", "humidity", "previous_level"]]
    y = df["groundwater_level"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), ["rainfall", "temperature", "humidity", "previous_level"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["soil_type"]),
    ])

    model = Pipeline([
        ("prep", preprocessor),
        ("reg", RandomForestRegressor(n_estimators=250, random_state=42)),
    ])
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    r2 = r2_score(y_test, preds)

    joblib.dump(model, MODEL_PATH)
    print(f"Saved groundwater model to {MODEL_PATH}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2: {r2:.4f}")


if __name__ == "__main__":
    main()
