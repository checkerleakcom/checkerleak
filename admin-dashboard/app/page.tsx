"use client";

import React, { useState } from "react";
import { Header } from "@/components/Header";
import { HeroMetricBand } from "@/components/HeroMetricBand";
import { ChartInventoryBand } from "@/components/ChartInventoryBand";
import { DataTableBand } from "@/components/DataTableBand";
import { FooterBand } from "@/components/FooterBand";

export default function AdminDashboardPage() {
  const [activeTab, setActiveTab] = useState("overview");
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
    }, 600);
  };

  return (
    <div className="min-h-screen bg-[#07090e] text-slate-100 flex flex-col selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Header & Global Status */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
      />

      {/* Main Content Dashboard Container with Generous Spacing */}
      <main className="flex-1 max-w-[1520px] w-full mx-auto px-6 sm:px-10 lg:px-12 pt-8">
        {/* Band 1: Hero Metric (3x Lead) + Dedicated Smooth Area Chart + Asymmetric Side Stats */}
        <HeroMetricBand />

        {/* Band 3: Diverse Chart Inventory (Donut, Ranked Bars, Clean Telemetry) */}
        <ChartInventoryBand />

        {/* Band 4: Real Interactive Sorting & Searchable Data Table */}
        <DataTableBand />

        {/* Band 5: Deliberate Termination Line */}
        <FooterBand />
      </main>
    </div>
  );
}
