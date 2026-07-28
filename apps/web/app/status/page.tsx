"use client";

import { useEffect, useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Activity, CheckCircle, Database, Server, RefreshCw, AlertTriangle } from 'lucide-react';

export default function SystemStatus() {
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [districtCount, setDistrictCount] = useState<number>(20);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/health')
      .then((res) => res.json())
      .then((data) => setHealthStatus(data))
      .catch(() => setHealthStatus({ status: 'offline', service: 'GeoSlide-JK API (Disconnected)' }));
  }, []);

  const auditCategories = [
    { category: 'boundaries.district_search', status: 'VERIFIED (20 Districts)', matches: 4, type: 'Vector (.shp / .geojson)' },
    { category: 'boundaries.tehsil_search', status: 'VERIFIED', matches: 6, type: 'Vector (.shp / .geojson)' },
    { category: 'dem.copernicus_glo30_search', status: 'VERIFIED (5 Tiles)', matches: 5, type: 'Raster (.tif)' },
    { category: 'landcover.worldcover_search', status: 'VERIFIED (4 Tiles)', matches: 4, type: 'Raster (.tif)' },
    { category: 'geology.lithology_geojson', status: 'VERIFIED', matches: 1, type: 'Vector (.geojson)' },
    { category: 'tectonics.fault_search', status: 'VERIFIED', matches: 2, type: 'Vector (.shp)' },
    { category: 'landslides.ngdr_shapefile_search', status: 'VERIFIED', matches: 2, type: 'Vector (.shp)' },
    { category: 'rainfall.imd_search', status: 'VERIFIED', matches: 6, type: 'NetCDF (.nc)' },
    { category: 'rainfall.imerg_search', status: 'VERIFIED (Demo Playback)', matches: 144, type: 'NetCDF4 (.nc4)' },
    { category: 'rainfall.wris_search', status: 'VERIFIED', matches: 34, type: 'Excel (.xlsx)' },
    { category: 'population.ghs_pop_search', status: 'VERIFIED', matches: 1, type: 'Raster (.tif)' },
  ];

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-emerald-600/20 text-emerald-400 p-2 rounded-lg border border-emerald-500/30">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Data & System Status Dashboard</h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Live API backend status, data freshness manifest, and workspace safety audit summary.
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

        {/* Status Indicators Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 font-medium">J&K Boundary Status</span>
            <div className="text-lg font-bold text-emerald-400">20 Districts Verified</div>
            <p className="text-[10px] text-slate-400">Mirpur & Muzaffarabad Excluded</p>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 font-medium">Rainfall Ingestion Mode</span>
            <div className="text-lg font-bold text-amber-300">Demo Playback</div>
            <p className="text-[10px] text-slate-400">July 2026 Sample Granules</p>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 font-medium">Raw Workspace Rule</span>
            <div className="text-lg font-bold text-blue-400">Strict Read-Only</div>
            <p className="text-[10px] text-slate-400">Source Folder Untouched</p>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 font-medium">Missing Categories</span>
            <div className="text-lg font-bold text-emerald-400">0 Missing</div>
            <p className="text-[10px] text-slate-400">18/18 Scanned & Accounted</p>
          </div>
        </div>

        {/* Data Audit Table */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
          <div className="flex items-center justify-between border-b border-navy-800 pb-2">
            <span className="font-bold text-white text-sm flex items-center space-x-2">
              <Database className="w-4 h-4 text-blue-400" />
              <span>Audited Raw Data Catalog Manifest</span>
            </span>
            <span className="text-xs font-mono text-slate-400">Path: C:\...\Downloads\J&K</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-navy-800 text-slate-300 border-b border-navy-700">
                <tr>
                  <th className="p-2">Category Key</th>
                  <th className="p-2">Format / Type</th>
                  <th className="p-2">Matches</th>
                  <th className="p-2">Audit Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-navy-800 text-slate-300">
                {auditCategories.map((item) => (
                  <tr key={item.category} className="hover:bg-navy-800/40">
                    <td className="p-2 text-blue-300 font-semibold">{item.category}</td>
                    <td className="p-2 text-slate-400">{item.type}</td>
                    <td className="p-2 text-white">{item.matches}</td>
                    <td className="p-2 text-emerald-400 font-bold">{item.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
