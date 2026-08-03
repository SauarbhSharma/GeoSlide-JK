"use client";

import React, { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Activity, ShieldAlert, Layers, ChevronRight, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface SegmentData {
  chainage: string;
  name: string;
  length: string;
  meanSusc: number;
  maxSusc: number;
  highRiskPct: number;
  classRating: string;
}

export default function CorridorPage() {
  const sampleSegments: SegmentData[] = [
    { chainage: 'Km 142.0 – 142.5', name: 'Panthyal Cut-Slope', length: '500 m', meanSusc: 0.74, maxSusc: 0.88, highRiskPct: 84.5, classRating: 'Very High' },
    { chainage: 'Km 148.0 – 148.5', name: 'Ramban Bypass Sector', length: '500 m', meanSusc: 0.68, maxSusc: 0.79, highRiskPct: 72.0, classRating: 'High' },
    { chainage: 'Km 153.0 – 153.5', name: 'Digdol Landslide Zone', length: '500 m', meanSusc: 0.65, maxSusc: 0.76, highRiskPct: 68.4, classRating: 'High' },
    { chainage: 'Km 165.5 – 166.0', name: 'Ramsu Mudslide Area', length: '500 m', meanSusc: 0.58, maxSusc: 0.71, highRiskPct: 52.1, classRating: 'High' },
    { chainage: 'Km 178.0 – 178.5', name: 'Banihal South Portal', length: '500 m', meanSusc: 0.42, maxSusc: 0.54, highRiskPct: 28.0, classRating: 'Moderate' },
  ];

  const [selectedSeg, setSelectedSeg] = useState<SegmentData>(sampleSegments[0]);

  return (
    <div className="flex flex-col min-h-screen bg-navy-950 text-slate-100">
      <Header />
      <main className="flex-1 p-4 max-w-6xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-2 shadow-xl">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-amber-400" />
            <h1 className="text-xl sm:text-2xl font-black text-white">NH-44 Corridor Monitor Shell</h1>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed max-w-2xl">
            Chainage-indexed 500m segment evaluation of <strong>Static Road-Segment Landslide Exposure</strong> along the NH-44 highway corridor.
          </p>
        </div>

        {/* Operational Terminology Disclaimer */}
        <div className="bg-navy-950 border border-amber-500/50 p-4 rounded-2xl text-xs space-y-1">
          <div className="flex items-center space-x-2 text-amber-300 font-bold">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>Operational Classification Label: Static Road-Segment Landslide Exposure</span>
          </div>
          <p className="text-slate-300">
            This module evaluates physical slope instability exposure. It DOES NOT report current pavement structural condition, live road closures, or real-time traffic status.
          </p>
        </div>

        {/* Strip View Simulator */}
        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-3">
          <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Linear Chainage Strip View (Udhampur to Banihal)
          </h2>

          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs">
            {sampleSegments.map((seg) => {
              const isSelected = selectedSeg.chainage === seg.chainage;
              return (
                <div
                  key={seg.chainage}
                  onClick={() => setSelectedSeg(seg)}
                  className={`p-3 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-amber-600 border-amber-500 text-white font-bold shadow-lg'
                      : 'bg-navy-950 border-navy-800 text-slate-300 hover:bg-navy-850'
                  }`}
                >
                  <div className="text-[10px] font-mono opacity-80">{seg.chainage}</div>
                  <div className="text-xs font-bold mt-0.5 truncate">{seg.name}</div>
                  <div className="text-[11px] mt-1 font-mono">
                    Max: {(seg.maxSusc * 100).toFixed(0)}%
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Segment Detail Card */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl md:col-span-2 space-y-4">
            <div className="flex items-center justify-between border-b border-navy-800 pb-3">
              <div>
                <span className="text-[10px] text-amber-400 font-mono uppercase tracking-wider">
                  Selected Segment Details
                </span>
                <h3 className="text-xl font-black text-white">{selectedSeg.name}</h3>
                <div className="text-xs text-slate-300 font-mono">{selectedSeg.chainage} ({selectedSeg.length})</div>
              </div>
              <span className="px-3 py-1 bg-amber-950 border border-amber-600/50 text-amber-300 font-bold text-xs rounded-xl font-mono">
                {selectedSeg.classRating} Exposure
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3 text-xs">
              <div className="bg-navy-950 p-3 rounded-xl border border-navy-800">
                <span className="text-slate-400">Mean Susceptibility:</span>
                <div className="text-base font-bold text-amber-400 mt-0.5 font-mono">
                  {(selectedSeg.meanSusc * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-navy-950 p-3 rounded-xl border border-navy-800">
                <span className="text-slate-400">Peak Susceptibility:</span>
                <div className="text-base font-bold text-rose-400 mt-0.5 font-mono">
                  {(selectedSeg.maxSusc * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-navy-950 p-3 rounded-xl border border-navy-800">
                <span className="text-slate-400">High Risk Cell Share:</span>
                <div className="text-base font-bold text-sky-400 mt-0.5 font-mono">
                  {selectedSeg.highRiskPct.toFixed(1)}%
                </div>
              </div>
            </div>

            {/* Technical Details Drawer */}
            <div className="bg-navy-950 p-4 rounded-xl border border-navy-800 space-y-2 text-xs">
              <span className="font-bold text-slate-200 block text-[11px] uppercase tracking-wider">
                Technical Details & Raster Attributes:
              </span>
              <div className="grid grid-cols-2 gap-2 text-slate-300 font-mono text-[11px]">
                <div>• Segment Width: 500 meters</div>
                <div>• Grid Resolution: 100 m EPSG:32643</div>
                <div>• Predictor Count: 30 Features</div>
                <div>• Data Confidence Placeholder: 100% Complete</div>
              </div>
            </div>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-3">
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Priority Segments Queue
            </h3>
            <div className="space-y-2 text-xs">
              {sampleSegments.map((s, idx) => (
                <div key={s.chainage} className="p-2.5 bg-navy-950 rounded-xl border border-navy-800 flex items-center justify-between">
                  <div>
                    <div className="font-bold text-white">#{idx + 1} {s.name}</div>
                    <div className="text-[10px] text-slate-400 font-mono">{s.chainage}</div>
                  </div>
                  <span className="text-amber-400 font-bold font-mono">{(s.meanSusc * 100).toFixed(0)}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
