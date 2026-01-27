from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

from datetime import date

from src.reporting.weekly_report_builder import build_weekly_report
from src.models.risk_persistence import run_risk_persistence
from src.models.isolation_forest import run_isolation_forest
from src.transform.parse_driver_behaviour import parse_driver_behaviour
from src.extract.fleetmatic_api import (
    FleetmaticClient,
    default_raw_dir,
    load_cfg_from_env,
    save_raw_json,
)



def main():
    cfg = load_cfg_from_env()
    client = FleetmaticClient(cfg)

    run_date = date.today()

    # ⚠️ TEST AVEC UN SEUL VEHICULE (pour valider)
    units_ids = 733655  # mets un ID réel

    payload = client.fetch_driver_behaviour(
        units_ids=units_ids,
        date_from=run_date,
        date_till=run_date,
    )

    out_dir = default_raw_dir(date.today())
    path = save_raw_json(payload, out_dir, f"driver_behaviour_{units_ids}.json")

    print(f"[OK] Driver behaviour saved to {path}")

    processed_csv_path = parse_driver_behaviour(
        input_json_path=path,
        output_csv_path= f"data/processed/daily_vehicle_metrics/{run_date}.csv",
        run_date=run_date,
    )

    print(f"[OK] Daily vehicles metrics saved to {processed_csv_path}")

    anomalies_path = run_isolation_forest(
        processed_csv_path=processed_csv_path,
        run_date=run_date,
    )

    print(f"[OK] Daily anomalies saved to {anomalies_path}")

    risk_report_path = run_risk_persistence(
        daily_metrics_dir="data/analytics/anomalies_daily",
        output_path=f"data/processed/risk_reports/{run_date}_risk_report.csv",
        window_days=7,
    )

    print(f"[OK] Weekly risk report generated at {risk_report_path}")

    weekly_report = build_weekly_report(
        risk_report_path=risk_report_path,
        output_dir="data/reports/weekly",
        run_date=run_date,
    )

    print(f"[OK] Weekly report generated:")
    print(f" - Text: {weekly_report['text']}")
    print(f" - JSON: {weekly_report['json']}")


if __name__ == "__main__":
    main()