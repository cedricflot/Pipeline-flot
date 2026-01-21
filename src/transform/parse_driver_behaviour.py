import json
from pathlib import Path
from datetime import date

import pandas as pd


def parse_driver_behaviour(
    input_json_path: str,
    output_csv_path: str,
    run_date: date,
) -> None:
    with open(input_json_path, "r", encoding="utf-8") as f:
        payload: Dict[str, Any] = json.load(f)

        if "data" not in payload:
            raise RuntimeError(f"Invalid Fleetmatic payload:no 'data' key in {input_json_path}")


        vehicles: List[Dict[str, Any]] = json.load(f)

        if not vehicles:
            raise RuntimeError(f"No vehicle data found in {input_json_path}")
            "Cannot generate csv"
    rows = []

    for vehicle in payload.get("data", []):
        driving_duration = vehicle.get("driving_duration") or 0
        excessive_idling = (
            vehicle.get("excessive_idling", {}).get("duration") or 0
        )

        row = {
            "vehicle_id": vehicle.get("unit_id"),
            "date": run_date.format(),

            "distance_km": vehicle.get("distance_gps") or 0,
            "driving_duration_min": driving_duration / 60,
            "avg_speed": vehicle.get("avg_speed") or 0,

            "stop_count": vehicle.get("stop_count") or 0,
            "stop_duration_hours": (vehicle.get("stop_duration") or 0) / 3600,

            "harsh_cornering_count": (
                vehicle.get("harsh_cornering", {}).get("count") or 0
            ),

            "excessive_idling_duration": excessive_idling,
            "idling_ratio": (
                excessive_idling / driving_duration
                if driving_duration > 0 else 0
            ),
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    out_dir = Path("data") / "processed" / "daily_vehicle_metrics"
    out_dir.mkdir(parents=True, exist_ok=True)

    output_path_csv = out_dir / f"{run_date.isoformat()}.csv"
    df.to_csv(output_path_csv, index=False)

    # 6. Vérifications finales
    if not output_path_csv.exists():
        raise RuntimeError("CSV file was not created")

    if output_path_csv.stat().st_size == 0:
        raise RuntimeError("CSV file is empty")

return str(output_path_csv)