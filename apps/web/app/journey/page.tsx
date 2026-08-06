"use client";

import React, { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Navigation, MapPin, Calendar, Car, AlertTriangle, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';

export default function JourneyPage() {
  const [source, setSource] = useState('Jammu');
  const [destination, setDestination] = useState('Srinagar');
  const [departureTime, setDepartureTime] = useState('Depart Now');
  const [vehicleType, setVehicleType] = useState('LMV (Car / SUV)');
  const [hasAnalyzed, setHasAnalyzed] = useState(true);

  return (
    <div className="flex flex-col min-h-screen bg-navy-950 text-slate-100">
      <Header />
      <main className="flex-1 p-4 max-w-5xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-2 shadow-xl">
          <div className="flex items-center space-x-2">
            <Navigation className="w-5 h-5 text-blue-400" />
            <h1 className="text-xl sm:text-2xl font-black text-white">Plan My Journey — Route Exposure Preview</h1>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed max-w-2xl">
            Evaluate research-based relative landslide exposure along mountain highway corridors before travelling between Jammu & Kashmir towns.
          </p>
        </div>

        {/* Journey Inputs Form */}
        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-4">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider text-slate-300 border-b border-navy-800 pb-2">
            Journey Parameters
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div>
              <label className="block text-slate-400 font-medium mb-1">Origin (Source):</label>
              <select
                value={source}
                onChange={(e) => setSource(e.target.value)}
                className="w-full bg-navy-800 border border-navy-700 rounded-xl p-2.5 font-bold text-white focus:outline-none focus:border-blue-500"
              >
                <option value="Jammu">Jammu City Center</option>
                <option value="Udhampur">Udhampur Town</option>
                <option value="Ramban">Ramban Hub</option>
                <option value="Banihal">Banihal Station</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 font-medium mb-1">Destination:</label>
              <select
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                className="w-full bg-navy-800 border border-navy-700 rounded-xl p-2.5 font-bold text-white focus:outline-none focus:border-blue-500"
              >
                <option value="Srinagar">Srinagar Aerodrome</option>
                <option value="Anantnag">Anantnag Hub</option>
                <option value="Baramulla">Baramulla Town</option>
                <option value="Kulgam">Kulgam Center</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 font-medium mb-1">Departure Window:</label>
              <select
                value={departureTime}
                onChange={(e) => setDepartureTime(e.target.value)}
                className="w-full bg-navy-800 border border-navy-700 rounded-xl p-2.5 font-bold text-white focus:outline-none focus:border-blue-500"
              >
                <option value="Depart Now">Depart Now</option>
                <option value="Depart in 6 Hours">Depart in 6 Hours</option>
                <option value="Depart Tomorrow Morning">Depart Tomorrow Morning</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 font-medium mb-1">Vehicle Category:</label>
              <select
                value={vehicleType}
                onChange={(e) => setVehicleType(e.target.value)}
                className="w-full bg-navy-800 border border-navy-700 rounded-xl p-2.5 font-bold text-white focus:outline-none focus:border-blue-500"
              >
                <option value="LMV (Car / SUV)">LMV (Car / SUV)</option>
                <option value="Heavy Commercial (Truck / Bus)">Heavy Commercial (Truck / Bus)</option>
                <option value="Two-Wheeler / Bike">Two-Wheeler / Bike</option>
              </select>
            </div>
          </div>

          <button
            onClick={() => setHasAnalyzed(true)}
            className="w-full py-2.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-xl flex items-center justify-center space-x-2 transition-colors shadow-lg shadow-blue-900/30"
          >
            <Navigation className="w-4 h-4" />
            <span>Analyze Route Exposure</span>
          </button>
        </div>

        {/* Route Exposure Preview Results */}
        {hasAnalyzed && (
          <div className="space-y-4">
            {/* Primary Advisory Card */}
            <div className="bg-navy-900 border border-amber-500/60 p-5 rounded-2xl space-y-3 shadow-xl">
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-navy-800 pb-3">
                <div>
                  <span className="text-[10px] font-mono text-amber-400 uppercase tracking-wider">
                    Research-Based Route Exposure Comparison
                  </span>
                  <h3 className="text-lg font-black text-white mt-0.5">
                    {source} ➔ {destination} (NH-44 Primary Route)
                  </h3>
                </div>
                <span className="px-3 py-1 bg-amber-950 border border-amber-600/50 text-amber-300 font-bold text-xs rounded-xl font-mono">
                  Moderate to High Relative Risk
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div className="bg-navy-950 p-3 rounded-xl border border-navy-800">
                  <span className="text-slate-400 font-medium">Total Distance:</span>
                  <div className="font-bold text-white text-sm mt-0.5">247 km</div>
                </div>
                <div className="bg-navy-950 p-3 rounded-xl border border-navy-800">
                  <span className="text-slate-400 font-medium">High Susceptibility Segments:</span>
                  <div className="font-bold text-amber-400 text-sm mt-0.5">14.5 km (5.8% of route)</div>
                </div>
                <div className="bg-navy-950 p-3 rounded-xl border border-navy-800">
                  <span className="text-slate-400 font-medium">Identified Hotspot Stretches:</span>
                  <div className="font-bold text-slate-200 text-xs mt-0.5">Panthyal, Ramban, Digdol</div>
                </div>
              </div>

              {/* Safe Language Assessment */}
              <div className="bg-navy-950 p-4 rounded-xl border border-navy-800 space-y-2 text-xs">
                <div className="flex items-center space-x-2 text-blue-300 font-bold">
                  <ShieldCheck className="w-4 h-4 text-blue-400 shrink-0" />
                  <span>Geospatial Risk Assessment Summary:</span>
                </div>
                <p className="text-slate-300 leading-relaxed">
                  Lower relative landslide exposure based on currently available geospatial data for early highway stretches. However, the Ramban–Banihal section contains 14.5 km of steep cut-slopes with elevated static susceptibility.
                </p>
                <div className="pt-2 text-amber-300 font-semibold border-t border-navy-800 flex items-center space-x-2">
                  <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                  <span>Always verify official road and traffic advisories before travelling.</span>
                </div>
              </div>
            </div>

            {/* Alternate Route Comparison */}
            <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-3">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider text-slate-300">
                Candidate Route Comparison
              </h3>

              <div className="space-y-2 text-xs">
                <div className="p-3 bg-navy-950 rounded-xl border border-navy-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div>
                    <div className="font-bold text-white">Route 1: NH-44 Direct (via Ramban & Banihal)</div>
                    <div className="text-slate-400 text-[11px]">Primary 4-lane highway corridor | Distance: 247 km</div>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="text-amber-400 font-bold">14.5 km High Risk</span>
                    <div className="text-[10px] text-slate-400 font-mono">Relative Risk Index: 0.68</div>
                  </div>
                </div>

                <div className="p-3 bg-navy-950 rounded-xl border border-navy-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div>
                    <div className="font-bold text-white">Route 2: Mughal Road (via Rajouri & Shopian)</div>
                    <div className="text-slate-400 text-[11px]">High-altitude mountain pass | Distance: 310 km</div>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="text-emerald-400 font-bold">8.0 km High Risk</span>
                    <div className="text-[10px] text-slate-400 font-mono">Relative Risk Index: 0.42</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
