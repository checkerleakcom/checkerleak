"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Header } from "@/components/Header";
import { HeroMetricBand } from "@/components/HeroMetricBand";
import { ChartInventoryBand } from "@/components/ChartInventoryBand";
import { DataTableBand } from "@/components/DataTableBand";
import { FooterBand } from "@/components/FooterBand";
import {
  fetchLiveStats,
  fetchLiveUsers,
  fetchLiveTransactions,
  adjustUserCreditsLive,
  toggleUserStatusLive,
  overrideTransactionLive,
  overrideUserEmailVerifiedLive,
  LiveStatsResponse,
  LiveUser,
  LiveTransaction,
} from "@/lib/api";

export default function AdminDashboardPage() {
  const [activeTab, setActiveTab] = useState("overview");
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [stats, setStats] = useState<LiveStatsResponse | null>(null);
  const [users, setUsers] = useState<LiveUser[]>([]);
  const [transactions, setTransactions] = useState<LiveTransaction[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const loadAllData = useCallback(async (showSpin = true) => {
    if (showSpin) setIsRefreshing(true);
    setErrorMessage(null);

    try {
      const [statsData, usersData, txsData] = await Promise.all([
        fetchLiveStats().catch((err) => {
          console.warn("Stats fetch warning:", err);
          return null;
        }),
        fetchLiveUsers().catch((err) => {
          console.warn("Users fetch warning:", err);
          return { total: 0, users: [] };
        }),
        fetchLiveTransactions().catch((err) => {
          console.warn("Txs fetch warning:", err);
          return { transactions: [] };
        }),
      ]);

      if (statsData) setStats(statsData);
      if (usersData?.users) setUsers(usersData.users);
      if (txsData?.transactions) setTransactions(txsData.transactions);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to connect to backend");
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadAllData(false);
    // Poll live data every 15 seconds
    const interval = setInterval(() => {
      loadAllData(false);
    }, 15000);
    return () => clearInterval(interval);
  }, [loadAllData]);

  const handleAdjustCredits = async (userId: number, delta: number, reason: string) => {
    await adjustUserCreditsLive(userId, delta, reason);
    await loadAllData(false);
  };

  const handleToggleStatus = async (userId: number, newStatus: "active" | "banned") => {
    await toggleUserStatusLive(userId, newStatus);
    await loadAllData(false);
  };

  const handleOverrideTx = async (txId: number) => {
    await overrideTransactionLive(txId);
    await loadAllData(false);
  };

  const handleToggleEmailVerified = async (userId: number, verified: boolean) => {
    await overrideUserEmailVerifiedLive(userId, verified);
    await loadAllData(false);
  };

  return (
    <div className="min-h-screen bg-[#07090e] text-slate-100 flex flex-col selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Header & Global Status */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onRefresh={() => loadAllData(true)}
        isRefreshing={isRefreshing}
      />

      {/* Main Content Dashboard Container with Generous Spacing */}
      <main className="flex-1 max-w-[1520px] w-full mx-auto px-6 sm:px-10 lg:px-12 pt-8">
        {errorMessage && (
          <div className="mb-6 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono flex items-center justify-between">
            <span>Notice: {errorMessage}. Check backend connection or secret key.</span>
            <button onClick={() => loadAllData(true)} className="underline font-bold ml-4">Retry</button>
          </div>
        )}

        {/* Band 1: Real Live Hero Metric (No fake demo data) */}
        <HeroMetricBand stats={stats} isLoading={isLoading} />

        {/* Band 3: Diverse Chart Inventory */}
        <ChartInventoryBand />

        {/* Band 4: Real Live Data Table (Real Users & Real Crypto Transactions) */}
        <DataTableBand
          users={users}
          transactions={transactions}
          isLoading={isLoading}
          onAdjustCredits={handleAdjustCredits}
          onToggleStatus={handleToggleStatus}
          onToggleEmailVerified={handleToggleEmailVerified}
          onOverrideTx={handleOverrideTx}
          onRefresh={() => loadAllData(true)}
        />

        {/* Band 5: Deliberate Termination Line */}
        <FooterBand />
      </main>
    </div>
  );
}
