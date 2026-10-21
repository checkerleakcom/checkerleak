"use client";

import React from "react";
import { PieChart, BarChart3, Activity } from "lucide-react";

export function ChartInventoryBand() {
  const circumference = 251.327;

  return (
    <section className="mb-8">
      <div className="grid grid-cols-12 gap-6">
        {/* ================= 1. DONUT CHART (LINE TYPE BREAKDOWN) ================= */}
        <div className="col-span-12 md:col-span-4 rounded-2xl bg-[#0d111a] border border-white/[0.07] p-7 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-4 border-b border-white/[0.04]">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-300 flex items-center gap-2 font-semibold">
              <PieChart className="w-4 h-4 text-cyan-400" />
              Line Type Share
            </span>
            <span className="text-[11px] font-mono text-slate-500">240+ COUNTRIES</span>
          </div>

          {/* Donut Geometry with High Contrast */}
          <div className="py-6 flex items-center justify-center">
            <div className="relative w-40 h-40">
              <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
                <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.05)" strokeWidth="10" fill="none" />
                {/* Mobile (Emerald) 74% */}
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#10b981"
                  strokeWidth="10"
                  fill="none"
                  strokeDasharray={`${0.74 * circumference} ${circumference}`}
                  strokeDashoffset="0"
                />
                {/* VoIP Burner (Rose) 16% */}
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#f43f5e"
                  strokeWidth="10"
                  fill="none"
                  strokeDasharray={`${0.16 * circumference} ${circumference}`}
                  strokeDashoffset={`${-0.74 * circumference}`}
                />
                {/* Landline (Cyan) 8% */}
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#06b6d4"
                  strokeWidth="10"
                  fill="none"
                  strokeDasharray={`${0.08 * circumference} ${circumference}`}
                  strokeDashoffset={`${-(0.74 + 0.16) * circumference}`}
                />
                {/* Other (Amber) 2% */}
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#f59e0b"
                  strokeWidth="10"
                  fill="none"
                  strokeDasharray={`${0.02 * circumference} ${circumference}`}
                  strokeDashoffset={`${-(0.74 + 0.16 + 0.08) * circumference}`}
                />
              </svg>
              {/* Inner Center Stat */}
              <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span className="text-2xl font-mono font-bold text-white tabular-nums">74.2%</span>
                <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Mobile SIM</span>
              </div>
            </div>
          </div>

          {/* Clean Spacious Legend */}
          <div className="grid grid-cols-2 gap-3 text-xs font-mono pt-4 border-t border-white/[0.04]">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <span className="text-slate-400">Mobile SIM:</span>
              <span className="text-white font-semibold ml-auto">74%</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              <span className="text-slate-400">VoIP:</span>
              <span className="text-white font-semibold ml-auto">16%</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-cyan-500"></span>
              <span className="text-slate-400">Landline:</span>
              <span className="text-white font-semibold ml-auto">8%</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
              <span className="text-slate-400">Other:</span>
              <span className="text-white font-semibold ml-auto">2%</span>
            </div>
          </div>
        </div>

        {/* ================= 2. RANKED BAR CHART (TOP ENGINES) ================= */}
        <div className="col-span-12 md:col-span-4 rounded-2xl bg-[#0d111a] border border-white/[0.07] p-7 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-4 border-b border-white/[0.04]">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-300 flex items-center gap-2 font-semibold">
              <BarChart3 className="w-4 h-4 text-blue-400" />
              Engine Load Ranking
            </span>
            <span className="text-[11px] font-mono text-slate-500">TOP ENGINES</span>
          </div>

          <div className="space-y-4 py-4">
            {[
              { name: "Carrier HLR Ping", count: "4.89M", percent: 100, color: "bg-cyan-400" },
              { name: "WhatsApp Footprint", count: "3.92M", percent: 80, color: "bg-emerald-400" },
              { name: "VoIP Burner Shield", count: "2.74M", percent: 56, color: "bg-rose-400" },
              { name: "Apple iMessage Probe", count: "1.98M", percent: 40, color: "bg-blue-400" },
            ].map((bar) => (
              <div key={bar.name}>
                <div className="flex justify-between text-xs font-mono mb-1.5">
                  <span className="text-slate-300">{bar.name}</span>
                  <span className="text-white font-semibold tabular-nums">{bar.count}</span>
                </div>
                <div className="w-full h-2 bg-[#07090e] rounded-full overflow-hidden">
                  <div
                    className={`h-full ${bar.color} rounded-full transition-all duration-500`}
                    style={{ width: `${bar.percent}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="pt-4 border-t border-white/[0.04] flex items-center justify-between text-xs font-mono text-slate-500">
            <span>Catalog: 102 Engines</span>
            <span className="text-slate-300 font-semibold">99.98% PASS</span>
          </div>
        </div>

        {/* ================= 3. GATE TELEMETRY ================= */}
        <div className="col-span-12 md:col-span-4 rounded-2xl bg-[#0d111a] border border-white/[0.07] p-7 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-4 border-b border-white/[0.04]">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-300 flex items-center gap-2 font-semibold">
              <Activity className="w-4 h-4 text-emerald-400" />
              Payment & Security Gate
            </span>
            <span className="text-[11px] font-mono text-emerald-400 font-semibold">ENFORCED</span>
          </div>

          {/* 2 Clean, Uncluttered Telemetry Metrics */}
          <div className="space-y-4 py-3">
            {/* Metric 1: Verified Pass Rate */}
            <div className="p-4 rounded-xl bg-[#07090e] border border-white/[0.04]">
              <div className="flex items-baseline justify-between mb-1">
                <span className="text-xs font-mono text-slate-400">Authenticated 200 OK Pass</span>
                <span className="text-lg font-mono font-bold text-emerald-400 tabular-nums">98.4%</span>
              </div>
              <svg viewBox="0 0 100 16" preserveAspectRatio="none" className="w-full h-4 mt-1">
                <polyline fill="none" stroke="#10b981" strokeWidth="2" points="0,12 20,10 40,11 60,7 80,8 100,4" />
              </svg>
            </div>

            {/* Metric 2: Burners Flagged */}
            <div className="p-4 rounded-xl bg-[#07090e] border border-white/[0.04]">
              <div className="flex items-baseline justify-between mb-1">
                <span className="text-xs font-mono text-slate-400">Burner & Fraud Filtered</span>
                <span className="text-lg font-mono font-bold text-rose-400 tabular-nums">16.5%</span>
              </div>
              <svg viewBox="0 0 100 16" preserveAspectRatio="none" className="w-full h-4 mt-1">
                <polyline fill="none" stroke="#f43f5e" strokeWidth="2" points="0,8 20,10 40,6 60,11 80,5 100,3" />
              </svg>
            </div>
          </div>

          <div className="pt-4 border-t border-white/[0.04] flex items-center justify-between text-xs font-mono text-slate-500">
            <span>Payment Gating Active</span>
            <span className="text-emerald-400 font-semibold">Zero Unpaid Leaks</span>
          </div>
        </div>
      </div>
    </section>
  );
}
