import React from 'react';
import { 
  BookOpen, 
  Activity, 
  Compass, 
  ArrowRight, 
  ShieldCheck, 
  Cpu, 
  Layers
} from 'lucide-react';

export default function HomeView({ setActiveTab, backendStatus }) {
  const engineCards = [
    {
      id: 'gap-analysis',
      title: 'Syllabus Skill Gap Analysis',
      category: 'Policy & Accreditation',
      description: 'Upload university curricula to evaluate institutional alignment against real-world employer demand and NAAC/NBA standards.',
      icon: BookOpen,
      actionText: 'Audit Curriculum',
    },
    {
      id: 'intelligence',
      title: 'National Skill Intelligence',
      category: 'Industry & Governance',
      description: 'Explore live hiring telemetry across Indian industrial corridors (Hyderabad, Bengaluru, Pune) with active job vacancies and deficit tracking.',
      icon: Activity,
      actionText: 'Explore Telemetry',
    },
    {
      id: 'career-path',
      title: 'Career Pathway Generator',
      category: 'Students & Job Seekers',
      description: 'Analyze learner skills and map technical deficiencies directly to certified Indian government programs like PMKVY 4.0 and FutureSkills Prime.',
      icon: Compass,
      actionText: 'Generate Trajectory',
    },
  ];

  const govHooks = [
    { name: 'PMKVY 4.0', org: 'Skill India Digital / MSDE', desc: 'NSQF-aligned certification tracks' },
    { name: 'FutureSkills Prime', org: 'MeitY & NASSCOM', desc: 'Deep-tech & digital upskilling' },
    { name: 'NEAT Portal', org: 'AICTE', desc: 'EdTech and adaptive skill modules' },
    { name: 'SWAYAM / NPTEL', org: 'Ministry of Education', desc: 'National university credits' },
  ];

  return (
    <div className="space-y-12">
      
      {/* Refined Linear-Style Hero Card */}
      <div className="relative rounded-2xl p-8 sm:p-12 bg-zinc-900/40 border border-zinc-800/80 overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-300 text-xs font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
            <span>Smart India Hackathon 2026 • Problem Statement SIH26134</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight text-zinc-100 leading-tight">
            Bridging Indian Higher Education with Emerging Industry Demands
          </h1>

          <p className="text-base text-zinc-400 leading-relaxed max-w-2xl font-normal">
            SkillPulse AI connects academic curricula, live market job requisitions, 
            and Government of India skilling frameworks into an automated intelligence engine.
          </p>

          <div className="flex flex-wrap gap-3 pt-2">
            <button
              onClick={() => setActiveTab('gap-analysis')}
              className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-colors shadow-sm"
            >
              <span>Audit University Syllabus</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => setActiveTab('intelligence')}
              className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-zinc-900 hover:bg-zinc-800 text-zinc-200 border border-zinc-800 font-medium text-sm transition-colors"
            >
              <Activity className="w-4 h-4 text-zinc-400" />
              <span>National Telemetry</span>
            </button>
          </div>

          {/* Engine Status Bar */}
          <div className="flex flex-wrap items-center gap-6 pt-6 text-xs text-zinc-500 border-t border-zinc-800/80">
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-zinc-400" />
              <span>Engine: <strong className="text-zinc-300 font-medium">{backendStatus?.data?.model || 'Gemini 3.6 Flash'}</strong></span>
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-zinc-400" />
              <span>Criteria: <strong className="text-zinc-300 font-medium">NAAC & NBA Standards</strong></span>
            </div>
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-zinc-400" />
              <span>Gateway: <strong className="text-zinc-300 font-medium">FastAPI v1.0.0</strong></span>
            </div>
          </div>
        </div>
      </div>

      {/* Skilling Engines Grid */}
      <div className="space-y-4">
        <div>
          <h2 className="text-lg font-semibold text-zinc-100">Core Engines</h2>
          <p className="text-xs text-zinc-400">Select a workflow tailored for academic auditors, policymakers, or learners.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {engineCards.map((engine) => {
            const Icon = engine.icon;
            return (
              <div 
                key={engine.id}
                onClick={() => setActiveTab(engine.id)}
                className="bg-zinc-900/40 hover:bg-zinc-900/70 border border-zinc-800/80 hover:border-zinc-700/80 rounded-xl p-6 transition-all duration-150 flex flex-col justify-between space-y-6 group cursor-pointer"
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="w-9 h-9 rounded-lg bg-zinc-800/70 border border-zinc-700/50 flex items-center justify-center text-zinc-300 group-hover:text-indigo-400 transition-colors">
                      <Icon className="w-4 h-4" />
                    </div>
                    <span className="text-[11px] font-mono text-zinc-500">
                      {engine.category}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-base font-semibold text-zinc-100 group-hover:text-white transition-colors">
                      {engine.title}
                    </h3>
                    <p className="text-xs text-zinc-400 leading-relaxed mt-2">
                      {engine.description}
                    </p>
                  </div>
                </div>

                <div className="pt-3 border-t border-zinc-800/60 flex items-center justify-between text-xs font-medium text-zinc-400 group-hover:text-indigo-400 transition-colors">
                  <span>{engine.actionText}</span>
                  <ArrowRight className="w-3.5 h-3.5 transform group-hover:translate-x-0.5 transition-transform" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Government Integrations */}
      <div className="rounded-xl p-6 bg-zinc-900/30 border border-zinc-800/80 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-sm font-semibold text-zinc-200">National Skilling Frameworks</h2>
            <p className="text-xs text-zinc-400">Direct programmatic alignment with verified Government of India initiatives.</p>
          </div>
          <span className="text-[11px] font-mono text-emerald-400 self-start sm:self-auto">
            ● Verification Hooks Active
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {govHooks.map((g, idx) => (
            <div key={idx} className="p-3.5 rounded-lg bg-zinc-950/60 border border-zinc-800/70 space-y-1">
              <div className="text-xs font-medium text-zinc-200">{g.name}</div>
              <div className="text-[11px] text-indigo-400 font-mono">{g.org}</div>
              <div className="text-[11px] text-zinc-500 leading-relaxed pt-0.5">{g.desc}</div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
