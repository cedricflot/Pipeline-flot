"use client";

import { Bell, Calendar, Search } from "lucide-react";
import { Button } from "@/components/ui/button";

export function DashboardHeader() {
  return (
    <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground tracking-tight">
          Operational Risk Dashboard
        </h1>
        <p className="text-sm text-muted-foreground mt-1">
          Real-time fleet monitoring and risk assessment
        </p>
      </div>
    </header>
  );
}
