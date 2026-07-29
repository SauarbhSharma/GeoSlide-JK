"use client";

import { useEffect, useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Activity, CheckCircle, AlertTriangle, FileWarning, ShieldCheck } from 'lucide-react';

export default function SystemStatus() {
  const [healthStatus, setHealthStatus] = useState<any>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/health')
      .then((res) => res.json())
      .then((data) => setHealthStatus(data))
      .catch(() => setHealthStatus({ status: 'offline', service: 'GeoSlide-JK API (Disconnected)' }));
  }, []);

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* DEM SAFETY MANDATE BANNER */}
        <div className="bg-amber-950/90 border border-amber-500/90 text-amber-100 p-4 rounded-xl flex items-center justify-between text-xs shadow-xl">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="w-6 h-6 text-amber-400 shrink-0" />
            <div>
              <h2 className="font-bold text-sm text-amber-300">DEM Processing Rule (Phase 2 Locked Manifest)</h2>
              <p className="text-amber-100 mt-1 font-semibold text-xs">
                Use exactly four full-J&K DEM tiles. Do not use the pilot DEM.
              </p>
            </div>
          </div>
          <span className="font-mono text-xs bg-amber-900 border border-amber-400/50 px-3 py-1.5 rounded text-amber-100 font-bold shrink-0">
            DEM Source Locked
          </span>
        </div>

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-emerald-600/20 text-emerald-400 p-2 rounded-lg border border-emerald-500/30">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Truthful Data & System Status</h1>
              <p className="text-xs text-slate-300 mt-0.5">
                Audit breakdown of completed Phase 2 geospatial products, data freshness, and project limitations.
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <span className="flex items-center space-x-1.5 bg-emerald-950 border border-emerald-600 text-emerald-300 text-xs px-3 py-1.5 rounded-lg font-mono">
              <CheckCircle className="w-3.5 h-3.5" />
              <span>FastAPI Backend: {healthStatus?.status || 'checking...'}</span>
            </span>
          </div>
        </div>

        {/* Phase 2 Completed Products Summary Card */}
        <div className="bg-navy-900 border border-emerald-600/40 p-4 rounded-xl space-y-3 text-xs">
          <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-emerald-400 font-bold text-sm">
            <ShieldCheck className="w-4 h-4" />
            <span>Completed Phase 2 Products & Hardened Services</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300 font-mono text-[11px]">
            <ul className="space-y-1.5 bg-slate-950 p-3 rounded border border-slate-800">
              <li className="text-emerald-300 font-bold mb-1">✓ Raster Derivatives (30m, EPSG:32643)</li>
              <li>✓ Elevation COG Ready (`jk_elevation_glo30_cog.tif`)</li>
              <li>✓ Slope COG Ready (`jk_slope_degrees_cog.tif`)</li>
              <li>✓ Aspect COG Ready (`jk_aspect_degrees_cog.tif`)</li>
              <li>✓ Hillshade COG Ready (`jk_hillshade_cog.tif`)</li>
              <li>✓ 51,322,278 Valid Land Pixels Mosaicked</li>
            </ul>
            <ul className="space-y-1.5 bg-slate-950 p-3 rounded border border-slate-800">
              <li className="text-emerald-300 font-bold mb-1">✓ Processed Static Vector Layers & Services</li>
              <li>✓ 20-District Boundaries (Mirpur & Muzaffarabad Absent)</li>
              <li>✓ NGDR Landslide Points (2,370 Points) & Polygons (7,436)</li>
              <li>✓ Tectonic Faults (3), Thrusts (14), Lineaments (774)</li>
              <li>✓ NH-44 Corridor, Major Roads, Settlements, Hospitals (1,079)</li>
              <li>✓ Map Inspector Hardened against Null / Out-of-Bounds Clicks</li>
              <li>✓ Next.js CSS Tailwind Styling Repaired & Verified</li>
            </ul>
          </div>
        </div>

        {/* Truthful Category Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          {/* Core datasets ready */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-emerald-400 font-bold">
              <CheckCircle className="w-4 h-4" />
              <span>Core datasets ready</span>
            </div>
            <ul className="space-y-1.5 text-slate-300 font-mono text-[11px]">
              <li>✓ 20-District J&K Boundary (Verified)</li>
              <li>✓ Copernicus DEM (Full-J&K DEM: 4 tiles used)</li>
              <li>✓ ESA WorldCover 2021 LULC (4 tiles)</li>
              <li>✓ Lithology 1:50k Vector (Single Match)</li>
              <li>✓ NGDR Landslide Inventory Vector</li>
            </ul>
          </div>

          {/* Ready after cleaning */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-amber-400 font-bold">
              <AlertTriangle className="w-4 h-4" />
              <span>Ready after cleaning</span>
            </div>
            <ul className="space-y-1.5 text-slate-300 font-mono text-[11px]">
              <li>! Tectonic Faults & Thrusts (EPSG:32643 Reprojected)</li>
              <li>! NGDR Landslide Polygons (Grouped & Clipped)</li>
              <li>! Infrastructure Vectors (GeoPackage Exported)</li>
              <li>! Health Facilities (1,079 Filtered Points)</li>
            </ul>
          </div>

          {/* Partial coverage */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-sky-400 font-bold">
              <FileWarning className="w-4 h-4" />
              <span>Partial coverage</span>
            </div>
            <ul className="space-y-1.5 text-slate-300 text-[11px]">
              <li className="font-mono">
                <strong>GHSL population: Coverage requires verification</strong>
              </li>
              <li className="font-mono">
                <strong>Full-J&K DEM: 4 tiles used</strong>
              </li>
            </ul>
          </div>
        </div>

        {/* Optional/unconfirmed & Excluded/problematic Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {/* Optional/unconfirmed */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-purple-400 font-bold text-sm">
              <FileWarning className="w-4 h-4" />
              <span>Optional/unconfirmed</span>
            </div>
            <ul className="space-y-2 text-slate-300 font-mono text-[11px]">
              <li className="bg-navy-950 p-2.5 rounded border border-navy-800">
                <strong className="text-amber-300">Geomorphology: Unconfirmed</strong>
                <p className="text-[10px] text-slate-400 mt-0.5">Spatial layer presence unconfirmed; pending verification prior to Phase 3 feature extraction.</p>
              </li>
              <li className="bg-navy-950 p-2.5 rounded border border-navy-800">
                <strong className="text-amber-300">IMERG Rainfall: Demonstration Mode</strong>
                <p className="text-[10px] text-slate-400 mt-0.5">Rainfall dataset not processed in Phase 2. Connects during Phase 5.</p>
              </li>
            </ul>
          </div>

          {/* Excluded/problematic */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-rose-400 font-bold text-sm">
              <AlertTriangle className="w-4 h-4" />
              <span>Excluded/problematic</span>
            </div>
            <ul className="space-y-2 text-slate-300 font-mono text-[11px]">
              <li className="bg-navy-950 p-2.5 rounded border border-navy-800">
                <strong className="text-rose-300">NLSM raster: Excluded</strong>
                <p className="text-[10px] text-slate-400 mt-0.5">Pre-existing susceptibility raster reserved solely for validation benchmarking. Excluded from training features.</p>
              </li>
              <li className="bg-navy-950 p-2.5 rounded border border-navy-800">
                <strong className="text-rose-300">Landslide event dates: Insufficient for supervised dynamic-event modelling</strong>
                <p className="text-[10px] text-slate-400 mt-0.5">Event dates lack temporal resolution for supervised dynamic event models.</p>
              </li>
              <li className="bg-navy-950 p-2.5 rounded border border-navy-800">
                <strong className="text-rose-300">Pilot DEM: Excluded</strong>
                <p className="text-[10px] text-amber-300 font-bold mt-0.5">Use exactly four full-J&K DEM tiles. Do not use the pilot DEM.</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
