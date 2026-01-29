import { PieChart, Pie, Cell, Tooltip } from "recharts";

const COLORS = ["#2ecc71", "#f1c40f", "#e74c3c"];

export default function RiskDistributionChart({ data }: any) {
  const chartData = Object.entries(data).map(([k, v]) => ({
    name: k.toUpperCase(),
    value: v,
  }));

  return (
    <PieChart width={300} height={300}>
      <Pie data={chartData} dataKey="value" outerRadius={120}>
        {chartData.map((_, i) => (
          <Cell key={i} fill={COLORS[i]} />
        ))}
      </Pie>
      <Tooltip />
    </PieChart>
  );
}
