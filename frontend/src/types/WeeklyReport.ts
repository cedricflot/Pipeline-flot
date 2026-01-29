export interface WeeklyReport {
  meta: {
    week_start: string;
    week_end: string;
    total_vehicles_observed: number;
  };

  fleet_overview: {
    risk_distribution: Record<string, number>;
    risk_percentages: {
      ok: number;
      warning: number;
      critical: number;
    };
    fleet_health_status: string;
    risk_concentration: {
      top_3_share: number;
    };
  };

  fleet_evolution: {
    delta_risk_percentages: {
      ok: number;
      warning: number;
      critical: number;
    };
  };

  vehicles_at_risk: {
    total_at_risk: number;
    display_limit: number;
    vehicles: VehicleRisk[];
  };

  stress_analysis: {
    stress_distribution: Record<string, number>;
  };
}

export interface VehicleRisk {
  vehicle_id: string;
  rank: number;
  risk_level: string;
  risk_score: number;
  anomaly_days_7d: number;
  consecutive_days: number;
  dominant_stress: string[];
  key_metrics: {
    avg_speed: number;
    stop_count: number;
    idling_ratio: number;
  };
}
