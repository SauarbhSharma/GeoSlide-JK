"use client";

import { useState, useEffect } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Search, MapPin, Navigation, AlertTriangle, RefreshCw, CheckCircle2, ChevronDown } from 'lucide-react';
import { apiUrl } from '@/lib/api';
import { useUserRole } from '@/lib/RoleContext';

interface LocationResult {
  success: boolean;
  code?: string;
  message?: string;
  inside_study_area: boolean;
  data_available?: boolean;
  location?: { latitude: number; longitude: number };
  district?: string;
  susceptibility_probability?: number;
  susceptibility_class?: number;
  susceptibility_label?: string;
  rainfall_accum_24h_mm?: number;
  imd_p90_baseline_mm?: number;
  rainfall_anomaly_ratio?: number;
  dynamic_hazard_index?: number;
  dynamic_hazard_class?: number;
  dynamic_hazard_label?: string;
  terrain?: {
    elevation_m?: number | null;
    slope_deg?: number | null;
    aspect_deg?: number | null;
    hillshade?: number | null;
  };
  advisory?: string;
  precautionary_measures?: string[];
  scenario_proxy_warning?: string;
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
  const { role } = useUserRole();
  const [latInput, setLatInput] = useState('33.2450');
  const [lonInput, setLonInput] = useState('75.2410');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<LocationResult | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [apiConnected, setApiConnected] = useState(false);

