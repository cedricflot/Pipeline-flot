from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Dict, List


def build_context(df: pd.DataFrame) -> Dict[str, any]:
    total = len(df)

    dist = df["risk_level"].value_counts().to_dict()
    dominant_stress = df["dominant_stress"].value_counts().to_dict()

    top = df.sort_values("risk_score", ascending=False).head(5)

    return {
        "fleet_size": total,
        "risk_distribution": dist,
        "dominant_stress": dominant_stress,
        "priority_vehicles": top[
            [
                "vehicle_id",
                "risk_level",
                "risk_score",
                "dominant_stress",
                "interpretation",
                "consecutive_days_anomaly",
            ]
        ].to_dict(orient="records"),
    }


def render_text(context: Dict[str, any]) -> str:
    lines = [
        "RAPPORT HEBDOMADAIRE – INTELLIGENCE OPÉRATIONNELLE\n",
        f"Flotte analysée : {context['fleet_size']} véhicules\n",
        "Répartition du risque :",
    ]

    for k, v in context["risk_distribution"].items():
        lines.append(f"- {k}: {v}")

    lines.append("\nStress opérationnels dominants observés :")
    for s, v in context["dominant_stress"].items():
        lines.append(f"- {s}: {v} véhicules")

    lines.append("\nVéhicules prioritaires :")
    for v in context["priority_vehicles"]:
        lines.append(
            f"- {v['vehicle_id']} | {v['risk_level']} | "
            f"{v['interpretation']} | "
            f"{v['consecutive_days_anomaly']} jours consécutifs"
        )

    lines.append(
        "\nRecommandation : prioriser une analyse ciblée des véhicules CRITICAL "
        "et surveiller l’évolution des stress dominants."
    )

    return "\n".join(lines)


def build_weekly_report(
    risk_report_path: str,
    output_dir: str,
    run_date: str,
) -> Dict[str, str]:
    df = pd.read_csv(risk_report_path)

    context = build_context(df)
    text = render_text(context)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text_path = output_dir / f"{run_date}_summary.txt"
    json_path = output_dir / f"{run_date}_context.json"

    text_path.write_text(text, encoding="utf-8")
    pd.Series(context).to_json(json_path, indent=2)

    return {"text": str(text_path), "json": str(json_path)}
