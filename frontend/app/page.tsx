import { DashboardSidebar } from "@/components/dashboard/sidebar";
import { DashboardHeader } from "@/components/dashboard/header";
import { KPICards } from "@/components/dashboard/kpi-cards";
import { RiskDistributionChart } from "@/components/dashboard/risk-distribution-chart";
import { VehiclesAtRiskTable } from "@/components/dashboard/vehicles-at-risk-table";

async function getWeeklyReport() {
  const res = await fetch("http://127.0.0.1:8000/api/weekly-report/latest", {
    cache: "no-store", // IMPORTANT : données toujours fraîches
  });

  if (!res.ok) {
    throw new Error("Failed to fetch weekly report");
  }

  return res.json();
}

export default async function DashboardPage() {
  const data = await getWeeklyReport();

  return (
    <div className="flex min-h-screen bg-background">
      <DashboardSidebar />
      <main className="flex-1 overflow-auto">
        <div className="p-6 lg:p-8 max-w-[1600px]">
          <DashboardHeader />
          <KPICards data={data} />
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 mt-6">
            <RiskDistributionChart data={data} />
            <VehiclesAtRiskTable data={data} />
          </div>
        </div>
      </main>
    </div>
  );
}