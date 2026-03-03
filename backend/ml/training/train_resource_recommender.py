from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "resource_recommender.pkl"


def build_data() -> pd.DataFrame:
    rng = np.random.default_rng(21)
    rows = 1500
    df = pd.DataFrame({
        "rainfall": rng.normal(120, 50, rows).clip(0),
        "temperature": rng.normal(27, 6, rows),
        "humidity": rng.normal(60, 12, rows).clip(20, 100),
        "soil_n": rng.uniform(5, 90, rows),
        "soil_p": rng.uniform(5, 90, rows),
        "soil_k": rng.uniform(5, 90, rows),
    })
    # rule + stochastic label
    score = (df["rainfall"] < 80).astype(int) + (df["soil_n"] < 30).astype(int) + (df["humidity"] < 45).astype(int)
    df["recommendation_class"] = np.select([score >= 2, score == 1], [2, 1], default=0)
    return df


def main() -> None:
    df = build_data()
    X = df[["rainfall", "temperature", "humidity", "soil_n", "soil_p", "soil_k"]]
    y = df["recommendation_class"]

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(n_estimators=250, random_state=42)),
    ])
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved resource recommender model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
