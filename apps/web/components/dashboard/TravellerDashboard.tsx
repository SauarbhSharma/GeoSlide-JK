"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { Navigation, MapPin, ShieldAlert, ArrowRight, CheckCircle2, AlertTriangle, Info, HelpCircle } from 'lucide-react';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { TrustStatusComponent } from '@/components/common/TrustStatusComponent';
import { ExecutiveDemoGuide } from '@/components/common/ExecutiveDemoGuide';

export function TravellerDashboard() {
  const [selectedDistrict, setSelectedDistrict] = useState('ramban');
  const [activeLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44',
    'susceptibility_class'
  ]);

  return (
    <div className="flex-1 flex flex-col overflow-y-auto p-3 sm:p-4 max-w-7xl mx-auto w-full space-y-4">
      <ResearchDisclaimer />

      {/* Main Landing Banner — Product Value Statement */}
      <div className="bg-navy-900 border border-navy-700 p-5 sm:p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="space-y-2">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-950 border border-emerald-600/50 text-emerald-300 text-[11px] font-mono">
              Traveller & Resident Mode
            </span>
            <TrustStatusComponent compact />
          </div>
          <h1 className="text-xl sm:text-2xl md:text-3xl font-black text-white tracking-tight">
            Understand Landslide Exposure for Your Location or Journey
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
            GeoSlide-JK combines terrain, geology, historical landslides and rainfall-scenario information to support screening, preparedness and inspection decisions across Jammu and Kashmir.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <Link
            href="/location-check"
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 transition-colors shadow-lg shadow-blue-900/30"
          >
            <MapPin className="w-4 h-4" />
            <span>Check My Area</span>
          </Link>
          <Link
            href="/journey"
            className="px-4 py-2.5 bg-navy-800 hover:bg-navy-700 text-slate-200 border border-navy-700 text-xs font-bold rounded-xl flex items-center space-x-2 transition-colors"
          >
            <Navigation className="w-4 h-4 text-blue-400" />
            <span>Plan Journey Preview</span>
          </Link>
        </div>
      </div>

      {/* Outcome Card — "What this platform helps you do" */}
      <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-2">
        <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
          What this platform helps you do:
        </h2>
        <ul className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2 text-xs text-slate-300">
          <li className="p-2.5 bg-navy-950 rounded-xl border border-navy-800 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span>Check relative slope susceptibility at your specific location.</span>
          </li>
          <li className="p-2.5 bg-navy-950 rounded-xl border border-navy-800 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span>Understand research route-exposure scenarios along mountain highways.</span>
          </li>
          <li className="p-2.5 bg-navy-950 rounded-xl border border-navy-800 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span>View practical non-operational travel & safety precautions.</span>
          </li>
          <li className="p-2.5 bg-navy-950 rounded-xl border border-navy-800 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span>Identify where official verification is required before travel.</span>
          </li>
        </ul>
      </div>

      {/* Quick Action Grid & Research Scenario */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Research Scenario Card */}
        <div className="bg-navy-900 border border-amber-500/50 p-4 rounded-2xl space-y-3 md:col-span-2 shadow-lg">
          <div className="flex items-center justify-between border-b border-navy-800 pb-2">
            <div className="flex items-center space-x-2 text-amber-300 font-bold text-sm">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              <span>Research Scenario — NH-44 Ramban Stretch</span>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-950 text-amber-200 border border-amber-600/40">
              Research Scenario Only
            </span>
          </div>

          <div className="space-y-2 text-xs">
            <div className="text-white font-bold text-sm">
              Elevated Relative Slope Exposure (Panthyal & Ramban Cut-Slopes)
            </div>
            <p className="text-slate-300 leading-relaxed">
              Terrain models indicate higher relative slope susceptibility around Panthyal, Ramban, and Digdol cut-slopes under assumed 24h rainfall proxy scenarios.
            </p>
          </div>

          {/* Plain Language Precautions */}
          <div className="bg-navy-950 p-3 rounded-xl border border-navy-800 space-y-2 text-xs">
            <span className="font-bold text-slate-200 block text-[11px] uppercase tracking-wider">
              Suggested General Precautions:
            </span>
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-slate-300 font-medium">
              <li className="flex items-center space-x-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Avoid stopping near steep un-engineered slope cuts.</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Verify official traffic advisories (@JKTrafficPolice).</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Exercise heightened caution during intense rainfall.</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Follow instructions issued by local authorities.</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Understand Susceptibility Tiers Card */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-3 flex flex-col justify-between shadow-lg">
          <div className="space-y-2">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <ShieldAlert className="w-4 h-4 text-blue-400" />
              <span>Understanding Susceptibility Tiers</span>
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              GeoSlide-JK classifies slope susceptibility into 5 relative tiers based on terrain slope, geology, drainage, and rainfall proxy scenarios.
            </p>

            <div className="space-y-1.5 pt-1 text-[11px] font-medium">
              <div className="flex items-center justify-between p-1.5 rounded bg-emerald-950/60 border border-emerald-600/40 text-emerald-200">
                <span>Green / Yellow: Baseline Relative Exposure</span>
                <span className="font-mono text-[10px]">Normal Baseline</span>
              </div>
              <div className="flex items-center justify-between p-1.5 rounded bg-amber-950/60 border border-amber-600/40 text-amber-200">
                <span>Orange: Elevated Relative Exposure</span>
                <span className="font-mono text-[10px]">Caution Required</span>
              </div>
              <div className="flex items-center justify-between p-1.5 rounded bg-rose-950/60 border border-rose-600/40 text-rose-200">
                <span>Red: Very High Exposure Scenario</span>
                <span className="font-mono text-[10px]">Verify Advisories</span>
              </div>
            </div>
          </div>

          <Link
            href="/advisories"
            className="w-full py-2 px-3 bg-navy-800 hover:bg-navy-750 text-blue-400 text-xs font-semibold rounded-xl flex items-center justify-center space-x-1 border border-navy-700 transition-colors"
          >
            <span>View Full Advisory Center</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Interactive Map View with Visible Susceptibility Classes */}
      <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-sm font-bold text-white">5-Class Susceptibility Overlay Map</h2>
            <p className="text-xs text-slate-400">High-contrast 5-class susceptibility layer overlaid on basemap.</p>
          </div>
          <Link
            href="/location-check"
            className="text-xs text-blue-400 hover:text-blue-300 font-semibold flex items-center space-x-1"
          >
            <span>Open Full Screen Checker</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="h-[450px] rounded-xl overflow-hidden border border-navy-800 relative">
          <MapContainer
            selectedDistrict={selectedDistrict}
            onSelectDistrict={setSelectedDistrict}
            activeLayers={activeLayers}
          />
        </div>
      </div>

      <ExecutiveDemoGuide />
    </div>
  );
}
