"use client";

import React, { useState } from "react";
import { ArrowUpRight, TrendingUp, Cpu, Wallet } from "lucide-react";

export function HeroMetricBand() {
  const [range, setRange] = useState<"24h" | "7d" | "30d">("30d");

  // Deterministic SVG coordinates for rolling area chart (viewBox 0 0 640 140)
  // 30 points representing healthy, high-throughput telecom verification curves
  const areaPath30d =
    "M 0 110 L 22 105 L 44 98 L 66 102 L 88 88 L 110 92 L 132 78 L 154 84 L 176 68 L 198 72 L 220 58 L 242 62 L 264 48 L 286 52 L 308 42 L 330 46 L 352 38 L 374 44 L 396 32 L 418 36 L 440 28 L 462 30 L 484 22 L 506 26 L 528 18 L 550 20 L 572 14 L 594 16 L 616 8 L 640 6 L 640 140 L 0 140 Z";
  const linePath30d =
    "M 0 110 L 22 105 L 44 98 L 66 102 L 88 88 L 110 92 L 132 78 L 154 84 L 176 68 L 198 72 L 220 58 L 242 62 L 264 48 L 286 52 L 308 42 L 330 46 L 352 38 L 374 44 L 396 32 L 418 36 L 440 28 L 462 30 L 484 22 L 506 26 L 528 18 L 550 20 L 572 14 L 594 16 L 616 8 L 640 6";

  const areaPath7d =
    "M 0 120 L 100 110 L 200 85 L 300 70 L 400 45 L 500 35 L 640 12 L 640 140 L 0 140 Z";
  const linePath7d =
    "M 0 120 L 100 110 L 200 85 L 300 70 L 400 45 L 500 35 L 640 12";

  const activeArea = range === "7d" ? areaPath7d : areaPath30d;
  const activeLine = range === "7d" ? linePath7d : linePath30d;

  return (
    <section className="mb-6">
      <div className="grid grid-cols-12 gap-4">
        {/* ================= BAND 1: HERO METRIC (SPAN 8) ================= */}
        <div className="col-span-12 lg:col-span-8 rounded-xl bg-[#0d111a] border border-white/[0.08] p-6 flex flex-col justify-between relative overflow-hidden group">
          {/* Subtle noise / hairline grid backdrop */}
          <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px] opacity-20 pointer-events-none" />

          {/* Header Row of Hero */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 relative z-10">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-medium uppercase tracking-wider text-slate-400">
                  Gross Telephony Volume
                </span>
                <span className="inline-flex items-center gap-1 text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <ArrowUpRight className="w-3 h-3" />
                  +24.8% vs last cycle
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                Total commercial API & on-chain verification turnover
              </p>
            </div>

            {/* Range Selector */}
            <div className="flex items-center gap-1 bg-[#07090e] p-1 rounded-lg border border-white/[0.06] text-xs font-mono">
              {(["24h", "7d", "30d"] as const).map((r) => (
                <button
                  key={r}
                  onClick={() => setRange(r)}
                  className={`px-2.5 py-1 rounded transition-colors uppercase ${
                    range === r
                      ? "bg-white/[0.12] text-white font-bold"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          {/* Hero Value: 3x Size */}
          <div className="my-5 relative z-10 flex flex-wrap items-baseline gap-3">
            <div className="text-4xl sm:text-5xl lg:text-6xl font-mono font-extrabold tracking-tight text-white tabular-nums">
              $148,920.40
            </div>
            <div className="text-sm font-mono text-slate-400">
              / <span className="text-slate-200 font-semibold">14,892,104</span> verified pings
            </div>
          </div>

          {/* Embedded Responsive SVG Area Chart */}
          <div className="w-full h-32 relative z-10 mt-auto">
            <svg
              viewBox="0 0 640 140"
              preserveAspectRatio="none"
              className="w-full h-full overflow-visible"
              role="img"
              aria-label="Gross Telephony Volume 30-day time series curve"
            >
              <defs>
                <linearGradient id="heroGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.28" />
                  <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.0" />
                </linearGradient>
              </defs>
              {/* Fill Area */}
              <path d={activeArea} fill="url(#heroGradient)" className="transition-all duration-300" />
              {/* Stroke Polyline */}
              <path
                d={activeLine}
                fill="none"
                stroke="#06b6d4"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="transition-all duration-300"
              />
            </svg>
          </div>

          {/* Time axis ticks */}
          <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 pt-2 border-t border-white/[0.04] relative z-10">
            <span>DAY 01</span>
            <span>DAY 08</span>
            <span>DAY 15</span>
            <span>DAY 22</span>
            <span className="text-cyan-400">TODAY (LIVE)</span>
          </div>
        </div>

        {/* ================= BAND 1 (SIDE): 2 ASYMMETRIC METRICS (SPAN 4) ================= */}
        <div className="col-span-12 lg:col-span-4 flex flex-col gap-4">
          {/* Card 1: Circulation Balance & Active Depositors */}
          <div className="flex-1 rounded-xl bg-[#0d111a] border border-white/[0.08] p-5 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <Wallet className="w-3.5 h-3.5 text-cyan-400" />
                Circulating Balance
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                100% RESERVES
              </span>
            </div>

            <div className="my-3">
              <div className="text-2xl sm:text-3xl font-mono font-bold text-white tabular-nums">
                $34,180.25
              </div>
              <p className="text-xs text-slate-400 mt-1 font-mono">
                Across <strong className="text-slate-200">4,821</strong> enterprise wallets
              </p>
            </div>

            {/* Micro visual breakdown bar */}
            <div>
              <div className="flex justify-between text-[11px] font-mono text-slate-400 mb-1.5">
                <span>BTC / USDT Deposits: 68%</span>
                <span className="text-slate-200">Card Invoices: 32%</span>
              </div>
              <div className="w-full h-1.5 bg-[#07090e] rounded-full overflow-hidden flex">
                <div className="h-full bg-cyan-400" style={{ width: "68%" }} />
                <div className="h-full bg-emerald-400" style={{ width: "32%" }} />
              </div>
            </div>
          </div>

          {/* Card 2: Engine Ping Latency & Gateway Health */}
          <div className="flex-1 rounded-xl bg-[#0d111a] border border-white/[0.08] p-5 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-emerald-400" />
                SS7 / HLR Telephony Ping
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                SUB-150ms
              </span>
            </div>

            <div className="my-3">
              <div className="text-2xl sm:text-3xl font-mono font-bold text-emerald-400 tabular-nums flex items-baseline gap-2">
                118<span className="text-sm font-normal text-slate-400">ms avg</span>
              </div>
              <p className="text-xs text-slate-400 mt-1 font-mono">
                P99 Peak: <span className="text-slate-300">142ms</span> · Zero dropped frames
              </p>
            </div>

            {/* Sparkline mini polyline */}
            <div className="w-full h-8 pt-1">
              <svg viewBox="0 0 200 30" preserveAspectRatio="none" className="w-full h-full" role="img" aria-label="Latency jitter sparkline">
                <polyline
                  fill="none"
                  stroke="#10b981"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  points="0,18 20,22 40,15 60,19 80,12 100,16 120,10 140,14 160,8 180,12 200,6"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
