"use client";

import React, { useState, useEffect } from "react";
import { Terminal, RefreshCw, Key, Globe } from "lucide-react";
import { getApiUrl, setApiUrl, getAdminKey, setAdminKey } from "@/lib/api";

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onRefresh: () => void;
  isRefreshing: boolean;
}

export function Header({ activeTab, setActiveTab, onRefresh, isRefreshing }: HeaderProps) {
  const [time, setTime] = useState<string>("");
  const [showConfigModal, setShowConfigModal] = useState(false);
  const [currentUrl, setCurrentUrl] = useState("");
  const [currentKey, setCurrentKey] = useState("");

  useEffect(() => {
    setCurrentUrl(getApiUrl());
    setCurrentKey(getAdminKey());

    const update = () => {
      const now = new Date();
      setTime(now.toUTCString().replace("GMT", "UTC"));
    };
    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, []);

  const saveConfig = () => {
    setApiUrl(currentUrl);
    setAdminKey(currentKey);
    setShowConfigModal(false);
    onRefresh();
  };

  return (
    <>
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

          {/* Right: API Target, Time & Sync */}
          <div className="flex items-center gap-3">
            {/* Live API target pill */}
            <button
              onClick={() => setShowConfigModal(true)}
              className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/[0.04] border border-white/[0.08] hover:border-cyan-400/50 text-slate-300 text-xs font-mono transition"
              title="Click to configure live API URL or master key"
            >
              <Globe className="w-3 h-3 text-cyan-400" />
              <span className="max-w-[130px] truncate">{currentUrl.replace("https://", "").replace("http://", "")}</span>
            </button>

            <span className="hidden sm:inline font-mono text-xs text-slate-400 tabular-nums">
              {time || "UTC 00:00:00"}
            </span>

            <div className="h-4 w-px bg-white/[0.08] hidden sm:block"></div>

            <button
              onClick={onRefresh}
              disabled={isRefreshing}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-white/[0.08] bg-white/[0.03] hover:bg-white/[0.06] text-xs font-mono text-slate-300 hover:text-white transition disabled:opacity-50"
              title="Sync Live Ledger"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin text-cyan-400" : ""}`} />
              <span className="hidden sm:inline">Sync</span>
            </button>
          </div>
        </div>
      </header>

      {/* Config Modal */}
      {showConfigModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4">
          <div className="rounded-2xl bg-[#0d111a] border border-cyan-500/30 p-6 max-w-md w-full shadow-2xl">
            <h4 className="text-base font-semibold text-white mb-1 flex items-center gap-2">
              <Key className="w-4 h-4 text-cyan-400" />
              Live Backend Connection Config
            </h4>
            <p className="text-xs text-slate-400 mb-4">
              Connect this dashboard to your live production or local backend.
            </p>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">Backend API URL</label>
                <input
                  type="text"
                  value={currentUrl}
                  onChange={(e) => setCurrentUrl(e.target.value)}
                  className="w-full px-3 py-2 bg-[#07090e] border border-white/[0.1] rounded-xl text-white font-mono text-xs focus:border-cyan-400 outline-none"
                  placeholder="https://checkerleak.com or http://localhost:8000"
                />
                <div className="flex gap-2 mt-1.5">
                  <button
                    onClick={() => setCurrentUrl("https://checkerleak.com")}
                    className="text-[11px] font-mono text-cyan-400 hover:underline"
                  >
                    Use Live Production (checkerleak.com)
                  </button>
                  <span className="text-slate-600">·</span>
                  <button
                    onClick={() => setCurrentUrl("http://localhost:8000")}
                    className="text-[11px] font-mono text-emerald-400 hover:underline"
                  >
                    Use Local Backend
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">Master Admin Secret Key</label>
                <input
                  type="password"
                  value={currentKey}
                  onChange={(e) => setCurrentKey(e.target.value)}
                  className="w-full px-3 py-2 bg-[#07090e] border border-white/[0.1] rounded-xl text-white font-mono text-xs focus:border-cyan-400 outline-none"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2 mt-6">
              <button
                onClick={() => setShowConfigModal(false)}
                className="px-4 py-2 rounded-xl text-xs font-mono text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={saveConfig}
                className="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-semibold text-xs font-mono transition"
              >
                Save & Connect Live
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
