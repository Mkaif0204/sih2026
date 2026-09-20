import React from 'react';

export default function MetricCard({ label, value, delta, icon: Icon }) {
  return (
    <div className="bg-zinc-900/50 hover:bg-zinc-900/70 border border-zinc-800/80 hover:border-zinc-700/80 rounded-xl p-5 transition-all duration-150 flex flex-col justify-between space-y-4">
      <div className="flex items-center justify-between gap-2">
        <span className="text-xs font-medium text-zinc-400">
          {label}
        </span>
        {Icon && (
          <div className="w-7 h-7 rounded-md bg-zinc-800/50 border border-zinc-700/40 flex items-center justify-center text-zinc-400">
            <Icon className="w-3.5 h-3.5" />
          </div>
        )}
      </div>

      <div className="flex items-baseline justify-between">
        <span className="text-2xl sm:text-3xl font-bold tracking-tight text-zinc-100">
          {value}
        </span>
        {delta && (
          <span className="text-[11px] font-mono font-medium px-2 py-0.5 rounded bg-zinc-950 border border-zinc-800 text-zinc-300">
            {delta}
          </span>
        )}
      </div>
    </div>
  );
}
