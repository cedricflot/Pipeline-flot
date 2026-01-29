type Props = {
  title: string;
  value: string | number;
  subtitle?: string;
};

export default function KpiCard({ title, value, subtitle }: Props) {
  return (
    <div className="kpi-card">
      <h4>{title}</h4>
      <h2>{value}</h2>
      {subtitle && <p>{subtitle}</p>}
    </div>
  );
}