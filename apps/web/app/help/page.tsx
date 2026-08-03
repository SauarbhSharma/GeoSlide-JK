"use client";

import React from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { HelpCircle, Info, ShieldCheck, CheckCircle2 } from 'lucide-react';

export default function HelpPage() {
  return (
    <div className="flex flex-col min-h-screen bg-navy-950 text-slate-100">
      <Header />
      <main className="flex-1 p-4 max-w-5xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-2 shadow-xl">
          <div className="flex items-center space-x-2">
            <HelpCircle className="w-5 h-5 text-blue-400" />
            <h1 className="text-xl sm:text-2xl font-black text-white">Help & User Guidance</h1>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed max-w-2xl">
            Frequently Asked Questions regarding GeoSlide-JK 2.0 landslide susceptibility ratings, travel advisories, and data sources.
          </p>
        </div>

        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-4 text-xs">
          <div className="space-y-1">
            <h3 className="font-bold text-white text-sm">What does GeoSlide-JK measure?</h3>
            <p className="text-slate-300 leading-relaxed">
              GeoSlide-JK measures relative physical slope instability exposure across Jammu & Kashmir using machine-learning models trained on terrain slope, geology, land cover, tectonics, and historical landslide inventories.
            </p>
          </div>

          <div className="space-y-1">
            <h3 className="font-bold text-white text-sm">Is GeoSlide-JK an official road closure warning system?</h3>
            <p className="text-slate-300 leading-relaxed">
              No. GeoSlide-JK is an experimental research decision-support prototype. It does not issue binding legal road closures or mandatory evacuation warnings. Always consult J&K Traffic Police (@JKTrafficPolice) for official road status.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
