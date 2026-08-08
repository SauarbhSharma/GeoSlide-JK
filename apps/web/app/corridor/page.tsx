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
  source: string;
}

interface SegmentRobustnessData {
  chainage: string;
  name: string;
  length: string;
  nativeCellId: string;
  supportNodeId: string;
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
  stability: 'STABLE_CONSENSUS' | 'MODERATE_AGREEMENT' | 'FORMULATION_SENSITIVE' | 'DRY_CONTROL_UNRANKED' | 'NON_DISCRIMINATING_COMPLETE_TIE';
  structureType: 'SURFACE' | 'TUNNEL' | 'BRIDGE';
  structureNote: string;
}

export default function CorridorPage() {
  const scenarios: ScenarioInfo[] = [
    { id: 'S0', name: 'S0 — DRY_REFERENCE', class: 'DRY_CONTROL', r24: '0 mm', r72: '0 mm', api7: '0 mm', basis: 'Zero Rainfall Baseline (Unranked Control)', source: 'configs/rainfall_thresholds.yaml' },
    { id: 'S1', name: 'S1 — MODERATE_RAIN', class: 'CLIMATOLOGY_DERIVED_REFERENCE', r24: '25 mm', r72: '45 mm', api7: '15 mm', basis: 'July Monsoon P50 Baseline', source: 'nh44_rainfall_climatology_percentiles.parquet' },
    { id: 'S2', name: 'S2 — HEAVY_24H', class: 'CLIMATOLOGY_DERIVED_REFERENCE', r24: '75 mm', r72: '110 mm', api7: '35 mm', basis: 'July Monsoon P90 Baseline', source: 'nh44_rainfall_climatology_percentiles.parquet' },
    { id: 'S3', name: 'S3 — PROLONGED_72H', class: 'CLIMATOLOGY_DERIVED_REFERENCE', r24: '90 mm', r72: '150 mm', api7: '55 mm', basis: 'July Monsoon P95 Baseline', source: 'nh44_rainfall_climatology_percentiles.parquet' },
    { id: 'S4', name: 'S4 — SATURATED_ANTECEDENT', class: 'COMPOUND_STRESS_TEST', r24: '120 mm', r72: '180 mm', api7: '95 mm', basis: 'High Antecedent + Heavy 24h Compound Basis', source: 'configs/rainfall_thresholds.yaml' },
    { id: 'S5', name: 'S5 — EXTREME_COMPOUND', class: 'SYNTHETIC_STRESS_TEST', r24: '160 mm', r72: '250 mm', api7: '140 mm', basis: 'P99 Compound Synthetic Stress Test', source: 'configs/rainfall_thresholds.yaml' },
  ];

  const [selectedScenario, setSelectedScenario] = useState<ScenarioInfo>(scenarios[2]); // Default S2 Heavy 24h
  const [selectedFormulation, setSelectedFormulation] = useState<'CONSENSUS' | 'DHI_A' | 'DHI_B' | 'DHI_C' | 'DHI_D'>('CONSENSUS');

  const sampleSegments: SegmentRobustnessData[] = [
    { chainage: 'Km 142.0 – 142.5', name: 'Panthyal Cut-Slope', length: '500 m', nativeCellId: 'GPM_NATIVE_33.25N_75.15E', supportNodeId: 'SUPPORT_NODE_33.25N_75.14E', cellSegments: 98, dhiA: 0.5032, dhiB: 0.5032, dhiC: 0.5032, dhiD: 0.7094, pctA: 50.32, pctB: 50.32, pctC: 50.32, consensusPct: 50.32, pctRange: 0.0, stability: 'NON_DISCRIMINATING_COMPLETE_TIE', structureType: 'SURFACE', structureNote: 'Direct cut slope surface exposure' },
    { chainage: 'Km 148.0 – 148.5', name: 'Ramban Bypass Sector', length: '500 m', nativeCellId: 'GPM_NATIVE_33.25N_75.15E', supportNodeId: 'SUPPORT_NODE_33.25N_75.14E', cellSegments: 98, dhiA: 0.5032, dhiB: 0.5032, dhiC: 0.5032, dhiD: 0.7094, pctA: 50.32, pctB: 50.32, pctC: 50.32, consensusPct: 50.32, pctRange: 0.0, stability: 'NON_DISCRIMINATING_COMPLETE_TIE', structureType: 'SURFACE', structureNote: 'Direct cut slope surface exposure' },
    { chainage: 'Km 153.0 – 153.5', name: 'Digdol Landslide Zone', length: '500 m', nativeCellId: 'GPM_NATIVE_33.25N_75.15E', supportNodeId: 'SUPPORT_NODE_33.25N_75.16E', cellSegments: 98, dhiA: 0.5032, dhiB: 0.5032, dhiC: 0.5032, dhiD: 0.7094, pctA: 50.32, pctB: 50.32, pctC: 50.32, consensusPct: 50.32, pctRange: 0.0, stability: 'NON_DISCRIMINATING_COMPLETE_TIE', structureType: 'SURFACE', structureNote: 'Direct cut slope surface exposure' },
    { chainage: 'Km 165.5 – 166.0', name: 'T5 Tunnel Interior', length: '500 m', nativeCellId: 'GPM_NATIVE_33.25N_75.15E', supportNodeId: 'SUPPORT_NODE_33.25N_75.18E', cellSegments: 98, dhiA: 0.5032, dhiB: 0.5032, dhiC: 0.5032, dhiD: 0.7094, pctA: 50.32, pctB: 50.32, pctC: 50.32, consensusPct: 50.32, pctRange: 0.0, stability: 'NON_DISCRIMINATING_COMPLETE_TIE', structureType: 'TUNNEL', structureNote: 'SURFACE_HAZARD_INTERPRETATION_LIMITED: Subsurface tunnel crown decouples surface runoff' },
    { chainage: 'Km 178.0 – 178.5', name: 'Banihal River Viaduct', length: '500 m', nativeCellId: 'GPM_NATIVE_33.25N_75.25E', supportNodeId: 'SUPPORT_NODE_33.25N_75.22E', cellSegments: 60, dhiA: 0.5032, dhiB: 0.5032, dhiC: 0.5032, dhiD: 0.7094, pctA: 50.32, pctB: 50.32, pctC: 50.32, consensusPct: 50.32, pctRange: 0.0, stability: 'NON_DISCRIMINATING_COMPLETE_TIE', structureType: 'BRIDGE', structureNote: 'ELEVATED_STRUCTURE_CONTEXT: Elevated deck over river crossing' },
  ];

  const [selectedSeg, setSelectedSeg] = useState<SegmentRobustnessData>(sampleSegments[0]);
  const isDryControl = selectedScenario.id === 'S0';

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header />
      <ResearchDisclaimer />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6 space-y-6">
        {/* Page Title & Status */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 text-xs font-semibold bg-amber-900/50 text-amber-300 border border-amber-700/50 rounded-full">
                V2-3F-R8A1 CANDIDATE
              </span>
              <span className="text-xs text-slate-400 font-mono">
                Candidate Branch: geoslide-jk-v2-nh44-v2-3f-r8a1-clean-clone-scientific-correction
              </span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white mt-1">
              NH-44 Corridor Dynamic Hazard Index (DHI) Explorer
            </h1>
            <p className="text-sm text-amber-400/90 font-mono mt-1">
              REPOSITORY_DECLARED_IMERG_COMPATIBLE_ANALYSIS_GRID — EMPIRICAL RASTER PROVENANCE NOT PROVEN
            </p>
            <p className="text-sm text-slate-400">
              158 Corridor Segments | 11 Native 2D GPM Cells (33.0°N..33.5°N) | Static Susceptibility Baseline
            </p>
          </div>
          
          <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 p-1.5 rounded-lg text-xs">
            <span className="text-slate-400 px-2 font-medium">Formulation Mode:</span>
            {(['CONSENSUS', 'DHI_A', 'DHI_B', 'DHI_C', 'DHI_D'] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => setSelectedFormulation(mode)}
                className={`px-2.5 py-1 rounded font-medium transition-all ${
                  selectedFormulation === mode
                    ? 'bg-emerald-500 text-slate-950 shadow'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {mode === 'CONSENSUS' ? '3-Formulation Consensus' : mode}
                {mode === 'DHI_D' && ' (Audit)'}
              </button>
            ))}
          </div>
        </div>

        {/* Audit Disclosure Banner */}
        <div className="bg-emerald-950/30 border border-emerald-800/40 rounded-xl p-4 text-xs text-emerald-300 space-y-1">
          <div className="font-semibold text-emerald-200 flex items-center gap-1.5">
            <Info className="w-4 h-4 text-emerald-400" />
            Authoritative V2-3F-R4 Dynamic Hazard Disclosures & Truthfulness
          </div>
          <p>
            - **2 Native GPM 0.1° Cells:** Corridor segments intersect exactly 2 native 0.1° (~11 km) GPM IMERG grid cells (98 segments in cell 75.15°E, 60 segments in cell 75.25°E). The 8 locations are derived 0.02° corridor-support interpolation nodes.
          </p>
          <p>
            - **Zero-Variance Within-Scenario Rank Correlation:** Uniform corridor-wide scenario rainfall broadcasting yields constant DHI values within each scenario S1–S5. Within-scenario rank correlation is mathematically undefined (`status = UNDEFINED_ZERO_VARIANCE`).
          </p>
          <p>
            - **Redundant DHI_D Excluded:** `DHI_D = sqrt(DHI_B)` with 0.0 residual is strictly excluded from all consensus, range, and stability calculations.
          </p>
          <p>
            - **Research Purpose:** Dynamic Hazard Indicators are for relative scenario screening. No live forecasts, alert levels, emergency warnings, or road-closure recommendations are issued.
          </p>
        </div>

        {/* Scenario Selection Grid */}
        <div>
          <h2 className="text-sm font-semibold text-slate-300 mb-3 flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-emerald-400" />
            Select Dynamic Rainfall Scenario (S0 – S5)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {scenarios.map((sc) => {
              const isSelected = selectedScenario.id === sc.id;
              return (
                <button
                  key={sc.id}
                  onClick={() => setSelectedScenario(sc)}
                  className={`flex flex-col justify-between text-left p-3 rounded-lg border text-xs transition-all ${
                    isSelected
                      ? 'bg-slate-900 border-emerald-500/80 shadow-md shadow-emerald-500/5 ring-1 ring-emerald-500/50'
                      : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-300'
                  }`}
                >
                  <div>
                    <div className="font-bold text-slate-200 flex items-center justify-between mb-1">
                      <span>{sc.id}</span>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${
                        sc.id === 'S0' ? 'bg-slate-800 text-slate-400' : 'bg-emerald-500/10 text-emerald-400'
                      }`}>
                        {sc.r24}
                      </span>
                    </div>
                    <div className="text-[11px] font-medium text-slate-300 truncate">{sc.name.split('—')[1]?.trim()}</div>
                    <div className="text-[10px] text-slate-500 mt-1">{sc.class}</div>
                  </div>
                  <div className="mt-2 pt-2 border-t border-slate-800/80 text-[10px] text-slate-400">
                    <div>R72: {sc.r72} | API7: {sc.api7}</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Main Content Split */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Segment List */}
          <div className="lg:col-span-2 space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className="font-semibold text-slate-200">Sample Segment Inventory (158 Total)</span>
              <span className="text-xs text-slate-400">Scenario: {selectedScenario.id} | Mode: {selectedFormulation}</span>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950/80 text-slate-400 font-medium border-b border-slate-800">
                    <tr>
                      <th className="p-3">Chainage / Name</th>
                      <th className="p-3">Native Cell / Support Node</th>
                      <th className="p-3 text-right">DHI Value</th>
                      <th className="p-3 text-right">Percentile</th>
                      <th className="p-3 text-center">Stability Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-slate-300">
                    {sampleSegments.map((seg) => {
                      const isSelected = selectedSeg.chainage === seg.chainage;
                      return (
                        <tr
                          key={seg.chainage}
                          onClick={() => setSelectedSeg(seg)}
                          className={`cursor-pointer transition-colors ${
                            isSelected ? 'bg-emerald-500/10 text-emerald-200' : 'hover:bg-slate-800/40'
                          }`}
                        >
                          <td className="p-3">
                            <div className="font-medium text-slate-200">{seg.name}</div>
                            <div className="text-[10px] text-slate-500 font-mono">{seg.chainage}</div>
                          </td>
                          <td className="p-3 font-mono text-[10px] text-slate-400">
                            <div>{seg.nativeCellId}</div>
                            <div className="text-slate-500">{seg.supportNodeId} ({seg.cellSegments} segs)</div>
                          </td>
                          <td className="p-3 text-right font-mono font-medium">
                            {isDryControl ? '0.00' : seg.dhiA.toFixed(4)}
                          </td>
                          <td className="p-3 text-right font-mono font-semibold text-emerald-400">
                            {isDryControl ? 'UNRANKED' : `${seg.consensusPct.toFixed(1)}%`}
                          </td>
                          <td className="p-3 text-center">
                            <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-semibold border ${
                              isDryControl
                                ? 'bg-slate-800 text-slate-400 border-slate-700'
                                : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                            }`}>
                              {isDryControl ? 'DRY_CONTROL' : 'COMPLETE_TIE'}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Inspector Panel */}
          <div className="space-y-4">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <h3 className="font-bold text-slate-100 text-sm">{selectedSeg.name}</h3>
                  <div className="text-xs text-slate-400 font-mono">{selectedSeg.chainage}</div>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300">
                  {selectedSeg.structureType}
                </span>
              </div>

              {/* Formulation Breakdown */}
              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-300">DHI Formulation Values & Percentiles</div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-slate-950 p-2 rounded border border-slate-800 font-mono">
                    <div className="text-[10px] text-slate-500">DHI_A (Linear)</div>
                    <div className="text-slate-200 font-bold">{isDryControl ? '0.0000' : selectedSeg.dhiA.toFixed(4)}</div>
                  </div>
                  <div className="bg-slate-950 p-2 rounded border border-slate-800 font-mono">
                    <div className="text-[10px] text-slate-500">DHI_B (Percentile)</div>
                    <div className="text-slate-200 font-bold">{isDryControl ? '0.0000' : selectedSeg.dhiB.toFixed(4)}</div>
                  </div>
                  <div className="bg-slate-950 p-2 rounded border border-slate-800 font-mono">
                    <div className="text-[10px] text-slate-500">DHI_C (Upper Tail P90)</div>
                    <div className="text-slate-200 font-bold">{isDryControl ? '0.0000' : selectedSeg.dhiC.toFixed(4)}</div>
                  </div>
                  <div className="bg-slate-950 p-2 rounded border border-slate-800 font-mono">
                    <div className="text-[10px] text-slate-500">DHI_D (sqrt Audit)</div>
                    <div className="text-slate-400">{isDryControl ? '0.0000' : selectedSeg.dhiD.toFixed(4)}</div>
                  </div>
                </div>
              </div>

              {/* Structural Context Note */}
              <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800/80 text-xs text-slate-400 space-y-1">
                <div className="font-semibold text-slate-300">Engineering Structure Context</div>
                <p>{selectedSeg.structureNote}</p>
              </div>

              {/* Native Cell Provenance */}
              <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800/80 text-xs text-slate-400 space-y-1 font-mono">
                <div className="font-semibold text-slate-300 font-sans">Native Grid Provenance</div>
                <div>Native Cell: {selectedSeg.nativeCellId} (0.1°)</div>
                <div>Support Node: {selectedSeg.supportNodeId} (0.02°)</div>
                <div>Assigned Segments: {selectedSeg.cellSegments} Corridor Segments</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
