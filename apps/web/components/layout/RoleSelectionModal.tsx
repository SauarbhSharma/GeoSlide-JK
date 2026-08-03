"use client";

import React from 'react';
import { useUserRole, UserRole } from '@/lib/RoleContext';
import { Navigation, ShieldAlert, Building2, Cpu, X, CheckCircle2 } from 'lucide-react';

interface RoleCardProps {
  id: UserRole;
  title: string;
  subtitle: string;
  description: string;
  outcome: string;
  icon: React.ReactNode;
  active: boolean;
  onSelect: (role: UserRole) => void;
}

function RoleCard({ id, title, subtitle, description, outcome, icon, active, onSelect }: RoleCardProps) {
  return (
    <div
      onClick={() => onSelect(id)}
      tabIndex={0}
      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') onSelect(id); }}
      className={`p-5 rounded-2xl border cursor-pointer transition-all flex flex-col justify-between space-y-4 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
        active
          ? 'bg-blue-950/80 border-blue-500 shadow-lg shadow-blue-900/30'
          : 'bg-navy-900/90 border-navy-700 hover:border-navy-500 hover:bg-navy-850'
      }`}
    >
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="p-2.5 rounded-xl bg-navy-800 border border-navy-700 text-blue-400">
            {icon}
          </div>
          {active && <CheckCircle2 className="w-5 h-5 text-blue-400 shrink-0" />}
        </div>
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-1.5">{title}</h3>
          <span className="text-[11px] font-mono text-blue-300 block mt-0.5">{subtitle}</span>
        </div>
        <p className="text-xs text-slate-300 leading-relaxed">{description}</p>
      </div>

      <div className="pt-3 border-t border-navy-800 space-y-3">
        <div className="text-[11px] text-slate-400">
          <strong className="text-slate-300">Expected Outcome:</strong> {outcome}
        </div>
        <button
          className={`w-full py-2 px-3 rounded-lg text-xs font-semibold transition-colors ${
            active
              ? 'bg-blue-600 hover:bg-blue-500 text-white'
              : 'bg-navy-800 hover:bg-navy-700 text-slate-200 border border-navy-700'
          }`}
        >
          {active ? 'Selected Mode' : `Switch to ${title}`}
        </button>
      </div>
    </div>
  );
}

export function RoleSelectionModal() {
  const { role, setRole, isModalOpen, setIsModalOpen } = useUserRole();

  if (!isModalOpen) return null;

  const handleSelectRole = (selectedRole: UserRole) => {
    setRole(selectedRole);
    setIsModalOpen(false);
  };

  return (
    <div className="fixed inset-0 z-[100] bg-navy-950/90 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-navy-900 border border-navy-700 rounded-3xl max-w-5xl w-full p-6 sm:p-8 space-y-6 shadow-2xl relative my-auto">
        {/* Close button if user already selected a role */}
        <button
          onClick={() => setIsModalOpen(false)}
          className="absolute top-6 right-6 p-2 text-slate-400 hover:text-white bg-navy-800 rounded-full border border-navy-700 transition-colors"
          title="Close Modal"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="text-center space-y-2 max-w-2xl mx-auto">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-950 border border-blue-500/40 text-blue-300 text-xs font-mono mb-1">
            <span>GeoSlide-JK 2.0 Role Selector</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
            How are you using GeoSlide-JK today?
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Choose a mode to view information relevant to your journey, highway operations, district preparedness or research.
          </p>
        </div>

        {/* 4 Role Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <RoleCard
            id="traveller"
            title="Traveller / Resident"
            subtitle="Commuter & Citizen Mode"
            description="Check a location, understand route exposure and view practical landslide precautions."
            outcome="Plan safe travel between Jammu & Kashmir towns with plain-language risk advisories."
            icon={<Navigation className="w-5 h-5" />}
            active={role === 'traveller'}
            onSelect={handleSelectRole}
          />

          <RoleCard
            id="highway"
            title="Highway Operations"
            subtitle="NHAI & Maintenance Mode"
            description="Review highway segments requiring monitoring and inspection."
            outcome="Chainage-indexed monitoring of NH-44 corridor slope instability exposure."
            icon={<ShieldAlert className="w-5 h-5" />}
            active={role === 'highway'}
            onSelect={handleSelectRole}
          />

          <RoleCard
            id="district"
            title="District Administration"
            subtitle="DDMA & Preparedness Mode"
            description="Identify vulnerable areas and support pre-monsoon preparedness."
            outcome="Assess district-wide slope vulnerability and vulnerable community access roads."
            icon={<Building2 className="w-5 h-5" />}
            active={role === 'district'}
            onSelect={handleSelectRole}
          />

          <RoleCard
            id="research"
            title="Research / Technical"
            subtitle="Geospatial & Model Audit Mode"
            description="Explore model outputs, geospatial layers, validation and datasets."
            outcome="Inspect 100m raster layers, 30-feature XGBoost metrics, and system status."
            icon={<Cpu className="w-5 h-5" />}
            active={role === 'research'}
            onSelect={handleSelectRole}
          />
        </div>

        {/* Footer Disclaimer */}
        <div className="pt-2 text-center text-[11px] text-slate-400 border-t border-navy-800">
          GeoSlide-JK 2.0 is a research decision-support prototype and is not an official government warning system.
        </div>
      </div>
    </div>
  );
}
