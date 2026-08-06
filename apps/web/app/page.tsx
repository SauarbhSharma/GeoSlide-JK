"use client";

import React from 'react';
import { useUserRole } from '@/lib/RoleContext';
import { Header } from '@/components/layout/Header';
import { TravellerDashboard } from '@/components/dashboard/TravellerDashboard';
import { HighwayOpsDashboard } from '@/components/dashboard/HighwayOpsDashboard';
import { DistrictAdminDashboard } from '@/components/dashboard/DistrictAdminDashboard';
import { ResearchDashboard } from '@/components/dashboard/ResearchDashboard';

export default function Home() {
  const { role } = useUserRole();

  const renderDashboard = () => {
    switch (role) {
      case 'traveller':
        return <TravellerDashboard />;
      case 'highway':
        return <HighwayOpsDashboard />;
      case 'district':
        return <DistrictAdminDashboard />;
      case 'research':
      default:
        return <ResearchDashboard />;
    }
  };

  return (
    <div className="flex flex-col h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <Header />
      <main className="flex-1 flex overflow-hidden relative">
        {renderDashboard()}
      </main>
    </div>
  );
}
