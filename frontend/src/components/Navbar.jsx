import React, { useState } from 'react';
import { Zap, Menu, X } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, backendStatus }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Clean navigation links without any "MODE 1/2/3" badges
  const navItems = [
    { id: 'home', label: 'Overview' },
    { id: 'gap-analysis', label: 'Syllabus Gap Audit' },
    { id: 'intelligence', label: 'Industry Intelligence' },
    { id: 'career-path', label: 'Career Pathways' },
  ];

  const isOnline = backendStatus?.online;
  const modelName = backendStatus?.data?.model || 'Gemini 3.6 Flash';

  return (
    <header className="sticky top-0 z-50 w-full backdrop-blur-md bg-zinc-950/75 border-b border-zinc-800/80 px-6 lg:px-8 py-3.5 transition-colors">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Left: Brand Identity */}
        <div 
          className="flex items-center gap-3 cursor-pointer select-none group"
          onClick={() => setActiveTab('home')}
        >
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-zinc-900 border border-zinc-800 group-hover:border-zinc-700 transition-colors">
            <Zap className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold tracking-tight text-zinc-100 group-hover:text-white transition-colors">
              SkillPulse AI
            </span>
            <span className="text-[10px] font-mono text-zinc-400 px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">
              SIH26134
            </span>
          </div>
        </div>

        {/* Center: Minimal Text Navigation Links (No Clunky Badges) */}
        <nav className="hidden md:flex items-center gap-1.5">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`text-sm font-medium transition-all duration-150 px-3.5 py-1.5 rounded-lg ${
                  isActive
                    ? 'text-white bg-zinc-900 border border-zinc-700/60 shadow-sm'
                    : 'text-zinc-400 hover:text-white hover:bg-zinc-900/50'
                }`}
              >
                {item.label}
              </button>
            );
          })}
        </nav>

        {/* Right: Compact Green Pill Status Indicator */}
        <div className="hidden sm:flex items-center">
          {isOnline ? (
            <div 
              className="flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900/90 border border-zinc-800 text-xs text-zinc-300 cursor-default hover:border-zinc-700 transition-colors"
              title={`FastAPI Gateway on Port 8000 • ${modelName}`}
            >
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span className="font-medium text-xs text-zinc-200">System Live</span>
            </div>
          ) : (
            <div 
              className="flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900/90 border border-rose-500/30 text-xs text-rose-400 cursor-default"
              title="FastAPI Backend unreachable on port 8000"
            >
              <span className="h-2 w-2 rounded-full bg-rose-500"></span>
              <span className="font-medium text-xs">System Offline</span>
            </div>
          )}
        </div>

        {/* Mobile Toggle Button */}
        <div className="flex md:hidden">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-900 transition-colors"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden mt-3 pt-3 border-t border-zinc-800/80 space-y-1">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  setMobileMenuOpen(false);
                }}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'text-white bg-zinc-900 border border-zinc-800'
                    : 'text-zinc-400 hover:text-white hover:bg-zinc-900/40'
                }`}
              >
                {item.label}
              </button>
            );
          })}

          <div className="pt-2 mt-2 border-t border-zinc-800/60 flex items-center justify-between px-3 py-1 text-xs text-zinc-400">
            <span>Status:</span>
            <span className={isOnline ? 'text-emerald-400 font-mono' : 'text-rose-400 font-mono'}>
              {isOnline ? 'System Live' : 'System Offline'}
            </span>
          </div>
        </div>
      )}
    </header>
  );
}
