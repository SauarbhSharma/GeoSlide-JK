"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { MapContainer } from '@/components/map/MapContainer';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Sliders, Search, Maximize2, Layers, Compass, Eye, Filter } from 'lucide-react';
import { JK_20_DISTRICTS } from '@/lib/constants';

export default function InteractiveRiskExplorer() {
  const [selectedDistrict, setSelectedDistrict] = useState('all');
  const [opacity, setOpacity] = useState(80);
  const [activeLayers, setActiveLayers] = useState([
    'jk_districts',
    'jk_ut_boundary',
    'nh44_corridor',
    'dem_elevation',
    'slope',
    'landslides'
  ]);

  const handleToggleLayer = (layerId: string) => {
    setActiveLayers((prev) =>
      prev.includes(layerId) ? prev.filter((id) => id !== layerId) : [...prev, layerId]
    );
  };

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex flex-1 overflow-hidden">
        {/* Left Filter & Controls Panel */}
        <div className="w-80 bg-navy-900 border-r border-navy-700 p-4 flex flex-col space-y-4 overflow-y-auto shrink-0 text-xs">
          <div className="flex items-center space-x-2 border-b border-navy-700 pb-2">
            <Sliders className="w-4 h-4 text-blue-400" />
            <span className="font-bold text-white text-sm">Interactive Risk Controls</span>
          </div>

          <ResearchDisclaimer />

          {/* Search Bar */}
          <div>
            <label className="text-xs font-medium text-slate-400 block mb-1">Search Location / Coordinates</label>
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder="e.g. Ramban, Panthyal, 33.24, 75.24"
                className="w-full bg-navy-800 border border-navy-700 rounded-md pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          {/* District Selector */}
          <div>
            <label className="text-xs font-medium text-slate-400 block mb-1">Filter District (20)</label>
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="w-full bg-navy-800 border border-navy-700 rounded-md px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
            >
              <option value="all">All 20 J&K Districts</option>
              {JK_20_DISTRICTS.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.displayName}
                </option>
              ))}
            </select>
          </div>

          {/* Opacity Slider */}
          <div className="bg-navy-800/60 p-3 rounded-lg border border-navy-700 space-y-2">
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-300 font-medium">Layer Opacity</span>
              <span className="font-mono text-blue-400">{opacity}%</span>
            </div>
            <input
              type="range"
              min="10"
              max="100"
              value={opacity}
              onChange={(e) => setOpacity(Number(e.target.value))}
              className="w-full h-1.5 bg-navy-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
          </div>

          {/* Layer Selection */}
          <div>
            <label className="text-xs font-medium text-slate-400 block mb-2">Toggle Raster & Vector Layers</label>
            <div className="space-y-1.5">
              {[
                { id: 'jk_districts', name: 'District Vector Boundaries' },
                { id: 'nh44_corridor', name: 'NH-44 Corridor Overlay' },
                { id: 'dem_elevation', name: 'Copernicus DEM Elevation' },
                { id: 'slope', name: 'Slope (Degrees)' },
                { id: 'landslides', name: 'NGDR Historical Landslides' },
                { id: 'rainfall_imerg', name: 'IMERG Satellite Rainfall (Demo)' },
              ].map((layer) => {
                const isVisible = activeLayers.includes(layer.id);
                return (
                  <button
                    key={layer.id}
                    onClick={() => handleToggleLayer(layer.id)}
                    className={`w-full text-left p-2 rounded-md border text-xs flex items-center justify-between transition-colors ${
                      isVisible
                        ? 'bg-blue-950/40 border-blue-600/50 text-white'
                        : 'bg-navy-800/40 border-navy-700 text-slate-400 hover:bg-navy-800'
                    }`}
                  >
                    <span>{layer.name}</span>
                    <Eye className={`w-3.5 h-3.5 ${isVisible ? 'text-blue-400' : 'text-slate-500'}`} />
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Center Canvas */}
        <div className="flex-1 relative overflow-hidden flex flex-col">
          <MapContainer
            selectedDistrict={selectedDistrict}
            onSelectDistrict={setSelectedDistrict}
            activeLayers={activeLayers}
          />
        </div>
      </div>
    </div>
  );
}
