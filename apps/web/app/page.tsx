"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { StateKpiCards } from '@/components/dashboard/StateKpiCards';
import { TimelineSlider } from '@/components/dashboard/TimelineSlider';
import { Activity, Shield } from 'lucide-react';
import { JK_20_DISTRICTS } from '@/lib/constants';

export default function StatewideCommandCentre() {
  const [selectedDistrict, setSelectedDistrict] = useState('all');
  const [activeLayers, setActiveLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44',
    'susceptibility_prob'
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
            <div className="flex items-center justify-between mb-2 px-1">
              <div className="flex items-center space-x-3">
                <img
                  src="/branding/geoslide-jk-logo-horizontal.png"
                  alt="GeoSlide-JK — Landslide Risk Intelligence"
                  className="h-7 sm:h-8 w-auto object-contain drop-shadow"
                />
              </div>
            </div>

            <ResearchDisclaimer />

            {/* AUDITED RELEASE STATUS BANNER */}
            <div className="bg-emerald-950/60 border border-emerald-500/50 p-2 px-3 rounded-lg mb-3 flex items-center justify-between text-xs text-emerald-200">
              <div className="flex items-center space-x-2 font-medium">
                <Shield className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>
                  <strong>GeoSlide-JK v1.0.0 Live:</strong> The static XGBoost susceptibility model and 100 m scenario-based dynamic hazard layers are available across all 20 J&K UT districts. Dynamic rainfall outputs are research proxy products and not operational observations.
                </span>
              </div>
              <span className="font-mono text-[10px] bg-emerald-900 px-2 py-0.5 rounded text-emerald-100 shrink-0 ml-2">
                Release v1.0.0
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
              <span>Statewide District Overview</span>
            </span>
            <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-600/40">
              20 Districts
            </span>
          </div>

          {/* District Selector List */}
          <div>
            <label className="text-[11px] font-semibold text-slate-300 uppercase tracking-wider block mb-2">
              All 20 J&K UT Districts
            </label>
            <div className="space-y-1 max-h-[500px] overflow-y-auto pr-1">
              {JK_20_DISTRICTS.map((d) => (
                <div
                  key={d.id}
                  onClick={() => setSelectedDistrict(d.id)}
                  className={`flex items-center justify-between p-2 rounded text-xs cursor-pointer border ${
                    selectedDistrict === d.id
                      ? 'bg-blue-600 border-blue-400 text-white font-semibold'
                      : 'bg-navy-950/60 border-navy-800 hover:bg-navy-800 text-slate-300'
                  }`}
                >
                  <span>{d.displayName}</span>
                  <span className="text-[10px] font-mono text-slate-400">
                    J&K UT
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
