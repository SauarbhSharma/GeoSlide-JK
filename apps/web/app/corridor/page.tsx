"use client";

import React, { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { Activity, ShieldAlert, Layers, ChevronRight, AlertTriangle, Info, Database } from 'lucide-react';

interface ScenarioInfo {
  id: string;
  name: string;
  class: string;
  r24: string;
  r72: string;
  api7: string;
  basis: string;
}

interface SegmentRobustnessData {
  chainage: string;
  name: string;
  length: string;
  cellId: string;
  cellSegments: number;
  dhiA: number;
  dhiB: number;
  dhiC: number;
  dhiD: number;
  pctA: number;
  pctB: number;
  pctC: number;
  consensusPct: number;
  pctRange: number;
  stability: 'STABLE_CONSENSUS' | 'MODERATE_AGREEMENT' | 'FORMULATION_SENSITIVE' | 'DRY_CONTROL_UNRANKED';
  structureType: 'SURFACE' | 'TUNNEL' | 'BRIDGE';
  structureNote: string;
}

export default function CorridorPage() {
  const scenarios: ScenarioInfo[] = [
    { id: 'S0', name: 'S0 — DRY_REFERENCE', class: 'DRY_CONTROL', r24: '0 mm', r72: '0 mm', api7: '0 mm', basis: 'Zero Rainfall Baseline (Unranked Control)' },
    { id: 'S1', name: 'S1 — MODERATE_RAIN', class: 'CLIMATOLOGY_DERIVED_REFERENCE', r24: '25 mm', r72: '45 mm', api7: '15 mm', basis: 'July Monsoon P50 Baseline' },
    { id: 'S2', name: 'S2 — HEAVY_24H', class: 'CLIMATOLOGY_DERIVED_REFERENCE', r24: '75 mm', r72: '110 mm', api7: '35 mm', basis: 'July Monsoon P90 Baseline' },
    { id: 'S3', name: 'S3 — PROLONGED_72H', class: 'CLIMATOLOGY_DERIVED_REFERENCE', r24: '90 mm', r72: '150 mm', api7: '55 mm', basis: 'July Monsoon P95 Baseline' },
    { id: 'S4', name: 'S4 — SATURATED_ANTECEDENT', class: 'CLIMATOLOGY_DERIVED_REFERENCE', r24: '120 mm', r72: '180 mm', api7: '95 mm', basis: 'High Antecedent + Heavy 24h' },
    { id: 'S5', name: 'S5 — EXTREME_COMPOUND', class: 'SYNTHETIC_STRESS_TEST', r24: '160 mm', r72: '250 mm', api7: '140 mm', basis: 'P99 Compound Stress Test' },
  ];

  const [selectedScenario, setSelectedScenario] = useState<ScenarioInfo>(scenarios[2]); // Default S2 Heavy 24h
  const [selectedFormulation, setSelectedFormulation] = useState<'CONSENSUS' | 'DHI_A' | 'DHI_B' | 'DHI_C' | 'DHI_D'>('CONSENSUS');

  const sampleSegments: SegmentRobustnessData[] = [
    { chainage: 'Km 142.0 – 142.5', name: 'Panthyal Cut-Slope', length: '500 m', cellId: 'GPM_CELL_33.25N_75.14E', cellSegments: 20, dhiA: 0.74, dhiB: 0.68, dhiC: 0.76, dhiD: 0.82, pctA: 98.1, pctB: 94.3, pctC: 96.8, consensusPct: 96.8, pctRange: 3.8, stability: 'STABLE_CONSENSUS', structureType: 'SURFACE', structureNote: 'Direct cut slope surface exposure' },
    { chainage: 'Km 148.0 – 148.5', name: 'Ramban Bypass Sector', length: '500 m', cellId: 'GPM_CELL_33.25N_75.14E', cellSegments: 20, dhiA: 0.68, dhiB: 0.62, dhiC: 0.70, dhiD: 0.79, pctA: 92.4, pctB: 88.6, pctC: 91.1, consensusPct: 91.1, pctRange: 3.8, stability: 'STABLE_CONSENSUS', structureType: 'SURFACE', structureNote: 'Direct cut slope surface exposure' },
    { chainage: 'Km 153.0 – 153.5', name: 'Digdol Landslide Zone', length: '500 m', cellId: 'GPM_CELL_33.25N_75.16E', cellSegments: 22, dhiA: 0.65, dhiB: 0.58, dhiC: 0.69, dhiD: 0.76, pctA: 87.3, pctB: 81.0, pctC: 89.2, consensusPct: 87.3, pctRange: 8.2, stability: 'STABLE_CONSENSUS', structureType: 'SURFACE', structureNote: 'Direct cut slope surface exposure' },
    { chainage: 'Km 165.5 – 166.0', name: 'T5 Tunnel Interior', length: '500 m', cellId: 'GPM_CELL_33.25N_75.18E', cellSegments: 19, dhiA: 0.58, dhiB: 0.52, dhiC: 0.61, dhiD: 0.72, pctA: 74.1, pctB: 69.6, pctC: 76.6, consensusPct: 74.1, pctRange: 7.0, stability: 'STABLE_CONSENSUS', structureType: 'TUNNEL', structureNote: 'SURFACE_HAZARD_INTERPRETATION_LIMITED: Subsurface tunnel crown decouples surface runoff' },
    { chainage: 'Km 178.0 – 178.5', name: 'Banihal River Viaduct', length: '500 m', cellId: 'GPM_CELL_33.25N_75.22E', cellSegments: 18, dhiA: 0.42, dhiB: 0.38, dhiC: 0.46, dhiD: 0.62, pctA: 48.1, pctB: 42.4, pctC: 51.9, consensusPct: 48.1, pctRange: 9.5, stability: 'STABLE_CONSENSUS', structureType: 'BRIDGE', structureNote: 'ELEVATED_STRUCTURE_CONTEXT: Elevated deck over river crossing' },
  ];

  const [selectedSeg, setSelectedSeg] = useState<SegmentRobustnessData>(sampleSegments[0]);
  const isDryControl = selectedScenario.id === 'S0';

  return (
    <div className="flex flex-col min-h-screen bg-navy-950 text-slate-100">
      <Header />
      <main className="flex-1 p-4 max-w-6xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-2 shadow-xl">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-sky-400" />
            <h1 className="text-xl sm:text-2xl font-black text-white">NH-44 Dynamic Hazard Robustness & Consensus Monitor</h1>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed max-w-3xl">
            Chainage-indexed 500m segment evaluation of <strong>Dynamic Hazard Index (DHI) Robustness, Consensus, and Native Grid Cell Support</strong> along the 78.6 km NH-44 corridor.
          </p>
        </div>

        {/* Mandatory Research Truthfulness Notice */}
        <div className="bg-navy-950 border border-sky-500/50 p-4 rounded-2xl text-xs space-y-1">
          <div className="flex items-center space-x-2 text-sky-300 font-bold">
            <Info className="w-4 h-4 shrink-0 text-sky-400" />
            <span>Research Scenario Screening Truthfulness Notice</span>
          </div>
          <p className="text-slate-300 leading-relaxed">
            “Research scenario screening only. Scenarios S1–S4 are climatology-derived, S5 is a synthetic stress test, and S0 is a dry control. These are not observed events, forecasts, alerts, emergency warnings, or road-closure recommendations. Rainfall forcing comes from eight native 0.1-degree cells shared by multiple road segments.”
          </p>
        </div>

        {/* Controls Panel */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Scenario Selector */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <Database className="w-4 h-4 text-sky-400" /> Select Research Scenario (S0–S5)
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 bg-navy-950 text-sky-300 border border-navy-700 rounded-md">
                {selectedScenario.class}
              </span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {scenarios.map((sc) => (
                <button
                  key={sc.id}
                  onClick={() => setSelectedScenario(sc)}
                  className={`p-2.5 rounded-xl border text-left text-xs transition-all ${
                    selectedScenario.id === sc.id
                      ? 'bg-sky-600 border-sky-400 text-white font-bold shadow-md'
                      : 'bg-navy-950 border-navy-800 text-slate-300 hover:bg-navy-850'
                  }`}
                >
                  <div className="font-bold">{sc.name}</div>
                  <div className="text-[10px] opacity-80 font-mono mt-0.5">24h: {sc.r24} | 72h: {sc.r72}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Formulation Selector */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <Layers className="w-4 h-4 text-amber-400" /> Select Formulation View
              </span>
              <span className="text-[10px] font-mono text-slate-400">
                3 Independent | 1 Audit Redundant
              </span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                onClick={() => setSelectedFormulation('CONSENSUS')}
                className={`p-2.5 rounded-xl border text-left font-bold ${
                  selectedFormulation === 'CONSENSUS'
                    ? 'bg-amber-600 border-amber-400 text-white shadow-md'
                    : 'bg-navy-950 border-navy-800 text-slate-300 hover:bg-navy-850'
                }`}
              >
                <div>Median Consensus</div>
                <div className="text-[10px] font-normal text-slate-200 mt-0.5">Median of DHI_A, B, C</div>
              </button>
              <button
                onClick={() => setSelectedFormulation('DHI_A')}
                className={`p-2.5 rounded-xl border text-left ${
                  selectedFormulation === 'DHI_A'
                    ? 'bg-sky-600 border-sky-400 text-white font-bold shadow-md'
                    : 'bg-navy-950 border-navy-800 text-slate-300 hover:bg-navy-850'
                }`}
              >
                <div>DHI_A (Linear Product)</div>
                <div className="text-[10px] opacity-80 mt-0.5">Static × Trigger Ratio</div>
              </button>
              <button
                onClick={() => setSelectedFormulation('DHI_B')}
                className={`p-2.5 rounded-xl border text-left ${
                  selectedFormulation === 'DHI_B'
                    ? 'bg-sky-600 border-sky-400 text-white font-bold shadow-md'
                    : 'bg-navy-950 border-navy-800 text-slate-300 hover:bg-navy-850'
                }`}
              >
                <div>DHI_B (Percentile Mod)</div>
                <div className="text-[10px] opacity-80 mt-0.5">Static × Trigger Pct</div>
              </button>
              <button
                onClick={() => setSelectedFormulation('DHI_C')}
                className={`p-2.5 rounded-xl border text-left ${
                  selectedFormulation === 'DHI_C'
                    ? 'bg-sky-600 border-sky-400 text-white font-bold shadow-md'
                    : 'bg-navy-950 border-navy-800 text-slate-300 hover:bg-navy-850'
                }`}
              >
                <div>DHI_C (Upper-Tail P90)</div>
                <div className="text-[10px] opacity-80 mt-0.5">P90 Static × Trigger Pct</div>
              </button>
            </div>
            <div className="text-[10px] text-slate-400 bg-navy-950 p-2 rounded-lg border border-navy-800">
              * Note: <strong>DHI_D</strong> is verified as a strictly monotonic transformation of DHI_B (Spearman = 1.000) and is excluded from consensus to prevent redundant weighting.
            </div>
          </div>
        </div>

        {/* Dry Control Alert State */}
        {isDryControl && (
          <div className="bg-navy-900 border border-amber-500/50 p-4 rounded-2xl text-xs space-y-1">
            <div className="flex items-center space-x-2 text-amber-300 font-bold">
              <AlertTriangle className="w-4 h-4 shrink-0 text-amber-400" />
              <span>DRY_CONTROL_NO_DYNAMIC_DISCRIMINATION</span>
            </div>
            <p className="text-slate-300 leading-relaxed">
              Under Scenario S0 (Dry Control 0 mm), all rainfall forcing is zero across the corridor. Relative dynamic segment rankings are disabled because zero rainfall provides no spatial dynamic discrimination.
            </p>
          </div>
        )}

        {/* Corridor Segment Detail Card */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl md:col-span-2 space-y-4">
            <div className="flex items-center justify-between border-b border-navy-800 pb-3">
              <div>
                <span className="text-[10px] text-sky-400 font-mono uppercase tracking-wider">
                  Selected Segment Robustness & Native Cell Profile
                </span>
                <h3 className="text-xl font-black text-white">{selectedSeg.name}</h3>
                <div className="text-xs text-slate-300 font-mono">{selectedSeg.chainage} ({selectedSeg.length})</div>
              </div>
              <span className="px-3 py-1 bg-sky-950 border border-sky-600/50 text-sky-300 font-bold text-xs rounded-xl font-mono">
                {isDryControl ? 'DRY_CONTROL_UNRANKED' : selectedSeg.stability}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3 text-xs">
              <div className="bg-navy-950 p-3 rounded-xl border border-navy-800">
                <span className="text-slate-400">Consensus Percentile:</span>
                <div className="text-base font-bold text-sky-400 mt-0.5 font-mono">
                  {isDryControl ? 'N/A' : `${selectedSeg.consensusPct.toFixed(1)}%`}
                </div>
              </div>
              <div className="bg-navy-950 p-3 rounded-xl border border-navy-800">
                <span className="text-slate-400">Formulation Spread:</span>
                <div className="text-base font-bold text-amber-400 mt-0.5 font-mono">
                  {isDryControl ? '0.0%' : `±${(selectedSeg.pctRange / 2).toFixed(1)}%`}
                </div>
              </div>
              <div className="bg-navy-950 p-3 rounded-xl border border-navy-800">
                <span className="text-slate-400">Native Cell Segments:</span>
                <div className="text-base font-bold text-emerald-400 mt-0.5 font-mono">
                  {selectedSeg.cellSegments} Segments
                </div>
              </div>
            </div>

            {/* Structure Context & Native Cell Drawer */}
            <div className="bg-navy-950 p-4 rounded-xl border border-navy-800 space-y-2 text-xs">
              <span className="font-bold text-slate-200 block text-[11px] uppercase tracking-wider">
                Native Grid Cell & Structure Decoupling Details:
              </span>
              <div className="space-y-1 font-mono text-[11px] text-slate-300">
                <div>• Intersecting Native Cell: <strong className="text-sky-300">{selectedSeg.cellId}</strong></div>
                <div>• Native Support Note: {selectedSeg.cellSegments} corridor segments share this native 0.1° cell's rainfall value.</div>
                <div>• Structure Context: <strong className="text-amber-300">{selectedSeg.structureType}</strong> — {selectedSeg.structureNote}</div>
              </div>
            </div>
          </div>

          {/* Priority Queue / Segment Selector */}
          <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-3">
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Representative Corridor Segments
            </h3>
            <div className="space-y-2 text-xs">
              {sampleSegments.map((s, idx) => (
                <div
                  key={s.chainage}
                  onClick={() => setSelectedSeg(s)}
                  className={`p-2.5 rounded-xl border cursor-pointer flex items-center justify-between transition-all ${
                    selectedSeg.chainage === s.chainage
                      ? 'bg-sky-600 border-sky-400 text-white font-bold shadow-md'
                      : 'bg-navy-950 border-navy-800 text-slate-300 hover:bg-navy-850'
                  }`}
                >
                  <div>
                    <div className="font-bold">#{idx + 1} {s.name}</div>
                    <div className="text-[10px] opacity-80 font-mono">{s.chainage}</div>
                  </div>
                  <span className="font-mono text-sky-300">
                    {isDryControl ? 'N/A' : `${s.consensusPct.toFixed(0)}%`}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
