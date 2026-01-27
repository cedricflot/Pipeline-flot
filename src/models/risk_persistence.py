from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import List, Dict

# =========================
# STRESS METIER
# =========================

STRESS_MAPPING = {
    "EXPLOITATION": [
        "stop_duration_hours",
        "avg_speed",
    ],
    "MECHANICAL": [
        "harsh_acceleration_count",
        "harsh_braking_count",
        "harsh_cornering_count",
    ],
    "ENERGY": [
        "excessive_idling_duration",
        "idling_ratio",
    ],
}


def load_last_n_days(data_dir: str, n_days: int) -> pd.DataFrame:
    files = sorted(Path(data_dir).glob("*.csv"), reverse=True)[:n_days]
    if not files:
        raise RuntimeError("No daily CSV files found")
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)


def compute_consecutive_anomalies(df: pd.DataFrame) -> pd.Series:
    df = df.sort_values(["vehicle_id", "date"])
    df["is_anomaly"] = (df["anomaly_label"] == -1).astype(int)

    result = {}

    for vid, group in df.groupby("vehicle_id"):
        max_streak, current = 0, 0
        for v in group["is_anomaly"]:
            if v == 1:
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 0
        result[vid] = max_streak

    return pd.Series(result, name="consecutive_days_anomaly")


def identify_dominant_stress(row: pd.Series) -> Dict[str, str]:
    scores = {}

    for stress, metrics in STRESS_MAPPING.items():
        values = [abs(row.get(m, 0)) for m in metrics if pd.notna(row.get(m))]
        scores[stress] = sum(values)

    dominant = max(scores, key=scores.get)
    affected = STRESS_MAPPING[dominant]

    interpretation = {
        "EXPLOITATION": "Conditions d’utilisation dégradées (arrêts prolongés, faible vitesse)",
        "MECHANICAL": "Conduite agressive générant un stress mécanique accru",
        "ENERGY": "Surconsommation énergétique liée à un ralenti excessif",
    }

    return {
        "dominant_stress": dominant,
        "affected_metrics": ", ".join(affected),
        "interpretation": interpretation[dominant],
    }


def run_risk_persistence(
    daily_metrics_dir: str,
    output_path: str,
    window_days: int = 7,
) -> str:
    df = load_last_n_days(daily_metrics_dir, window_days)

    agg = (
        df.assign(is_anomaly=lambda x: x["anomaly_label"] == -1)
        .groupby("vehicle_id")
        .agg(
            anomaly_days_7d=("is_anomaly", "sum"),
            mean_anomaly_score_7d=("anomaly_score", "mean"),
        )
        .reset_index()
    )

    consecutive = compute_consecutive_anomalies(df).reset_index()
    consecutive.columns = ["vehicle_id", "consecutive_days_anomaly"]

    agg = agg.merge(consecutive, on="vehicle_id", how="left")
    agg["consecutive_days_anomaly"] = agg["consecutive_days_anomaly"].fillna(0)

    # === SCORE METIER ===
    agg["risk_score"] = (
        0.5 * agg["anomaly_days_7d"]
        + 0.3 * agg["mean_anomaly_score_7d"].abs()
        + 0.2 * agg["consecutive_days_anomaly"]
    )

    def bucket(score: float) -> str:
        if score >= 3:
            return "CRITICAL"
        elif score >= 1.5:
            return "WARNING"
        return "OK"

    agg["risk_level"] = agg["risk_score"].apply(bucket)

    # === STRESS DOMINANT ===
    stress_info = agg.apply(identify_dominant_stress, axis=1, result_type="expand")
    agg = pd.concat([agg, stress_info], axis=1)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    agg.to_csv(output_path, index=False)

    return str(output_path)
