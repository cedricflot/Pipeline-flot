from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from requests import Response


# =========================
# CONFIG
# =========================

@dataclass(frozen=True)
class FleetmaticConfig:
    base_url: str
    driver_behaviour_endpoint: str
    api_token: str
    timeout_seconds: int = 30
    max_retries: int = 3
    backoff_seconds: float = 1.5


# =========================
# CLIENT API
# =========================

class FleetmaticClient:
    def __init__(self, cfg: FleetmaticConfig) -> None:
        self.cfg = cfg
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        return {
            "key": self.cfg.api_token,
            "Accept": "application/json",
        }

    def fetch_driver_behaviour(
        self,
        units_ids: int,
        date_from: str,
        date_till: str,
    ) -> Dict[str, Any]:

        url = (
            self.cfg.base_url.rstrip("/")
            + "/"
            + self.cfg.driver_behaviour_endpoint.lstrip("/")
        )

        params = {
            "units_ids": units_ids,   
            "date_from": date_from,
            "date_till": date_till,
        }

        resp = self._request_with_retries(
            method="GET",
            url=url,
            params=params,
        )

        return resp.json()

    def _request_with_retries(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Response:
        last_exc: Optional[Exception] = None

        for attempt in range(1, self.cfg.max_retries + 1):
            try:
                resp = self.session.request(
                    method=method,
                    url=url,
                    headers=self._headers(),
                    params=params,
                    timeout=self.cfg.timeout_seconds,
                )

                if resp.status_code in (429, 500, 502, 503, 504):
                    time.sleep(self.cfg.backoff_seconds * attempt)
                    continue

                resp.raise_for_status()
                return resp

            except Exception as exc:
                last_exc = exc
                time.sleep(self.cfg.backoff_seconds * attempt)

        raise RuntimeError(
            f"Fleetmatic API request failed after retries: {last_exc}"
        ) from last_exc


# =========================
# UTILITAIRES
# =========================

def save_raw_json(payload: Dict[str, Any], out_dir: str, filename: str) -> str:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_path = Path(out_dir) / filename

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return str(out_path)


def default_raw_dir(run_date: date) -> str:
    return str(Path("data") / "raw" / "fleetmatic" / run_date.isoformat())


def load_cfg_from_env() -> FleetmaticConfig:
    base_url = os.environ.get("FLEETMATIC_BASE_URL", "").strip()
    token = os.environ.get("FLEETMATIC_API_TOKEN", "").strip()
    endpoint = os.environ.get(
        "FLEETMATIC_DRIVER_BEHAVIOUR_ENDPOINT", ""
    ).strip()

    if not base_url or not token or not endpoint:
        raise RuntimeError(
            "Missing env vars. Required:\n"
            "- FLEETMATIC_BASE_URL\n"
            "- FLEETMATIC_API_TOKEN\n"
            "- FLEETMATIC_DRIVER_BEHAVIOUR_ENDPOINT"
        )

    return FleetmaticConfig(
        base_url=base_url,
        driver_behaviour_endpoint=endpoint,
        api_token=token,
        timeout_seconds=int(os.environ.get("FLEETMATIC_TIMEOUT_SECONDS", "30")),
        max_retries=int(os.environ.get("FLEETMATIC_MAX_RETRIES", "3")),
        backoff_seconds=float(os.environ.get("FLEETMATIC_BACKOFF_SECONDS", "1.5")),
    )
