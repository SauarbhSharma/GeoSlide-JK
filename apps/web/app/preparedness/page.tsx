"use client";

import React from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { ShieldCheck, CheckCircle2, Calendar, FileText } from 'lucide-react';

export default function PreparednessPage() {
  return (
    <div className="flex flex-col min-h-screen bg-navy-950 text-slate-100">
      <Header />
      <main className="flex-1 p-4 max-w-5xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-2 shadow-xl">
          <div className="flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <h1 className="text-xl sm:text-2xl font-black text-white">Pre-Monsoon Preparedness Portal</h1>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed max-w-2xl">
            Pre-monsoon preparedness outlook, drainage clearing priorities, and settlement isolation risk assessment for state disaster management authorities.
          </p>
        </div>

        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-3">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider text-slate-300">
            Pre-Monsoon Checklist & Action Plan
          </h2>
          <ul className="space-y-2 text-xs text-slate-300">
            <li className="flex items-start space-x-2 p-2.5 bg-navy-950 rounded-xl border border-navy-800">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>Inspect culvert drainage and clearing along NH-44 Ramban–Banihal stretch.</span>
            </li>
            <li className="flex items-start space-x-2 p-2.5 bg-navy-950 rounded-xl border border-navy-800">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>Pre-position earthmoving loaders and rescue machinery at Panthyal & Digdol staging areas.</span>
            </li>
            <li className="flex items-start space-x-2 p-2.5 bg-navy-950 rounded-xl border border-navy-800">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>Verify emergency shelter availability in top 5 high-susceptibility districts (Ramban, Doda, Kishtwar, Reasi, Poonch).</span>
            </li>
          </ul>
        </div>
      </main>
    </div>
  );
}
