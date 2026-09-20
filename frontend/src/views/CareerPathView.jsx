import React, { useState } from 'react';
import { 
  Target, 
  Sparkles, 
  Award, 
  AlertTriangle, 
  GraduationCap,
  ArrowUpRight,
  Loader2 
} from 'lucide-react';
import { apiClient } from '../api/client';
import DonutChart from '../components/DonutChart';

export default function CareerPathView({ backendStatus }) {
  const [currentSkills, setCurrentSkills] = useState('html, css, python basics');
  const [targetCareer, setTargetCareer] = useState('Full Stack Developer');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [trajectory, setTrajectory] = useState(null);

  const quickSkillChips = [
    'html, css, python basics',
    'c++, data structures, sql',
    'python, pandas, data analysis',
    'javascript, react, git',
  ];

  const handleGenerate = async () => {
    setError(null);
    if (!backendStatus?.online) {
      setError('FastAPI backend is offline. Please start the backend service on port 8000.');
      return;
    }

    if (!currentSkills.trim()) {
      setError('Please enter your current skills.');
      return;
    }

    if (!targetCareer.trim()) {
      setError('Please specify a target career track.');
      return;
    }

    try {
      setLoading(true);
      const res = await apiClient.generateCareerTrajectory(currentSkills, targetCareer);
      setTrajectory(res);
    } catch (err) {
      setError(err.message || 'Failed to generate learning trajectory.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-[11px] font-mono text-indigo-400">
            Learner & Career Development
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-zinc-100">
          Career Pathway Generator
        </h1>
        <p className="text-xs sm:text-sm text-zinc-400 mt-1">
          Maps candidate skill deficits directly to accredited Government of India skilling initiatives via FastAPI.
        </p>
      </div>

      {/* Input Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Input Form */}
        <div className="lg:col-span-8 bg-zinc-900/50 border border-zinc-800/80 rounded-xl p-6 space-y-6">
          <div className="flex items-center gap-2 pb-4 border-b border-zinc-800/80">
            <Target className="w-4 h-4 text-zinc-400" />
            <h2 className="text-sm font-semibold text-zinc-100">
              Candidate Profile Assessment
            </h2>
          </div>

          <div className="space-y-4">
            
            {/* Current Skills */}
            <div>
              <label className="block text-xs font-medium text-zinc-300 mb-1.5">
                Current Technical Competencies
              </label>
              <input
                type="text"
                value={currentSkills}
                onChange={(e) => setCurrentSkills(e.target.value)}
                placeholder="e.g. html, css, python basics, sql"
                className="w-full px-3.5 py-2 rounded-lg bg-zinc-950 border border-zinc-800 text-zinc-100 placeholder-zinc-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition"
              />

              {/* Quick Suggestion Chips */}
              <div className="flex flex-wrap gap-1.5 mt-2">
                <span className="text-[11px] text-zinc-500 self-center mr-1">Suggestions:</span>
                {quickSkillChips.map((chip, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => setCurrentSkills(chip)}
                    className="text-[11px] px-2.5 py-0.5 rounded-md bg-zinc-950 border border-zinc-800 text-zinc-400 hover:text-white hover:border-zinc-700 transition"
                  >
                    {chip}
                  </button>
                ))}
              </div>
            </div>

            {/* Target Career Track */}
            <div>
              <label className="block text-xs font-medium text-zinc-300 mb-1.5">
                Target Career Track / Job Title
              </label>
              <input
                type="text"
                value={targetCareer}
                onChange={(e) => setTargetCareer(e.target.value)}
                placeholder="e.g. Full Stack Developer, AI Engineer, Cloud Architect"
                className="w-full px-3.5 py-2 rounded-lg bg-zinc-950 border border-zinc-800 text-zinc-100 placeholder-zinc-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition"
              />
            </div>

            {/* Error Banner */}
            {error && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs">
                <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {/* Trigger Button */}
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Mapping Trajectory against National Frameworks...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-indigo-200" />
                  <span>Generate Learning Trajectory</span>
                </>
              )}
            </button>

          </div>
        </div>

        {/* Right Info Box */}
        <div className="lg:col-span-4 space-y-4">
          <div className="bg-zinc-900/50 border border-zinc-800/80 rounded-xl p-5 space-y-3">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5">
              <Award className="w-3.5 h-3.5 text-zinc-400" />
              <span>Accredited Indian Schemes</span>
            </h3>

            <p className="text-xs text-zinc-400 leading-relaxed">
              SkillPulse AI cross-references candidate deficits exclusively against authorized Indian government frameworks.
            </p>

            <div className="space-y-2 text-xs">
              <div className="p-2.5 rounded-lg bg-zinc-950/60 border border-zinc-800/60">
                <div className="text-zinc-200 font-medium">PMKVY 4.0 (Skill India Digital)</div>
                <div className="text-zinc-500 text-[11px] mt-0.5">NSQF-certified technical domain programs</div>
              </div>
              <div className="p-2.5 rounded-lg bg-zinc-950/60 border border-zinc-800/60">
                <div className="text-zinc-200 font-medium">NASSCOM FutureSkills Prime</div>
                <div className="text-zinc-500 text-[11px] mt-0.5">MeitY deep-tech competence pathways</div>
              </div>
              <div className="p-2.5 rounded-lg bg-zinc-950/60 border border-zinc-800/60">
                <div className="text-zinc-200 font-medium">AICTE NEAT Portal</div>
                <div className="text-zinc-500 text-[11px] mt-0.5">EdTech & advanced skilling alliance</div>
              </div>
              <div className="p-2.5 rounded-lg bg-zinc-950/60 border border-zinc-800/60">
                <div className="text-zinc-200 font-medium">SWAYAM / NPTEL</div>
                <div className="text-zinc-500 text-[11px] mt-0.5">IIT/IISc verified academic courses</div>
              </div>
            </div>
          </div>
        </div>

      </div>

      {/* Results Output */}
      {trajectory && (
        <div className="bg-zinc-900/50 border border-zinc-800/80 rounded-xl p-6 sm:p-8 space-y-6">
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-zinc-800/80">
            <div>
              <span className="text-xs font-mono text-zinc-500">Career Trajectory Prepared</span>
              <h3 className="text-xl font-bold text-zinc-100">{trajectory.target_career}</h3>
            </div>
            <span className="text-xs font-mono text-zinc-400 px-2.5 py-1 rounded bg-zinc-950 border border-zinc-800 self-start sm:self-auto">
              Source: {trajectory.source === 'gemini' ? 'Gemini 3.6 Flash' : 'Baseline Cache'}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
            
            {/* Employability Donut */}
            <div className="md:col-span-4 flex flex-col items-center justify-center p-6 rounded-xl bg-zinc-950/60 border border-zinc-800/80">
              <DonutChart score={trajectory.employability_match} label="Employability Match" size={150} />
              <p className="text-xs text-zinc-500 text-center mt-2">
                Candidate Readiness Evaluation
              </p>
            </div>

            {/* Assessment Details */}
            <div className="md:col-span-8 space-y-5">
              <div className="p-3.5 rounded-lg bg-zinc-950/60 border border-zinc-800/80">
                <span className="text-xs font-medium text-zinc-400 block mb-1">Readiness Verdict</span>
                <p className="text-xs sm:text-sm text-zinc-200 leading-relaxed">
                  {trajectory.summary}
                </p>
              </div>

              {/* Technical Deficits */}
              <div className="space-y-2">
                <h4 className="text-xs font-semibold text-rose-400 flex items-center gap-1.5 uppercase tracking-wider">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>Identified Technical Deficits</span>
                </h4>
                <ul className="space-y-1.5 text-xs text-zinc-300">
                  {trajectory.technical_deficits?.map((item, idx) => (
                    <li key={idx} className="p-2.5 rounded-lg bg-zinc-950/50 border border-zinc-800/60 flex items-start gap-2">
                      <span className="text-rose-400 font-bold">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Recommended Pathways */}
              <div className="space-y-2">
                <h4 className="text-xs font-semibold text-indigo-400 flex items-center gap-1.5 uppercase tracking-wider">
                  <GraduationCap className="w-3.5 h-3.5" />
                  <span>Mapped Government Training Pathways</span>
                </h4>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {trajectory.government_pathways?.map((path, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-zinc-950/70 border border-zinc-800/80 space-y-1">
                      <div className="text-xs font-semibold text-indigo-300 flex items-center justify-between">
                        <span>{path.provider}</span>
                        <ArrowUpRight className="w-3.5 h-3.5 text-zinc-500" />
                      </div>
                      <p className="text-xs text-zinc-300 font-normal leading-relaxed">
                        {path.program}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

            </div>

          </div>

        </div>
      )}

    </div>
  );
}
