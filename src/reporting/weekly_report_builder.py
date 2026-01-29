from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Dict, List
from datetime import datetime, timedelta


# =========================
# UTILS
# =========================

def load_last_n_files(folder: Path, n: int) -> List[pd.DataFrame]:
    files = sorted(folder.glob("*.csv"), reverse=True)[:n]
    if not files:
        raise RuntimeError(f"No CSV files found in {folder}")
    return [pd.read_csv(f) for f in files]


# =========================
# STRESS CLASSIFICATION
# =========================

def detect_stress_types(row: pd.Series) -> List[str]:
    stress = []

    if row.get("idling_ratio", 0) >= 0.3:
        stress.append("EXCESSIVE_IDLING")

    if row.get("harsh_acceleration_count", 0) >= 3:
        stress.append("HARSH_ACCELERATION")

    if row.get("harsh_cornering_count", 0) >= 3:
        stress.append("HARSH_CORNERING")

    if row.get("avg_speed", 999) <= 15:
        stress.append("LOW_SPEED_USAGE")

    if row.get("stop_count", 0) >= 10:
        stress.append("FREQUENT_STOPS")

    return stress or ["NORMAL_USAGE"]


# =========================
# WEEKLY REPORT BUILDER
# =========================

def build_weekly_report(
    anomalies_daily_dir: str,
    daily_metrics_dir: str,
    risk_reports_dir: str,
    output_json_path: str,
    window_days: int = 7,
    top_k: int = 10,
) -> str:

    anomalies_daily_dir = Path(anomalies_daily_dir)
    daily_metrics_dir = Path(daily_metrics_dir)
    risk_reports_dir = Path(risk_reports_dir)

    # === LOAD DATA ===
    anomalies_df = pd.concat(
        load_last_n_files(anomalies_daily_dir, window_days),
        ignore_index=True
    )

    metrics_df = pd.concat(
        load_last_n_files(daily_metrics_dir, window_days),
        ignore_index=True
    )

    # Nettoyage de sécurité
    metrics_df = metrics_df.loc[:, ~metrics_df.columns.duplicated()]

    # === LOAD RISK REPORTS (N / N-1) ===
    risk_files = sorted(risk_reports_dir.glob("*.csv"))
    if len(risk_files) < 2:
        raise RuntimeError("At least two risk reports are required for comparison")

    risk_current = pd.read_csv(risk_files[-1])
    risk_previous = pd.read_csv(risk_files[-2])

    # === META ===
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=window_days)

    meta = {
        "week_start": start_date.isoformat(),
        "week_end": end_date.isoformat(),
        "window_days": window_days,
        "total_vehicles_observed": int(risk_current["vehicle_id"].nunique()),
    }

    # === FLEET OVERVIEW ===
    dist = risk_current["risk_level"].value_counts()
    total = len(risk_current)

    fleet_overview = {
        "risk_distribution": dist.to_dict(),
        "risk_percentages": {
            k.lower(): round(v / total * 100, 1)
            for k, v in dist.items()
        },
        "fleet_health_status": (
            "HIGH_RISK" if dist.get("CRITICAL", 0) / total >= 0.1
            else "MODERATE_RISK" if dist.get("CRITICAL", 0) > 0
            else "LOW_RISK"
        ),
        "risk_concentration": {
            "top_3_share": round(
                risk_current.sort_values("risk_score", ascending=False)
                .head(3)["risk_score"].sum()
                / risk_current["risk_score"].sum(),
                2
            )
        }
    }

    # === EVOLUTION VS LAST WEEK ===
    def pct(df, level):
        return round((df["risk_level"] == level).sum() / len(df) * 100, 1)

    fleet_evolution = {
        "delta_risk_percentages": {
            "ok": pct(risk_current, "OK") - pct(risk_previous, "OK"),
            "warning": pct(risk_current, "WARNING") - pct(risk_previous, "WARNING"),
            "critical": pct(risk_current, "CRITICAL") - pct(risk_previous, "CRITICAL"),
        }
    }

    # === METRICS AGGREGATION (SAFE) ===
    numeric_metrics = (
        metrics_df
        .select_dtypes(include=["number"])
        .drop(columns=["vehicle_id"], errors="ignore")
    )

    metrics_agg = (
        metrics_df[["vehicle_id"]]
        .join(numeric_metrics)
        .groupby("vehicle_id", as_index=False)
        .mean()
    )

    # === MERGE RISK + METRICS ===
    merged = risk_current.merge(metrics_agg, on="vehicle_id", how="left")

    merged["stress_types"] = merged.apply(detect_stress_types, axis=1)

    # === VEHICLES AT RISK ===
    vehicles_at_risk = (
        merged[merged["risk_level"] != "OK"]
        .sort_values("risk_score", ascending=False)
        .head(top_k)
        .assign(rank=lambda x: range(1, len(x) + 1))
    )

    vehicles_payload = [
        {
            "vehicle_id": int(r["vehicle_id"]),
            "rank": int(r["rank"]),
            "risk_level": r["risk_level"],
            "risk_score": round(r["risk_score"], 2),
            "anomaly_days_7d": int(r["anomaly_days_7d"]),
            "consecutive_days": int(r["consecutive_days_anomaly"]),
            "dominant_stress": r["stress_types"],
            "key_metrics": {
                "avg_speed": round(r.get("avg_speed", 0), 2),
                "stop_count": int(r.get("stop_count", 0)),
                "idling_ratio": round(r.get("idling_ratio", 0), 2),
            }
        }
        for _, r in vehicles_at_risk.iterrows()
    ]

    vehicles_section = {
        "total_at_risk": int((risk_current["risk_level"] != "OK").sum()),
        "display_limit": top_k,
        "vehicles": vehicles_payload,
    }

    # === STRESS ANALYSIS (USAGE LEVEL) ===
    stress_series = metrics_df.apply(detect_stress_types, axis=1).explode()

    stress_analysis = {
        "stress_distribution": (
            stress_series.value_counts(normalize=True)
            .round(2)
            .to_dict()
        )
    }

    # === FINAL JSON ===
    weekly_report = {
        "meta": meta,
        "fleet_overview": fleet_overview,
        "fleet_evolution": fleet_evolution,
        "vehicles_at_risk": vehicles_section,
        "stress_analysis": stress_analysis,
    }

    output_path = Path(output_json_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pd.Series(weekly_report).to_json(output_path, indent=2)

    return str(output_path)
