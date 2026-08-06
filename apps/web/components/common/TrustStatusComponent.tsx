"use client";

import React from 'react';
import { Database, CloudRain, ShieldAlert } from 'lucide-react';

interface TrustStatusComponentProps {
  compact?: boolean;
}

export function TrustStatusComponent({ compact = false }: TrustStatusComponentProps) {
  if (compact) {
    return (
      <div className="flex flex-wrap items-center gap-1.5 text-[10px] font-mono">
        <span className="px-2 py-0.5 rounded bg-emerald-950/80 border border-emerald-600/50 text-emerald-300 flex items-center space-x-1">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          <span>STATIC: Verified</span>
        </span>
        <span className="px-2 py-0.5 rounded bg-amber-950/80 border border-amber-600/50 text-amber-300 flex items-center space-x-1">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
          <span>SCENARIO: Proxy Model</span>
        </span>
        <span className="px-2 py-0.5 rounded bg-slate-900/80 border border-slate-700 text-slate-400 flex items-center space-x-1">
          <span className="w-1.5 h-1.5 rounded-full bg-slate-500"></span>
          <span>OPERATIONAL: Not Integrated</span>
        </span>
      </div>
    );
  }

  return (
    <div className="bg-navy-950/90 border border-navy-800 p-4 rounded-xl space-y-2 text-xs">
      <div className="flex items-center justify-between border-b border-navy-800 pb-2">
        <span className="font-bold text-slate-200 text-xs uppercase tracking-wider">
          Data Provenance & Operational Status
        </span>
        <a
          href="/transparency"
          className="text-[11px] text-blue-400 hover:text-blue-300 font-semibold"
        >
          Why am I seeing this?
        </a>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-1 font-mono text-[11px]">
        <div className="p-2.5 rounded-lg bg-navy-900 border border-emerald-600/40 space-y-1">
          <div className="flex items-center space-x-1.5 text-emerald-300 font-bold">
            <Database className="w-3.5 h-3.5" />
            <span>STATIC DATA</span>
          </div>
          <p className="text-[10px] text-slate-300 leading-tight">
            Derived from 100m terrain slope, geology, LULC & historical landslides.
          </p>
          <div className="text-[10px] text-emerald-400 font-bold uppercase">Status: Available & Verified</div>
        </div>

        <div className="p-2.5 rounded-lg bg-navy-900 border border-amber-600/40 space-y-1">
          <div className="flex items-center space-x-1.5 text-amber-300 font-bold">
            <CloudRain className="w-3.5 h-3.5" />
            <span>SCENARIO MODEL</span>
          </div>
          <p className="text-[10px] text-slate-300 leading-tight">
            Derived using 24h rainfall proxy & P90 baseline climatology scenarios.
          </p>
          <div className="text-[10px] text-amber-400 font-bold uppercase">Status: Research Proxy Only</div>
        </div>

        <div className="p-2.5 rounded-lg bg-navy-900 border border-slate-700 space-y-1">
          <div className="flex items-center space-x-1.5 text-slate-400 font-bold">
            <ShieldAlert className="w-3.5 h-3.5 text-slate-500" />
            <span>OPERATIONAL DATA</span>
          </div>
          <p className="text-[10px] text-slate-400 leading-tight">
            Live road closures, official warnings, RAMS pavement telemetry.
          </p>
          <div className="text-[10px] text-slate-400 font-bold uppercase">Status: Not Yet Integrated</div>
        </div>
      </div>
    </div>
  );
}