  useEffect(() => {
    fetch(apiUrl('/api/v1/health'))
      .then((res) => {
        if (res.ok) setApiConnected(true);
      })
      .catch(() => setApiConnected(false));
  }, []);

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
      const res = await fetch(apiUrl(`/api/v1/location-check?lat=${lat}&lon=${lon}`));
      if (!res.ok) {
        throw new Error(`API returned HTTP ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
      setApiConnected(true);
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

  const getPlainLanguageTitle = (label?: string) => {
    switch (label?.toLowerCase()) {
      case 'very high':
      case 'high':
        return 'High Landslide Susceptibility';
      case 'moderate':
        return 'Moderate Landslide Susceptibility';
      case 'low':
      case 'very low':
        return 'Baseline Landslide Susceptibility';
      default:
        return 'Moderate Landslide Susceptibility';
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-navy-950 text-slate-100">
      <Header />

      <main className="flex-1 overflow-y-auto p-4 max-w-5xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Search Panel */}
        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-bold text-white flex items-center space-x-2">
              <MapPin className="w-5 h-5 text-blue-400" />
              <span>Check My Area — Location Risk Checker</span>
            </h1>
            <span className={`text-xs font-mono border px-2.5 py-1 rounded-md ${
              apiConnected
                ? 'bg-emerald-950 text-emerald-300 border-emerald-600/40'
                : 'bg-amber-950 text-amber-300 border-amber-600/40'
            }`}>
              {apiConnected ? 'API Connected (HTTP 200)' : 'API Disconnected'}
            </span>
          </div>
          <p className="text-xs text-slate-300">
            Select an example location or enter latitude and longitude coordinates to inspect slope instability exposure.
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
                  className="w-full bg-navy-800 border border-navy-700 rounded-xl pl-12 pr-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
              <div className="flex-1 relative">
                <span className="absolute left-3 top-2.5 text-xs text-slate-400 font-mono">Lon:</span>
                <input
                  type="text"
                  value={lonInput}
                  onChange={(e) => setLonInput(e.target.value)}
                  placeholder="75.2410"
                  className="w-full bg-navy-800 border border-navy-700 rounded-xl pl-12 pr-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="flex gap-2">
              <select
                onChange={handleSelectPreset}
                className="bg-navy-800 border border-navy-700 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-semibold"
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
                className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-4 py-2 rounded-xl flex items-center justify-center space-x-1.5 transition-colors disabled:opacity-50 shadow-lg shadow-blue-900/30"
              >
                {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                <span>Check Location</span>
              </button>

              <button
                type="button"
                onClick={handleGeolocate}
                className="bg-navy-800 hover:bg-navy-700 text-white text-xs font-semibold px-3 py-2 rounded-xl flex items-center justify-center border border-navy-700 transition-colors"
                title="Use current GPS location"
              >
                <Navigation className="w-4 h-4" />
              </button>
            </div>
          </form>

          {errorMsg && (
            <div className="bg-rose-950/60 border border-rose-600/60 p-3 rounded-xl text-xs text-rose-200 flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}
        </div>

        {/* Location Risk Result */}
        {result && (
          <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-4 shadow-xl">
            {result.inside_study_area ? (
              <>
                {/* Simplified Plain-Language Headline for Citizens */}
                <div className="bg-navy-950 p-4 rounded-xl border border-navy-800 space-y-2">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-navy-800 pb-3">
                    <div>
                      <span className="text-[10px] text-amber-400 font-mono uppercase tracking-wider">
                        Location Instability Assessment
                      </span>
                      <h2 className="text-xl sm:text-2xl font-black text-white mt-0.5">
                        {getPlainLanguageTitle(result.susceptibility_label)}
                      </h2>
                      <div className="text-xs text-slate-400 font-mono mt-0.5">
                        {result.district ? `${result.district} District` : 'Jammu & Kashmir UT'} | {result.location?.latitude?.toFixed(4)}° N, {result.location?.longitude?.toFixed(4)}° E
                      </div>
                    </div>

                    <span className="px-3 py-1 bg-amber-950 border border-amber-600/50 text-amber-300 font-bold text-xs rounded-xl font-mono self-start">
                      {result.susceptibility_label || 'Moderate'} Exposure
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed pt-1">
                    This location lies in terrain where slope angle, geological lithology, drainage, or nearby historical landslides indicate higher relative susceptibility compared to valley baseline areas.
                  </p>
                </div>

                {/* Practical Suggested Precautions */}
                <div className="bg-navy-950 p-4 rounded-xl border border-navy-800 space-y-2 text-xs">
                  <span className="font-bold text-white block text-xs uppercase tracking-wider text-slate-200">
                    Suggested Travel & Safety Precautions:
                  </span>
                  <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-slate-300 font-medium">
                    <li className="flex items-center space-x-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span>Avoid stopping or parking vehicle near steep un-engineered slope cuts.</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span>Exercise heightened caution during intense or prolonged rainfall.</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span>Verify official traffic and road advisories before travel.</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span>Follow instructions issued by district or highway authorities.</span>
                    </li>
                  </ul>
                </div>

                {/* Expandable Technical Details Section */}
                <details className="bg-navy-950 rounded-xl border border-navy-800 p-4 text-xs group">
                  <summary className="font-bold text-slate-300 cursor-pointer flex items-center justify-between hover:text-white select-none">
                    <span>Technical Details & Raw Raster Attributes (For Analysts / Researchers)</span>
                    <ChevronDown className="w-4 h-4 text-slate-400 group-open:rotate-180 transition-transform" />
                  </summary>

                  <div className="mt-3 pt-3 border-t border-navy-800 space-y-3">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 font-mono text-[11px]">
                      <div className="bg-navy-900 p-2.5 rounded-lg border border-navy-800">
                        <span className="text-slate-400 block text-[10px]">Static Probability:</span>
                        <span className="font-bold text-amber-300 text-xs">
                          {result.susceptibility_probability != null ? (result.susceptibility_probability * 100).toFixed(2) + '%' : 'N/A'}
                        </span>
                      </div>
                      <div className="bg-navy-900 p-2.5 rounded-lg border border-navy-800">
                        <span className="text-slate-400 block text-[10px]">Dynamic Hazard Index:</span>
                        <span className="font-bold text-rose-300 text-xs">
                          {result.dynamic_hazard_index != null ? result.dynamic_hazard_index.toFixed(4) : 'N/A'}
                        </span>
                      </div>
                      <div className="bg-navy-900 p-2.5 rounded-lg border border-navy-800">
                        <span className="text-slate-400 block text-[10px]">Elevation / Slope:</span>
                        <span className="font-bold text-white text-xs">
                          {result.terrain?.elevation_m != null ? `${result.terrain.elevation_m}m` : 'N/A'} / {result.terrain?.slope_deg != null ? `${result.terrain.slope_deg}°` : 'N/A'}
                        </span>
                      </div>
                      <div className="bg-navy-900 p-2.5 rounded-lg border border-navy-800">
                        <span className="text-slate-400 block text-[10px]">Processing Grid:</span>
                        <span className="font-bold text-emerald-300 text-xs">100m EPSG:32643</span>
                      </div>
                    </div>
                  </div>
                </details>
              </>
            ) : (
              <div className="bg-navy-950 border border-navy-800 p-6 rounded-xl text-center space-y-2">
                <AlertTriangle className="w-8 h-8 text-amber-400 mx-auto" />
                <h3 className="font-bold text-white text-sm">Location outside J&K UT study domain</h3>
                <p className="text-xs text-slate-400 max-w-md mx-auto">
                  The queried coordinates lie outside the 20 J&K UT district administrative boundary grid (EPSG:32643).
                </p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
