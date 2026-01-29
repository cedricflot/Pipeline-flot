import { createBrowserRouter } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard";
import Vehicles from "./pages/Vehicles";
import Trends from "./pages/Trends";
import WeeklyReport from "./pages/WeeklyReport";

export const router = createBrowserRouter([
  {
    element: <MainLayout />,
    children: [
      { path: "/", element: <Dashboard /> },
      { path: "/vehicles", element: <Vehicles /> },
      { path: "/trends", element: <Trends /> },
      { path: "/weekly", element: <WeeklyReport /> },
    ],
  },
]);