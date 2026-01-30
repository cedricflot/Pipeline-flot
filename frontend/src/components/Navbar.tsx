import { NavLink } from "react-router-dom";
import "../styles/navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <h1>FLOT</h1>

      <NavLink to="/" end>
        Dashboard
      </NavLink>

      <NavLink to="/vehicles">
        Vehicles at Risk
      </NavLink>

      <NavLink to="/trends">
        Trends
      </NavLink>

      <NavLink to="/weekly">
        Weekly Report
      </NavLink>
    </nav>
  );
}