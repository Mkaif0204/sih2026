import React from 'react';

export default function DonutChart({ score = 55, label = 'Alignment', size = 140 }) {
  const normalizedScore = Math.max(0, Math.min(100, score));

  let strokeColor = '#EF4444'; // Rose

  if (normalizedScore >= 75) {
    strokeColor = '#10B981'; // Emerald
  } else if (normalizedScore >= 50) {
    strokeColor = '#6366F1'; // Indigo
  }

  const radius = 38;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (circumference * normalizedScore) / 100;

  return (
    <div className="flex flex-col items-center justify-center p-2">
      <div className="relative flex items-center justify-center">
        <svg 
          width={size} 
          height={size} 
          viewBox="0 0 100 100" 
          className="transform -rotate-90"
        >
          {/* Subtle Background Track */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="#27272a"
            strokeWidth="7"
          />
          {/* Active Metric Arc */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke={strokeColor}
            strokeWidth="7"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-700 ease-out"
          />
        </svg>

        {/* Center Percentage Display */}
        <div className="absolute flex flex-col items-center justify-center pointer-events-none">
          <span className="text-2xl font-bold text-zinc-100 tracking-tight">
            {normalizedScore}%
          </span>
        </div>
      </div>

      <span className="mt-2 text-xs font-semibold tracking-wider uppercase text-zinc-400">
        {label}
      </span>
    </div>
  );
}
