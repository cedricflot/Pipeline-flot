"use client";

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type WeeklyReport = {
  fleet_overview?: {
    risk_distribution?: {
      OK?: number;
      WARNING?: number;
      CRITICAL?: number;
    };
  };
};

export function RiskDistributionChart({
  data,
}: {
  data: WeeklyReport | null;
}) {
  // 🛡️ Sécurité totale
  const distribution = data?.fleet_overview?.risk_distribution;

  if (!distribution) {
    return null;
  }

  const chartData = [
    {
      name: "OK",
      value: distribution.OK ?? 0,
      color: "#22c55e",
    },
    {
      name: "Warning",
      value: distribution.WARNING ?? 0,
      color: "#eab308",
    },
    {
      name: "Critical",
      value: distribution.CRITICAL ?? 0,
      color: "#ef4444",
    },
  ].filter((item) => item.value > 0); // évite les parts vides

  const total = chartData.reduce((sum, d) => sum + d.value, 0);

  return (
    <Card className="bg-card border-border min-h-[480px]">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold">
          Risk Distribution
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Fleet health overview
        </p>
      </CardHeader>

      <CardContent>
        <div className="h-[280px] relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                cx="50%"
                cy="45%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={3}
                stroke="none"
              >
                {chartData.map((entry, index) => (
                  <Cell key={index} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>

          {/* Total au centre */}
          
        </div>
      </CardContent>
    </Card>
  );
}