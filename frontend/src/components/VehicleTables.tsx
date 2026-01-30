import type { VehicleRisk } from "../types/WeeklyReport";

export default function VehiclesTable({
  vehicles,
}: {
  vehicles: VehicleRisk[];
}) {
  return (
    <div className="overflow-x-auto bg-white rounded-xl shadow">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-slate-500">
          <tr>
            <th className="px-4 py-3 text-left">#</th>
            <th className="px-4 py-3 text-left">Vehicle</th>
            <th className="px-4 py-3 text-left">Risk</th>
            <th className="px-4 py-3 text-left">Score</th>
            <th className="px-4 py-3 text-left">Main stress</th>
          </tr>
        </thead>
        <tbody>
          {vehicles.map(v => (
            <tr key={v.vehicle_id} className="border-t">
              <td className="px-4 py-3">{v.rank}</td>
              <td className="px-4 py-3">{v.vehicle_id}</td>
              <td className="px-4 py-3">
                <span
                  className={`px-2 py-1 rounded text-xs font-medium ${
                    v.risk_level === "OK"
                      ? "bg-green-100 text-green-700"
                      : v.risk_level === "WARNING"
                      ? "bg-yellow-100 text-yellow-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {v.risk_level}
                </span>
              </td>
              <td className="px-4 py-3">{v.risk_score}</td>
              <td className="px-4 py-3">
                {v.dominant_stress.join(", ")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
