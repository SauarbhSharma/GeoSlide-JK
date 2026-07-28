"use client";

import { Shield, AlertTriangle, Users, Navigation, CheckCircle } from 'lucide-react';

export function StateKpiCards() {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
      {/* Total Districts */}
      <div className="bg-navy-900/90 border border-navy-700 p-3 rounded-xl flex items-center space-x-3">
        <div className="bg-blue-600/20 text-blue-400 p-2 rounded-lg border border-blue-500/30">
          <Shield className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-medium text-slate-400">J&K State Coverage</div>
          <div className="text-xl font-bold text-white flex items-center space-x-1">
            <span>20 / 20</span>
            <span className="text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-600/40 px-1.5 py-0.5 rounded font-normal">
              100% UT
            </span>
          </div>
        </div>
      </div>

      {/* Elevated Hazard Zones */}
      <div className="bg-navy-900/90 border border-navy-700 p-3 rounded-xl flex items-center space-x-3">
        <div className="bg-orange-600/20 text-orange-400 p-2 rounded-lg border border-orange-500/30">
          <AlertTriangle className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-medium text-slate-400">Elevated Priority Zones (Demo)</div>
          <div className="text-xl font-bold text-white flex items-center space-x-1">
            <span>5 Districts</span>
            <span className="text-[10px] bg-orange-950 text-orange-400 border border-orange-600/40 px-1.5 py-0.5 rounded font-normal">
              Ramban / Doda
            </span>
          </div>
        </div>
      </div>

      {/* Exposed Population */}
      <div className="bg-navy-900/90 border border-navy-700 p-3 rounded-xl flex items-center space-x-3">
        <div className="bg-purple-600/20 text-purple-400 p-2 rounded-lg border border-purple-500/30">
          <Users className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-medium text-slate-400">Exposed Population (Demo)</div>
          <div className="text-xl font-bold text-white flex items-center space-x-1">
            <span>~485,000</span>
            <span className="text-[10px] bg-purple-950 text-purple-300 border border-purple-600/40 px-1.5 py-0.5 rounded font-normal">
              GHS-POP
            </span>
          </div>
        </div>
      </div>

      {/* Corridor Priority */}
      <div className="bg-navy-900/90 border border-navy-700 p-3 rounded-xl flex items-center space-x-3">
        <div className="bg-sky-600/20 text-sky-400 p-2 rounded-lg border border-sky-500/30">
          <Navigation className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-medium text-slate-400">Focus Corridor</div>
          <div className="text-xl font-bold text-white flex items-center space-x-1">
            <span>NH-44 Highway</span>
            <span className="text-[10px] bg-sky-950 text-sky-300 border border-sky-600/40 px-1.5 py-0.5 rounded font-normal">
              Active
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
