import  { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-flotBlue text-white px-8 py-4 flex gap-6">
      <span className="font-bold">Flot</span>

      <NavLink to="/" className="hover:text-flotGreen">
        Dashboard
      </NavLink>
      <NavLink to="/vehicles" className="hover:text-flotGreen">
        Vehicles at risk
      </NavLink>
      <NavLink to="/trends" className="hover:text-flotGreen">
        Trends
      </NavLink>
      <NavLink to="/weekly" className="hover:text-flotGreen">
        Weekly report
      </NavLink>
    </nav>
  );
}