"use client";

import React, { useEffect } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { TrustStatusComponent } from '@/components/common/TrustStatusComponent';
import { useUserRole } from '@/lib/RoleContext';
import { ShieldAlert, Info, MapPin, Layers } from 'lucide-react';

export default function CorridorMonitorPage() {
  const { setRole } = useUserRole();

  // Enforce Highway Operations role context
  useEffect(() => {
    setRole('highway');
  }, [setRole]);

  return (
    <div className="min-h-screen bg-navy-950 text-slate-100 flex flex-col font-sans">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 space-y-4">
        <ResearchDisclaimer />

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full bg-amber-950 border border-amber-600/50 text-amber-300 text-[11px] font-mono">
                Highway Operations Screening Shell (NHAI)
              </span>
              <TrustStatusComponent compact />
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-white tracking-tight">
              NH-44 Jammu–Srinagar Highway Screening
            </h1>
            <p className="text-xs text-slate-300 max-w-3xl leading-relaxed">
              Screening shell for the NH-44 mountain highway corridor across Udhampur, Ramban, and Banihal sectors.
            </p>
          </div>

          <div className="flex items-center space-x-2 shrink-0">
            <div className="bg-navy-950 p-2.5 px-3 rounded-xl border border-navy-800 text-xs font-mono">
              <span className="text-slate-400 block text-[10px]">CORRIDOR STATUS</span>
              <span className="text-amber-400 font-bold">Verified NH-44 geometry under validation</span>
            </div>
          </div>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 text-xs font-medium">Target Highway Corridor</span>
            <div className="text-lg font-bold text-white font-mono">
              NH-44 Jammu–Srinagar
            </div>
            <span className="text-[10px] text-slate-400 font-mono">Arterial National Highway</span>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 text-xs font-medium">Target Mountain Sector</span>
            <div className="text-sm font-bold text-amber-300 font-mono mt-1">
              Udhampur → Ramban → Banihal
            </div>
            <span className="text-[10px] text-slate-400 font-mono">Excludes NH-244 Sinthan Pass</span>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 text-xs font-medium">Geometric Status</span>
            <div className="text-sm font-bold text-emerald-400 font-mono mt-1">
              Under Validation
            </div>
            <span className="text-[10px] text-slate-400 font-mono">Reset Gate V2-3A</span>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 text-xs font-medium">Exposure Scoring Status</span>
            <div className="text-xs font-bold text-slate-400 font-mono mt-1">
              Not Calculated
            </div>
            <span className="text-[10px] text-slate-400 font-mono">Pending V2-3B Target</span>
          </div>
        </div>

        {/* Validation Status Banner */}
        <div className="bg-navy-900 border border-navy-700 p-6 rounded-2xl space-y-4 shadow-xl text-center">
          <div className="inline-flex items-center justify-center p-3 bg-amber-950/80 border border-amber-600/40 rounded-full text-amber-400 mb-2">
            <Info className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-white">
            Verified NH-44 geometry under validation
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mx-auto leading-relaxed">
            The authoritative NH-44 Jammu–Srinagar highway route (Udhampur–Ramban–Banihal) is currently undergoing source identity audit and topological verification. Segmentation and exposure metrics are suppressed during the Reset Gate.
          </p>
          <div className="pt-2 text-[11px] font-mono text-slate-400">
            GeoSlide-JK 2.0 Checkpoint V2-3A Reset Gate — Authoritative Highway Source Audit
          </div>
        </div>
      </main>
    </div>
  );
}
