import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { WeeklyReport } from "../types/WeeklyReport";

import KpiCard from "../components/KPICard";
import RiskDistributionChart from "../components/RiskDistributionChart";
import VehiclesTable from "../components/VehicleTables";

export default function Dashboard() {
  const [data, setData] = useState<WeeklyReport | null>(null);

  const load = async () => {
    const res = await api.get("/api/weekly-report/latest");
    setData(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  if (!data) return <p>Loading…</p>;

  return (
    
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">
          Fleet Operational Risk Dashboard
        </h1>
        <button
          onClick={load}
          className="px-4 py-2 rounded-lg bg-teal-600 text-white hover:bg-teal-700"
        >
          Refresh
        </button>
      </header>
      {/* KPI */}
      <div className="grid grid-cols-4 gap-6">
        <KpiCard
          title="Vehicles observed"
          value={data.meta.total_vehicles_observed}
          variant="neutral"
        />
        <KpiCard
          title="OK (%)"
          value={data.fleet_overview.risk_percentages.ok}
          variant="ok"
        />
        <KpiCard
          title="Warning (%)"
          value={data.fleet_overview.risk_percentages.warning}
          variant="warning"
        />
        <KpiCard
          title="Critical (%)"
          value={data.fleet_overview.risk_percentages.critical}
          variant="critical"
        />
      </div>

      {/* Charts + Table */}
      <div className="grid grid-cols-2 gap-8">
        <div className="bg-white rounded-xl p-6 shadow">
          <h3 className="mb-4 font-medium">Risk distribution</h3>
          <RiskDistributionChart
            data={data.fleet_overview.risk_distribution}
          />
        </div>

        <div>
          <h3 className="mb-4 font-medium">Top vehicles at risk</h3>
          <VehiclesTable vehicles={data.vehicles_at_risk.vehicles} />
        </div>
      </div>
    </div>
  );
}
