"use client";

import { useState } from 'react';
import { JK_20_DISTRICTS, District, RISK_COLORS } from '@/lib/constants';
import { MapPin, Navigation, Info, Layers, Maximize2, Compass } from 'lucide-react';

interface MapContainerProps {
  selectedDistrict: string;
  onSelectDistrict: (districtId: string) => void;
  activeLayers: string[];
}

export function MapContainer({ selectedDistrict, onSelectDistrict, activeLayers }: MapContainerProps) {
  const [clickedLocation, setClickedLocation] = useState<{
    lat: number;
    lon: number;
    district: District | null;
  } | null>(null);

  const [basemap, setBasemap] = useState<'standard' | 'satellite' | 'dark'>('dark');

  // Convert lat/lon coordinates to SVG canvas space (bbox approx for J&K)
  // Lon: 73.5 to 76.5 -> X: 50 to 750
  // Lat: 32.0 to 35.0 -> Y: 550 to 50
  const projectCoords = (lon: number, lat: number) => {
    const x = ((lon - 73.5) / (76.5 - 73.5)) * 700 + 50;
    const y = 550 - ((lat - 32.0) / (35.0 - 32.0)) * 500;
    return { x, y };
  };

  const handleDistrictClick = (district: District) => {
    onSelectDistrict(district.id);
    setClickedLocation({
      lat: district.coordinates[1],
      lon: district.coordinates[0],
      district
    });
  };

  const showDistricts = activeLayers.includes('jk_districts') || activeLayers.includes('jk_ut_boundary');
  const showNH44 = activeLayers.includes('nh44_corridor');
  const showRainfall = activeLayers.includes('rainfall_imerg');

  return (
    <div className="relative w-full h-full bg-navy-950 flex flex-col overflow-hidden text-slate-100 select-none">
      {/* Map Header Overlay */}
      <div className="absolute top-3 left-3 z-10 flex items-center space-x-2 bg-navy-900/90 border border-navy-700 backdrop-blur px-3 py-1.5 rounded-lg text-xs">
        <Compass className="w-4 h-4 text-blue-400 animate-spin" style={{ animationDuration: '10s' }} />
        <span className="font-semibold text-white">Full J&K UT Interactive View (EPSG:4326)</span>
        <span className="text-slate-400 font-mono text-[11px]">| 20 Verified Districts</span>
      </div>

      {/* Map Control Buttons */}
      <div className="absolute top-3 right-3 z-10 flex items-center space-x-2">
        <div className="bg-navy-900/90 border border-navy-700 backdrop-blur rounded-lg p-1 flex space-x-1 text-xs">
          <button
            onClick={() => setBasemap('dark')}
            className={`px-2.5 py-1 rounded transition-colors ${
              basemap === 'dark' ? 'bg-blue-600 text-white font-semibold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Dark Command
          </button>
          <button
            onClick={() => setBasemap('standard')}
            className={`px-2.5 py-1 rounded transition-colors ${
              basemap === 'standard' ? 'bg-blue-600 text-white font-semibold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Terrain Topo
          </button>
        </div>
      </div>

      {/* Interactive SVG Canvas */}
      <div className="w-full h-full flex items-center justify-center p-4">
        <svg viewBox="0 0 800 600" className="w-full h-full max-h-[750px] drop-shadow-2xl">
          {/* Background Grid Lines */}
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#334155" strokeWidth="0.5" opacity="0.3" />
            </pattern>
            {/* Insufficient Data Hatch Pattern */}
            <pattern id="hatch" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
              <line x1="0" y1="0" x2="0" y2="8" stroke="#64748b" strokeWidth="2" />
            </pattern>
          </defs>

          <rect width="800" height="600" fill={basemap === 'dark' ? '#090d16' : '#1e293b'} />
          <rect width="800" height="600" fill="url(#grid)" />

          {/* Dissolved J&K Outer Glow / Envelope */}
          <ellipse cx="400" cy="300" rx="320" ry="240" fill="none" stroke="#2563eb" strokeWidth="1" strokeDasharray="4 4" opacity="0.4" />

          {/* NH-44 Focus Corridor (Jammu -> Udhampur -> Ramban -> Srinagar) */}
          {showNH44 && (
            <g>
              <path
                d="M 370 480 Q 420 380, 410 320 T 360 250"
                fill="none"
                stroke="#38bdf8"
                strokeWidth="4"
                strokeDasharray="6 3"
                opacity="0.85"
              />
              <text x="420" y="350" fill="#38bdf8" fontSize="10" fontWeight="bold" fontFamily="sans-serif">
                NH-44 Corridor (Focus Area)
              </text>
            </g>
          )}

          {/* 20 J&K District Interactive Nodes & Polygons */}
          {showDistricts &&
            JK_20_DISTRICTS.map((d) => {
              const { x, y } = projectCoords(d.coordinates[0], d.coordinates[1]);
              const isSelected = selectedDistrict === d.id;
              const color = RISK_COLORS[d.riskLevel];

              return (
                <g key={d.id} className="cursor-pointer group" onClick={() => handleDistrictClick(d)}>
                  {/* District Boundary Area Representation */}
                  <circle
                    cx={x}
                    cy={y}
                    r={isSelected ? 28 : 22}
                    fill={color}
                    fillOpacity={isSelected ? 0.45 : 0.25}
                    stroke={color}
                    strokeWidth={isSelected ? 2.5 : 1}
                    className="transition-all duration-300 group-hover:fill-opacity-50"
                  />

                  {/* Center Node */}
                  <circle
                    cx={x}
                    cy={y}
                    r={isSelected ? 6 : 4}
                    fill={color}
                    stroke="#ffffff"
                    strokeWidth="1.5"
                  />

                  {/* Label */}
                  <text
                    x={x}
                    y={y + 16}
                    textAnchor="middle"
                    fill={isSelected ? '#ffffff' : '#cbd5e1'}
                    fontSize={isSelected ? '11' : '9.5'}
                    fontWeight={isSelected ? 'bold' : 'normal'}
                    className="group-hover:fill-white group-hover:font-semibold transition-all pointer-events-none"
                  >
                    {d.displayName}
                  </text>

                  {/* Risk Badge */}
                  <rect
                    x={x - 22}
                    y={y - 20}
                    width="44"
                    height="12"
                    rx="3"
                    fill="#0f172a"
                    stroke={color}
                    strokeWidth="0.8"
                    opacity="0.9"
                  />
                  <text
                    x={x}
                    y={y - 11}
                    textAnchor="middle"
                    fill={color}
                    fontSize="7.5"
                    fontWeight="bold"
                  >
                    {d.riskLevel}
                  </text>
                </g>
              );
            })}
        </svg>
      </div>

      {/* Map Click Inspection Panel */}
      {clickedLocation && (
        <div className="absolute bottom-16 right-4 z-20 bg-navy-900/95 border border-navy-700 backdrop-blur rounded-xl p-4 w-80 text-xs shadow-2xl space-y-2">
          <div className="flex items-center justify-between border-b border-navy-700 pb-2">
            <div className="flex items-center space-x-2">
              <MapPin className="w-4 h-4 text-blue-400" />
              <span className="font-bold text-white text-sm">
                {clickedLocation.district?.displayName || 'Custom Point'}
              </span>
            </div>
            <button
              onClick={() => setClickedLocation(null)}
              className="text-slate-400 hover:text-white"
            >
              ✕
            </button>
          </div>

          <div className="space-y-1.5 font-mono text-[11px] text-slate-300">
            <div className="flex justify-between">
              <span className="text-slate-400">Coordinates:</span>
              <span>{clickedLocation.lat.toFixed(4)}°N, {clickedLocation.lon.toFixed(4)}°E</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Source Name:</span>
              <span>{clickedLocation.district?.sourceName}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Status:</span>
              <span className="text-emerald-400 font-bold">Included in J&K UT (20/20)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Hazard Class (Demo):</span>
              <span className="font-bold" style={{ color: RISK_COLORS[clickedLocation.district?.riskLevel || 'Low'] }}>
                {clickedLocation.district?.riskLevel}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Rainfall Mode:</span>
              <span className="text-amber-300">Demo Playback</span>
            </div>
          </div>
        </div>
      )}

      {/* Coordinate & Status Footer Bar */}
      <div className="bg-navy-900 border-t border-navy-800 px-4 py-1.5 text-xs flex items-center justify-between text-slate-400 font-mono">
        <div>
          <span>CRS: EPSG:4326 (WGS84)</span>
          <span className="ml-4">Center: 33.7000° N, 75.2000° E</span>
        </div>
        <div>
          <span className="text-blue-400">20 J&K Districts Active</span>
        </div>
      </div>
    </div>
  );
}
