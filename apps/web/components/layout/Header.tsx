"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useUserRole, UserRole } from '@/lib/RoleContext';
import { Navigation, ShieldAlert, Building2, Cpu, ChevronDown, Menu, X } from 'lucide-react';

export function Header() {
  const pathname = usePathname();
  const { role, setRole, openRoleModal } = useUserRole();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Role-specific navigation tabs
  const getNavItems = () => {
    switch (role) {
      case 'traveller':
        return [
          { label: 'Home', path: '/' },
          { label: 'Check Area', path: '/location-check' },
          { label: 'Plan Journey', path: '/journey' },
          { label: 'Advisories', path: '/advisories' },
          { label: 'Help', path: '/help' },
        ];
      case 'highway':
        return [
          { label: 'Operations Overview', path: '/' },
          { label: 'Corridor Monitor', path: '/corridor' },
          { label: 'Priority Segments', path: '/corridor#priority' },
          { label: 'Preparedness', path: '/preparedness' },
          { label: 'Reports', path: '/reports' },
        ];
      case 'district':
        return [
          { label: 'District Overview', path: '/districts' },
          { label: 'Vulnerable Areas', path: '/vulnerable' },
          { label: 'Preparedness', path: '/preparedness' },
          { label: 'Advisories', path: '/advisories' },
          { label: 'Reports', path: '/reports' },
        ];
      case 'research':
      default:
        return [
          { label: 'Risk Explorer', path: '/explorer' },
          { label: 'Districts', path: '/districts' },
          { label: 'Rainfall', path: '/rainfall' },
          { label: 'Model Transparency', path: '/transparency' },
          { label: 'Data & System Status', path: '/status' },
        ];
    }
  };

  const navItems = getNavItems();

  const roleMeta: Record<UserRole, { title: string; icon: React.ReactNode; color: string }> = {
    traveller: { title: 'Traveller / Resident', icon: <Navigation className="w-3.5 h-3.5" />, color: 'bg-emerald-950 text-emerald-300 border-emerald-600/50' },
    highway: { title: 'Highway Operations', icon: <ShieldAlert className="w-3.5 h-3.5" />, color: 'bg-amber-950 text-amber-300 border-amber-600/50' },
    district: { title: 'District Administration', icon: <Building2 className="w-3.5 h-3.5" />, color: 'bg-purple-950 text-purple-300 border-purple-600/50' },
    research: { title: 'Research / Technical', icon: <Cpu className="w-3.5 h-3.5" />, color: 'bg-blue-950 text-blue-300 border-blue-600/50' },
  };

  const currentRole = roleMeta[role] || roleMeta.traveller;

  return (
    <header className="bg-navy-900 border-b border-navy-700 text-slate-100 sticky top-0 z-50">
      <div className="flex items-center justify-between px-3 sm:px-4 py-2">
        {/* Brand */}
        <div className="flex items-center space-x-2 sm:space-x-3 shrink-0">
          <Link href="/" className="flex items-center shrink-0" title="GeoSlide-JK Home">
            <img
              src="/branding/geoslide-jk-emblem.png"
              alt="GeoSlide-JK — Landslide Risk Intelligence"
              className="h-7 sm:h-9 md:h-10 w-auto object-contain drop-shadow-md shrink-0"
              onError={(e) => {
                (e.currentTarget as HTMLElement).style.display = 'none';
              }}
            />
          </Link>
          <div>
            <div className="flex items-center space-x-1.5 sm:space-x-2">
              <span className="font-bold text-sm sm:text-base md:text-lg tracking-wide text-white">GeoSlide-JK v2.0</span>
              <span className="bg-blue-900/60 border border-blue-500/30 text-blue-300 text-[10px] sm:text-xs px-1.5 py-0.5 rounded font-mono hidden sm:inline-block">
                Research Prototype
              </span>
            </div>
            <p className="text-[10px] sm:text-xs text-slate-300">Landslide Risk Intelligence</p>
          </div>
        </div>

        {/* Role Switcher & Mobile Menu Trigger */}
        <div className="flex items-center space-x-2">
          {/* Role Switcher Dropdown */}
          <div className="relative">
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className={`flex items-center space-x-1.5 border px-2.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${currentRole.color}`}
            >
              {currentRole.icon}
              <span className="hidden sm:inline">{currentRole.title}</span>
              <ChevronDown className="w-3.5 h-3.5 opacity-75" />
            </button>

            {dropdownOpen && (
              <div className="absolute right-0 mt-2 w-56 bg-navy-900 border border-navy-700 rounded-xl shadow-2xl z-50 py-1.5 overflow-hidden">
                <div className="px-3 py-1.5 text-[10px] font-mono text-slate-400 uppercase tracking-wider border-b border-navy-800">
                  Switch Active Role Mode
                </div>
                {(Object.keys(roleMeta) as UserRole[]).map((r) => (
                  <button
                    key={r}
                    onClick={() => {
                      setRole(r);
                      setDropdownOpen(false);
                    }}
                    className={`w-full text-left px-3 py-2 text-xs flex items-center space-x-2 hover:bg-navy-800 transition-colors ${
                      role === r ? 'font-bold text-white bg-navy-800/60' : 'text-slate-300'
                    }`}
                  >
                    {roleMeta[r].icon}
                    <span>{roleMeta[r].title}</span>
                  </button>
                ))}
                <div className="border-t border-navy-800 mt-1 pt-1 px-1">
                  <button
                    onClick={() => {
                      setDropdownOpen(false);
                      openRoleModal();
                    }}
                    className="w-full text-center px-3 py-1.5 text-xs text-blue-400 hover:text-blue-300 font-semibold"
                  >
                    Open Role Selection Modal
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Mobile Menu Toggle Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-1.5 rounded-lg bg-navy-800 border border-navy-700 text-slate-300 hover:text-white"
            title="Toggle Mobile Navigation"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Desktop Navigation Bar */}
      <nav className="hidden md:flex items-center space-x-1 px-4 border-t border-navy-800 text-xs font-semibold">
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

      {/* Mobile Menu Overlay */}
      {mobileMenuOpen && (
        <nav className="md:hidden border-t border-navy-800 bg-navy-950 p-2 space-y-1 text-xs">
          {navItems.map((item) => {
            const isActive = pathname === item.path;
            return (
              <Link
                key={item.path}
                href={item.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`block px-3 py-2 rounded-lg font-semibold transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white font-bold'
                    : 'text-slate-300 hover:bg-navy-800 hover:text-white'
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      )}
    </header>
  );
}
