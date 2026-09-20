import React from 'react';
import { ExternalLink } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-zinc-800/80 bg-[#09090b] mt-16 py-8 text-xs text-zinc-500">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        
        {/* Left Branding */}
        <div className="flex items-center gap-2">
          <span className="font-semibold text-zinc-300">SkillPulse AI</span>
          <span className="text-zinc-600">•</span>
          <span className="font-mono text-zinc-500">SIH26134</span>
        </div>

        {/* Center */}
        <div className="text-center sm:text-left text-zinc-500 text-[11px]">
          Smart India Hackathon 2026 • Aligning Higher Education with Emerging Market Demand
        </div>

        {/* Right Links */}
        <div className="flex items-center gap-4 text-zinc-400">
          <a 
            href="http://localhost:8000/api/v1/docs" 
            target="_blank" 
            rel="noreferrer"
            className="flex items-center gap-1 hover:text-zinc-200 transition-colors"
          >
            <span>FastAPI Docs</span>
            <ExternalLink className="w-3 h-3" />
          </a>
          <span className="text-zinc-700">•</span>
          <span className="text-zinc-500 font-mono">Gemini 3.6 Flash</span>
        </div>

      </div>
    </footer>
  );
}
