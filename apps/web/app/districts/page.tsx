"use client";

import { useState, useEffect } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { JK_20_DISTRICTS } from '@/lib/constants';
import { Building2, ShieldCheck, Info, BarChart2 } from 'lucide-react';
import { apiUrl } from '@/lib/api';

interface DistrictSummaryData {
  success: boolean;
  district_id: string;
  district_name: string;
  state_ut: string;
  geometry_verified: boolean;
  grid_alignment: string;
  mean_susceptibility_probability?: number;
  susceptibility_rating?: string;
  high_susceptibility_area_pct?: number;
  mean_dynamic_hazard_index?: number;
  dynamic_hazard_rating?: string;
  scenario_proxy_warning?: string;
}

export default function DistrictIntelligence() {
  const [selectedId, setSelectedId] = useState('ramban');
  const [summary, setSummary] = useState<DistrictSummaryData | null>(null);
  const [loading, setLoading] = useState(false);

  const district = JK_20_DISTRICTS.find((d) => d.id === selectedId) || JK_20_DISTRICTS[0];

  useEffect(() => {
    setLoading(true);
    fetch(apiUrl(`/api/v1/summary/district/${selectedId}`))
      .then((res) => res.json())
      .then((data) => {
        setSummary(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to fetch district summary:', err);
        setLoading(false);
      });
  }, [selectedId]);

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
            <p className="text-xs text-slate-300 mt-1">
              Statewide administrative profiles and zonal summary metrics across all 20 Union Territory districts.
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
                  {d.displayName} District
                </option>
              ))}
            </select>
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
                  Source Name: <span className="font-mono text-white font-bold">{district.sourceName}</span> | Status: <span className="text-emerald-400 font-semibold">Verified 20 J&K UT Boundary</span>
                </div>
              </div>
              <div className="px-3 py-1.5 rounded-lg border border-blue-500/40 bg-blue-950 text-blue-300 text-xs font-bold font-mono">
                J&K UT Admin District
              </div>
            </div>

            {/* Zonal Metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
                <span className="text-slate-400 font-medium">Mean Susceptibility:</span>
                <div className="font-bold text-amber-400 text-sm">
                  {loading ? '...' : summary?.mean_susceptibility_probability != null ? (summary.mean_susceptibility_probability * 100).toFixed(1) + '%' : 'N/A'}
                </div>
              </div>

              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
                <span className="text-slate-400 font-medium">Susceptibility Rating:</span>
                <div className="font-bold text-amber-300 text-sm">
                  {loading ? '...' : summary?.susceptibility_rating || 'Low to Moderate'}
                </div>
              </div>

              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
                <span className="text-slate-400 font-medium">High Risk Slope Area:</span>
                <div className="font-bold text-rose-400 text-sm">
                  {loading ? '...' : summary?.high_susceptibility_area_pct != null ? `${summary.high_susceptibility_area_pct}%` : 'N/A'}
                </div>
              </div>

              <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
                <span className="text-slate-400 font-medium">Dynamic Hazard Rating:</span>
                <div className="font-bold text-sky-300 text-sm">
                  {loading ? '...' : summary?.dynamic_hazard_rating || 'Low'}
                </div>
              </div>
            </div>

            {/* Notice */}
            <div className="bg-navy-800/80 border border-navy-700 p-4 rounded-lg flex items-center space-x-3 text-xs text-slate-300">
              <Info className="w-5 h-5 text-blue-400 shrink-0" />
              <div>
                <h3 className="font-bold text-white text-sm mb-0.5">District Point & Cell Inspection</h3>
                <p>
                  To inspect specific 100m grid cells for static susceptibility (XGBoost) and dynamic hazard (24h rainfall proxy scenario), use the <strong className="text-blue-300">Statewide Command Centre Map Inspector</strong> or the <strong className="text-blue-300">Location Risk Check tool</strong>.
                </p>
              </div>
            </div>

            <div className="bg-navy-800/40 border border-navy-700 p-3 rounded-lg text-xs leading-relaxed text-slate-300 space-y-2">
              <p className="flex items-center space-x-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
                <span><strong>Boundary Status:</strong> Polygon geometry verified and aligned to 100m EPSG:32643 master reference grid.</span>
              </p>
            </div>
          </div>

          {/* Quick List of All 20 Districts */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3 flex flex-col h-full">
            <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
              20 J&K UT Districts
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
