"use client";

import React from 'react';
import { AlertTriangle, Info, CheckCircle2, ShieldAlert, Clock, MapPin, FileText } from 'lucide-react';

export type AdvisoryLevel = 'green' | 'yellow' | 'orange' | 'red';

export interface AdvisoryPayload {
  id: string;
  level: AdvisoryLevel;
  location: string;
  reason: string;
  suggestedAction: string;
  confidence: string;
  source: string;
  issuedTime: string;
  expiryTime: string;
  verificationStatus: string;
}

interface AdvisoryCardProps {
  advisory: AdvisoryPayload;
}

export function AdvisoryCard({ advisory }: AdvisoryCardProps) {
  const levelMeta: Record<AdvisoryLevel, { title: string; color: string; badgeColor: string; icon: React.ReactNode }> = {
    green: {
      title: 'Green — Normal Baseline Risk',
      color: 'border-emerald-500/60 bg-emerald-950/40 text-emerald-200',
      badgeColor: 'bg-emerald-900 border-emerald-600/50 text-emerald-100',
      icon: <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />,
    },
    yellow: {
      title: 'Yellow — Watch & Caution',
      color: 'border-amber-500/60 bg-amber-950/40 text-amber-200',
      badgeColor: 'bg-amber-900 border-amber-600/50 text-amber-100',
      icon: <Info className="w-5 h-5 text-amber-400 shrink-0" />,
    },
    orange: {
      title: 'Orange — High Relative Risk',
      color: 'border-orange-500/60 bg-orange-950/40 text-orange-200',
      badgeColor: 'bg-orange-900 border-orange-600/50 text-orange-100',
      icon: <AlertTriangle className="w-5 h-5 text-orange-400 shrink-0" />,
    },
    red: {
      title: 'Red — Critical Exposure',
      color: 'border-rose-500/60 bg-rose-950/40 text-rose-200',
      badgeColor: 'bg-rose-900 border-rose-600/50 text-rose-100',
      icon: <ShieldAlert className="w-5 h-5 text-rose-400 shrink-0" />,
    },
  };

  const meta = levelMeta[advisory.level] || levelMeta.yellow;

  return (
    <div className={`p-4 sm:p-5 rounded-2xl border ${meta.color} space-y-3 shadow-xl backdrop-blur-md`}>
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-navy-800/80 pb-2.5">
        <div className="flex items-center space-x-2">
          {meta.icon}
          <h3 className="font-bold text-sm sm:text-base text-white">{meta.title}</h3>
        </div>
        <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono border ${meta.badgeColor}`}>
          {advisory.verificationStatus || 'Research Advisory'}
        </span>
      </div>

      {/* Location & Reason */}
      <div className="space-y-1.5 text-xs">
        <div className="flex items-center space-x-1.5 text-slate-200 font-semibold">
          <MapPin className="w-3.5 h-3.5 text-blue-400 shrink-0" />
          <span>Location: {advisory.location}</span>
        </div>
        <p className="text-slate-300 leading-relaxed font-normal">{advisory.reason}</p>
      </div>

      {/* Suggested Action */}
      <div className="bg-navy-950/80 p-3 rounded-xl border border-navy-800 text-xs space-y-1">
        <span className="font-bold text-slate-200 block text-[11px] uppercase tracking-wider">
          Suggested Action:
        </span>
        <p className="text-slate-300 font-medium">{advisory.suggestedAction}</p>
      </div>

      {/* 9 Mandatory Schema Attributes */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 text-[11px] text-slate-400 border-t border-navy-800/80 font-mono">
        <div>
          <span className="text-slate-400 block text-[10px]">Confidence:</span>
          <span className="text-slate-200 font-bold">{advisory.confidence || 'Not currently available'}</span>
        </div>
        <div>
          <span className="text-slate-400 block text-[10px]">Data Source:</span>
          <span className="text-slate-200 font-bold">{advisory.source || 'GeoSlide-JK 100m Grid'}</span>
        </div>
        <div>
          <span className="text-slate-400 block text-[10px]">Issued Time:</span>
          <span className="text-slate-200">{advisory.issuedTime || 'Not currently available'}</span>
        </div>
        <div>
          <span className="text-slate-400 block text-[10px]">Expiry Window:</span>
          <span className="text-slate-200">{advisory.expiryTime || 'Not currently available'}</span>
        </div>
      </div>

      {/* Mandatory Disclaimer */}
      <div className="text-[10px] text-slate-400 font-mono border-t border-navy-800/60 pt-2 text-center">
        ⚠️ Research Advisory — Not an Official Government Warning
      </div>
    </div>
  );
}
