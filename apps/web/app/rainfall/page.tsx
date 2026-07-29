"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { CloudRain, Clock, Play, Pause, Database, AlertTriangle } from 'lucide-react';

export default function RainfallMonitor() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedWindow, setSelectedWindow] = useState('24h');

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        {/* Prominent Interface Demonstration Only Banner */}
        <div className="bg-amber-950/90 border border-amber-500/80 text-amber-100 p-4 rounded-xl flex items-center justify-between text-xs shadow-lg">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
            <div>
              <h2 className="font-bold text-sm text-amber-200">Risk & Rainfall Modules: Demo</h2>
              <p className="text-slate-300 mt-0.5">
                No numbers on this page represent calculated rainfall outputs. Source calculations will be executed & verified in Phase 5.
              </p>
            </div>
          </div>
          <span className="font-mono text-xs bg-amber-900 border border-amber-400/50 px-3 py-1 rounded text-amber-200 font-bold shrink-0">
            Risk & Rainfall Modules: Demo
          </span>
        </div>

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-600/20 text-blue-400 p-2 rounded-lg border border-blue-500/30">
              <CloudRain className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Rainfall Monitor Interface Shell</h1>
              <p className="text-xs text-slate-300 mt-0.5">
                Conceptual Precipitation Interface Layout — IMERG satellite precipitation playback & IMD historical percentile climatology layout.
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2 bg-amber-950/60 border border-amber-600/40 px-3 py-1.5 rounded-lg text-amber-300 text-xs font-semibold">
            <span>Risk & Rainfall Modules: Demo</span>
          </div>
        </div>

        {/* Timeline Playback Shell */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-4">
          <div className="flex items-center justify-between border-b border-navy-800 pb-3">
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-blue-400" />
              <span className="font-bold text-white text-sm">Accumulation Window Selector (Demo)</span>
            </div>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="flex items-center space-x-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs px-3 py-1.5 rounded-lg font-semibold transition-colors"
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
              <span>{isPlaying ? 'Pause Demo' : 'Play Timeline Demo'}</span>
            </button>
          </div>

          {/* Accumulation Buttons */}
          <div className="grid grid-cols-4 md:grid-cols-8 gap-2 text-xs font-mono">
            {['30min', '1h', '3h', '6h', '12h', '24h', '48h', '72h'].map((w) => (
              <button
                key={w}
                onClick={() => setSelectedWindow(w)}
                className={`p-3 rounded-lg border text-center transition-all ${
                  selectedWindow === w
                    ? 'bg-blue-600 border-blue-500 text-white font-bold shadow-lg'
                    : 'bg-navy-800/60 border-navy-700 text-slate-300 hover:bg-navy-800'
                }`}
              >
                <div className="text-[10px] text-slate-400">Window</div>
                <div className="text-sm mt-0.5">{w}</div>
              </button>
            ))}
          </div>

          {/* Conceptual Precipitation Interface Layout Representation */}
          <div className="bg-navy-950 border border-navy-800 p-6 rounded-lg flex flex-col items-center justify-center min-h-[240px] text-center space-y-3">
            <CloudRain className="w-10 h-10 text-blue-500 animate-pulse" />
            <div className="text-base font-bold text-white">Conceptual Precipitation Interface Layout</div>
            <p className="text-xs text-slate-300 max-w-md">
              Showing conceptual accumulation visualization for window <span className="font-mono text-blue-400">{selectedWindow}</span>. Risk & Rainfall Modules: Demo.
            </p>
            <div className="flex flex-col sm:flex-row items-center gap-2 text-xs font-mono text-amber-300 pt-2 bg-navy-900/80 px-4 py-2 rounded-md border border-navy-700">
              <span>64.5 mm (Illustrative Demo Value — not calculated from the processing pipeline.)</span>
              <span className="hidden sm:inline">•</span>
              <span>18.2 mm (Illustrative Demo Value — not calculated from the processing pipeline.)</span>
              <span className="hidden sm:inline">•</span>
              <span>90th percentile (Illustrative Demo Value — not calculated from the processing pipeline.)</span>
            </div>
          </div>
        </div>

        {/* Data Source Details Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-blue-400" />
              <span>NASA GPM IMERG</span>
            </div>
            <p className="text-slate-300">144 half-hourly NetCDF4 granules discovered. Processing scheduled for Phase 5.</p>
            <div className="text-amber-300 font-mono text-[11px]">Illustrative Demo Value — not calculated from the processing pipeline.</div>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-emerald-400" />
              <span>IMD Daily Gridded Climatology</span>
            </div>
            <p className="text-slate-300">Historical NetCDF files audited. Percentile baselines will be derived in Phase 5.</p>
            <div className="text-amber-300 font-mono text-[11px]">Illustrative Demo Value — not calculated from the processing pipeline.</div>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-purple-400" />
              <span>India-WRIS Station Network</span>
            </div>
            <p className="text-slate-300">34 station workbooks audited for surface raingauge cross-validation.</p>
            <div className="text-amber-300 font-mono text-[11px]">Illustrative Demo Value — not calculated from the processing pipeline.</div>
          </div>
        </div>
      </div>
    </div>
  );
}
