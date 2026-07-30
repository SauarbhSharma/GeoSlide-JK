"use client";

import { useState, useEffect } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Search, MapPin, Navigation, AlertTriangle, RefreshCw, CheckCircle2 } from 'lucide-react';

interface LocationResult {
  inside_study_area: boolean;
  code?: string;
  latitude?: number;
  longitude?: number;
  district?: string;
  elevation_m?: number;
  slope_deg?: number;
  susceptibility_probability?: number;
  susceptibility_class?: number;
  susceptibility_label?: string;
  rainfall_accum_24h_mm?: number;
  imd_p90_baseline_mm?: number;
  rainfall_anomaly_ratio?: number;
  dynamic_hazard_index?: number;
  dynamic_hazard_class?: number;
  dynamic_hazard_label?: string;
  distance_to_road_m?: number;
  distance_to_nh44_m?: number;
  data_confidence?: string;
  data_limitations?: string[];
}

const PRESET_LOCATIONS = [
  { label: 'Select Example Location...', lat: null, lon: null },
  { label: 'Panthyal NH-44, Ramban', lat: 33.245, lon: 75.241 },
  { label: 'Jammu City Center', lat: 32.726, lon: 74.857 },
  { label: 'Srinagar Aerodrome', lat: 34.083, lon: 74.797 },
  { label: 'Kupwara North Slopes', lat: 34.526, lon: 74.256 },
  { label: 'Kishtwar Chenab Valley', lat: 33.312, lon: 75.768 }
];

