"use client";

import { useState } from 'react';
import { Layers, MapPin, Search, ChevronLeft, ChevronRight, Eye, EyeOff, Lock } from 'lucide-react';
import { JK_20_DISTRICTS } from '@/lib/constants';
import { MASTER_LAYER_REGISTRY } from '@/lib/layerRegistry';

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
      <div className="p-3 border-b border-navy-700 flex items-center justify-between">
        <div className="flex items-center space-x-2 font-bold text-xs text-white">
          <Layers className="w-4 h-4 text-blue-400" />
          <span>Layer Controls & Search</span>
        </div>
        <button
          onClick={() => setCollapsed(true)}
          className="p-1 hover:bg-navy-800 rounded text-slate-400 hover:text-white"
          title="Collapse Sidebar"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
      </div>

      <div className="p-3 space-y-4 overflow-y-auto flex-1 text-xs">
        {/* District Selector & Search */}
        <div>
          <label className="text-xs font-semibold text-slate-300 block mb-1.5">Select J&K District (20)</label>
          <div className="relative mb-2">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search district..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-navy-800 border border-navy-700 rounded-md pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-400 focus:outline-none focus:border-blue-500"
            />
          </div>
          <select
            value={selectedDistrict}
            onChange={(e) => onSelectDistrict(e.target.value)}
            className="w-full bg-navy-800 border border-navy-700 rounded-md px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-medium"
          >
            <option value="all">All 20 Districts (Statewide J&K)</option>
            {filteredDistricts.map((d) => (
              <option key={d.id} value={d.id}>
                {d.displayName} ({d.riskLevel} - Demo)
              </option>
            ))}
          </select>
        </div>

        {/* Master Layer Registry List */}
        <div>
          <label className="text-xs font-semibold text-slate-300 block mb-2">Phase 2 Geospatial Layers</label>
          <div className="space-y-1.5">
            {MASTER_LAYER_REGISTRY.map((layer) => {
              const isVisible = activeLayers.includes(layer.id) || layer.defaultVisibility;
              const isAvailable = layer.availability === "Available";
              return (
                <div
                  key={layer.id}
                  onClick={() => onToggleLayer(layer.id)}
                  className={`flex items-center justify-between p-2 rounded-md border text-xs transition-all ${
                    isVisible && isAvailable
                      ? 'bg-blue-950/50 border-blue-600/60 text-white cursor-pointer'
                      : !isAvailable
                      ? 'bg-navy-950/60 border-navy-800 text-slate-400 opacity-80 cursor-not-allowed'
                      : 'bg-navy-800/40 border-navy-700 text-slate-300 hover:bg-navy-800 cursor-pointer'
                  }`}
                >
                  <div className="flex flex-col pr-2">
                    <span className="font-medium">{layer.displayName}</span>
                    <span className={`text-[9.5px] font-mono flex items-center space-x-1 ${
                      isAvailable ? 'text-emerald-400' : 'text-amber-400'
                    }`}>
                      {!isAvailable && <Lock className="w-2.5 h-2.5 inline mr-0.5" />}
                      <span>{layer.availability} • {layer.processingPhase}</span>
                    </span>
                  </div>
                  {isVisible && isAvailable ? (
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
        <div className="bg-navy-800/80 border border-navy-700 p-3 rounded-md">
          <label className="text-xs font-bold text-slate-200 block mb-2">Risk Scale & Legend (Demo)</label>
          <div className="space-y-1.5 text-xs font-medium">
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
                <span>Low</span>
              </span>
              <span className="text-slate-400 text-[11px]">Demo Priority</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-amber-500"></span>
                <span>Moderate</span>
              </span>
              <span className="text-slate-400 text-[11px]">Demo Priority</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-orange-500"></span>
                <span>High</span>
              </span>
              <span className="text-slate-400 text-[11px]">Demo Priority</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-red-500"></span>
                <span>Very High</span>
              </span>
              <span className="text-slate-400 text-[11px]">Demo Priority</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-rose-950 border border-rose-600"></span>
                <span>Critical</span>
              </span>
              <span className="text-slate-400 text-[11px]">Demo Priority</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-slate-500 border border-dashed border-slate-300"></span>
                <span>Insufficient Data</span>
              </span>
              <span className="text-slate-400 text-[11px]">Masked Zone</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
