import type { VehicleRisk } from "../types/WeeklyReport";

export default function VehiclesTable({ vehicles }: { vehicles: VehicleRisk[] }) {
  return (
    <table className="vehicles-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Vehicle</th>
          <th>Risk</th>
          <th>Score</th>
          <th>Stress</th>
        </tr>
      </thead>
      <tbody>
        {vehicles.map(v => (
          <tr key={v.vehicle_id}>
            <td>{v.rank}</td>
            <td>{v.vehicle_id}</td>
            <td>{v.risk_level}</td>
            <td>{v.risk_score}</td>
            <td>{v.dominant_stress.join(", ")}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}