"use client";

import React from "react";
import { Shield, Check } from "lucide-react";

export function FooterBand() {
  return (
    <footer className="pt-8 pb-16 border-t border-white/[0.06] text-xs font-mono text-slate-500">
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2.5">
          <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
          <span className="text-slate-400 font-medium">CheckerLeak Telemetry Engine</span>
          <span className="text-slate-700">•</span>
          <span>v2.2 Production Cluster</span>
        </div>

        <div className="flex items-center gap-5 text-xs">
          <span className="flex items-center gap-1.5 text-slate-400">
            <Shield className="w-3.5 h-3.5 text-cyan-400" />
            Zero-Log Architecture
          </span>
          <span className="text-slate-700">•</span>
          <span className="flex items-center gap-1.5 text-emerald-400">
            <Check className="w-3.5 h-3.5 text-emerald-400" />
            Payment Gating Active
          </span>
          <span className="text-slate-700">•</span>
          <span className="text-slate-500">240+ Countries Connected</span>
        </div>
      </div>
    </footer>
  );
}
