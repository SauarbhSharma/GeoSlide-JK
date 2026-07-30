"use client";

import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Cpu, CheckCircle2, AlertCircle, BarChart3, ShieldCheck } from 'lucide-react';

export default function ModelTransparency() {
  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Phase 4 Status Banner */}
        <div className="bg-emerald-950/70 border border-emerald-500/60 p-4 rounded-xl flex items-center justify-between text-xs text-emerald-200 shadow-lg">
          <div className="flex items-center space-x-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
            <div>
              <h2 className="font-bold text-sm text-emerald-300">Phase 4 Susceptibility Model: Trained & Audited</h2>
              <p className="text-emerald-100 mt-0.5 font-medium">
                Primary Model: XGBoost Classifier | 5-Fold Spatial District Block ROC-AUC: <span className="font-mono font-bold text-emerald-300">0.8694</span> | PR-AUC: <span className="font-mono font-bold text-emerald-300">0.2760</span> | Brier Score: <span className="font-mono font-bold text-emerald-300">0.1788</span>
              </p>
            </div>
          </div>
          <span className="font-mono text-xs bg-emerald-900 border border-emerald-400/40 px-3 py-1.5 rounded text-emerald-100 font-bold shrink-0">
            Phase 4 Complete
          </span>
        </div>

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-purple-600/20 text-purple-400 p-2 rounded-lg border border-purple-500/30">
              <Cpu className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Model & Methodology Transparency</h1>
              <p className="text-xs text-slate-300 mt-0.5">
                Evaluated algorithms, spatial validation strategy, feature importance, and NLSM comparative benchmarks.
              </p>
            </div>
          </div>
          <div className="text-xs font-mono bg-navy-800 border border-emerald-700 px-3 py-1.5 rounded-lg text-emerald-400 font-semibold">
            Status: Phase 4 Verified
          </div>
        </div>

        {/* Models & Validation Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Models Evaluated */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2">
              <Cpu className="w-4 h-4 text-blue-400" />
              <h2 className="font-bold text-white text-sm">Models Evaluated</h2>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Machine learning algorithms trained and evaluated during Phase 4:
            </p>
            <ul className="space-y-2 text-xs text-slate-200 font-mono">
              <li className="flex items-center justify-between bg-navy-800/60 p-2 rounded border border-navy-700">
                <span className="flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                  <span>Logistic Regression (Baseline)</span>
                </span>
                <span className="text-slate-400">Evaluated</span>
              </li>
              <li className="flex items-center justify-between bg-navy-800/60 p-2 rounded border border-navy-700">
                <span className="flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                  <span>Random Forest Classifier</span>
                </span>
                <span className="text-slate-400">Evaluated</span>
              </li>
              <li className="flex items-center justify-between bg-navy-800/60 p-2 rounded border border-emerald-500/50 bg-emerald-950/40 font-bold">
                <span className="flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                  <span>XGBoost Classifier (Primary Selected)</span>
                </span>
                <span className="text-emerald-300">ROC-AUC: 0.8694</span>
              </li>
            </ul>
          </div>

          {/* Spatial Validation & Fold Metrics */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <h2 className="font-bold text-white text-sm">5-Fold Spatial District CV Results</h2>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              District-block spatial cross-validation out-of-fold ROC-AUC scores across 5 spatial folds:
            </p>
            <div className="grid grid-cols-5 gap-1.5 text-center font-mono text-xs">
              <div className="bg-navy-800 p-2 rounded border border-navy-700">
                <div className="text-[10px] text-slate-400">Fold 1</div>
                <div className="font-bold text-emerald-400 mt-0.5">0.8919</div>
              </div>
              <div className="bg-navy-800 p-2 rounded border border-navy-700">
                <div className="text-[10px] text-slate-400">Fold 2</div>
                <div className="font-bold text-emerald-400 mt-0.5">0.8279</div>
              </div>
              <div className="bg-amber-950/60 p-2 rounded border border-amber-600/60">
                <div className="text-[10px] text-amber-300">Fold 3</div>
                <div className="font-bold text-amber-400 mt-0.5">0.6210</div>
              </div>
              <div className="bg-navy-800 p-2 rounded border border-navy-700">
                <div className="text-[10px] text-slate-400">Fold 4</div>
                <div className="font-bold text-emerald-400 mt-0.5">0.8584</div>
              </div>
              <div className="bg-navy-800 p-2 rounded border border-navy-700">
                <div className="text-[10px] text-slate-400">Fold 5</div>
                <div className="font-bold text-emerald-400 mt-0.5">0.9033</div>
              </div>
            </div>
            <p className="text-[11px] text-amber-300/90 font-mono pt-1">
              * Performance varies geographically; Fold 3 produced lower generalization performance due to geomorphological heterogeneity across Baramulla/Rajouri/Samba.
            </p>
          </div>
        </div>

        {/* Feature Importance & Top Predictors */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
          <div className="flex items-center space-x-2 border-b border-navy-800 pb-2">
            <BarChart3 className="w-4 h-4 text-purple-400" />
            <h2 className="font-bold text-white text-sm">Top 5 Predictor Features (30 Total Features)</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-5 gap-2 text-xs font-mono">
            <div className="bg-navy-800/80 p-2.5 rounded border border-navy-700">
              <div className="text-[10px] text-slate-400">#1 Feature</div>
              <div className="font-bold text-white mt-1">log1p_distance_to_fault</div>
            </div>
            <div className="bg-navy-800/80 p-2.5 rounded border border-navy-700">
              <div className="text-[10px] text-slate-400">#2 Feature</div>
              <div className="font-bold text-white mt-1">snow_ice_fraction</div>
            </div>
            <div className="bg-navy-800/80 p-2.5 rounded border border-navy-700">
              <div className="text-[10px] text-slate-400">#3 Feature</div>
              <div className="font-bold text-white mt-1">elevation</div>
            </div>
            <div className="bg-navy-800/80 p-2.5 rounded border border-navy-700">
              <div className="text-[10px] text-slate-400">#4 Feature</div>
              <div className="font-bold text-white mt-1">log1p_distance_to_active_fault</div>
            </div>
            <div className="bg-navy-800/80 p-2.5 rounded border border-navy-700">
              <div className="text-[10px] text-slate-400">#5 Feature</div>
              <div className="font-bold text-white mt-1">distance_to_drainage</div>
            </div>
          </div>
        </div>

        {/* Benchmark Evaluation Disclosure */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
          <h2 className="font-bold text-white text-sm flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-blue-400" />
            <span>NLSM Benchmark Audit Note</span>
          </h2>
          <p className="text-slate-300">
            Pre-existing NLSM benchmark comparison was unavailable because the supplied raster was constant NoData (127) over the evaluated J&K domain.
          </p>
        </div>

        {/* Non-Negotiable Isolation & Leakage Safeguards */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
          <h2 className="font-bold text-white text-sm flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-amber-400" />
            <span>Strict Predictor Isolation & Data Leakage Safeguards</span>
          </h2>
          <ul className="list-disc list-inside space-y-1 text-slate-300">
            <li>NLSM raster: Excluded from training features. Used solely for audit verification.</li>
            <li>Coordinates (Latitude / Longitude) excluded from training predictors to prevent spatial memorization.</li>
            <li>Landslide Target Labels (NGDR points & polygons) excluded from predictor stack.</li>
            <li>Exposure-only fields (hospitals, settlements, NH-44 highway) excluded from susceptibility predictors.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
