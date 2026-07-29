"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { StateKpiCards } from '@/components/dashboard/StateKpiCards';
import { TimelineSlider } from '@/components/dashboard/TimelineSlider';
import { Activity, AlertTriangle } from 'lucide-react';
import { JK_20_DISTRICTS, RISK_COLORS } from '@/lib/constants';

export default function StatewideCommandCentre() {
  const [selectedDistrict, setSelectedDistrict] = useState('all');
  const [activeLayers, setActiveLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44'
  ]);

  const handleToggleLayer = (layerId: string) => {
    setActiveLayers((prev) =>
      prev.includes(layerId) ? prev.filter((id) => id !== layerId) : [...prev, layerId]
    );
  };

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex flex-1 overflow-hidden relative">
        <Sidebar
          selectedDistrict={selectedDistrict}
          onSelectDistrict={setSelectedDistrict}
          activeLayers={activeLayers}
          onToggleLayer={handleToggleLayer}
        />

        {/* Center Map & Summary Area */}
        <div className="flex-1 flex flex-col overflow-hidden relative">
          <div className="p-3 bg-navy-900/60 border-b border-navy-800">
            <ResearchDisclaimer />

            {/* PHASE 2 STATUS NOTE */}
            <div className="bg-emerald-950/60 border border-emerald-500/50 p-2 px-3 rounded-lg mb-3 flex items-center justify-between text-xs text-emerald-200">
              <div className="flex items-center space-x-2 font-medium">
                <AlertTriangle className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>
                  <strong>Phase 2 Active:</strong> Full-J&K 30m DEM elevation, slope, aspect, hillshade COGs, and 10 static vector layers are live. District risk classes remain illustrative demonstration data.
                </span>
              </div>
              <span className="font-mono text-[10px] bg-emerald-900 px-2 py-0.5 rounded text-emerald-100 shrink-0 ml-2">
                Phase 2 — Static Geospatial Products
              </span>
            </div>

            <StateKpiCards />
          </div>

          {/* Map Section */}
          <div className="flex-1 relative overflow-hidden">
            <MapContainer
              selectedDistrict={selectedDistrict}
              onSelectDistrict={setSelectedDistrict}
              activeLayers={activeLayers}
            />
          </div>

          <TimelineSlider />
        </div>

        {/* Right Advisory & Situational Panel */}
        <div className="w-80 bg-navy-900 border-l border-navy-700 p-3 hidden xl:flex flex-col space-y-4 overflow-y-auto shrink-0 text-xs">
          <div className="border-b border-navy-700 pb-2 flex items-center justify-between">
            <span className="font-bold text-white flex items-center space-x-1.5">
              <Activity className="w-4 h-4 text-blue-400" />
              <span>Situational Summary (Demo)</span>
            </span>
            <span className="text-[10px] font-mono text-amber-400 bg-amber-950 px-2 py-0.5 rounded border border-amber-600/40">
              Illustrative
            </span>
          </div>

          {/* Elevated Focus Areas (Demo) */}
          <div>
            <label className="text-[11px] font-semibold text-slate-300 uppercase tracking-wider block mb-2">
              Elevated Focus Areas (Demo)
            </label>
            <div className="space-y-2">
              <div className="bg-rose-950/40 border border-rose-600/40 p-2.5 rounded-lg space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-300">Ramban District</span>
                  <span className="bg-rose-900 text-rose-200 text-[10px] px-1.5 py-0.5 rounded font-mono">Critical (Demo)</span>
                </div>
                <p className="text-[11px] text-slate-300">
                  NH-44 Panthyal corridor. Demo value — not derived from processed project data.
                </p>
                <div className="text-[10px] font-mono text-amber-300 pt-1">
                  Illustrative Demo Priority
                </div>
              </div>

              <div className="bg-orange-950/40 border border-orange-600/40 p-2.5 rounded-lg space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-orange-300">Doda & Kishtwar</span>
                  <span className="bg-orange-900 text-orange-200 text-[10px] px-1.5 py-0.5 rounded font-mono">Very High (Demo)</span>
                </div>
                <p className="text-[11px] text-slate-300">
                  Chenab river valley corridor. Demo value — not derived from processed project data.
                </p>
                <div className="text-[10px] font-mono text-amber-300 pt-1">
                  Illustrative Demo Priority
                </div>
              </div>
            </div>
          </div>

          {/* District Status List */}
          <div>
            <label className="text-[11px] font-semibold text-slate-300 uppercase tracking-wider block mb-2">
              All 20 J&K Districts List (Demo)
            </label>
            <div className="space-y-1 max-h-64 overflow-y-auto pr-1">
              {JK_20_DISTRICTS.map((d) => (
                <div
                  key={d.id}
                  onClick={() => setSelectedDistrict(d.id)}
                  className={`flex items-center justify-between p-1.5 rounded text-xs cursor-pointer ${
                    selectedDistrict === d.id ? 'bg-blue-600 text-white font-semibold' : 'hover:bg-navy-800 text-slate-300'
                  }`}
                >
                  <span>{d.displayName}</span>
                  <span
                    className="text-[10px] px-1.5 py-0.5 rounded font-mono"
                    style={{ backgroundColor: RISK_COLORS[d.riskLevel] + '33', color: RISK_COLORS[d.riskLevel] }}
                  >
                    {d.riskLevel} (Demo)
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
