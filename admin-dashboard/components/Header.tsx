"use client";

import React, { useState, useEffect } from "react";
import { Terminal, Shield, RefreshCw, Radio } from "lucide-react";

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onRefresh: () => void;
  isRefreshing: boolean;
}

export function Header({ activeTab, setActiveTab, onRefresh, isRefreshing }: HeaderProps) {
  const [time, setTime] = useState<string>("");

  useEffect(() => {
    const update = () => {
      const now = new Date();
      setTime(now.toUTCString().replace("GMT", "UTC"));
    };
    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="border-b border-white/[0.06] bg-[#07090e]/80 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-[1520px] mx-auto px-6 lg:px-10 h-16 flex items-center justify-between">
        {/* Left: Brand & Engine status */}
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white shadow-sm">
              <Terminal className="w-4 h-4 text-white" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-base font-semibold tracking-tight text-white">
                CheckerLeak
              </span>
              <span className="text-xs text-slate-400 font-mono">Console</span>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex items-center gap-1">
            {[
              { id: "overview", label: "Overview" },
              { id: "telemetry", label: "Telemetry & 102 Engines" },
              { id: "users", label: "Users & Accounts" },
              { id: "crypto", label: "Crypto Radar" },
            ].map((t) => (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  activeTab === t.id
                    ? "bg-white/[0.08] text-white shadow-xs font-semibold"
                    : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.03]"
                }`}
              >
                {t.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Right: Live Telemetry, UTC Time & Actions */}
        <div className="flex items-center gap-4">
          <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Cluster 99.99%</span>
          </div>

          <span className="hidden sm:inline font-mono text-xs text-slate-400 tabular-nums">
            {time || "UTC 00:00:00"}
          </span>

          <div className="h-4 w-px bg-white/[0.08] hidden sm:block"></div>

          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-white/[0.08] bg-white/[0.03] hover:bg-white/[0.06] text-xs font-mono text-slate-300 hover:text-white transition disabled:opacity-50"
            title="Sync Ledger"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin text-cyan-400" : ""}`} />
            <span className="hidden sm:inline">Sync</span>
          </button>
        </div>
      </div>
    </header>
  );
}
