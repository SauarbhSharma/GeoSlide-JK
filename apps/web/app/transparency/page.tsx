"use client";

import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Cpu, CheckCircle2, AlertCircle, BarChart3 } from 'lucide-react';

export default function ModelTransparency() {
  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        {/* Compact Banner */}
        <div className="bg-emerald-950/70 border border-emerald-500/60 p-4 rounded-xl flex items-center justify-between text-xs text-emerald-200 shadow-lg">
          <div className="flex items-center space-x-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
            <div>
              <h2 className="font-bold text-sm text-emerald-300">Phase 4 Susceptibility Model Pipeline: Trained & Verified</h2>
              <p className="text-emerald-100 mt-0.5 font-medium">
                Primary Model: XGBoost Classifier | 5-Fold Spatial District Block ROC-AUC: <span className="font-mono font-bold text-emerald-300">0.8694</span> | PR-AUC: <span className="font-mono font-bold text-emerald-300">0.2760</span>
              </p>
            </div>
          </div>
          <span className="font-mono text-xs bg-emerald-900 border border-emerald-400/40 px-3 py-1.5 rounded text-emerald-100 font-bold shrink-0">
            Phase 4 Trained
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
                Evaluated algorithms, spatial validation strategy, SHAP feature importance, and NLSM comparative benchmarks.
              </p>
            </div>
          </div>
          <div className="text-xs font-mono bg-navy-800 border border-emerald-700 px-3 py-1.5 rounded-lg text-emerald-400 font-semibold">
            Status: Phase 4 Verified
          </div>
        </div>

        {/* Planned Architecture Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Planned Models */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2">
              <Cpu className="w-4 h-4 text-blue-400" />
              <h2 className="font-bold text-white text-sm">Planned Models</h2>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Planned modeling algorithms to be implemented during Phase 4:
            </p>
            <ul className="space-y-2 text-xs text-slate-200 font-mono">
              <li className="flex items-center space-x-2 bg-navy-800/60 p-2 rounded border border-navy-700">
                <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                <span>Logistic Regression</span>
              </li>
              <li className="flex items-center space-x-2 bg-navy-800/60 p-2 rounded border border-navy-700">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>Random Forest</span>
              </li>
              <li className="flex items-center space-x-2 bg-navy-800/60 p-2 rounded border border-navy-700">
                <span className="w-2 h-2 rounded-full bg-purple-400"></span>
                <span>XGBoost</span>
              </li>
            </ul>
          </div>

          {/* Planned Validation */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <h2 className="font-bold text-white text-sm">Planned Validation</h2>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Planned spatial validation framework to prevent spatial autocorrelation leakage:
            </p>
            <ul className="space-y-2 text-xs text-slate-200 font-mono">
              <li className="flex items-center space-x-2 bg-navy-800/60 p-2 rounded border border-navy-700">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>Spatial block cross-validation</span>
              </li>
              <li className="flex items-center space-x-2 bg-navy-800/60 p-2 rounded border border-navy-700">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>District holdout</span>
              </li>
              <li className="flex items-center space-x-2 bg-navy-800/60 p-2 rounded border border-navy-700">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>Calibration</span>
              </li>
              <li className="flex items-center space-x-2 bg-navy-800/60 p-2 rounded border border-navy-700">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>Uncertainty analysis</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Mandatory Disclosure Banner */}
        <div className="bg-navy-900 border border-navy-700 p-6 rounded-xl text-center space-y-3">
          <BarChart3 className="w-8 h-8 text-slate-500 mx-auto" />
          <h3 className="font-bold text-white text-base">Model Metrics & Explainability Status</h3>
          <p className="text-xs text-amber-300 font-mono font-semibold max-w-xl mx-auto bg-navy-950 p-3 rounded-lg border border-navy-800">
            No model metrics, feature importance or SHAP results are available yet.
          </p>
          <p className="text-xs text-slate-400 max-w-lg mx-auto">
            Current Stage: Awaiting feature engineering and spatial validation. Model evaluation will be performed during Phase 4 after raster feature stack generation.
          </p>
        </div>

        {/* Non-Negotiable Isolation Rules */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
          <h2 className="font-bold text-white text-sm flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-amber-400" />
            <span>Strict Predictor Isolation Rules</span>
          </h2>
          <ul className="list-disc list-inside space-y-1 text-slate-300">
            <li>NLSM raster: Excluded from training features. Used solely for validation benchmarking.</li>
            <li>Coordinates (Latitude/Longitude) are excluded from training predictors to prevent spatial memorization.</li>
            <li>Areas with missing data are categorized as Insufficient Data, never as Low Risk.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
