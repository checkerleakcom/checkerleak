"use client";

import React, { useState } from "react";
import { ArrowUpRight, Cpu, Wallet } from "lucide-react";

export function HeroMetricBand() {
  const [range, setRange] = useState<"24h" | "7d" | "30d">("30d");

  // Smooth deterministic SVG curves for time-series chart
  const areaPath30d =
    "M 0 120 C 100 110, 180 95, 260 85 C 340 75, 420 50, 500 35 C 580 20, 620 10, 640 8 L 640 160 L 0 160 Z";
  const linePath30d =
    "M 0 120 C 100 110, 180 95, 260 85 C 340 75, 420 50, 500 35 C 580 20, 620 10, 640 8";

  const areaPath7d =
    "M 0 130 C 120 115, 240 90, 360 65 C 480 40, 560 25, 640 10 L 640 160 L 0 160 Z";
  const linePath7d =
    "M 0 130 C 120 115, 240 90, 360 65 C 480 40, 560 25, 640 10";

  const activeArea = range === "7d" ? areaPath7d : areaPath30d;
  const activeLine = range === "7d" ? linePath7d : linePath30d;

  return (
    <section className="mb-8">
      <div className="grid grid-cols-12 gap-6">
        {/* ================= BAND 1: HERO METRIC (SPAN 8) ================= */}
        <div className="col-span-12 lg:col-span-8 rounded-2xl bg-[#0d111a] border border-white/[0.07] p-8 sm:p-10 flex flex-col justify-between relative overflow-hidden group">
          {/* Subtle noise backdrop */}
          <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:24px_24px] opacity-15 pointer-events-none" />

          {/* Header Row */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative z-10">
            <div>
              <span className="text-xs font-mono font-medium uppercase tracking-wider text-slate-400">
                Gross Telephony Volume
              </span>
              <p className="text-xs text-slate-500 mt-1">
                Real-time commercial verification turnover and API queries
              </p>
            </div>

            {/* Range Toggle */}
            <div className="flex items-center gap-1 bg-[#07090e] p-1 rounded-xl border border-white/[0.06] text-xs font-mono self-start sm:self-auto">
              {(["24h", "7d", "30d"] as const).map((r) => (
                <button
                  key={r}
                  onClick={() => setRange(r)}
                  className={`px-3 py-1 rounded-lg transition-all uppercase ${
                    range === r
                      ? "bg-white/[0.12] text-white font-bold shadow-xs"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          {/* Large Hero Metric Display */}
          <div className="my-8 relative z-10 flex flex-wrap items-baseline gap-4">
            <div className="text-5xl sm:text-6xl font-mono font-extrabold tracking-tight text-white tabular-nums">
              $148,920.40
            </div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1 text-xs font-mono font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <ArrowUpRight className="w-3.5 h-3.5" />
                +24.8%
              </span>
              <span className="text-xs font-mono text-slate-400">
                / 14,892,104 pings
              </span>
            </div>
          </div>

          {/* Smooth SVG Area Chart */}
          <div className="w-full h-40 relative z-10 mt-auto">
            <svg
              viewBox="0 0 640 160"
              preserveAspectRatio="none"
              className="w-full h-full overflow-visible"
              role="img"
              aria-label="Gross Telephony Volume time series"
            >
              <defs>
                <linearGradient id="heroSmoothGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.22" />
                  <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.0" />
                </linearGradient>
              </defs>
              <path d={activeArea} fill="url(#heroSmoothGradient)" className="transition-all duration-500" />
              <path
                d={activeLine}
                fill="none"
                stroke="#06b6d4"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="transition-all duration-500"
              />
            </svg>
          </div>

          {/* Clean timeline axis */}
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-3 border-t border-white/[0.04] relative z-10">
            <span>30 DAYS AGO</span>
            <span>15 DAYS AGO</span>
            <span>7 DAYS AGO</span>
            <span className="text-cyan-400 font-semibold">TODAY (LIVE)</span>
          </div>
        </div>

        {/* ================= BAND 1 (SIDE): ASYMMETRIC METRICS (SPAN 4) ================= */}
        <div className="col-span-12 lg:col-span-4 flex flex-col gap-6">
          {/* Side Card 1: Circulating Balance */}
          <div className="flex-1 rounded-2xl bg-[#0d111a] border border-white/[0.07] p-7 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono uppercase tracking-wider text-slate-400 flex items-center gap-2">
                <Wallet className="w-4 h-4 text-cyan-400" />
                Circulating Balance
              </span>
              <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                100% Backed
              </span>
            </div>

            <div className="my-4">
              <div className="text-3xl font-mono font-bold text-white tabular-nums">
                $34,180.25
              </div>
              <p className="text-xs text-slate-400 mt-1 font-mono">
                Across <strong className="text-slate-200">4,821</strong> enterprise wallets
              </p>
            </div>

            {/* Clean Progress Breakdown */}
            <div className="pt-3 border-t border-white/[0.04]">
              <div className="flex justify-between text-xs font-mono text-slate-400 mb-2">
                <span>Crypto (BTC/USDT): 68%</span>
                <span className="text-slate-200">Cards: 32%</span>
              </div>
              <div className="w-full h-1.5 bg-[#07090e] rounded-full overflow-hidden flex">
                <div className="h-full bg-cyan-400 rounded-full" style={{ width: "68%" }} />
                <div className="h-full bg-emerald-400 rounded-full" style={{ width: "32%" }} />
              </div>
            </div>
          </div>

          {/* Side Card 2: Engine Ping Latency */}
          <div className="flex-1 rounded-2xl bg-[#0d111a] border border-white/[0.07] p-7 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono uppercase tracking-wider text-slate-400 flex items-center gap-2">
                <Cpu className="w-4 h-4 text-emerald-400" />
                Carrier Ping Latency
              </span>
              <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Sub-150ms
              </span>
            </div>

            <div className="my-4">
              <div className="text-3xl font-mono font-bold text-emerald-400 tabular-nums flex items-baseline gap-2">
                118<span className="text-base font-normal text-slate-400">ms avg</span>
              </div>
              <p className="text-xs text-slate-400 mt-1 font-mono">
                SS7 Gateway response time across 240+ countries
              </p>
            </div>

            {/* Clean sparkline indicator */}
            <div className="w-full h-8 pt-1">
              <svg viewBox="0 0 200 30" preserveAspectRatio="none" className="w-full h-full">
                <polyline
                  fill="none"
                  stroke="#10b981"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  points="0,18 20,20 40,15 60,18 80,12 100,15 120,10 140,14 160,8 180,11 200,6"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
