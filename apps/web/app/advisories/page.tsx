"use client";

import React from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { AdvisoryCard, AdvisoryPayload } from '@/components/common/AdvisoryCard';
import { AlertTriangle } from 'lucide-react';

export default function AdvisoriesPage() {
  const sampleAdvisories: AdvisoryPayload[] = [
    {
      id: 'adv-01',
      level: 'orange',
      location: 'NH-44 Mountain Corridor (Udhampur – Ramban – Banihal Sector)',
      reason: 'Research Scenario: Elevated terrain slope instability exposure detected along mountain highway cut-slopes under dynamic 24h rainfall proxy scenarios.',
      suggestedAction: 'Research Scenario: Verify official advisories (@JKTrafficPolice) before transit. Precautionary monitoring suggested for field patrols.',
      confidence: 'Moderate (XGBoost ROC 0.8694 + 100m Orographic Proxy)',
      source: 'GeoSlide-JK 100m Master Grid (v1.0.0 Pipeline)',
      issuedTime: 'Today 08:00 IST',
      expiryTime: 'Research Scenario Window',
      verificationStatus: 'Research Scenario — Not an Official Government Warning',
    },
    {
      id: 'adv-02',
      level: 'yellow',
      location: 'Mughal Road (Rajouri – Shopian Corridor via Peer Ki Gali)',
      reason: 'Research Scenario: Moderate baseline slope vulnerability across high-elevation mountain passes.',
      suggestedAction: 'Research Scenario: Exercise caution during intense or prolonged rainfall. Verify pass opening status before departure.',
      confidence: 'Moderate (Copernicus DEM 30m Morphometrics)',
      source: 'GeoSlide-JK 100m Master Grid',
      issuedTime: 'Today 08:00 IST',
      expiryTime: 'Research Scenario Window',
      verificationStatus: 'Research Scenario — Not an Official Government Warning',
    },
    {
      id: 'adv-03',
      level: 'green',
      location: 'Jammu – Udhampur Expressway Sector',
      reason: 'Slope instability parameters remain within baseline normal thresholds.',
      suggestedAction: 'Normal travel precautions apply. Maintain standard highway speeds and distance.',
      confidence: 'High (Verified 100m Susceptibility Raster)',
      source: 'GeoSlide-JK 100m Master Grid',
      issuedTime: 'Today 08:00 IST',
      expiryTime: 'Research Scenario Window',
      verificationStatus: 'Verified Baseline',
    },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-navy-950 text-slate-100">
      <Header />
      <main className="flex-1 p-4 max-w-5xl mx-auto w-full space-y-4">
        <ResearchDisclaimer />

        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl space-y-2 shadow-xl">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <h1 className="text-xl sm:text-2xl font-black text-white">Active Research Advisories</h1>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed max-w-2xl">
            Standardized 4-tier risk advisories (Green, Yellow, Orange, Red) generated from 100m slope susceptibility rasters and dynamic rainfall scenarios. All outputs are research prototypes and not official government warnings.
          </p>
        </div>

        <div className="space-y-4">
          {sampleAdvisories.map((adv) => (
            <AdvisoryCard key={adv.id} advisory={adv} />
          ))}
        </div>
      </main>
    </div>
  );
}
