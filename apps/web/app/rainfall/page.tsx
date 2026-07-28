"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { CloudRain, Clock, Play, Pause, Database, AlertCircle } from 'lucide-react';

export default function RainfallMonitor() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedWindow, setSelectedWindow] = useState('24h');

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-600/20 text-blue-400 p-2 rounded-lg border border-blue-500/30">
              <CloudRain className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Rainfall Monitor & Accumulation Engine</h1>
              <p className="text-xs text-slate-400 mt-0.5">
                IMERG satellite precipitation playback & IMD historical percentile climatology indicators.
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2 bg-blue-950/60 border border-blue-600/40 px-3 py-1.5 rounded-lg text-blue-300 text-xs font-semibold">
            <span>Data Mode: Demo Playback (July 2026 Sample)</span>
          </div>
        </div>

        {/* Timeline Playback Shell */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-4">
          <div className="flex items-center justify-between border-b border-navy-800 pb-3">
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-blue-400" />
              <span className="font-bold text-white text-sm">Accumulation Duration Select</span>
            </div>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="flex items-center space-x-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs px-3 py-1.5 rounded-lg font-medium transition-colors"
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
              <span>{isPlaying ? 'Pause Demo Playback' : 'Start Playback Sequence'}</span>
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
                    : 'bg-navy-800/60 border-navy-700 text-slate-400 hover:bg-navy-800'
                }`}
              >
                <div className="text-[10px] text-slate-400">Window</div>
                <div className="text-sm mt-0.5">{w}</div>
              </button>
            ))}
          </div>

          {/* Sample Plot Representation */}
          <div className="bg-navy-950 border border-navy-800 p-4 rounded-lg flex flex-col items-center justify-center min-h-[220px] text-center space-y-2">
            <CloudRain className="w-10 h-10 text-blue-500 animate-pulse" />
            <div className="text-sm font-bold text-white">IMERG 24-Hour Precipitation Grid (Demo Playback)</div>
            <p className="text-xs text-slate-400 max-w-md">
              Showing satellite accumulation raster for window <span className="font-mono text-blue-400">{selectedWindow}</span>. Peak rainfall localized along Ramban-Udhampur corridor.
            </p>
            <div className="flex items-center space-x-3 text-[11px] font-mono text-slate-400 pt-2">
              <span>Max Accumulation: <strong className="text-blue-300">64.5 mm</strong></span>
              <span>•</span>
              <span>Mean State Rainfall: <strong className="text-blue-300">18.2 mm</strong></span>
              <span>•</span>
              <span>Trigger Level: <strong className="text-amber-400">Elevated (90th Percentile)</strong></span>
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
            <p className="text-slate-400">Half-hourly satellite precipitation estimates at 0.1° resolution (~10 km grid).</p>
            <div className="text-blue-300 font-mono text-[11px]">144 Sample NetCDF4 Granules Audited</div>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-emerald-400" />
              <span>IMD Daily Gridded Data</span>
            </div>
            <p className="text-slate-400">Historical long-term daily gridded rainfall (0.25° resolution) for baseline percentiles.</p>
            <div className="text-emerald-300 font-mono text-[11px]">6 Yearly NetCDF Files Audited</div>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-purple-400" />
              <span>India-WRIS Stations</span>
            </div>
            <p className="text-slate-400">Surface raingauge station workbooks used for cross-validation and bias adjustment.</p>
            <div className="text-purple-300 font-mono text-[11px]">34 Excel Workbooks Audited</div>
          </div>
        </div>
      </div>
    </div>
  );
}
