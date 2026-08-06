"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { ShieldAlert, Activity, AlertTriangle, ArrowRight, Layers, FileText, CheckCircle2 } from 'lucide-react';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { TrustStatusComponent } from '@/components/common/TrustStatusComponent';

export function HighwayOpsDashboard() {
  const [selectedDistrict, setSelectedDistrict] = useState('ramban');
  const [activeLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44',
    'susceptibility_class'
  ]);

  return (
    <div className="flex-1 flex flex-col overflow-y-auto p-3 sm:p-4 max-w-7xl mx-auto w-full space-y-4">
      <ResearchDisclaimer />

      {/* Header Banner */}
      <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="space-y-2">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded-full bg-amber-950 border border-amber-600/50 text-amber-300 text-[11px] font-mono">
              Highway Operations Mode (NHAI)
            </span>
            <TrustStatusComponent compact />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-white">
            NH-44 Landslide Exposure Screening
          </h1>
          <p className="text-xs text-slate-300 max-w-3xl leading-relaxed">
            Screen static susceptibility along the highway corridor to identify segments requiring further geotechnical and field inspection.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <Link
            href="/corridor"
            className="px-4 py-2.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 transition-colors shadow-lg shadow-amber-900/30"
          >
            <Activity className="w-4 h-4" />
            <span>Open Corridor Screening</span>
          </Link>
        </div>
      </div>

      {/* Outcome Card — "What this platform helps you do" */}
      <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-2">
        <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
          What this platform helps you do:
        </h2>
        <ul className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2 text-xs text-slate-300">
          <li className="p-2.5 bg-navy-950 rounded-xl border border-navy-800 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span>Screen highway segments for static slope susceptibility exposure.</span>
          </li>
          <li className="p-2.5 bg-navy-950 rounded-xl border border-navy-800 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span>Identify candidate corridor areas requiring field inspection.</span>
          </li>
          <li className="p-2.5 bg-navy-950 rounded-xl border border-navy-800 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span>Understand underlying morphometric terrain & geological factors.</span>
          </li>
          <li className="p-2.5 bg-navy-950 rounded-xl border border-navy-800 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span>Document data gaps and missing operational telemetry inputs.</span>
          </li>
        </ul>
      </div>

      {/* Available vs Unavailable Data Separation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-navy-900 border border-emerald-600/40 p-4 rounded-2xl space-y-2">
          <h3 className="text-xs font-bold text-emerald-300 uppercase tracking-wider">
            Available Verified Data (Current System)
          </h3>
          <ul className="space-y-1.5 text-xs text-slate-300 font-mono text-[11px]">
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span>100m Static XGBoost Susceptibility Probability & 5-Class Rating</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span>Copernicus DEM 30m Morphometrics (Elevation, Slope, Aspect)</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span>GSI 50K Tectonic Vectors (Faults, Thrusts, Lineaments)</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span>NGDR Historical Landslide Point & Polygon Inventory</span>
            </li>
          </ul>
        </div>

        <div className="bg-navy-900 border border-slate-700 p-4 rounded-2xl space-y-2">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Not Currently Available (Future Integration)
          </h3>
          <ul className="space-y-1.5 text-xs text-slate-400 font-mono text-[11px]">
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-slate-600"></span>
              <span>NHAI RAMS Pavement Structural Condition Telemetry</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-slate-600"></span>
              <span>Live Traffic Police Road Blockage & Clearance Feeds</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-slate-600"></span>
              <span>Real-Time Geotechnical Slope Displacement Sensors</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-slate-600"></span>
              <span>Official Assigned Maintenance Work Orders & Inspection Logs</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Corridor Map Preview */}
      <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-sm font-bold text-white">NH-44 Highway Spatial Map</h2>
            <p className="text-xs text-slate-400">Corridor polyline overlaid on 100m 5-class susceptibility master grid.</p>
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
