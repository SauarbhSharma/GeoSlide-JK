"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { Cpu, Layers, Activity, CheckCircle, ShieldCheck, ArrowRight, BarChart2, Server, CheckCircle2 } from 'lucide-react';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { StateKpiCards } from '@/components/dashboard/StateKpiCards';
import { TimelineSlider } from '@/components/dashboard/TimelineSlider';
import { TrustStatusComponent } from '@/components/common/TrustStatusComponent';

export function ResearchDashboard() {
  const [selectedDistrict, setSelectedDistrict] = useState('all');
  const [activeLayers, setActiveLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44',
    'susceptibility_prob'
  ]);

  return (
    <div className="flex-1 flex flex-col overflow-hidden relative">
      <div className="p-3 bg-navy-900/60 border-b border-navy-800 space-y-2">
        <ResearchDisclaimer />

        {/* Unified Technical Research Status Panel */}
        <div className="bg-emerald-950/60 border border-emerald-500/50 p-2.5 px-3 rounded-xl flex flex-wrap items-center justify-between gap-2 text-xs text-emerald-200">
          <div className="flex items-center space-x-2 font-medium">
            <Cpu className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>
              <strong>Research & Technical GIS Explorer:</strong> 30-feature XGBoost susceptibility model (5-fold spatial district CV ROC-AUC: 0.8694), 100m EPSG:32643 master grid, and dynamic rainfall scenario microservices active.
            </span>
          </div>
          <TrustStatusComponent compact />
        </div>

        {/* Outcome Card — "What this platform helps you do" */}
        <div className="bg-navy-900 border border-navy-700 p-3 rounded-xl space-y-1">
          <h2 className="text-[11px] font-bold text-slate-300 uppercase tracking-wider">
            What this platform helps you do (Researcher & Technical Auditor):
          </h2>
          <ul className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px] text-slate-300 font-medium">
            <li className="flex items-center space-x-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              <span>Inspect raw 100m raster layers & vector geometries.</span>
            </li>
            <li className="flex items-center space-x-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              <span>Review 5-fold spatial CV model validation metrics.</span>
            </li>
            <li className="flex items-center space-x-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              <span>Audit 30 predictor feature importance & leakage rules.</span>
            </li>
            <li className="flex items-center space-x-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              <span>Verify microservice endpoint health & tile provenance.</span>
            </li>
          </ul>
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
