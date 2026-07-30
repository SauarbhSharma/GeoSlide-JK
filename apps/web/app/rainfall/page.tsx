"use client";

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { CloudRain, Clock, Database, AlertTriangle, Search, RefreshCw, MapPin } from 'lucide-react';
import { apiUrl } from '@/lib/api';

const PRESET_LOCATIONS = [
  { label: 'Select Example Location...', lat: null, lon: null },
  { label: 'Panthyal NH-44, Ramban', lat: 33.245, lon: 75.241 },
  { label: 'Jammu City Center', lat: 32.726, lon: 74.857 },
  { label: 'Srinagar Aerodrome', lat: 34.083, lon: 74.797 },
  { label: 'Kupwara North Slopes', lat: 34.526, lon: 74.256 },
  { label: 'Kishtwar Chenab Valley', lat: 33.312, lon: 75.768 }
];

export default function RainfallMonitor() {
  const [latInput, setLatInput] = useState('33.2450');
  const [lonInput, setLonInput] = useState('75.2410');
  const [loading, setLoading] = useState(false);
  const [queryResult, setQueryResult] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchRainfallData = async (latStr: string, lonStr: string) => {
    const lat = parseFloat(latStr);
    const lon = parseFloat(lonStr);
    if (isNaN(lat) || isNaN(lon)) {
      setErrorMsg('Please enter valid numeric latitude and longitude coordinates.');
      return;
    }

    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch(apiUrl(`/api/v1/terrain/value?lat=${lat}&lon=${lon}`));
      if (!res.ok) {
        throw new Error(`API returned HTTP ${res.status}`);
      }
      const data = await res.json();
      setQueryResult(data);
    } catch (err: any) {
      console.error('Failed to query rainfall proxy:', err);
      setErrorMsg(err.message || 'Failed to query rainfall proxy raster endpoint.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchRainfallData(latInput, lonInput);
  };

  const handleSelectPreset = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const idx = parseInt(e.target.value);
    if (idx >= 0 && PRESET_LOCATIONS[idx].lat !== null) {
      const loc = PRESET_LOCATIONS[idx];
      const newLat = loc.lat!.toString();
      const newLon = loc.lon!.toString();
      setLatInput(newLat);
      setLonInput(newLon);
      fetchRainfallData(newLat, newLon);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Truthful Scenario / Proxy Notice Banner */}
        <div className="bg-amber-950/90 border border-amber-500/80 text-amber-100 p-4 rounded-xl flex items-center justify-between text-xs shadow-lg">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
            <div>
              <h2 className="font-bold text-sm text-amber-200">24-Hour Rainfall Proxy and Dynamic Hazard Scenario</h2>
              <p className="text-slate-300 mt-0.5">
                The current rainfall accumulation and P90 layers are model-derived scenario/proxy products for research demonstration. They are not live operational rainfall observations.
              </p>
            </div>
          </div>
          <span className="font-mono text-xs bg-amber-900 border border-amber-400/50 px-3 py-1.5 rounded text-amber-200 font-bold shrink-0">
            Scenario / Proxy Mode
          </span>
        </div>

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-600/20 text-blue-400 p-2 rounded-lg border border-blue-500/30">
              <CloudRain className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">24-Hour Rainfall Proxy and Dynamic Hazard Scenario</h1>
              <p className="text-xs text-slate-300 mt-0.5">
                Model-derived 24-hour precipitation accumulation and IMD 90th percentile baseline proxy rasters (100m EPSG:32643).
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2 bg-amber-950/60 border border-amber-600/40 px-3 py-1.5 rounded-lg text-amber-300 text-xs font-semibold">
            <span>24h Scenario Mode Active</span>
          </div>
        </div>

        {/* Interactive Point Query Panel */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-4">
          <div className="flex items-center justify-between border-b border-navy-800 pb-3">
            <div className="flex items-center space-x-2">
              <MapPin className="w-4 h-4 text-blue-400" />
              <span className="font-bold text-white text-sm">Sample Raster Values at Location</span>
            </div>
            <span className="text-xs text-slate-400 font-mono">100m EPSG:32643 Raster Sampling</span>
          </div>

          <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-2">
            <div className="flex-1 flex gap-2">
              <div className="flex-1 relative">
                <span className="absolute left-3 top-2.5 text-xs text-slate-400 font-mono">Lat:</span>
                <input
                  type="text"
                  value={latInput}
                  onChange={(e) => setLatInput(e.target.value)}
                  placeholder="33.2450"
                  className="w-full bg-navy-800 border border-navy-700 rounded-lg pl-12 pr-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
              <div className="flex-1 relative">
                <span className="absolute left-3 top-2.5 text-xs text-slate-400 font-mono">Lon:</span>
                <input
                  type="text"
                  value={lonInput}
                  onChange={(e) => setLonInput(e.target.value)}
                  placeholder="75.2410"
                  className="w-full bg-navy-800 border border-navy-700 rounded-lg pl-12 pr-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="flex gap-2">
              <select
                onChange={handleSelectPreset}
                className="bg-navy-800 border border-navy-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
              >
                {PRESET_LOCATIONS.map((loc, i) => (
                  <option key={i} value={i}>
                    {loc.label}
                  </option>
                ))}
              </select>

              <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-lg flex items-center justify-center space-x-1.5 transition-colors disabled:opacity-50"
              >
                {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                <span>Sample Values</span>
              </button>
            </div>
          </form>

          {errorMsg && (
            <div className="bg-rose-950/60 border border-rose-600/60 p-2.5 rounded-lg text-xs text-rose-200 flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {queryResult && queryResult.success && (
            <div className="bg-navy-950 border border-navy-800 p-4 rounded-lg space-y-3 text-xs">
              <div className="flex items-center justify-between border-b border-navy-800 pb-2">
                <span className="font-bold text-white text-sm">
                  {queryResult.district} ({queryResult.location?.lat}° N, {queryResult.location?.lon}° E)
                </span>
                <span className="font-mono text-emerald-400">Sampled 100m Raster Data</span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="bg-navy-900 p-3 rounded-lg border border-navy-700">
                  <span className="text-slate-400 text-[10px]">24h Rain Proxy</span>
                  <div className="text-lg font-bold text-sky-300 mt-0.5">
                    {queryResult.dynamic_hazard?.rainfall_accum_24h_mm != null ? `${queryResult.dynamic_hazard.rainfall_accum_24h_mm} mm` : 'N/A'}
                  </div>
                </div>

                <div className="bg-navy-900 p-3 rounded-lg border border-navy-700">
                  <span className="text-slate-400 text-[10px]">P90 Baseline Proxy</span>
                  <div className="text-lg font-bold text-emerald-300 mt-0.5">
                    {queryResult.dynamic_hazard?.p90_baseline_mm != null ? `${queryResult.dynamic_hazard.p90_baseline_mm} mm` : 'N/A'}
                  </div>
                </div>

                <div className="bg-navy-900 p-3 rounded-lg border border-navy-700">
                  <span className="text-slate-400 text-[10px]">Dynamic Hazard Index</span>
                  <div className="text-lg font-bold text-amber-400 mt-0.5">
                    {queryResult.dynamic_hazard?.hazard_index != null ? queryResult.dynamic_hazard.hazard_index.toFixed(4) : 'N/A'}
                  </div>
                </div>

                <div className="bg-navy-900 p-3 rounded-lg border border-navy-700">
                  <span className="text-slate-400 text-[10px]">Dynamic Hazard Class</span>
                  <div className="text-lg font-bold text-rose-400 mt-0.5">
                    {queryResult.dynamic_hazard?.hazard_class || 'N/A'}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Data Source Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-blue-400" />
              <span>Rainfall Proxy Raster</span>
            </div>
            <p className="text-slate-300">Statewide 100m 24-hour precipitation accumulation proxy raster (5.0 - 160.0 mm).</p>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-emerald-400" />
              <span>P90 Proxy Baseline</span>
            </div>
            <p className="text-slate-300">Statewide 100m historical IMD 90th percentile baseline proxy raster (30.0 - 95.0 mm).</p>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white flex items-center space-x-1.5 text-sm">
              <Database className="w-4 h-4 text-purple-400" />
              <span>Dynamic Hazard Scenario</span>
            </div>
            <p className="text-slate-300">Statewide 100m dynamic hazard index and 5-class rating scenario rasters.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
