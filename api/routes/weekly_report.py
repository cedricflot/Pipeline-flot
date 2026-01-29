from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()

WEEKLY_REPORTS_DIR = Path("data/reports/weekly")


@router.get("/weekly-report/latest")
def get_latest_weekly_report():
    files = sorted(WEEKLY_REPORTS_DIR.glob("*.json"))

    if not files:
        raise HTTPException(status_code=404, detail="No weekly report found")

    latest = files[-1]

    with latest.open("r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/weekly-report/{date}")
def get_weekly_report_by_date(date: str):
    path = WEEKLY_REPORTS_DIR / f"{date}_weekly_report.json"

    if not path.exists():
        raise HTTPException(status_code=404, detail="Weekly report not found")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)