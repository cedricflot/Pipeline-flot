from datetime import date
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


FEATURES = [
    "distance_km",
    "driving_duration_min",
    "avg_speed",
    "stop_count",
    "stop_duration_hours",
    "harsh_cornering_count",
    "excessive_idling_duration",
    "idling_ratio",
]


def run_isolation_forest(processed_csv_path: str, run_date: date) -> str:
    # 1. Load data
    df = pd.read_csv(processed_csv_path)

    X = df[FEATURES].fillna(0)

    # 2. Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. Isolation Forest
    iso_forest = IsolationForest(
        n_estimators=200,
        contamination=0.15,  # proportion attendue d'anomalies
        random_state=42,
    )

    df["anomaly_label"] = iso_forest.fit_predict(X_scaled)
    df["anomaly_score"] = iso_forest.decision_function(X_scaled)

    # 4. Save results
    out_dir = Path("data") / "analytics" / "anomalies_daily"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{run_date.isoformat()}.csv"
    df.to_csv(out_path, index=False)

    return str(out_path)