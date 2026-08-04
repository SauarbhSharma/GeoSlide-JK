"use client";

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/layout/Header';
import { ResearchDisclaimer } from '@/components/layout/ResearchDisclaimer';
import { TrustStatusComponent } from '@/components/common/TrustStatusComponent';
import { ShieldAlert, Activity, CheckCircle2, MapPin, Info, ArrowRight, Layers, FileText } from 'lucide-react';

interface SegmentDetail {
  segment_id: string;
  sequence_number: number;
  start_chainage_km: number;
  end_chainage_km: number;
  segment_length_m: number;
  district_primary: string;
  districts_intersected: string;
  start_coords: { latitude: number; longitude: number };
  end_coords: { latitude: number; longitude: number };
  geometry_source: string;
  geometry_version: string;
  data_quality_status: string;
  exposure_status: string;
  lhs_score?: number | null;
  dis_score?: number | null;
  ips_score?: number | null;
}

export default function CorridorMonitorPage() {
  const [corridorInfo, setCorridorInfo] = useState<{
    corridor_name: string;
    verified_length_km: number;
    verified_segment_count: number;
    geometry_version: string;
    data_quality_status: string;
  }>({
    corridor_name: 'NH-44 Jammu-Srinagar Highway Pilot Corridor',
    verified_length_km: 74.88,
    verified_segment_count: 150,
    geometry_version: '2.3A',
    data_quality_status: 'Verified Continuous Geometry'
  });

  const [segments, setSegments] = useState<SegmentDetail[]>([]);
  const [selectedSegId, setSelectedSegId] = useState<string>('NH44-JK-0001');
  const [selectedSegDetail, setSelectedSegDetail] = useState<SegmentDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

  useEffect(() => {
    async function fetchCorridorData() {
      try {
        const infoRes = await fetch(`${apiBaseUrl}/api/v1/corridors/nh44`);
        if (infoRes.ok) {
          const data = await infoRes.json();
          setCorridorInfo({
            corridor_name: data.corridor_name || 'NH-44 Jammu-Srinagar Highway Pilot Corridor',
            verified_length_km: data.verified_length_km || 74.88,
            verified_segment_count: data.verified_segment_count || 150,
            geometry_version: data.geometry_version || '2.3A',
            data_quality_status: data.data_quality_status || 'Verified Continuous Geometry'
          });
        }

        const segsRes = await fetch(`${apiBaseUrl}/api/v1/corridors/nh44/segments?limit=200`);
        if (segsRes.ok) {
          const segsData = await segsRes.json();
          setSegments(segsData.segments || []);
        }
      } catch (err) {
        console.warn('API fetch warning, using fallback local segment dataset');
      } finally {
        setLoading(false);
      }
    }

    fetchCorridorData();
  }, [apiBaseUrl]);

  useEffect(() => {
    async function fetchSegDetail() {
      try {
        const res = await fetch(`${apiBaseUrl}/api/v1/corridors/nh44/segments/${selectedSegId}`);
        if (res.ok) {
          const detail = await res.json();
          setSelectedSegDetail(detail);
        }
      } catch (err) {
        // Fallback local match
        const localMatch = segments.find(s => s.segment_id === selectedSegId);
        if (localMatch) {
          setSelectedSegDetail({
            ...localMatch,
            exposure_status: 'Not yet calculated (Checkpoint V2-3B)'
          });
        }
      }
    }

    fetchSegDetail();
  }, [selectedSegId, apiBaseUrl, segments]);

  return (
    <div className="min-h-screen bg-navy-950 text-slate-100 flex flex-col font-sans">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 space-y-4">
        <ResearchDisclaimer />

        {/* Page Header */}
        <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full bg-amber-950 border border-amber-600/50 text-amber-300 text-[11px] font-mono">
                Highway Operations Screening Shell (NHAI)
              </span>
              <TrustStatusComponent compact />
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-white tracking-tight">
              NH-44 Landslide Exposure Screening
            </h1>
            <p className="text-xs text-slate-300 max-w-3xl leading-relaxed">
              Screen static slope susceptibility along verified 500m corridor chainage segments across Udhampur, Ramban, and Banihal sectors.
            </p>
          </div>

          <div className="flex items-center space-x-2 shrink-0">
            <div className="bg-navy-950 p-2.5 px-3 rounded-xl border border-navy-800 text-xs font-mono">
              <span className="text-slate-400 block text-[10px]">CORRIDOR VERSION</span>
              <span className="text-emerald-400 font-bold">{corridorInfo.geometry_version} ({corridorInfo.data_quality_status})</span>
            </div>
          </div>
        </div>

        {/* Verified Metadata Overview Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 text-xs font-medium">Verified Pilot Corridor Length</span>
            <div className="text-2xl font-black text-white font-mono">
              {corridorInfo.verified_length_km} km
            </div>
            <span className="text-[10px] text-emerald-400 font-mono">Udhampur–Ramban–Banihal Sector</span>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 text-xs font-medium">Verified 500m Segment Count</span>
            <div className="text-2xl font-black text-amber-400 font-mono">
              {corridorInfo.verified_segment_count} Segments
            </div>
            <span className="text-[10px] text-slate-400 font-mono">NH44-JK-0001 to NH44-JK-0150</span>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 text-xs font-medium">Geometric CRS & Basis</span>
            <div className="text-lg font-bold text-slate-200 font-mono">
              EPSG:32643
            </div>
            <span className="text-[10px] text-slate-400 font-mono">UTM Zone 43N Projected Distance</span>
          </div>

          <div className="bg-navy-900 border border-navy-700 p-4 rounded-xl space-y-1">
            <span className="text-slate-400 text-xs font-medium">Exposure Scoring Status</span>
            <div className="text-sm font-bold text-amber-300 font-mono mt-1">
              Checkpoint V2-3B Target
            </div>
            <span className="text-[10px] text-amber-400 font-mono">Exposure calculation begins in V2-3B</span>
          </div>
        </div>

        {/* Segment Selector & Detail Inspector Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Segment Selector List */}
          <div className="bg-navy-900 border border-navy-700 p-4 rounded-2xl space-y-3 flex flex-col max-h-[500px]">
            <div className="flex items-center justify-between border-b border-navy-800 pb-2">
              <h2 className="text-xs font-bold text-white uppercase tracking-wider">
                Candidate 500m Segments
              </h2>
              <span className="text-[10px] font-mono text-slate-400">
                {segments.length > 0 ? `${segments.length} loaded` : '150 verified'}
              </span>
            </div>

            <div className="space-y-1.5 overflow-y-auto flex-1 pr-1">
              {segments.map((seg) => {
                const isSelected = seg.segment_id === selectedSegId;
                return (
                  <div
                    key={seg.segment_id}
                    onClick={() => setSelectedSegId(seg.segment_id)}
                    className={`p-2.5 rounded-xl border text-xs cursor-pointer flex items-center justify-between transition-all font-mono ${
                      isSelected
                        ? 'bg-amber-600 border-amber-500 text-white font-bold shadow-md'
                        : 'bg-navy-800/60 border-navy-700 text-slate-300 hover:bg-navy-800 hover:text-white'
                    }`}
                  >
                    <div>
                      <div className="font-bold">{seg.segment_id}</div>
                      <div className="text-[10px] opacity-80">
                        KM {seg.start_chainage_km.toFixed(1)} – {seg.end_chainage_km.toFixed(1)}
                      </div>
                    </div>
                    <div className="text-right text-[10px]">
                      <span className="px-1.5 py-0.5 rounded bg-navy-950/80 border border-navy-700 block">
                        {seg.district_primary}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Segment Detail Inspector */}
          <div className="bg-navy-900 border border-navy-700 p-5 rounded-2xl md:col-span-2 space-y-4 flex flex-col justify-between shadow-xl">
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-navy-800 pb-3">
                <div>
                  <span className="text-[10px] font-mono text-amber-400 uppercase tracking-wider block">
                    Selected 500m Highway Segment
                  </span>
                  <h2 className="text-2xl font-black text-white font-mono">
                    {selectedSegId}
                  </h2>
                </div>
                <div className="px-3 py-1 rounded-xl bg-navy-950 border border-navy-800 text-xs font-mono text-emerald-400">
                  {corridorInfo.data_quality_status}
                </div>
              </div>

              {selectedSegDetail ? (
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                  <div className="bg-navy-950 p-3 rounded-xl border border-navy-800 space-y-0.5">
                    <span className="text-slate-400 text-[10px]">Chainage Span</span>
                    <div className="font-bold text-white font-mono text-sm">
                      {selectedSegDetail.start_chainage_km.toFixed(3)} – {selectedSegDetail.end_chainage_km.toFixed(3)} km
                    </div>
                  </div>

                  <div className="bg-navy-950 p-3 rounded-xl border border-navy-800 space-y-0.5">
                    <span className="text-slate-400 text-[10px]">Segment Length</span>
                    <div className="font-bold text-white font-mono text-sm">
                      {selectedSegDetail.segment_length_m} meters
                    </div>
                  </div>

                  <div className="bg-navy-950 p-3 rounded-xl border border-navy-800 space-y-0.5">
                    <span className="text-slate-400 text-[10px]">Administrative District</span>
                    <div className="font-bold text-amber-400 text-sm">
                      {selectedSegDetail.district_primary}
                    </div>
                  </div>

                  <div className="bg-navy-950 p-3 rounded-xl border border-navy-800 space-y-0.5">
                    <span className="text-slate-400 text-[10px]">Start Coordinates</span>
                    <div className="font-mono text-slate-300 text-[11px]">
                      {selectedSegDetail.start_coords?.latitude.toFixed(4)}°N, {selectedSegDetail.start_coords?.longitude.toFixed(4)}°E
                    </div>
                  </div>

                  <div className="bg-navy-950 p-3 rounded-xl border border-navy-800 space-y-0.5">
                    <span className="text-slate-400 text-[10px]">End Coordinates</span>
                    <div className="font-mono text-slate-300 text-[11px]">
                      {selectedSegDetail.end_coords?.latitude.toFixed(4)}°N, {selectedSegDetail.end_coords?.longitude.toFixed(4)}°E
                    </div>
                  </div>

                  <div className="bg-navy-950 p-3 rounded-xl border border-navy-800 space-y-0.5">
                    <span className="text-slate-400 text-[10px]">Geometry Source</span>
                    <div className="text-slate-300 text-[11px] font-mono truncate">
                      {selectedSegDetail.geometry_source || 'GeoSlide-JK Processed'}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="p-8 text-center text-slate-400 text-xs">
                  Loading segment details...
                </div>
              )}

              {/* Exposure Calculation Status Banner */}
              <div className="bg-navy-950 p-4 rounded-xl border border-amber-600/40 space-y-2">
                <div className="flex items-center space-x-2 font-bold text-amber-300 text-xs">
                  <Info className="w-4 h-4 shrink-0 text-amber-400" />
                  <span>Landslide Hazard Exposure Status</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Exposure calculation begins in Checkpoint V2-3B. Susceptibility score ($LHS$), Disruption Impact Score ($DIS$), and Intervention Priority Score ($IPS$) will be computed across 100m COG rasters during V2-3B.
                </p>
                <div className="grid grid-cols-3 gap-2 pt-1 font-mono text-[11px]">
                  <div className="p-2 rounded bg-navy-900 border border-navy-800 text-slate-400 text-center">
                    LHS: Not yet calculated
                  </div>
                  <div className="p-2 rounded bg-navy-900 border border-navy-800 text-slate-400 text-center">
                    DIS: Not yet calculated
                  </div>
                  <div className="p-2 rounded bg-navy-900 border border-navy-800 text-slate-400 text-center">
                    IPS: Not yet calculated
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-2 text-[11px] text-slate-400 border-t border-navy-800">
              NH-44 Highway Operations Screening Shell — GeoSlide-JK 2.0 Checkpoint V2-3A Foundation
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
