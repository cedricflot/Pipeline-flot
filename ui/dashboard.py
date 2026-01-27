import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Fleet Operational Risk Intelligence",
    page_icon="🚗",
    layout="wide",
)

# =========================
# UTILS
# =========================
DATA_PROCESSED = Path("data/processed")
DATA_ANALYTICS = Path("data/analytics")
DATA_REPORTS = Path("data/reports")

def load_latest_csv(folder: Path):
    files = sorted(folder.glob("*.csv"))
    if not files:
        return None
    return pd.read_csv(files[-1])

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🚦 Fleet Risk Intelligence")
page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Vue globale",
        "🚗 Véhicules à risque",
        "📈 Tendances & persistance",
        "📝 Rapport hebdomadaire",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Mise à jour automatique quotidienne")

# =========================
# LOAD DATA
# =========================
risk_df = load_latest_csv(DATA_PROCESSED / "risk_reports")

if risk_df is None:
    st.error("Aucune donnée disponible.")
    st.stop()

# =========================
# PAGE 1 — VUE GLOBALE
# =========================
if page == "📊 Vue globale":

    st.title("📊 État global de la flotte")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Véhicules surveillés", len(risk_df))
    col2.metric("CRITICAL", (risk_df["risk_level"] == "CRITICAL").sum())
    col3.metric("WARNING", (risk_df["risk_level"] == "WARNING").sum())
    col4.metric("OK", (risk_df["risk_level"] == "OK").sum())

    st.markdown("---")

    st.subheader("Répartition du risque")

    risk_counts = risk_df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["Niveau de risque", "Nombre"]

    st.bar_chart(risk_counts.set_index("Niveau de risque"))

    st.info(
        "Cette vue synthétise l’état opérationnel actuel de la flotte. "
        "Les niveaux de risque sont calculés à partir des comportements réels d’exploitation "
        "et de leur persistance dans le temps."
    )

# =========================
# PAGE 2 — VÉHICULES À RISQUE
# =========================
elif page == "🚗 Véhicules à risque":

    st.title("🚗 Véhicules à risque prioritaire")

    critical_df = risk_df[risk_df["risk_level"] != "OK"].copy()
    critical_df = critical_df.sort_values(
        ["risk_level", "consecutive_days_anomaly"],
        ascending=[True, False],
    )

    st.dataframe(
        critical_df[
            [
                "vehicle_id",
                "risk_level",
                "consecutive_days_anomaly",
                "mean_anomaly_score_7d",
            ]
        ],
        use_container_width=True,
    )

    st.warning(
        "Les véhicules listés ici présentent des anomalies persistantes "
        "dans leurs conditions d’exploitation. "
        "Une intervention préventive est recommandée en priorité sur les niveaux CRITICAL."
    )

# =========================
# PAGE 3 — TENDANCES & PERSISTANCE
# =========================
elif page == "📈 Tendances & persistance":

    st.title("📈 Analyse de la persistance des anomalies")

    st.subheader("Distribution des jours consécutifs anormaux")

    st.bar_chart(
        risk_df["consecutive_days_anomaly"].value_counts().sort_index()
    )

    st.markdown("---")

    st.subheader("Top véhicules les plus persistants")

    top_persistent = (
        risk_df.sort_values("consecutive_days_anomaly", ascending=False)
        .head(10)
    )

    st.dataframe(
        top_persistent[
            [
                "vehicle_id",
                "risk_level",
                "consecutive_days_anomaly",
                "mean_anomaly_score_7d",
            ]
        ],
        use_container_width=True,
    )

    st.info(
        "La persistance est un indicateur clé du risque opérationnel. "
        "Plus une anomalie se répète sur plusieurs jours, plus le risque d’immobilisation "
        "ou de dégradation s’accroît."
    )

# =========================
# PAGE 4 — RAPPORT HEBDOMADAIRE
# =========================
elif page == "📝 Rapport hebdomadaire":

    st.title("📝 Rapport hebdomadaire automatisé")

    reports = sorted((DATA_REPORTS / "weekly").glob("*.txt"))

    if not reports:
        st.warning("Aucun rapport hebdomadaire disponible.")
    else:
        latest_report = reports[-1]
        st.subheader(f"Rapport – Semaine du {latest_report.stem}")

        report_text = latest_report.read_text(encoding="utf-8")
        st.text_area("Résumé exécutif", report_text, height=300)

        st.success(
            "Ce rapport est généré automatiquement à partir des observations réelles "
            "de la flotte et vise à soutenir la prise de décision opérationnelle."
        )
        
        st.markdown(
            """
            <style>
            body { background-color: #0B1C2D; color: #E5E7EB; }
            .stMetric { background-color: #112A44; border-radius: 10px; padding: 15px; }
            </style>
            """,
            unsafe_allow_html=True,
        )

elif page == "🧠 Analyse des causes":

    st.title("🧠 Causes principales du risque")

    stress_counts = risk_df["dominant_stress"].value_counts()
    st.bar_chart(stress_counts)

    st.caption(
        "Ce graphique montre les types de stress opérationnels dominants observés "
        "sur la flotte cette semaine."
    )

    st.subheader("Exemples d’interprétation")
    st.dataframe(
        risk_df[
            [
                "vehicle_id",
                "dominant_stress",
                "interpretation",
                "risk_level",
            ]
        ].head(10),
        use_container_width=True,
    )

