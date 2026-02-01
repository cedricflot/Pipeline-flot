"use client";

import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Truck,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

type WeeklyReport = {
  meta: {
    total_vehicles_observed: number;
  };
  fleet_overview: {
    risk_percentages: {
      ok: number;
      warning: number;
      critical?: number; // <- optionnel
    };
  };
};

export function KPICards({ data }: { data: WeeklyReport | null }) {
  // 🛡️ Protection absolue
  if (!data || !data.fleet_overview) {
    return null;
  }

  const {
    ok = 0,
    warning = 0,
    critical = 0,
  } = data.fleet_overview.risk_percentages;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <KPICard
        title="Vehicles OK"
        value={`${ok}%`}
        icon={<CheckCircle2 />}
        variant="success"
      />
      <KPICard
        title="Warnings"
        value={`${warning}%`}
        icon={<AlertTriangle />}
        variant="warning"
      />
      <KPICard
        title="Critical"
        value={`${critical}%`}
        icon={<XCircle />}
        variant="critical"
      />
      <KPICard
        title="Vehicles Observed"
        value={data.meta.total_vehicles_observed}
        icon={<Truck />}
        variant="neutral"
      />
    </div>
  );
}

function KPICard({
  title,
  value,
  icon,
  variant,
}: {
  title: string;
  value: number | string;
  icon: React.ReactNode;
  variant: "success" | "warning" | "critical" | "neutral";
}) {
  const colors = {
    success: "text-success bg-success/10",
    warning: "text-warning bg-warning/10",
    critical: "text-critical bg-critical/10",
    neutral: "text-muted-foreground bg-muted",
  };

  return (
    <Card className="bg-card border-border">
      <CardContent className="p-5 flex justify-between items-start">
        <div>
          <p className="text-sm text-muted-foreground">{title}</p>
          <p className="text-3xl font-bold">{value}</p>
        </div>
        <div className={`p-2 rounded-lg ${colors[variant]}`}>
          {icon}
        </div>
      </CardContent>
    </Card>
  );
}