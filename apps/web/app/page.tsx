"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { StateKpiCards } from '@/components/dashboard/StateKpiCards';
import { TimelineSlider } from '@/components/dashboard/TimelineSlider';
import { AlertCircle, ArrowUpRight, Activity } from 'lucide-react';
import { JK_20_DISTRICTS, RISK_COLORS } from '@/lib/constants';

export default function StatewideCommandCentre() {
  const [selectedDistrict, setSelectedDistrict] = useState('all');
  const [activeLayers, setActiveLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44_corridor',
    'rainfall_imerg',
    'landslides'
  ]);

  const handleToggleLayer = (layerId: string) => {
    setActiveLayers((prev) =>
      prev.includes(layerId) ? prev.filter((id) => id !== layerId) : [...prev, layerId]
    );
  };

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      {/* Main Workspace Grid */}
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

          {/* Bottom Timeline Control */}
          <TimelineSlider />
        </div>

        {/* Right Advisory & Situational Panel */}
        <div className="w-80 bg-navy-900 border-l border-navy-700 p-3 hidden xl:flex flex-col space-y-4 overflow-y-auto shrink-0 text-xs">
          <div className="border-b border-navy-700 pb-2 flex items-center justify-between">
            <span className="font-bold text-white flex items-center space-x-1.5">
              <Activity className="w-4 h-4 text-blue-400" />
              <span>Situational Summary</span>
            </span>
            <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-600/30">
              Active Feed
            </span>
          </div>

          {/* Elevated Risk Advisory Cards (Demo) */}
          <div>
            <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
              Elevated Priority Focus
            </label>
            <div className="space-y-2">
              <div className="bg-rose-950/40 border border-rose-600/40 p-2.5 rounded-lg space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-300">Ramban District</span>
                  <span className="bg-rose-900 text-rose-200 text-[10px] px-1.5 py-0.5 rounded font-mono">Critical</span>
                </div>
                <p className="text-[11px] text-slate-300">
                  NH-44 Panthyal to Digdol slope section. High antecedent rainfall trigger index (Demo).
                </p>
                <div className="text-[10px] font-mono text-slate-400 flex justify-between pt-1">
                  <span>Confidence: High</span>
                  <span>Data: Demo Playback</span>
                </div>
              </div>

              <div className="bg-orange-950/40 border border-orange-600/40 p-2.5 rounded-lg space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-orange-300">Doda & Kishtwar</span>
                  <span className="bg-orange-900 text-orange-200 text-[10px] px-1.5 py-0.5 rounded font-mono">Very High</span>
                </div>
                <p className="text-[11px] text-slate-300">
                  Steep terrain slopes along Chenab river valley corridor.
                </p>
                <div className="text-[10px] font-mono text-slate-400 flex justify-between pt-1">
                  <span>Confidence: High</span>
                  <span>Data: Demo Playback</span>
                </div>
              </div>

              <div className="bg-amber-950/40 border border-amber-600/40 p-2.5 rounded-lg space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-300">Reasi & Rajouri</span>
                  <span className="bg-amber-900 text-amber-200 text-[10px] px-1.5 py-0.5 rounded font-mono">High</span>
                </div>
                <p className="text-[11px] text-slate-300">
                  Savage terrain slopes & road excavation disturbances.
                </p>
                <div className="text-[10px] font-mono text-slate-400 flex justify-between pt-1">
                  <span>Confidence: Moderate</span>
                  <span>Data: Demo Playback</span>
                </div>
              </div>
            </div>
          </div>

          {/* District Status List */}
          <div>
            <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
              All 20 J&K District Status
            </label>
            <div className="space-y-1 max-h-56 overflow-y-auto pr-1">
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
                    {d.riskLevel}
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
