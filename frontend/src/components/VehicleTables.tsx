import type { VehicleRisk } from "../types/WeeklyReport";
import "./layout.css";

export default function VehiclesTable({ vehicles }: { vehicles: VehicleRisk[] }) {
  return (
    <table className="vehicles-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Vehicle</th>
          <th>Risk</th>
          <th>Score</th>
          <th>Main stress</th>
        </tr>
      </thead>
      <tbody>
        {vehicles.map(v => (
          <tr key={v.vehicle_id}>
            <td>{v.rank}</td>
            <td>{v.vehicle_id}</td>
            <td>
              <span className={`badge ${v.risk_level.toLowerCase()}`}>
                {v.risk_level}
              </span>
            </td>
            <td>{v.risk_score}</td>
            <td>{v.dominant_stress.join(", ")}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}