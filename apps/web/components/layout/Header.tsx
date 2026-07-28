"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Shield, Activity, Database, Info, Map, AlertTriangle, CloudRain, CheckCircle } from 'lucide-react';

export function Header() {
  const pathname = usePathname();

  const navItems = [
    { label: 'Statewide Command Centre', path: '/' },
    { label: 'Risk Explorer', path: '/explorer' },
    { label: 'District Intelligence', path: '/districts' },
    { label: 'Rainfall Monitor', path: '/rainfall' },
    { label: 'Location Risk Check', path: '/location-check' },
    { label: 'Model Transparency', path: '/transparency' },
    { label: 'Data & System Status', path: '/status' },
  ];

  return (
    <header className="bg-navy-900 border-b border-navy-700 text-slate-100 sticky top-0 z-50">
      <div className="flex items-center justify-between px-4 py-2.5">
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="bg-blue-600/20 border border-blue-500/40 p-2 rounded-lg text-blue-400">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-wide text-white">GeoSlide J&K</span>
              <span className="bg-blue-900/60 border border-blue-500/30 text-blue-300 text-xs px-2 py-0.5 rounded font-mono">
                v0.1.0 Prototype
              </span>
            </div>
            <p className="text-xs text-slate-400">Terrain Intelligence & Rainfall-Triggered Landslide Risk</p>
          </div>
        </div>

        {/* System Badges */}
        <div className="hidden lg:flex items-center space-x-3">
          <div className="flex items-center space-x-1.5 bg-amber-950/40 border border-amber-600/40 text-amber-300 text-xs px-2.5 py-1 rounded-md">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>Research Prototype</span>
          </div>
          <div className="flex items-center space-x-1.5 bg-blue-950/40 border border-blue-600/40 text-blue-300 text-xs px-2.5 py-1 rounded-md">
            <CloudRain className="w-3.5 h-3.5" />
            <span>Demo Playback (July 2026 Sample)</span>
          </div>
          <div className="flex items-center space-x-1.5 bg-emerald-950/40 border border-emerald-600/40 text-emerald-300 text-xs px-2.5 py-1 rounded-md">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>20 Districts Verified</span>
          </div>
        </div>
      </div>

      {/* Navigation Bar */}
      <nav className="flex items-center space-x-1 px-4 overflow-x-auto border-t border-navy-800 text-xs font-medium">
        {navItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link
              key={item.path}
              href={item.path}
              className={`px-3 py-2 border-b-2 whitespace-nowrap transition-colors ${
                isActive
                  ? 'border-blue-500 text-white bg-navy-800/80 font-semibold'
                  : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-navy-800/40'
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </header>
  );
}
