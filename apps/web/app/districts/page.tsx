"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { JK_20_DISTRICTS, RISK_COLORS } from '@/lib/constants';
import { Building2, Download, AlertTriangle, Users, Navigation, ShieldCheck } from 'lucide-react';

export default function DistrictIntelligence() {
  const [selectedId, setSelectedId] = useState('ramban');
  const district = JK_20_DISTRICTS.find((d) => d.id === selectedId) || JK_20_DISTRICTS[0];

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Page Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-navy-900 border border-navy-700 p-4 rounded-xl">
          <div>
            <div className="flex items-center space-x-2">
              <Building2 className="w-5 h-5 text-blue-400" />
              <h1 className="text-xl font-bold text-white">District Intelligence Dashboard</h1>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Detailed risk profile, exposure metrics, and research advisories across all 20 Union Territory districts.
            </p>
          </div>

          {/* District Selector */}
          <div className="flex items-center space-x-3">
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="bg-navy-800 border border-navy-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 font-medium"
            >
              {JK_20_DISTRICTS.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.displayName} District ({d.riskLevel})
                </option>
              ))}
            </select>
            <button className="flex items-center space-x-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs px-3 py-2 rounded-lg font-medium transition-colors">
              <Download className="w-4 h-4" />
              <span>Download District Report (PDF)</span>
            </button>
          </div>
        </div>

        {/* Selected District Overview Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Main Card */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl md:col-span-2 space-y-4">
            <div className="flex items-center justify-between border-b border-navy-800 pb-3">
              <div>
                <span className="text-xs text-slate-400 uppercase font-mono">Selected District</span>
                <h2 className="text-2xl font-extrabold text-white">{district.displayName}</h2>
                <div className="text-xs text-slate-400 mt-0.5">
                  Source Name: <span className="font-mono text-slate-200">{district.sourceName}</span> | Status: <span className="text-emerald-400">Included in J&K UT</span>
                </div>
              </div>
              <div
                className="px-3 py-1.5 rounded-lg border text-sm font-bold font-mono"
                style={{
                  backgroundColor: RISK_COLORS[district.riskLevel] + '22',
                  borderColor: RISK_COLORS[district.riskLevel],
                  color: RISK_COLORS[district.riskLevel]
                }}
              >
                {district.riskLevel} Hazard Priority
              </div>
            </div>

            {/* Metrics */}
            <div className="grid grid-cols-3 gap-3">
              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg">
                <div className="text-[11px] text-slate-400 flex items-center space-x-1">
                  <Users className="w-3.5 h-3.5 text-purple-400" />
                  <span>Exposed Population</span>
                </div>
                <div className="text-lg font-bold text-white mt-1">~42,500</div>
                <div className="text-[10px] text-purple-300 font-mono mt-0.5">GHS-POP Demo Metric</div>
              </div>

              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg">
                <div className="text-[11px] text-slate-400 flex items-center space-x-1">
                  <Navigation className="w-3.5 h-3.5 text-sky-400" />
                  <span>Exposed Highways</span>
                </div>
                <div className="text-lg font-bold text-white mt-1">68.4 km</div>
                <div className="text-[10px] text-sky-300 font-mono mt-0.5">Includes NH-44 Section</div>
              </div>

              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg">
                <div className="text-[11px] text-slate-400 flex items-center space-x-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Data Confidence</span>
                </div>
                <div className="text-lg font-bold text-emerald-400 mt-1">HIGH</div>
                <div className="text-[10px] text-slate-400 font-mono mt-0.5">Full Data Mask Coverage</div>
              </div>
            </div>

            {/* Summary Text */}
            <div className="bg-navy-800/40 border border-navy-700 p-3 rounded-lg text-xs leading-relaxed text-slate-300 space-y-2">
              <p>
                <strong>Terrain Profile:</strong> {district.displayName} contains steep mountain topography with significant elevation gradients. Structural features (faults, lineaments) are present along deep stream valleys.
              </p>
              <p>
                <strong>Rainfall Trigger State:</strong> Currently under <span className="text-amber-300 font-semibold">Demo Playback</span> mode utilizing July 2026 satellite sample granules. Percentile triggers indicate elevated antecedent moisture.
              </p>
            </div>
          </div>

          {/* Quick List of All 20 Districts */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3 flex flex-col h-full">
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Select from 20 J&K Districts
            </h3>
            <div className="space-y-1 overflow-y-auto flex-1 max-h-96 pr-1">
              {JK_20_DISTRICTS.map((d) => (
                <div
                  key={d.id}
                  onClick={() => setSelectedId(d.id)}
                  className={`p-2 rounded-lg border text-xs cursor-pointer flex items-center justify-between transition-all ${
                    selectedId === d.id
                      ? 'bg-blue-600 border-blue-500 text-white font-semibold'
                      : 'bg-navy-800/50 border-navy-700 text-slate-300 hover:bg-navy-800'
                  }`}
                >
                  <span>{d.displayName}</span>
                  <span
                    className="text-[10px] font-mono px-1.5 py-0.5 rounded"
                    style={{
                      backgroundColor: RISK_COLORS[d.riskLevel] + '33',
                      color: selectedId === d.id ? '#ffffff' : RISK_COLORS[d.riskLevel]
                    }}
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
