"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { Cpu, Layers, Activity, CheckCircle, ShieldCheck, ArrowRight, BarChart2, Server } from 'lucide-react';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { StateKpiCards } from '@/components/dashboard/StateKpiCards';
import { TimelineSlider } from '@/components/dashboard/TimelineSlider';

export function ResearchDashboard() {
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
    <div className="flex-1 flex flex-col overflow-hidden relative">
      <div className="p-3 bg-navy-900/60 border-b border-navy-800">
        <ResearchDisclaimer />

        {/* Technical Release Status Banner */}
        <div className="bg-emerald-950/60 border border-emerald-500/50 p-2 px-3 rounded-lg mb-3 flex items-center justify-between text-xs text-emerald-200">
          <div className="flex items-center space-x-2 font-medium">
            <Cpu className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>
              <strong>Research & Technical GIS Explorer:</strong> 30-feature XGBoost susceptibility model (5-fold spatial district CV ROC-AUC: 0.8694), 100m EPSG:32643 master grid, and dynamic rainfall scenario microservices active.
            </span>
          </div>
          <span className="font-mono text-[10px] bg-emerald-900 px-2 py-0.5 rounded text-emerald-100 shrink-0 ml-2">
            ROC-AUC: 0.8694
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
  );
}
