import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `block rounded-lg px-3 py-2 text-sm font-medium ${
    isActive
      ? "bg-slate-200 text-slate-900"
      : "text-slate-600 hover:bg-slate-100"
  }`;

export default function Navbar() {
  return (
    <aside className="w-64 bg-white border-r p-5">
      <h1 className="text-xl font-bold mb-8">FLOT</h1>

      <nav className="space-y-2">
        <NavLink to="/" end className={linkClass}>
          Dashboard
        </NavLink>
        <NavLink to="/vehicles" className={linkClass}>
          Vehicles at Risk
        </NavLink>
        <NavLink to="/trends" className={linkClass}>
          Trends
        </NavLink>
        <NavLink to="/weekly" className={linkClass}>
          Weekly Report
        </NavLink>
      </nav>
    </aside>
  );
}
