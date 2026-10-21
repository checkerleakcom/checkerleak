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
    <header className="border-b border-white/[0.08] bg-[#07090e]/90 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-[1520px] mx-auto px-4 sm:px-6 lg:px-8">
        {/* Top telemetry status bar */}
        <div className="flex items-center justify-between py-2 border-b border-white/[0.04] text-[11px] text-slate-400 font-mono">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              CLUSTER ACTIVE
            </span>
            <span className="text-slate-600">/</span>
            <span>NODE: us-east-core-01</span>
            <span className="text-slate-600 hidden sm:inline">/</span>
            <span className="text-slate-500 hidden sm:inline">GATEWAY: SS7/HLR PROXY</span>
          </div>

          <div className="flex items-center gap-4">
            <span className="hidden md:inline tabular-nums text-slate-400">{time || "UTC 00:00:00"}</span>
            <span className="text-slate-600 hidden md:inline">|</span>
            <span className="flex items-center gap-1 text-cyan-400">
              <Shield className="w-3 h-3 text-cyan-400" />
              MASTER GUARD AUTHENTICATED
            </span>
          </div>
        </div>

        {/* Primary Navbar */}
        <div className="flex items-center justify-between h-14">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white shadow-xs">
                <Terminal className="w-4 h-4 text-white" />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-semibold tracking-tight text-white flex items-center gap-1.5">
                  CheckerLeak <span className="text-[10px] uppercase font-mono px-1.5 py-0.2 rounded bg-white/[0.06] text-slate-300 border border-white/[0.08]">v2.2 Cockpit</span>
                </span>
              </div>
            </div>

            {/* Navigation Tabs */}
            <nav className="hidden sm:flex items-center gap-1 text-xs font-medium">
              {[
                { id: "overview", label: "Overview & Revenue" },
                { id: "telemetry", label: "Live Telemetry" },
                { id: "users", label: "User Directory" },
                { id: "crypto", label: "Crypto Radar" },
              ].map((t) => (
                <button
                  key={t.id}
                  onClick={() => setActiveTab(t.id)}
                  className={`px-3 py-1.5 rounded-md transition-colors ${
                    activeTab === t.id
                      ? "bg-white/[0.1] text-white shadow-2xs font-semibold"
                      : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.04]"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Action triggers */}
          <div className="flex items-center gap-2">
            <button
              onClick={onRefresh}
              disabled={isRefreshing}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded border border-white/[0.08] bg-[#0d111a] hover:bg-[#121824] text-xs font-mono text-slate-300 hover:text-white transition disabled:opacity-50"
            >
              <RefreshCw className={`w-3 h-3 ${isRefreshing ? "animate-spin text-cyan-400" : ""}`} />
              <span>SYNC LEDGER</span>
            </button>
            <div className="h-4 w-px bg-white/[0.08] mx-1"></div>
            <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono">
              <Radio className="w-2.5 h-2.5" />
              STREAM LIVE
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
