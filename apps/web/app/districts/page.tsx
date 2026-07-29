"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { JK_20_DISTRICTS, RISK_COLORS } from '@/lib/constants';
import { Building2, Download, Users, Navigation, ShieldCheck, AlertTriangle } from 'lucide-react';

export default function DistrictIntelligence() {
  const [selectedId, setSelectedId] = useState('ramban');
  const district = JK_20_DISTRICTS.find((d) => d.id === selectedId) || JK_20_DISTRICTS[0];

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        {/* Compact Phase Notice */}
        <div className="bg-navy-900/90 border border-blue-600/40 p-2.5 rounded-lg flex items-center justify-between text-xs text-blue-200">
          <span className="flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
            <span>
              <strong>District Profile Status:</strong> All displayed numerical values, exposure counts, and hazard classes below are <strong>Illustrative — not derived from processed project data</strong>.
            </span>
          </span>
          <span className="font-mono text-[10px] bg-blue-950 px-2 py-0.5 rounded text-blue-300">Phase 2 — Static Geospatial Products</span>
        </div>

        {/* Page Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-navy-900 border border-navy-700 p-4 rounded-xl">
          <div>
            <div className="flex items-center space-x-2">
              <Building2 className="w-5 h-5 text-blue-400" />
              <h1 className="text-xl font-bold text-white">District Intelligence Dashboard</h1>
            </div>
            <p className="text-xs text-slate-300 mt-1">
              Statewide administrative profiles across all 20 Union Territory districts.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="bg-navy-800 border border-navy-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 font-semibold"
            >
              {JK_20_DISTRICTS.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.displayName} District ({d.riskLevel} - Demo)
                </option>
              ))}
            </select>
            <button className="flex items-center space-x-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs px-3 py-2 rounded-lg font-semibold transition-colors opacity-60 cursor-not-allowed">
              <Download className="w-4 h-4" />
              <span>Report Download (Pending Phase 6)</span>
            </button>
          </div>
        </div>

        {/* Selected District Overview Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl md:col-span-2 space-y-4">
            <div className="flex items-center justify-between border-b border-navy-800 pb-3">
              <div>
                <span className="text-xs text-slate-400 uppercase font-mono">Selected District</span>
                <h2 className="text-2xl font-black text-white">{district.displayName}</h2>
                <div className="text-xs text-slate-300 mt-0.5">
                  Source Name: <span className="font-mono text-white font-bold">{district.sourceName}</span> | Status: <span className="text-emerald-400 font-semibold">Included in J&K UT</span>
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
                Illustrative Demo Priority: {district.riskLevel} (Demo)
              </div>
            </div>

            {/* Metrics */}
            <div className="grid grid-cols-3 gap-3">
              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg">
                <div className="text-[11px] text-slate-300 flex items-center space-x-1 font-medium">
                  <Users className="w-3.5 h-3.5 text-purple-400" />
                  <span>Population (Demo)</span>
                </div>
                <div className="text-lg font-bold text-white mt-1">~42,500</div>
                <div className="text-[10px] text-amber-300 font-mono mt-0.5">Illustrative Demo Value</div>
              </div>

              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg">
                <div className="text-[11px] text-slate-300 flex items-center space-x-1 font-medium">
                  <Navigation className="w-3.5 h-3.5 text-sky-400" />
                  <span>Road Length (Demo)</span>
                </div>
                <div className="text-lg font-bold text-white mt-1">68.4 km</div>
                <div className="text-[10px] text-amber-300 font-mono mt-0.5">Illustrative Demo Value</div>
              </div>

              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg">
                <div className="text-[11px] text-slate-300 flex items-center space-x-1 font-medium">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Data Confidence (Demo)</span>
                </div>
                <div className="text-lg font-bold text-amber-300 mt-1">Demo / Unvalidated</div>
                <div className="text-[10px] text-slate-400 font-mono mt-0.5">Vector Mask Available</div>
              </div>
            </div>

            <div className="bg-navy-800/40 border border-navy-700 p-3 rounded-lg text-xs leading-relaxed text-slate-300 space-y-2">
              <p>
                <strong>Terrain Status:</strong> Phase 2 terrain products are available. District-level terrain feature summaries will be calculated during Phase 3.
              </p>
              <p>
                <strong>Rainfall State (Demo):</strong> Interface demonstration mode. Dynamic calculations connect in Phase 5. Illustrative Demo Value.
              </p>
            </div>
          </div>

          {/* Quick List of All 20 Districts */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3 flex flex-col h-full">
            <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
              20 J&K UT Districts (Demo)
            </h3>
            <div className="space-y-1 overflow-y-auto flex-1 max-h-96 pr-1">
              {JK_20_DISTRICTS.map((d) => (
                <div
                  key={d.id}
                  onClick={() => setSelectedId(d.id)}
                  className={`p-2 rounded-lg border text-xs cursor-pointer flex items-center justify-between transition-all ${
                    selectedId === d.id
                      ? 'bg-blue-600 border-blue-500 text-white font-bold'
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
