"use client";

import { useState } from 'react';
import { Layers, MapPin, Search, ChevronLeft, ChevronRight, Eye, EyeOff } from 'lucide-react';
import { JK_20_DISTRICTS, District } from '@/lib/constants';

interface SidebarProps {
  selectedDistrict: string;
  onSelectDistrict: (districtId: string) => void;
  activeLayers: string[];
  onToggleLayer: (layerId: string) => void;
}

export function Sidebar({ selectedDistrict, onSelectDistrict, activeLayers, onToggleLayer }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredDistricts = JK_20_DISTRICTS.filter(d =>
    d.displayName.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.sourceName.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const layersList = [
    { id: 'jk_ut_boundary', name: 'J&K UT Boundary', category: 'Boundaries' },
    { id: 'jk_districts', name: 'District Boundaries (20)', category: 'Boundaries' },
    { id: 'dem_elevation', name: 'Copernicus DEM Elevation', category: 'Terrain' },
    { id: 'slope', name: 'Terrain Slope', category: 'Terrain' },
    { id: 'lithology', name: 'Lithology (1:50k)', category: 'Geology' },
    { id: 'landslides', name: 'NGDR Landslide Inventory', category: 'Landslides' },
    { id: 'rainfall_imerg', name: 'IMERG Satellite Rainfall (Demo)', category: 'Rainfall' },
    { id: 'nh44_corridor', name: 'NH-44 Focus Corridor', category: 'Infrastructure' },
  ];

  if (collapsed) {
    return (
      <div className="bg-navy-900 border-r border-navy-700 w-12 flex flex-col items-center py-4 space-y-4 shrink-0">
        <button
          onClick={() => setCollapsed(false)}
          className="p-2 hover:bg-navy-800 rounded text-slate-300 hover:text-white"
          title="Expand Sidebar"
        >
          <ChevronRight className="w-5 h-5" />
        </button>
        <Layers className="w-5 h-5 text-blue-400" />
        <MapPin className="w-5 h-5 text-emerald-400" />
      </div>
    );
  }

  return (
    <div className="bg-navy-900 border-r border-navy-700 w-80 flex flex-col h-full shrink-0 text-slate-200">
      {/* Header */}
      <div className="p-3 border-b border-navy-700 flex items-center justify-between">
        <div className="flex items-center space-x-2 font-semibold text-sm">
          <Layers className="w-4 h-4 text-blue-400" />
          <span>Layers & Controls</span>
        </div>
        <button
          onClick={() => setCollapsed(true)}
          className="p-1 hover:bg-navy-800 rounded text-slate-400 hover:text-white"
          title="Collapse Sidebar"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
      </div>

      <div className="p-3 space-y-4 overflow-y-auto flex-1">
        {/* District Selector & Search */}
        <div>
          <label className="text-xs font-medium text-slate-400 block mb-1.5">Select J&K District (20)</label>
          <div className="relative mb-2">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search district..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-navy-800 border border-navy-700 rounded-md pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>
          <select
            value={selectedDistrict}
            onChange={(e) => onSelectDistrict(e.target.value)}
            className="w-full bg-navy-800 border border-navy-700 rounded-md px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="all">All 20 Districts (Statewide J&K)</option>
            {filteredDistricts.map((d) => (
              <option key={d.id} value={d.id}>
                {d.displayName} ({d.riskLevel} Risk)
              </option>
            ))}
          </select>
        </div>

        {/* Layer Controls */}
        <div>
          <label className="text-xs font-medium text-slate-400 block mb-2">Active Map Layers</label>
          <div className="space-y-1.5">
            {layersList.map((layer) => {
              const isVisible = activeLayers.includes(layer.id);
              return (
                <div
                  key={layer.id}
                  onClick={() => onToggleLayer(layer.id)}
                  className={`flex items-center justify-between p-2 rounded-md border text-xs cursor-pointer transition-all ${
                    isVisible
                      ? 'bg-blue-950/40 border-blue-600/50 text-white'
                      : 'bg-navy-800/40 border-navy-700 text-slate-400 hover:bg-navy-800'
                  }`}
                >
                  <span className="font-medium truncate pr-2">{layer.name}</span>
                  {isVisible ? (
                    <Eye className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                  ) : (
                    <EyeOff className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Risk Palette Legend */}
        <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-md">
          <label className="text-xs font-medium text-slate-300 block mb-2">Risk Scale & Legend</label>
          <div className="space-y-1.5 text-xs">
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
                <span>Low</span>
              </span>
              <span className="text-slate-500">Baseline Slope</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-amber-500"></span>
                <span>Moderate</span>
              </span>
              <span className="text-slate-500">Elevated Trigger</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-orange-500"></span>
                <span>High</span>
              </span>
              <span className="text-slate-500">Active Monitoring</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-red-500"></span>
                <span>Very High</span>
              </span>
              <span className="text-slate-500">High Susceptibility</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-rose-950 border border-rose-600"></span>
                <span>Critical</span>
              </span>
              <span className="text-slate-500">Ramban / NH-44</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-slate-500 border border-dashed border-slate-300"></span>
                <span>Insufficient Data</span>
              </span>
              <span className="text-slate-500">Masked Area</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
