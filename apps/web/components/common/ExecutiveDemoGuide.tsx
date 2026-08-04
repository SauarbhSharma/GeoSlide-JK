"use client";

import React, { useState } from 'react';
import { Play, ChevronRight, ChevronLeft, CheckCircle2, X } from 'lucide-react';
import { useUserRole, UserRole } from '@/lib/RoleContext';

interface DemoStep {
  stepNumber: number;
  title: string;
  targetRole: UserRole;
  targetPath: string;
  description: string;
  presenterNotes: string;
}

const DEMO_STEPS: DemoStep[] = [
  {
    stepNumber: 1,
    title: 'Select Traveller / Resident Mode',
    targetRole: 'traveller',
    targetPath: '/',
    description: 'Switch to Traveller mode to present the plain-language citizen interface.',
    presenterNotes: 'Emphasize that citizens immediately see plain-language risk headlines rather than raw float32 probability numbers.',
  },
  {
    stepNumber: 2,
    title: 'Check a Location',
    targetRole: 'traveller',
    targetPath: '/location-check',
    description: 'Query slope susceptibility at a specific location or preset (e.g. Panthyal).',
    presenterNotes: 'Show how point queries return plain-language ratings with practical precautions.',
  },
  {
    stepNumber: 3,
    title: 'Explain Susceptibility Class',
    targetRole: 'traveller',
    targetPath: '/location-check',
    description: 'Explain the 5-class susceptibility rating (Very Low to Very High).',
    presenterNotes: 'Highlight that No Data is explicitly separated from Low Risk to prevent false security.',
  },
  {
    stepNumber: 4,
    title: 'Show Research Scenario Limitation',
    targetRole: 'traveller',
    targetPath: '/',
    description: 'Point out the mandatory "Research Scenario — Not an Official Warning" disclaimer.',
    presenterNotes: 'Reiterate that GeoSlide-JK does not issue binding legal road closures.',
  },
  {
    stepNumber: 5,
    title: 'Switch to Highway Operations',
    targetRole: 'highway',
    targetPath: '/',
    description: 'Switch mode to Highway Operations (NHAI).',
    presenterNotes: 'Explain that the operational focus shifts from citizen travel safety to corridor exposure screening.',
  },
  {
    stepNumber: 6,
    title: 'Show NH-44 Exposure Screening',
    targetRole: 'highway',
    targetPath: '/corridor',
    description: 'Open the NH-44 Corridor Monitor shell with 500m segment concept.',
    presenterNotes: 'Explain that segments are evaluated using "Static Road-Segment Landslide Exposure" metrics.',
  },
  {
    stepNumber: 7,
    title: 'Switch to District Administration',
    targetRole: 'district',
    targetPath: '/',
    description: 'Switch mode to District Administration (DDMA).',
    presenterNotes: 'Demonstrate pre-monsoon preparedness screening across all 20 J&K districts.',
  },
  {
    stepNumber: 8,
    title: 'Show Preparedness Screening',
    targetRole: 'district',
    targetPath: '/preparedness',
    description: 'View the pre-monsoon checklist and settlement isolation risk profile.',
    presenterNotes: 'Emphasize that suggestions support preliminary DDMA staging planning.',
  },
  {
    stepNumber: 9,
    title: 'Switch to Research / Technical',
    targetRole: 'research',
    targetPath: '/explorer',
    description: 'Switch mode to Research / Technical GIS Explorer.',
    presenterNotes: 'Show that researchers retain unrestricted access to raw rasters and layers.',
  },
  {
    stepNumber: 10,
    title: 'Show Model Validation & Transparency',
    targetRole: 'research',
    targetPath: '/transparency',
    description: 'Inspect 30-feature XGBoost metrics (Spatial CV ROC-AUC: 0.8694).',
    presenterNotes: 'Conclude by showcasing scientific rigor, leakage safeguards, and endpoint status.',
  },
];

export function ExecutiveDemoGuide() {
  const { setRole } = useUserRole();
  const [isOpen, setIsOpen] = useState(false);
  const [currentStepIdx, setCurrentStepIdx] = useState(0);

  const step = DEMO_STEPS[currentStepIdx];

  const handleGoToStep = (idx: number) => {
    setCurrentStepIdx(idx);
    const target = DEMO_STEPS[idx];
    setRole(target.targetRole);
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 z-40 bg-blue-600 hover:bg-blue-500 text-white px-3 py-2 rounded-xl text-xs font-bold shadow-2xl flex items-center space-x-2 border border-blue-400 transition-all"
        title="Open Executive Demo Guide"
      >
        <Play className="w-4 h-4" />
        <span>Executive Demo Guide</span>
      </button>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 bg-navy-900 border border-blue-500/80 rounded-2xl p-4 shadow-2xl max-w-md w-full text-xs space-y-3 backdrop-blur-md">
      <div className="flex items-center justify-between border-b border-navy-800 pb-2">
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-blue-400 animate-pulse"></span>
          <h3 className="font-bold text-white text-sm">Executive Demo Guide</h3>
          <span className="text-[10px] font-mono text-blue-300 bg-blue-950 px-2 py-0.5 rounded border border-blue-600/40">
            Step {step.stepNumber} of {DEMO_STEPS.length}
          </span>
        </div>
        <button
          onClick={() => setIsOpen(false)}
          className="text-slate-400 hover:text-white p-1 rounded hover:bg-navy-800"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="space-y-1.5">
        <h4 className="font-black text-white text-sm">{step.title}</h4>
        <p className="text-slate-300 leading-relaxed">{step.description}</p>
        <div className="bg-navy-950 p-2.5 rounded-xl border border-navy-800 text-[11px] text-amber-300 font-medium">
          <strong>Presenter Note:</strong> {step.presenterNotes}
        </div>
      </div>

      <div className="flex items-center justify-between pt-1 border-t border-navy-800">
        <button
          disabled={currentStepIdx === 0}
          onClick={() => handleGoToStep(currentStepIdx - 1)}
          className="px-3 py-1.5 bg-navy-800 hover:bg-navy-750 text-slate-200 rounded-lg font-semibold disabled:opacity-40 flex items-center space-x-1"
        >
          <ChevronLeft className="w-3.5 h-3.5" />
          <span>Previous</span>
        </button>

        <a
          href={step.targetPath}
          onClick={() => setRole(step.targetRole)}
          className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-bold flex items-center space-x-1"
        >
          <span>Go to View</span>
        </a>

        <button
          disabled={currentStepIdx === DEMO_STEPS.length - 1}
          onClick={() => handleGoToStep(currentStepIdx + 1)}
          className="px-3 py-1.5 bg-navy-800 hover:bg-navy-750 text-slate-200 rounded-lg font-semibold disabled:opacity-40 flex items-center space-x-1"
        >
          <span>Next</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
