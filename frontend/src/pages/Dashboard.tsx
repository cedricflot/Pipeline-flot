import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { WeeklyReport } from "../types/WeeklyReport";

import KpiCard from "../components/KPICard";
import RiskDistributionChart from "../components/RiskDistributionChart";
import VehiclesTable from "../components/VehicleTables";

export default function Dashboard() {
  const [data, setData] = useState<WeeklyReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setLoading(true);
      const res = await api.get("/api/weekly-report/latest");
      setData(res.data);
      setError(null);
    } catch (e) {
      setError("Failed to load weekly report");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (loading) return <p>Loading dashboard…</p>;
  if (error) return <p>{error}</p>;
  if (!data) return <p>No data available</p>;

  return (
    <div className="dashboard">
      <h1>Fleet Operational Risk Dashboard</h1>

      {/* KPIs */}
      <div className="kpis">
        <KpiCard
          title="Vehicles observed"
          value={data.meta?.total_vehicles_observed ?? 0}
        />
        <KpiCard
          title="OK (%)"
          value={data.fleet_overview?.risk_percentages?.ok ?? 0}
        />
        <KpiCard
          title="Warning (%)"
          value={data.fleet_overview?.risk_percentages?.warning ?? 0}
        />
        <KpiCard
          title="Critical (%)"
          value={data.fleet_overview?.risk_percentages?.critical ?? 0}
        />
      </div>

      {/* Charts */}
      <div className="charts">
        {data.fleet_overview?.risk_distribution && (
          <RiskDistributionChart
            data={data.fleet_overview.risk_distribution}
          />
        )}
      </div>

      {/* Vehicles */}
      <h2>Top Vehicles at Risk</h2>
      {data.vehicles_at_risk?.vehicles && (
        <VehiclesTable vehicles={data.vehicles_at_risk.vehicles} />
      )}

      <button onClick={load}>Refresh data</button>
    </div>
  );
}
