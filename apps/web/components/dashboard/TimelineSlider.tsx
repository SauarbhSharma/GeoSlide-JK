"use client";

import { useState } from 'react';
import { Play, Pause, RotateCcw, Clock, CloudRain } from 'lucide-react';

export function TimelineSlider() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeWindow, setActiveWindow] = useState('24h');

  const windows = ['30min', '1h', '3h', '6h', '12h', '24h', '48h', '72h'];

  return (
    <div className="bg-navy-900 border-t border-navy-700 px-4 py-2 text-xs flex items-center justify-between text-slate-200">
      {/* Play Controls */}
      <div className="flex items-center space-x-2">
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="p-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-md flex items-center space-x-1 font-medium transition-colors"
        >
          {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
          <span>{isPlaying ? 'Pause' : 'Play Demo'}</span>
        </button>
        <button
          onClick={() => setActiveWindow('24h')}
          className="p-1.5 bg-navy-800 hover:bg-navy-700 text-slate-300 rounded-md"
          title="Reset Timeline"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Accumulation Windows */}
      <div className="flex items-center space-x-1 bg-navy-800 p-1 rounded-lg border border-navy-700">
        <div className="flex items-center space-x-1 text-slate-400 px-2 font-mono">
          <Clock className="w-3.5 h-3.5 text-blue-400" />
          <span>IMERG Window:</span>
        </div>
        {windows.map((w) => (
          <button
            key={w}
            onClick={() => setActiveWindow(w)}
            className={`px-2.5 py-1 rounded text-xs font-mono transition-colors ${
              activeWindow === w
                ? 'bg-blue-600 text-white font-bold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-navy-700'
            }`}
          >
            {w}
          </button>
        ))}
      </div>

      {/* Demo Playback Indicator */}
      <div className="flex items-center space-x-2 bg-blue-950/60 border border-blue-600/40 px-3 py-1 rounded-md text-blue-300">
        <CloudRain className="w-3.5 h-3.5" />
        <span className="font-semibold">Demo Playback (July 2026 Sample)</span>
      </div>
    </div>
  );
}
