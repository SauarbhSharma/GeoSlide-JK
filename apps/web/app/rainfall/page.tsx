"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { CloudRain, Clock, Database, AlertTriangle } from 'lucide-react';

export default function RainfallMonitor() {
  const [selectedWindow] = useState('24h');

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Truthful Scenario / Proxy Notice Banner */}
        <div className="bg-amber-950/90 border border-amber-500/80 text-amber-100 p-4 rounded-xl flex items-center justify-between text-xs shadow-lg">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
            <div>
              <h2 className="font-bold text-sm text-amber-200">24-Hour Rainfall Proxy and Dynamic Hazard Scenario</h2>
              <p className="text-slate-300 mt-0.5">
                The current rainfall accumulation and P90 layers are model-derived scenario/proxy products for research demonstration. They are not live operational rainfall observations.
              </p>
            </div>
          </div>
          <span className="font-mono text-xs bg-amber-900 border border-amber-400/50 px-3 py-1 rounded text-amber-200 font-bold shrink-0">
            Scenario / Proxy Mode
          </span>
        </div>

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-600/20 text-blue-400 p-2 rounded-lg border border-blue-500/30">
              <CloudRain className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">24-Hour Rainfall Proxy and Dynamic Hazard Scenario</h1>
              <p className="text-xs text-slate-300 mt-0.5">
                Model-derived 24-hour precipitation accumulation and IMD 90th percentile baseline proxy rasters (100m EPSG:32643).
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2 bg-amber-950/60 border border-amber-600/40 px-3 py-1.5 rounded-lg text-amber-300 text-xs font-semibold">
            <span>24h Scenario Mode Active</span>
          </div>
        </div>

        {/* Accumulation Window Selector */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-4">
          <div className="flex items-center justify-between border-b border-navy-800 pb-3">
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-blue-400" />
              <span className="font-bold text-white text-sm">Accumulation Window</span>
            </div>
            <span className="text-xs text-slate-400 font-mono">Documented Release Raster: 24-Hour Accumulation</span>
          </div>

          {/* 24-Hour Window Only */}
          <div className="flex items-center space-x-3 text-xs font-mono">
            <button
              className="px-6 py-2.5 rounded-lg border bg-blue-600 border-blue-500 text-white font-bold shadow-lg"
            >
              24-Hour Window (Derived Proxy)
            </button>
            <span className="text-slate-400 text-xs font-sans">
              (Other sub-daily/multi-day accumulation windows are omitted in the release raster stack.)
            </span>
          </div>

          {/* Inspection Notice */}
          <div className="bg-navy-950 border border-navy-800 p-6 rounded-lg flex flex-col items-center justify-center min-h-[160px] text-center space-y-3">
            <CloudRain className="w-8 h-8 text-blue-400" />
            <div className="text-sm font-bold text-white">Select a valid location on the map or location-check tool to inspect derived values.</div>
            <p className="text-xs text-slate-400 max-w-lg">
              Dynamic hazard index formula: <span className="font-mono text-blue-300">H_dyn = Susceptibility_Probability * (Rainfall_24h_Proxy / P90_Proxy_Baseline)</span>.
            </p>
          </div>
        </div>

        {/* Data Source Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-blue-400" />
              <span>Rainfall Proxy Raster</span>
            </div>
            <p className="text-slate-300">Statewide 100m 24-hour precipitation accumulation proxy raster (5.0 - 160.0 mm).</p>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-emerald-400" />
              <span>P90 Proxy Baseline</span>
            </div>
            <p className="text-slate-300">Statewide 100m historical IMD 90th percentile baseline proxy raster (30.0 - 95.0 mm).</p>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-purple-400" />
              <span>Dynamic Hazard Scenario</span>
            </div>
            <p className="text-slate-300">Statewide 100m dynamic hazard index and 5-class rating scenario rasters.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
