"use client";

import React from "react";
import { Terminal, Shield, Check } from "lucide-react";

export function FooterBand() {
  return (
    <footer className="pt-6 pb-12 border-t border-white/[0.06] text-xs font-mono text-slate-500">
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
          <span className="text-slate-400 font-semibold">CheckerLeak Telemetry Gateway</span>
          <span className="text-slate-700">•</span>
          <span>Build: rev-b06e6ee (Linux x86_64)</span>
        </div>

        <div className="flex items-center gap-4 text-[11px]">
          <span className="flex items-center gap-1 text-slate-400">
            <Shield className="w-3 h-3 text-cyan-400" />
            Zero-Log Pipeline
          </span>
          <span className="text-slate-700">•</span>
          <span className="flex items-center gap-1 text-emerald-400">
            <Check className="w-3 h-3 text-emerald-400" />
            Strict Payment Gating Active
          </span>
          <span className="text-slate-700">•</span>
          <span className="text-slate-500">240+ Countries Connected</span>
        </div>
      </div>
    </footer>
  );
}
