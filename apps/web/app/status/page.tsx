"use client";

import { useEffect, useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Activity, CheckCircle, AlertTriangle, ShieldCheck, Database, Server } from 'lucide-react';
import { apiUrl } from '@/lib/api';

export default function SystemStatus() {
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [endpointsStatus, setEndpointsStatus] = useState<Record<string, number>>({});

  useEffect(() => {
    fetch(apiUrl('/api/v1/health'))
      .then((res) => res.json())
      .then((data) => setHealthStatus(data))
      .catch(() => setHealthStatus({ status: 'offline', phase: 'Disconnected' }));

    const endpointsToTest = [
      '/api/v1/health',
      '/api/v1/status',
      '/api/v1/districts',
      '/api/v1/location-check?lat=33.245&lon=75.241',
      '/api/v1/terrain/value?lat=33.245&lon=75.241',
      '/api/v1/tiles/susceptibility_prob/8/181/102.png',
      '/api/v1/layers',
      '/api/v1/summary/statewide',
      '/api/v1/summary/district/ramban'
    ];

    endpointsToTest.forEach((ep) => {
      fetch(apiUrl(ep))
        .then((res) => {
          setEndpointsStatus((prev) => ({ ...prev, [ep]: res.status }));
        })
        .catch(() => {
          setEndpointsStatus((prev) => ({ ...prev, [ep]: 0 }));
        });
    });
  }, []);

  const isHealthy = healthStatus?.status === 'healthy';
  const liveCount = Object.values(endpointsStatus).filter((code) => code === 200).length;

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* RELEASE AUDIT STATUS BANNER */}
        <div className="bg-amber-950/90 border border-amber-500/90 text-amber-100 p-4 rounded-xl flex items-center justify-between text-xs shadow-xl">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="w-6 h-6 text-amber-400 shrink-0" />
            <div>
              <h2 className="font-bold text-sm text-amber-300">GeoSlide-JK v1.0.0 Final Release Audit: Conditional Pass</h2>
              <p className="text-amber-100 mt-1 font-semibold text-xs">
                Rainfall and P90 layers in this release are derived proxy products. Operational GPM/IMD ingestion remains future work.
              </p>
            </div>
          </div>
          <span className="font-mono text-xs bg-amber-900 border border-amber-400/50 px-3 py-1.5 rounded text-amber-100 font-bold shrink-0">
            Conditional Pass
          </span>
        </div>

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-emerald-600/20 text-emerald-400 p-2 rounded-lg border border-emerald-500/30">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Data & System Status — v1.0.0 Release</h1>
              <p className="text-xs text-slate-300 mt-0.5">
                Live endpoint status across Phase 2 static layers, Phase 4 XGBoost ML model, Phase 5 dynamic hazard scenario, and FastAPI tile microservices.
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <div className={`flex items-center space-x-2 border px-3 py-1.5 rounded-lg text-xs font-mono font-bold ${
              isHealthy
                ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-300'
                : 'bg-amber-950/80 border-amber-500/50 text-amber-300'
            }`}>
              <span className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
              <span>{isHealthy ? 'FastAPI Backend Operational' : 'Backend Connecting...'}</span>
            </div>
          </div>
        </div>

        {/* System Overview Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <div className="bg-navy-900 border border-navy-700 p-3 rounded-xl">
            <div className="text-[11px] text-slate-400 font-mono">Release Version</div>
            <div className="text-lg font-bold text-white mt-0.5">v1.0.0</div>
            <div className="text-[10px] text-emerald-400 font-mono">Final Release</div>
          </div>
          <div className="bg-navy-900 border border-navy-700 p-3 rounded-xl">
            <div className="text-[11px] text-slate-400 font-mono">Susceptibility Model</div>
            <div className="text-lg font-bold text-emerald-300 mt-0.5">XGBoost (ROC 0.8694)</div>
            <div className="text-[10px] text-slate-400 font-mono">30 Features Trained</div>
          </div>
          <div className="bg-navy-900 border border-navy-700 p-3 rounded-xl">
            <div className="text-[11px] text-slate-400 font-mono">FastAPI Microservices</div>
            <div className="text-lg font-bold text-white mt-0.5">{isHealthy ? 'Healthy (HTTP 200)' : 'Offline'}</div>
            <div className="text-[10px] text-emerald-400 font-mono">{liveCount} Live Tested Endpoints</div>
          </div>
          <div className="bg-navy-900 border border-navy-700 p-3 rounded-xl">
            <div className="text-[11px] text-slate-400 font-mono">Next.js Web UI</div>
            <div className="text-lg font-bold text-white mt-0.5">Healthy (10 Routes)</div>
            <div className="text-[10px] text-emerald-400 font-mono">Build Clean</div>
          </div>
        </div>

        {/* Tested Endpoints Matrix */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3 text-xs">
          <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-white font-bold text-sm">
            <Server className="w-4 h-4 text-blue-400" />
            <span>FastAPI Live Service Endpoints Status</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-2 font-mono text-[11px]">
            {Object.entries(endpointsStatus).map(([ep, status]) => (
              <div key={ep} className={`p-2 rounded border flex items-center justify-between ${
                status === 200
                  ? 'bg-navy-950 border-emerald-600/40 text-emerald-300'
                  : 'bg-rose-950/60 border-rose-600/60 text-rose-300'
              }`}>
                <span className="truncate pr-2">{ep}</span>
                <span className="font-bold shrink-0">{status === 200 ? 'HTTP 200' : status === 0 ? 'Failed' : `HTTP ${status}`}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Phase Pipeline Execution Status */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3 text-xs">
          <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-white font-bold text-sm">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Phased Pipeline Execution Lifecycle Status</span>
          </div>

          <div className="space-y-2 font-mono text-[11px]">
            <div className="flex items-center justify-between bg-navy-950 p-2.5 rounded border border-emerald-600/40">
              <span className="flex items-center space-x-2 text-emerald-300 font-bold">
                <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Phase 2: Static Geospatial Products</span>
              </span>
              <span className="text-slate-400">Completed (30m Elevation, Slope, Aspect, Hillshade, 10 Vector Layers)</span>
            </div>

            <div className="flex items-center justify-between bg-navy-950 p-2.5 rounded border border-emerald-600/40">
              <span className="flex items-center space-x-2 text-emerald-300 font-bold">
                <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Phase 3: Feature Engineering & Grid Alignment</span>
              </span>
              <span className="text-slate-400">Completed (30 Predictors Aligned to 100m EPSG:32643 Master Grid)</span>
            </div>

            <div className="flex items-center justify-between bg-navy-950 p-2.5 rounded border border-emerald-600/40">
              <span className="flex items-center space-x-2 text-emerald-300 font-bold">
                <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Phase 4: Susceptibility Model Training & Validation</span>
              </span>
              <span className="text-slate-400">Completed (XGBoost 5-Fold Spatial CV ROC-AUC: 0.8694, PR-AUC: 0.2760)</span>
            </div>

            <div className="flex items-center justify-between bg-navy-950 p-2.5 rounded border border-emerald-600/40">
              <span className="flex items-center space-x-2 text-emerald-300 font-bold">
                <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Phase 5: Dynamic Hazard Scenario Pipeline</span>
              </span>
              <span className="text-slate-400">Completed (24h Rainfall Proxy 5-160mm, P90 Proxy 30-95mm, H_dyn = S * R)</span>
            </div>

            <div className="flex items-center justify-between bg-navy-950 p-2.5 rounded border border-emerald-600/40">
              <span className="flex items-center space-x-2 text-emerald-300 font-bold">
                <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Phase 6: Full API Services & Web Integration</span>
              </span>
              <span className="text-slate-400">Completed (FastAPI Tile Microservices & Next.js Web UI Integrated)</span>
            </div>

            <div className="flex items-center justify-between bg-navy-950 p-2.5 rounded border border-amber-500/50">
              <span className="flex items-center space-x-2 text-amber-300 font-bold">
                <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                <span>Final Independent Release Audit</span>
              </span>
              <span className="text-amber-200">Conditional Pass (Precipitation Layers Derived Scenario/Proxy Products)</span>
            </div>
          </div>
        </div>

        {/* Data Provenance & Safeguards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-blue-400 font-bold">
              <Database className="w-4 h-4" />
              <span>Verified Core Data Assets</span>
            </div>
            <ul className="space-y-1.5 text-slate-300 font-mono text-[11px]">
              <li>✓ 20 J&K UT District Boundaries (EPSG:32643)</li>
              <li>✓ Copernicus DEM GLO-30 (4 tiles mosaicked)</li>
              <li>✓ ESA WorldCover 2021 LULC Mosaic (4 tiles)</li>
              <li>✓ GSI 1:50k Lithology & Structural Tectonics</li>
              <li>✓ NGDR Landslide Inventory (2,370 Points / 7,436 Polygons)</li>
            </ul>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2 text-purple-400 font-bold">
              <Server className="w-4 h-4" />
              <span>Key Limitations & Research Disclaimers</span>
            </div>
            <ul className="space-y-1.5 text-slate-300 font-mono text-[11px]">
              <li>! Rainfall accumulation is an elevation-based orographic proxy model.</li>
              <li>! Operational GPM IMERG and IMD daily NetCDF ingestion is future work.</li>
              <li>! Pre-existing NLSM raster was constant NoData `127` over study domain.</li>
              <li>! System is a decision-support research prototype, not an official warning system.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
