"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Shield, Layers, CloudRain, CheckCircle } from 'lucide-react';

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
              <span className="font-bold text-lg tracking-wide text-white">GeoSlide-JK v1.0.0</span>
              <span className="bg-blue-900/60 border border-blue-500/30 text-blue-300 text-xs px-2 py-0.5 rounded font-mono">
                Research Decision-Support Prototype
              </span>
            </div>
            <p className="text-xs text-slate-300">Terrain Intelligence & Rainfall-Triggered Landslide Risk</p>
          </div>
        </div>

        {/* System Badges */}
        <div className="hidden lg:flex items-center space-x-2.5">
          <div className="flex items-center space-x-1.5 bg-emerald-950/70 border border-emerald-600/70 text-emerald-200 text-xs px-2.5 py-1 rounded-md font-medium shadow-sm">
            <Layers className="w-3.5 h-3.5 text-emerald-400" />
            <span>Static Susceptibility Model: Trained</span>
          </div>
          <div className="flex items-center space-x-1.5 bg-amber-950/70 border border-amber-600/70 text-amber-200 text-xs px-2.5 py-1 rounded-md font-medium shadow-sm">
            <CloudRain className="w-3.5 h-3.5 text-amber-400" />
            <span>Dynamic Hazard: Scenario / Proxy Mode</span>
          </div>
          <div className="flex items-center space-x-1.5 bg-sky-950/70 border border-sky-600/70 text-sky-200 text-xs px-2.5 py-1 rounded-md font-medium shadow-sm">
            <CheckCircle className="w-3.5 h-3.5 text-sky-400" />
            <span>20 J&K UT Districts</span>
          </div>
        </div>
      </div>

      {/* Navigation Bar */}
      <nav className="flex items-center space-x-1 px-4 overflow-x-auto border-t border-navy-800 text-xs font-semibold">
        {navItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link
              key={item.path}
              href={item.path}
              className={`px-3 py-2 border-b-2 whitespace-nowrap transition-colors ${
                isActive
                  ? 'border-blue-500 text-white bg-navy-800/90 font-bold'
                  : 'border-transparent text-slate-300 hover:text-white hover:bg-navy-800/40'
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
