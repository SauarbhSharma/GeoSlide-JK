"use client";

import { Info } from 'lucide-react';

export function ResearchDisclaimer() {
  return (
    <div className="bg-amber-950/30 border border-amber-500/30 text-amber-200/90 px-4 py-2 text-xs flex items-center justify-between rounded-lg mb-3">
      <div className="flex items-center space-x-2">
        <Info className="w-4 h-4 text-amber-400 shrink-0" />
        <span>
          <strong>Research Disclaimer:</strong> GeoSlide-JK is a research decision-support prototype and is not an official government warning system.
        </span>
      </div>
      <span className="text-[10px] uppercase font-mono tracking-wider bg-amber-900/60 px-2 py-0.5 rounded text-amber-300 ml-4 shrink-0">
        Research Prototype
      </span>
    </div>
  );
}
