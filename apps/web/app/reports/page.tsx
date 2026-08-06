"use client";

import React from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { FileText, Download, CheckCircle2 } from 'lucide-react';

export default function ReportsPage() {
  return (
    <div className="flex flex-col min-h-screen bg-navy-950 text-slate-100">
      <Header />
      <main className="flex-1 p-4 max-w-5xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-2 shadow-xl">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-blue-400" />
            <h1 className="text-xl sm:text-2xl font-black text-white">Corridor & District Risk Reports</h1>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed max-w-2xl">
            Downloadable audit reports and corridor vulnerability summaries for official review.
          </p>
        </div>

        <div className="space-y-3">
          <div className="p-4 bg-navy-900 border border-navy-700 rounded-2xl flex items-center justify-between">
            <div>
              <div className="font-bold text-white text-sm">NH-44 Corridor Risk Audit Report 2026</div>
              <div className="text-xs text-slate-400">Chainage-indexed 500m segment exposure summary</div>
            </div>
            <button className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-xl flex items-center space-x-1.5">
              <Download className="w-3.5 h-3.5" />
              <span>Download PDF</span>
            </button>
          </div>

          <div className="p-4 bg-navy-900 border border-navy-700 rounded-2xl flex items-center justify-between">
            <div>
              <div className="font-bold text-white text-sm">Statewide 20-District Vulnerability Report</div>
              <div className="text-xs text-slate-400">DDMA pre-monsoon preparedness and zonal rankings</div>
            </div>
            <button className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-xl flex items-center space-x-1.5">
              <Download className="w-3.5 h-3.5" />
              <span>Download PDF</span>
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
