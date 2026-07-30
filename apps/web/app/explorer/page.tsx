"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Shield } from 'lucide-react';

export default function InteractiveRiskExplorer() {
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

        <div className="flex-1 flex flex-col overflow-hidden relative">
          <div className="p-3 bg-navy-900/60 border-b border-navy-800">
            <ResearchDisclaimer />

            <div className="bg-emerald-950/60 border border-emerald-500/50 p-2 px-3 rounded-lg flex items-center justify-between text-xs text-emerald-200">
              <div className="flex items-center space-x-2 font-medium">
                <Shield className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>
                  <strong>GeoSlide-JK v1.0.0 Live:</strong> Static XGBoost susceptibility model (ROC-AUC: 0.8694) & 100m EPSG:32643 dynamic hazard index layers are fully active across all 20 J&K UT districts.
                </span>
              </div>
              <span className="font-mono text-[10px] bg-emerald-900 px-2 py-0.5 rounded text-emerald-100 shrink-0 ml-2">
                Release v1.0.0
              </span>
            </div>
          </div>

          <div className="flex-1 relative overflow-hidden">
            <MapContainer
              selectedDistrict={selectedDistrict}
              onSelectDistrict={setSelectedDistrict}
              activeLayers={activeLayers}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
