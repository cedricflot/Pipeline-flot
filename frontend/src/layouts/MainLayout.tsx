// src/layouts/MainLayout.tsx
import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import "../styles/layout.css";

export default function MainLayout() {
  return (
    <div className="layout">
      <Navbar />
      <div className="content">
        <Outlet />
      </div>
    </div>
  );
}