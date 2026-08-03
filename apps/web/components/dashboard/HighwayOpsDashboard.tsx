"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { ShieldAlert, Activity, AlertTriangle, ArrowRight, Layers, FileText, CheckCircle2 } from 'lucide-react';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';

export function HighwayOpsDashboard() {
  const [selectedDistrict, setSelectedDistrict] = useState('ramban');
  const [activeLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44',
    'susceptibility_prob'
  ]);

  return (
    <div className="flex-1 flex flex-col overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
      <ResearchDisclaimer />

      {/* Header Banner */}
      <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded-full bg-amber-950 border border-amber-600/50 text-amber-300 text-[11px] font-mono">
              Highway Operations Mode (NHAI)
            </span>
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-white">
            NH-44 Corridor Instability & Maintenance Monitor
          </h1>
          <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
            Monitor static road-segment landslide exposure along the 295 km NH-44 highway corridor and prioritize slope maintenance inspections.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <Link
            href="/corridor"
            className="px-4 py-2.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 transition-colors shadow-lg shadow-amber-900/30"
          >
            <Activity className="w-4 h-4" />
            <span>Open Corridor Monitor</span>
          </Link>
        </div>
      </div>

      {/* Corridor Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-1">
          <span className="text-slate-400 text-[11px] font-mono uppercase tracking-wider">Pilot Corridor</span>
          <div className="text-lg font-black text-white">NH-44 Jammu–Srinagar</div>
          <div className="text-[11px] text-amber-400 font-mono">295 km Total Length</div>
        </div>

        <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-1">
          <span className="text-slate-400 text-[11px] font-mono uppercase tracking-wider">Evaluation Segments</span>
          <div className="text-lg font-black text-white">590 Segments (500m)</div>
          <div className="text-[11px] text-emerald-400 font-mono">Chainage Indexed</div>
        </div>

        <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-1">
          <span className="text-slate-400 text-[11px] font-mono uppercase tracking-wider">High Instability Segments</span>
          <div className="text-lg font-black text-amber-400">29 Segments (14.5 km)</div>
          <div className="text-[11px] text-slate-400 font-mono">Ramban–Banihal Stretch</div>
        </div>

        <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-1">
          <span className="text-slate-400 text-[11px] font-mono uppercase tracking-wider">Data Status</span>
          <div className="text-lg font-black text-sky-400">Static Exposure Only</div>
          <div className="text-[11px] text-slate-400 font-mono">Live Telemetry Future Work</div>
        </div>
      </div>

      {/* Operational Disclaimer Notice */}
      <div className="bg-navy-950 border border-amber-500/60 p-4 rounded-2xl text-xs space-y-2">
        <div className="flex items-center space-x-2 text-amber-300 font-bold">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>Operational Terminology & Safety Disclaimer</span>
        </div>
        <p className="text-slate-300 leading-relaxed">
          GeoSlide-JK 2.0 measures <strong>Static Road-Segment Landslide Exposure</strong> based on 100m terrain slope, geology, and historical landslide density. It DOES NOT report current structural pavement condition, live road closures, or real-time traffic status.
        </p>
      </div>

      {/* Corridor Map Preview */}
      <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-sm font-bold text-white">NH-44 Highway Spatial Map</h2>
            <p className="text-xs text-slate-400">Corridor polyline overlaid on 100m slope susceptibility master grid.</p>
          </div>
          <Link
            href="/corridor"
            className="text-xs text-amber-400 hover:text-amber-300 font-semibold flex items-center space-x-1"
          >
            <span>Full Chainage Inspector</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="h-[400px] rounded-xl overflow-hidden border border-navy-800 relative">
          <MapContainer
            selectedDistrict={selectedDistrict}
            onSelectDistrict={setSelectedDistrict}
            activeLayers={activeLayers}
          />
        </div>
      </div>
    </div>
  );
}
