"use client";

import { useState } from 'react';
import { RotateCcw, Clock, CloudRain } from 'lucide-react';

export function TimelineSlider() {
  const [activeWindow, setActiveWindow] = useState('24h');

  return (
    <div className="bg-navy-900 border-t border-navy-700 px-4 py-2 text-xs flex items-center justify-between text-slate-200">
      {/* Reset Control */}
      <div className="flex items-center space-x-2">
        <button
          onClick={() => setActiveWindow('24h')}
          className="p-1.5 bg-navy-800 hover:bg-navy-700 text-slate-300 rounded-md flex items-center space-x-1 font-mono text-[11px]"
          title="Reset Timeline"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset 24h Window</span>
        </button>
      </div>

      {/* Accumulation Window */}
      <div className="flex items-center space-x-1 bg-navy-800 p-1 rounded-lg border border-navy-700">
        <div className="flex items-center space-x-1 text-slate-300 px-2 font-mono text-[11px]">
          <Clock className="w-3.5 h-3.5 text-blue-400" />
          <span>24h Precipitation Accumulation:</span>
        </div>
        <button
          className="px-3 py-1 rounded text-xs font-mono bg-blue-600 text-white font-bold"
        >
          24h (Derived Proxy)
        </button>
      </div>

      {/* Dynamic Hazard Status Badge */}
      <div className="flex items-center space-x-2 bg-amber-950/60 border border-amber-600/40 px-3 py-1 rounded-md text-amber-300 font-medium">
        <CloudRain className="w-3.5 h-3.5 text-amber-400" />
        <span>Dynamic Hazard: Scenario / Proxy Mode</span>
      </div>
    </div>
  );
}
