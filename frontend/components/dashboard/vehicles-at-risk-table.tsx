"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

type Vehicle = {
  vehicle_id: number;
  rank: number;
  risk_level: "WARNING" | "CRITICAL";
  risk_score: number;
  dominant_stress: string[];
};

type WeeklyReport = {
  vehicles_at_risk?: {
    vehicles?: Vehicle[];
  };
};

export function VehiclesAtRiskTable({
  data,
}: {
  data: WeeklyReport | null;
}) {
  const vehicles = data?.vehicles_at_risk?.vehicles;

  // 🛡️ Sécurité totale
  if (!vehicles || vehicles.length === 0) {
    return (
      <Card className="bg-card border-border">
        <CardHeader>
          <CardTitle>Top Vehicles at Risk</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground">
          No vehicles currently at risk 🎉
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-card border-border">
      <CardHeader>
        <CardTitle>Top Vehicles at Risk</CardTitle>
        <p className="text-sm text-muted-foreground">
          Vehicles requiring attention
        </p>
      </CardHeader>

      <CardContent className="p-0">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-y border-border bg-muted/40">
              <th className="px-4 py-3 text-left">#</th>
              <th className="px-4 py-3 text-left">Vehicle</th>
              <th className="px-4 py-3 text-left">Risk</th>
              <th className="px-4 py-3 text-left">Score</th>
              <th className="px-4 py-3 text-left">Main stress</th>
            </tr>
          </thead>
          <tbody>
            {vehicles.map((v) => (
              <tr
                key={v.vehicle_id}
                className="border-b border-border hover:bg-muted/20"
              >
                <td className="px-4 py-3">{v.rank}</td>
                <td className="px-4 py-3 font-medium">{v.vehicle_id}</td>
                <td className="px-4 py-3">
                  <span
                    className={cn(
                      "inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-semibold",
                      v.risk_level === "CRITICAL"
                        ? "bg-critical/15 text-critical"
                        : "bg-warning/15 text-warning"
                    )}
                  >
                    <AlertTriangle className="w-3 h-3" />
                    {v.risk_level}
                  </span>
                </td>
                <td className="px-4 py-3">{v.risk_score}</td>
                <td className="px-4 py-3 text-muted-foreground max-w-[220px]">
                  <div className="line-clamp-2 break-words">
                    {v.dominant_stress.join(", ")}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent>
    </Card>
  );
}