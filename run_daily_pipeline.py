from __future__ import annotations

from datetime import date

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

    run_date = date.today().isoformat()

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
    


if __name__ == "__main__":
    main()