"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { TrustStatusComponent } from '@/components/common/TrustStatusComponent';
import { Shield, Layers, Cpu } from 'lucide-react';

export default function InteractiveRiskExplorer() {
  const [selectedDistrict, setSelectedDistrict] = useState('all');
  const [activeLayers, setActiveLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44',
    'susceptibility_prob'
  ]);

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex flex-1 overflow-hidden relative">
        <div className="flex-1 flex flex-col overflow-hidden relative">
          <div className="p-3 bg-navy-900/60 border-b border-navy-800 space-y-2">
            <ResearchDisclaimer />

            <div className="bg-emerald-950/60 border border-emerald-500/50 p-2.5 px-3 rounded-xl flex flex-wrap items-center justify-between gap-2 text-xs text-emerald-200">
              <div className="flex items-center space-x-2 font-medium">
                <Cpu className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>
                  <strong>Full GIS Spatial Explorer:</strong> Single authoritative layer drawer active. Inspect 100m EPSG:32643 raster layers, 5-class susceptibility classes, tectonics, and NGDR historical landslide inventories.
                </span>
              </div>
              <TrustStatusComponent compact />
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
