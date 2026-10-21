"use client";

import React from "react";
import { PieChart, BarChart3, Activity } from "lucide-react";

export function ChartInventoryBand() {
  // Donut chart stroke-dasharray calculations for circumference of radius 40:
  // 2 * PI * 40 = 251.327
  // Mobile SIM: 74% = 185.98
  // VoIP Burner: 16% = 40.21
  // Landline: 8% = 20.10
  // Other: 2% = 5.03
  const circumference = 251.327;

  return (
    <section className="mb-6">
      <div className="grid grid-cols-12 gap-4">
        {/* ================= 1. DONUT CHART (LINE TYPE BREAKDOWN) ================= */}
        <div className="col-span-12 md:col-span-4 rounded-xl bg-[#0d111a] border border-white/[0.08] p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-white/[0.04]">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-300 flex items-center gap-1.5 font-semibold">
              <PieChart className="w-3.5 h-3.5 text-cyan-400" />
              Line Type Distribution
            </span>
            <span className="text-[10px] font-mono text-slate-500">240+ COUNTRIES</span>
          </div>

          {/* Donut Geometry */}
          <div className="py-5 flex items-center justify-center">
            <div className="relative w-36 h-36">
              <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90" role="img" aria-label="Line type distribution donut chart">
                {/* Background Ring */}
                <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.05)" strokeWidth="12" fill="none" />
                {/* Slice 1: Mobile (Emerald) 74% */}
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#10b981"
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray={`${0.74 * circumference} ${circumference}`}
                  strokeDashoffset="0"
                />
                {/* Slice 2: VoIP (Rose) 16% */}
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#f43f5e"
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray={`${0.16 * circumference} ${circumference}`}
                  strokeDashoffset={`${-0.74 * circumference}`}
                />
                {/* Slice 3: Landline (Cyan) 8% */}
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#06b6d4"
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray={`${0.08 * circumference} ${circumference}`}
                  strokeDashoffset={`${-(0.74 + 0.16) * circumference}`}
                />
                {/* Slice 4: Other (Amber) 2% */}
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#f59e0b"
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray={`${0.02 * circumference} ${circumference}`}
                  strokeDashoffset={`${-(0.74 + 0.16 + 0.08) * circumference}`}
                />
              </svg>
              {/* Inner Center Stat */}
              <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span className="text-xl font-mono font-bold text-white tabular-nums">74.2%</span>
                <span className="text-[10px] font-mono text-slate-400 uppercase">Mobile SIM</span>
              </div>
            </div>
          </div>

          {/* Legend */}
          <div className="grid grid-cols-2 gap-2 text-[11px] font-mono pt-3 border-t border-white/[0.04]">
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span className="text-slate-400">Mobile SIM:</span>
              <span className="text-white font-medium ml-auto">74%</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-rose-500"></span>
              <span className="text-slate-400">VoIP Burner:</span>
              <span className="text-white font-medium ml-auto">16%</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-cyan-500"></span>
              <span className="text-slate-400">Landline:</span>
              <span className="text-white font-medium ml-auto">8%</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-amber-500"></span>
              <span className="text-slate-400">Other/Sat:</span>
              <span className="text-white font-medium ml-auto">2%</span>
            </div>
          </div>
        </div>

        {/* ================= 2. RANKED BAR CHART (TOP 5 CHECKERS) ================= */}
        <div className="col-span-12 md:col-span-4 rounded-xl bg-[#0d111a] border border-white/[0.08] p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-white/[0.04]">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-300 flex items-center gap-1.5 font-semibold">
              <BarChart3 className="w-3.5 h-3.5 text-blue-400" />
              Engine Load Ranking
            </span>
            <span className="text-[10px] font-mono text-slate-500">102 CATALOG</span>
          </div>

          <div className="space-y-3.5 py-4">
            {[
              { name: "Carrier HLR Ping", pings: "4.89M", percent: 100, color: "bg-cyan-400" },
              { name: "WhatsApp Footprint", pings: "3.92M", percent: 80, color: "bg-emerald-400" },
              { name: "VoIP Burner Shield", pings: "2.74M", percent: 56, color: "bg-rose-400" },
              { name: "Apple iMessage Probe", pings: "1.98M", percent: 40, color: "bg-blue-400" },
              { name: "Telegram Presence", pings: "1.32M", percent: 27, color: "bg-amber-400" },
            ].map((bar) => (
              <div key={bar.name}>
                <div className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-slate-300">{bar.name}</span>
                  <span className="text-white font-semibold tabular-nums">{bar.pings}</span>
                </div>
                <div className="w-full h-2 bg-[#07090e] rounded-sm overflow-hidden">
                  <div
                    className={`h-full ${bar.color} rounded-sm transition-all duration-500`}
                    style={{ width: `${bar.percent}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="pt-3 border-t border-white/[0.04] flex items-center justify-between text-[11px] font-mono text-slate-500">
            <span>Aggregated Across 102 Engines</span>
            <span className="text-slate-300 font-semibold">99.98% SUCCESS</span>
          </div>
        </div>

        {/* ================= 3. SPARKLINES GRID (GATEWAY SECURITY & GATING) ================= */}
        <div className="col-span-12 md:col-span-4 rounded-xl bg-[#0d111a] border border-white/[0.08] p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-white/[0.04]">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-300 flex items-center gap-1.5 font-semibold">
              <Activity className="w-3.5 h-3.5 text-emerald-400" />
              API Gate Telemetry
            </span>
            <span className="text-[10px] font-mono text-slate-500">ENFORCED</span>
          </div>

          <div className="grid grid-cols-2 gap-3 py-3">
            {/* Metric 1 */}
            <div className="p-3 rounded-lg bg-[#07090e] border border-white/[0.04]">
              <span className="text-[10px] font-mono text-slate-400 uppercase">200 OK Pass</span>
              <div className="text-lg font-mono font-bold text-emerald-400 tabular-nums my-0.5">
                98.4%
              </div>
              <svg viewBox="0 0 100 20" preserveAspectRatio="none" className="w-full h-4 mt-1">
                <polyline fill="none" stroke="#10b981" strokeWidth="1.5" points="0,15 20,12 40,14 60,8 80,10 100,5" />
              </svg>
            </div>

            {/* Metric 2 */}
            <div className="p-3 rounded-lg bg-[#07090e] border border-white/[0.04]">
              <span className="text-[10px] font-mono text-slate-400 uppercase">401 Auth Rejected</span>
              <div className="text-lg font-mono font-bold text-amber-400 tabular-nums my-0.5">
                1.2%
              </div>
              <svg viewBox="0 0 100 20" preserveAspectRatio="none" className="w-full h-4 mt-1">
                <polyline fill="none" stroke="#f59e0b" strokeWidth="1.5" points="0,5 20,8 40,6 60,12 80,10 100,16" />
              </svg>
            </div>

            {/* Metric 3 */}
            <div className="p-3 rounded-lg bg-[#07090e] border border-white/[0.04]">
              <span className="text-[10px] font-mono text-slate-400 uppercase">402 Balance Gated</span>
              <div className="text-lg font-mono font-bold text-cyan-400 tabular-nums my-0.5">
                0.4%
              </div>
              <svg viewBox="0 0 100 20" preserveAspectRatio="none" className="w-full h-4 mt-1">
                <polyline fill="none" stroke="#06b6d4" strokeWidth="1.5" points="0,18 20,14 40,16 60,10 80,12 100,8" />
              </svg>
            </div>

            {/* Metric 4 */}
            <div className="p-3 rounded-lg bg-[#07090e] border border-white/[0.04]">
              <span className="text-[10px] font-mono text-slate-400 uppercase">Burner Blocked</span>
              <div className="text-lg font-mono font-bold text-rose-400 tabular-nums my-0.5">
                16.5%
              </div>
              <svg viewBox="0 0 100 20" preserveAspectRatio="none" className="w-full h-4 mt-1">
                <polyline fill="none" stroke="#f43f5e" strokeWidth="1.5" points="0,10 20,12 40,8 60,14 80,7 100,4" />
              </svg>
            </div>
          </div>

          <div className="pt-3 border-t border-white/[0.04] flex items-center justify-between text-[11px] font-mono text-slate-500">
            <span>Payment Gating Active</span>
            <span className="text-emerald-400 font-semibold">ZERO FREE LEAKS</span>
          </div>
        </div>
      </div>
    </section>
  );
}
