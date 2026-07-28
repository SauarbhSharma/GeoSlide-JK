"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Search, MapPin, Navigation, ShieldCheck, Printer, Share2, AlertTriangle } from 'lucide-react';
import { JK_20_DISTRICTS } from '@/lib/constants';

export default function LocationRiskCheck() {
  const [query, setQuery] = useState('Panthyal, Ramban');
  const [activeLocation, setActiveLocation] = useState({
    name: 'Panthyal, Ramban District',
    coordinates: '33.2450° N, 75.2410° E',
    district: 'Ramban',
    hazardLevel: 'Critical',
    confidence: 'High',
    rainfallTrigger: 'Elevated (90th Percentile)',
    terrainSlope: '34.2° (Steep Mountain Slope)',
    nearbyHighway: 'NH-44 Corridor (0.2 km distance)'
  });

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-5xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Search Panel */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
          <h1 className="text-xl font-bold text-white flex items-center space-x-2">
            <MapPin className="w-5 h-5 text-blue-400" />
            <span>Location Landslide Risk Check & Advisory</span>
          </h1>
          <p className="text-xs text-slate-400">
            Search town, highway section, or enter precise coordinates (Lat/Lon) across Jammu and Kashmir.
          </p>

          <div className="flex flex-col sm:flex-row gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search village, town, highway segment or lat/lon..."
                className="w-full bg-navy-800 border border-navy-700 rounded-lg pl-9 pr-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
              />
            </div>
            <button className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-lg flex items-center justify-center space-x-1.5 transition-colors">
              <Navigation className="w-4 h-4" />
              <span>Use Current Location</span>
            </button>
          </div>
        </div>

        {/* Location Advisory Output Card */}
        <div className="bg-navy-900 border border-navy-700 p-5 rounded-xl space-y-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-navy-800 pb-4 gap-3">
            <div>
              <div className="text-xs text-slate-400 font-mono">Location Advisory Result</div>
              <h2 className="text-2xl font-black text-white mt-0.5">{activeLocation.name}</h2>
              <div className="text-xs text-slate-400 mt-1 font-mono">{activeLocation.coordinates}</div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="bg-rose-950 border border-rose-600 text-rose-200 px-4 py-2 rounded-xl text-center">
                <div className="text-[10px] uppercase font-mono text-rose-300">Hazard Level (Demo)</div>
                <div className="text-lg font-black">{activeLocation.hazardLevel}</div>
              </div>

              <div className="bg-emerald-950 border border-emerald-600 text-emerald-300 px-4 py-2 rounded-xl text-center">
                <div className="text-[10px] uppercase font-mono text-emerald-400">Data Confidence</div>
                <div className="text-lg font-black">{activeLocation.confidence}</div>
              </div>
            </div>
          </div>

          {/* Environmental Factors Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
              <span className="text-slate-400 font-medium">Rainfall Trigger State:</span>
              <div className="font-bold text-amber-300">{activeLocation.rainfallTrigger}</div>
              <span className="text-[10px] text-slate-400 font-mono">Demo Playback Mode</span>
            </div>

            <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
              <span className="text-slate-400 font-medium">Terrain Slope Gradient:</span>
              <div className="font-bold text-white">{activeLocation.terrainSlope}</div>
              <span className="text-[10px] text-slate-400 font-mono">Copernicus DEM Derived</span>
            </div>

            <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
              <span className="text-slate-400 font-medium">Infrastructure Exposure:</span>
              <div className="font-bold text-sky-300">{activeLocation.nearbyHighway}</div>
              <span className="text-[10px] text-slate-400 font-mono">High Priority Corridor</span>
            </div>
          </div>

          {/* Safety Precautions Box */}
          <div className="bg-amber-950/40 border border-amber-500/40 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-amber-300 flex items-center space-x-1.5 text-sm">
              <AlertTriangle className="w-4 h-4" />
              <span>Recommended Research Safety Precautions</span>
            </div>
            <ul className="list-disc list-inside space-y-1 text-slate-300">
              <li>Exercise caution along steep road cuts during persistent rain.</li>
              <li>Avoid stopping near vulnerable rockfall zones along the NH-44 highway.</li>
              <li>Monitor local meteorological bulletins for updated precipitation triggers.</li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-between pt-2 border-t border-navy-800">
            <span className="text-[11px] text-slate-400 font-mono">Report Ref: ADVISORY-2026-JK-0042</span>
            <div className="flex items-center space-x-2">
              <button className="flex items-center space-x-1.5 bg-navy-800 hover:bg-navy-700 text-white text-xs px-3 py-1.5 rounded-lg border border-navy-700">
                <Printer className="w-3.5 h-3.5" />
                <span>Print Advisory</span>
              </button>
              <button className="flex items-center space-x-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs px-3 py-1.5 rounded-lg font-medium">
                <Share2 className="w-3.5 h-3.5" />
                <span>Share Link</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
