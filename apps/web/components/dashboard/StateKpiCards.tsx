"use client";

import { Shield, Layers, CloudRain, Navigation } from 'lucide-react';

export function StateKpiCards() {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
      {/* Total Districts */}
      <div className="bg-navy-900/90 border border-navy-700 p-3 rounded-xl flex items-center space-x-3">
        <div className="bg-blue-600/20 text-blue-400 p-2 rounded-lg border border-blue-500/30">
          <Shield className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-medium text-slate-300">J&K UT Spatial Coverage</div>
          <div className="text-xl font-bold text-white flex items-center space-x-1">
            <span>20 / 20</span>
            <span className="text-[10px] bg-emerald-950 text-emerald-300 border border-emerald-600/40 px-1.5 py-0.5 rounded font-mono">
              Full UT Grid
            </span>
          </div>
          <div className="text-[10px] text-slate-400 font-mono">20 J&K UT Districts</div>
        </div>
      </div>

      {/* Static Susceptibility Model */}
      <div className="bg-navy-900/90 border border-navy-700 p-3 rounded-xl flex items-center space-x-3">
        <div className="bg-emerald-600/20 text-emerald-400 p-2 rounded-lg border border-emerald-500/30">
          <Layers className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-medium text-slate-300">Static ML Model</div>
          <div className="text-xl font-bold text-white flex items-center space-x-1">
            <span>ROC 0.8694</span>
            <span className="text-[10px] bg-emerald-950 text-emerald-300 border border-emerald-600/40 px-1.5 py-0.5 rounded font-mono">
              Trained
            </span>
          </div>
          <div className="text-[10px] text-emerald-400 font-mono">XGBoost 30 Predictors</div>
        </div>
      </div>

      {/* Dynamic Hazard Scenario Mode */}
      <div className="bg-navy-900/90 border border-navy-700 p-3 rounded-xl flex items-center space-x-3">
        <div className="bg-amber-600/20 text-amber-400 p-2 rounded-lg border border-amber-500/30">
          <CloudRain className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-medium text-slate-300">Dynamic Hazard Mode</div>
          <div className="text-xl font-bold text-white flex items-center space-x-1">
            <span>Scenario/Proxy</span>
            <span className="text-[10px] bg-amber-950 text-amber-300 border border-amber-600/40 px-1.5 py-0.5 rounded font-mono">
              Proxy
            </span>
          </div>
          <div className="text-[10px] text-slate-400 font-mono">H_dyn = S * (Rain_24h / P90)</div>
        </div>
      </div>

      {/* Critical Transport Corridor */}
      <div className="bg-navy-900/90 border border-navy-700 p-3 rounded-xl flex items-center space-x-3">
        <div className="bg-sky-600/20 text-sky-400 p-2 rounded-lg border border-sky-500/30">
          <Navigation className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-medium text-slate-300">Strategic Highway Corridor</div>
          <div className="text-xl font-bold text-white flex items-center space-x-1">
            <span>NH-44 Axis</span>
            <span className="text-[10px] bg-sky-950 text-sky-300 border border-sky-600/40 px-1.5 py-0.5 rounded font-mono">
              Monitored
            </span>
          </div>
          <div className="text-[10px] text-slate-400 font-mono">Jammu-Ramban-Srinagar</div>
        </div>
      </div>
    </div>
  );
}
