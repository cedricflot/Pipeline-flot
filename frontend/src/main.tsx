import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard";
import Vehicles from "./pages/Vehicles";
import Trends from "./pages/Trends";
import Weekly from "./pages/Weekly";

import "./styles/variables.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: "vehicles", element: <Vehicles /> },
      { path: "trends", element: <Trends /> },
      { path: "weekly", element: <Weekly /> },
    ],
  },
]);


ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);