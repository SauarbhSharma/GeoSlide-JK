"use client";

import React from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { DistrictAdminDashboard } from '@/components/dashboard/DistrictAdminDashboard';

export default function VulnerablePage() {
  return (
    <div className="flex flex-col min-h-screen bg-navy-950 text-slate-100">
      <Header />
      <main className="flex-1 flex overflow-hidden relative">
        <DistrictAdminDashboard />
      </main>
    </div>
  );
}
