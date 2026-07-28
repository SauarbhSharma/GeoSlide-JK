"use client";

import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { FileText, Cpu, CheckCircle2, Layers, AlertCircle, BarChart3 } from 'lucide-react';

export default function ModelTransparency() {
  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-4 max-w-7xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-purple-600/20 text-purple-400 p-2 rounded-lg border border-purple-500/30">
              <Cpu className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Model & Data Transparency</h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Methodology, spatial validation strategy, SHAP explainability rules, and model cards.
              </p>
            </div>
          </div>
          <div className="text-xs font-mono bg-navy-800 border border-navy-700 px-3 py-1.5 rounded-lg text-slate-300">
            Model Version: XGBoost v0.1.0-prototype
          </div>
        </div>

        {/* Transparency Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Spatial Cross Validation */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <h2 className="font-bold text-white text-sm">Spatial Block Cross-Validation</h2>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              To prevent spatial autocorrelation leakage, training and validation splits are strictly grouped by spatial block clusters and district holdouts. Samples from the same landslide polygon are never split across train and test sets.
            </p>
            <div className="bg-navy-950 border border-navy-800 p-3 rounded-lg text-xs font-mono space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-400">Target ROC-AUC:</span>
                <span className="text-emerald-400 font-bold">&gt; 0.85 (Spatial CV)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Target PR-AUC:</span>
                <span className="text-emerald-400 font-bold">&gt; 0.75</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Primary Predictor Grid:</span>
                <span className="text-white">100m UTM (EPSG:32643)</span>
              </div>
            </div>
          </div>

          {/* Predictor Feature Importance */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-3">
            <div className="flex items-center space-x-2 border-b border-navy-800 pb-2">
              <BarChart3 className="w-4 h-4 text-blue-400" />
              <h2 className="font-bold text-white text-sm">Global SHAP Feature Drivers</h2>
            </div>
            <div className="space-y-2 text-xs">
              <div>
                <div className="flex justify-between text-slate-300 font-mono text-[11px] mb-1">
                  <span>Slope Steepness (slope_deg)</span>
                  <span className="text-blue-400 font-bold">34% Importance</span>
                </div>
                <div className="w-full h-2 bg-navy-800 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full" style={{ width: '34%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-slate-300 font-mono text-[11px] mb-1">
                  <span>Distance to Fault/Thrust (dist_fault_m)</span>
                  <span className="text-blue-400 font-bold">22% Importance</span>
                </div>
                <div className="w-full h-2 bg-navy-800 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full" style={{ width: '22%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-slate-300 font-mono text-[11px] mb-1">
                  <span>Antecedent Rainfall Index (IMERG / IMD)</span>
                  <span className="text-blue-400 font-bold">19% Importance</span>
                </div>
                <div className="w-full h-2 bg-navy-800 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full" style={{ width: '19%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-slate-300 font-mono text-[11px] mb-1">
                  <span>Lithology Class (50k GSI)</span>
                  <span className="text-blue-400 font-bold">15% Importance</span>
                </div>
                <div className="w-full h-2 bg-navy-800 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full" style={{ width: '15%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Non-Negotiable Isolation Rules */}
        <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-2 text-xs">
          <h2 className="font-bold text-white text-sm flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-amber-400" />
            <span>Strict Predictor Isolation Rules</span>
          </h2>
          <ul className="list-disc list-inside space-y-1 text-slate-300">
            <li>The pre-existing NLSM susceptibility raster is strictly isolated and used <strong>only for benchmark validation</strong>. It is never used as an input feature for training models.</li>
            <li>Coordinates (Latitude/Longitude) are excluded from training to prevent geographic memorization.</li>
            <li>Missing data areas are explicitly assigned an <strong>Insufficient Data</strong> mask, never categorized as Low Risk.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