export default function LocationRiskCheck() {
  const [latInput, setLatInput] = useState('33.2450');
  const [lonInput, setLonInput] = useState('75.2410');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<LocationResult | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchLocationRisk = async (latStr: string, lonStr: string) => {
    const lat = parseFloat(latStr);
    const lon = parseFloat(lonStr);
    if (isNaN(lat) || isNaN(lon)) {
      setErrorMsg('Please enter valid numeric latitude and longitude coordinates.');
      return;
    }

    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch(`/api/v1/location-check?lat=${lat}&lon=${lon}`);
      if (!res.ok) {
        throw new Error(`API returned HTTP ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      console.error('Failed to fetch location risk check:', err);
      setErrorMsg(err.message || 'Failed to query live location risk check API.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLocationRisk(latInput, lonInput);
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchLocationRisk(latInput, lonInput);
  };

  const handleSelectPreset = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const idx = parseInt(e.target.value);
    if (idx >= 0 && PRESET_LOCATIONS[idx].lat !== null) {
      const loc = PRESET_LOCATIONS[idx];
      const newLat = loc.lat!.toString();
      const newLon = loc.lon!.toString();
      setLatInput(newLat);
      setLonInput(newLon);
      fetchLocationRisk(newLat, newLon);
    }
  };

  const handleGeolocate = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const newLat = pos.coords.latitude.toFixed(4);
          const newLon = pos.coords.longitude.toFixed(4);
          setLatInput(newLat);
          setLonInput(newLon);
          fetchLocationRisk(newLat, newLon);
        },
        () => {
          setErrorMsg('Browser location access denied or unavailable. Please enter coordinates manually.');
        }
      );
    } else {
      setErrorMsg('Geolocation is not supported by your browser.');
    }
  };

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-5xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Search Panel */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-bold text-white flex items-center space-x-2">
              <MapPin className="w-5 h-5 text-blue-400" />
              <span>Location Risk Check — Point Query Engine</span>
            </h1>
            <span className="text-xs font-mono bg-blue-950 text-blue-300 border border-blue-600/40 px-2.5 py-1 rounded-md">
              Live API Mode
            </span>
          </div>
          <p className="text-xs text-slate-300">
            Query real-time 100m raster values for static susceptibility (XGBoost) and dynamic hazard (24h rainfall proxy scenario) at any location in J&K UT.
          </p>

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
                <span>Query</span>
              </button>

              <button
                type="button"
                onClick={handleGeolocate}
                className="bg-navy-800 hover:bg-navy-700 text-white text-xs font-semibold px-3 py-2 rounded-lg flex items-center justify-center border border-navy-700 transition-colors"
                title="Use current GPS location"
              >
                <Navigation className="w-4 h-4" />
              </button>
            </div>
          </form>

          {errorMsg && (
            <div className="bg-rose-950/60 border border-rose-600/60 p-2.5 rounded-lg text-xs text-rose-200 flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}
        </div>

        {/* Location Advisory Output Card */}
        {result && (
          <div className="bg-navy-900 border border-navy-700 p-5 rounded-xl space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-navy-800 pb-4 gap-3">
              <div>
                <div className="text-xs text-amber-400 font-mono font-semibold uppercase tracking-wider">
                  Research advisory scenario — not an official warning.
                </div>
                <h2 className="text-2xl font-black text-white mt-0.5">
                  {result.district ? `${result.district} District` : 'Query Location'}
                </h2>
                <div className="text-xs text-slate-300 mt-1 font-mono">
                  Coordinates: {result.latitude?.toFixed(4)}° N, {result.longitude?.toFixed(4)}° E
                </div>
              </div>

              {result.inside_study_area ? (
                <div className="flex items-center space-x-3">
                  <div className="bg-navy-950 border border-blue-500/40 text-blue-200 px-4 py-2 rounded-xl text-center">
                    <div className="text-[10px] uppercase font-mono text-slate-400">Susceptibility Class</div>
                    <div className="text-sm font-black text-white">{result.susceptibility_label || 'N/A'}</div>
                    <div className="text-[10px] text-blue-300 font-mono">Prob: {result.susceptibility_probability?.toFixed(4)}</div>
                  </div>

                  <div className="bg-amber-950/80 border border-amber-600 text-amber-200 px-4 py-2 rounded-xl text-center">
                    <div className="text-[10px] uppercase font-mono text-amber-300">Dynamic Hazard</div>
                    <div className="text-sm font-black">{result.dynamic_hazard_label || 'N/A'}</div>
                    <div className="text-[10px] text-amber-300 font-mono">Index: {result.dynamic_hazard_index?.toFixed(4)}</div>
                  </div>
                </div>
              ) : (
                <div className="bg-slate-900 border border-slate-700 text-slate-300 px-4 py-2 rounded-xl text-center text-xs font-mono">
                  OUTSIDE J&K STUDY AREA
                </div>
              )}
            </div>

            {result.inside_study_area ? (
              <>
                {/* Environmental Factors Grid */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                  <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
                    <span className="text-slate-400 font-medium">Elevation / Slope:</span>
                    <div className="font-bold text-white">{result.elevation_m}m ASL / {result.slope_deg}°</div>
                  </div>

                  <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
                    <span className="text-slate-400 font-medium">24h Rain Proxy / P90:</span>
                    <div className="font-bold text-sky-300">{result.rainfall_accum_24h_mm}mm / {result.imd_p90_baseline_mm}mm</div>
                  </div>

                  <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
                    <span className="text-slate-400 font-medium">Rainfall Anomaly Ratio:</span>
                    <div className="font-bold text-amber-300">{result.rainfall_anomaly_ratio?.toFixed(2)}x Baseline</div>
                  </div>

                  <div className="bg-navy-800/60 border border-navy-700 p-3 rounded-lg space-y-1">
                    <span className="text-slate-400 font-medium">NH-44 Proximity:</span>
                    <div className="font-bold text-emerald-300">
                      {result.distance_to_nh44_m ? `${(result.distance_to_nh44_m / 1000).toFixed(2)} km` : 'N/A'}
                    </div>
                  </div>
                </div>

                {/* Data Confidence & Limitations */}
                <div className="bg-navy-800/40 border border-navy-700 p-4 rounded-lg space-y-2 text-xs">
                  <div className="flex items-center space-x-2 font-bold text-white">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>Data Confidence: {result.data_confidence || 'High (Model-derived 100m grid)'}</span>
                  </div>
                  {result.data_limitations && (
                    <ul className="list-disc list-inside space-y-1 text-slate-300 pl-2">
                      {result.data_limitations.map((lim, i) => (
                        <li key={i}>{lim}</li>
                      ))}
                    </ul>
                  )}
                </div>
              </>
            ) : (
              <div className="bg-navy-950 border border-navy-800 p-6 rounded-lg text-center space-y-2">
                <AlertTriangle className="w-8 h-8 text-amber-400 mx-auto" />
                <h3 className="font-bold text-white text-sm">Location outside J&K UT study domain</h3>
                <p className="text-xs text-slate-400 max-w-md mx-auto">
                  The queried coordinates lie outside the 20 J&K UT district administrative boundary grid (EPSG:32643).
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
