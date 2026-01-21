from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Dict


def analyze_fleet_state(df: pd.DataFrame) -> Dict[str, any]:
    """
    Analyse globale de l'état de la flotte
    """
    total = len(df)

    counts = df["risk_level"].value_counts().to_dict()

    critical = counts.get("CRITICAL", 0)
    warning = counts.get("WARNING", 0)
    ok = counts.get("OK", 0)

    persistent = (df["consecutive_days_anomaly"] >= 3).sum()

    return {
        "total": total,
        "critical": critical,
        "warning": warning,
        "ok": ok,
        "persistent": persistent,
    }


def determine_pattern(stats: Dict[str, any]) -> str:
    """
    Identifie le pattern dominant de risque
    """
    if stats["critical"] == 0 and stats["warning"] == 0:
        return "HEALTHY"

    if stats["critical"] > 0 and stats["persistent"] >= stats["critical"]:
        return "CONCENTRATED_CRITICAL"

    if stats["warning"] >= stats["critical"] and stats["warning"] >= 3:
        return "DIFFUSE_WARNING"

    return "MIXED"


def generate_report_text(stats: Dict[str, any], pattern: str) -> str:
    """
    Génère le texte du rapport en fonction du pattern
    """
    if pattern == "HEALTHY":
        return (
            "Résumé hebdomadaire – État de la flotte\n\n"
            "La flotte présente un fonctionnement globalement stable sur la période analysée.\n"
            "Les anomalies détectées sont restées isolées et sans persistance notable.\n\n"
            "Aucun véhicule ne présente actuellement de signal indiquant un risque opérationnel élevé.\n\n"
            "Action recommandée : Maintenir la surveillance standard."
        )

    if pattern == "CONCENTRATED_CRITICAL":
        return (
            "Résumé hebdomadaire – État de la flotte\n\n"
            "L’analyse met en évidence un nombre limité de véhicules présentant des comportements anormaux persistants.\n"
            "Ces véhicules concentrent l’essentiel du risque opérationnel observé sur la période.\n\n"
            "Action recommandée : Prioriser une intervention ciblée sur les véhicules identifiés comme CRITICAL "
            "afin de prévenir une immobilisation non planifiée."
        )

    if pattern == "DIFFUSE_WARNING":
        return (
            "Résumé hebdomadaire – État de la flotte\n\n"
            "Plusieurs véhicules présentent des signaux de dérive modérée dans leurs conditions d’exploitation.\n"
            "Bien qu’aucun cas critique ne soit observé, la fréquence des anomalies suggère une dégradation progressive "
            "du fonctionnement sur une partie du parc.\n\n"
            "Action recommandée : Renforcer la surveillance et analyser les conditions d’utilisation."
        )

    # MIXED
    return (
        "Résumé hebdomadaire – État de la flotte\n\n"
        "La situation observée présente un mélange de signaux modérés et critiques sur différents véhicules.\n"
        "Certaines anomalies montrent des signes de persistance nécessitant une attention particulière.\n\n"
        "Action recommandée : Prioriser les véhicules critiques tout en maintenant une surveillance renforcée "
        "sur les autres cas détectés."
    )


def build_weekly_report(
    risk_report_path: str,
    output_dir: str,
    run_date: str,
) -> Dict[str, str]:
    """
    Construit le rapport hebdomadaire texte + résumé structuré
    """
    df = pd.read_csv(risk_report_path)

    stats = analyze_fleet_state(df)
    pattern = determine_pattern(stats)
    text = generate_report_text(stats, pattern)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text_path = output_dir / f"{run_date}_summary.txt"
    json_path = output_dir / f"{run_date}_summary.json"

    text_path.write_text(text, encoding="utf-8")

    summary = {
        "date": run_date,
        "pattern": pattern,
        "stats": stats,
    }

    pd.Series(summary).to_json(json_path, indent=2)

    return {
        "text": str(text_path),
        "json": str(json_path),
    }
