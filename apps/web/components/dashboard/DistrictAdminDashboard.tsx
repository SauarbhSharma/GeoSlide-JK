"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { Building2, Layers, AlertTriangle, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { JK_20_DISTRICTS } from '@/lib/constants';

export function DistrictAdminDashboard() {
  const [selectedDistrict, setSelectedDistrict] = useState('ramban');
  const [activeLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44',
    'susceptibility_prob'
  ]);

  const currentDist = JK_20_DISTRICTS.find((d) => d.id === selectedDistrict) || JK_20_DISTRICTS[0];

  return (
    <div className="flex-1 flex flex-col overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
      <ResearchDisclaimer />

      {/* Header Banner */}
      <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded-full bg-purple-950 border border-purple-600/50 text-purple-300 text-[11px] font-mono">
              District Administration Mode (DDMA)
            </span>
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-white">
            Statewide District Vulnerability & Preparedness Portal
          </h1>
          <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
            Identify high-susceptibility zones, vulnerable rural access roads, and pre-monsoon staging priorities across all 20 Union Territory districts.
          </p>
        </div>

        <div className="flex items-center space-x-2 shrink-0">
          <select
            value={selectedDistrict}
            onChange={(e) => setSelectedDistrict(e.target.value)}
            className="bg-navy-800 border border-navy-700 rounded-xl px-3 py-2 text-xs font-bold text-white focus:outline-none focus:border-purple-500"
          >
            {JK_20_DISTRICTS.map((d) => (
              <option key={d.id} value={d.id}>
                {d.displayName} District
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* District Vulnerability Profile Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Selected District Card */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl md:col-span-2 space-y-3">
          <div className="flex items-center justify-between border-b border-navy-800 pb-3">
            <div>
              <span className="text-[10px] text-slate-400 font-mono uppercase tracking-wider">Selected Administrative District</span>
              <h2 className="text-2xl font-black text-white">{currentDist.displayName} District</h2>
              <div className="text-xs text-slate-300 mt-0.5">
                J&K UT Admin Boundary | Status: <span className="text-emerald-400 font-semibold">Verified Geometry</span>
              </div>
            </div>
            <div className="px-3 py-1.5 rounded-xl border border-purple-500/40 bg-purple-950 text-purple-300 text-xs font-bold font-mono">
              DDMA Profile Active
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
            <div className="bg-navy-800/60 p-3 rounded-xl border border-navy-700">
              <span className="text-slate-400 font-medium">Susceptibility Rating:</span>
              <div className="font-bold text-amber-400 text-sm mt-0.5">
                {['ramban', 'doda', 'kishtwar', 'reasi', 'poonch'].includes(selectedDistrict) ? 'High Instability' : 'Moderate Baseline'}
              </div>
            </div>
            <div className="bg-navy-800/60 p-3 rounded-xl border border-navy-700">
              <span className="text-slate-400 font-medium">Vulnerable Access Roads:</span>
              <div className="font-bold text-white text-sm mt-0.5">Identified & Mapped</div>
            </div>
            <div className="bg-navy-800/60 p-3 rounded-xl border border-navy-700">
              <span className="text-slate-400 font-medium">Pre-Monsoon Status:</span>
              <div className="font-bold text-emerald-400 text-sm mt-0.5">Preparedness Audit Ready</div>
            </div>
          </div>

          <div className="bg-navy-950 p-3 rounded-xl border border-navy-800 text-xs text-slate-300 space-y-1">
            <div className="flex items-center space-x-2 font-bold text-slate-200">
              <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>DDMA Pre-Monsoon Action Items ({currentDist.displayName}):</span>
            </div>
            <ul className="list-disc list-inside space-y-1 pl-2 text-[11px] text-slate-300">
              <li>Inspect culvert drainage and clearing along main district connectivity roads.</li>
              <li>Pre-position heavy earthmoving loaders near known historical landslide sectors.</li>
              <li>Identify emergency shelter locations for vulnerable hill-slope hamlets.</li>
            </ul>
          </div>
        </div>

        {/* All 20 Districts Selector */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-3 flex flex-col h-full">
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
            All 20 J&K UT Districts
          </h3>
          <div className="space-y-1 overflow-y-auto flex-1 max-h-72 pr-1">
            {JK_20_DISTRICTS.map((d) => (
              <div
                key={d.id}
                onClick={() => setSelectedDistrict(d.id)}
                className={`p-2 rounded-xl border text-xs cursor-pointer flex items-center justify-between transition-all ${
                  selectedDistrict === d.id
                    ? 'bg-purple-600 border-purple-500 text-white font-bold'
                    : 'bg-navy-800/50 border-navy-700 text-slate-300 hover:bg-navy-800'
                }`}
              >
                <span>{d.displayName}</span>
                <span className="text-[10px] font-mono text-slate-400">J&K UT</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* District Map View */}
      <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-sm font-bold text-white">District Vulnerability Map</h2>
            <p className="text-xs text-slate-400">District administrative boundary overlaid on 100m master grid.</p>
          </div>
          <Link
            href="/districts"
            className="text-xs text-purple-400 hover:text-purple-300 font-semibold flex items-center space-x-1"
          >
            <span>Full District Intelligence Page</span>
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
