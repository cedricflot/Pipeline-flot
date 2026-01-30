type Props = {
  title: string;
  value: string | number;
  variant?: "ok" | "warning" | "critical" | "neutral";
};

const variantStyles = {
  ok: "border-l-green-500",
  warning: "border-l-yellow-500",
  critical: "border-l-red-500",
  neutral: "border-l-blue-500",
};

export default function KpiCard({
  title,
  value,
  variant = "neutral",
}: Props) {
  return (
    <div
      className={`bg-white rounded-xl p-5 shadow border-l-4 ${variantStyles[variant]}`}
    >
      <p className="text-sm text-slate-500 mb-1">{title}</p>
      <p className="text-3xl font-semibold">{value}</p>
    </div>
  );
}