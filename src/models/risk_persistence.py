from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import List


def load_last_n_days(
    data_dir: str,
    n_days: int
) -> pd.DataFrame:
    """
    Charge les N derniers fichiers CSV journaliers
    """
    files = sorted(Path(data_dir).glob("*.csv"), reverse=True)[:n_days]

    if not files:
        raise RuntimeError("No daily CSV files found for persistence analysis")

    dfs = [pd.read_csv(f) for f in files]
    return pd.concat(dfs, ignore_index=True)


def compute_consecutive_anomalies(df: pd.DataFrame) -> pd.Series:
    """
    Calcule le nombre maximum de jours consécutifs anormaux par véhicule
    """
    df = df.sort_values(["vehicle_id", "date"])
    df["is_anomaly"] = (df["anomaly_label"] == -1).astype(int)

    consecutive = {}

    for vehicle_id, group in df.groupby("vehicle_id"):
        max_streak = 0
        current = 0

        for v in group["is_anomaly"]:
            if v == 1:
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 0

        consecutive[vehicle_id] = max_streak

    return pd.Series(consecutive, name="consecutive_days_anomaly")


def run_risk_persistence(
    daily_metrics_dir: str,
    output_path: str,
    window_days: int = 7
) -> str:
    """
    Analyse de persistance des anomalies et scoring métier
    """
    df = load_last_n_days(daily_metrics_dir, window_days)

    if "date" not in df.columns:
        raise RuntimeError("Column 'date' is required for persistence analysis")

    # === INDICATEURS DE PERSISTANCE ===
    agg = (
        df.assign(is_anomaly=lambda x: x["anomaly_label"] == -1)
        .groupby("vehicle_id")
        .agg(
            anomaly_days_7d=("is_anomaly", "sum"),
            mean_anomaly_score_7d=("anomaly_score", "mean"),
        )
        .reset_index()
    )

    consecutive = compute_consecutive_anomalies(df)
    agg = agg.merge(
        consecutive,
        left_on="vehicle_id",
        right_index=True,
        how="left"
    )

    agg["consecutive_days_anomaly"] = agg["consecutive_days_anomaly"].fillna(0)

    # === SCORE MÉTIER ===
    agg["risk_score"] = (
        0.5 * agg["anomaly_days_7d"]
        + 0.3 * abs(agg["mean_anomaly_score_7d"])
        + 0.2 * agg["consecutive_days_anomaly"]
    )

    # === NIVEAU DE RISQUE ===
    def risk_bucket(score: float) -> str:
        if score >= 3.0:
            return "CRITICAL"
        elif score >= 1.5:
            return "WARNING"
        else:
            return "OK"

    agg["risk_level"] = agg["risk_score"].apply(risk_bucket)

    # === SAUVEGARDE ===
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    agg.to_csv(output_path, index=False)

    return str(output_path)
