import React, { useState } from 'react';
import { 
  UploadCloud, 
  FileText, 
  CheckCircle2, 
  AlertTriangle, 
  Sparkles, 
  Info,
  Loader2 
} from 'lucide-react';
import { apiClient } from '../api/client';
import DonutChart from '../components/DonutChart';

export default function GapAnalysisView({ backendStatus }) {
  const [file, setFile] = useState(null);
  const [rawText, setRawText] = useState('');
  const [inputMode, setInputMode] = useState('file'); // 'file' | 'text'
  const [targetRole, setTargetRole] = useState('Software Engineer');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [auditResult, setAuditResult] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleAudit = async () => {
    setError(null);
    if (!backendStatus?.online) {
      setError('FastAPI backend is offline. Please start the backend service on port 8000.');
      return;
    }

    if (inputMode === 'file' && !file) {
      setError('Please select a syllabus PDF file first.');
      return;
    }

    if (inputMode === 'text' && !rawText.trim()) {
      setError('Please enter syllabus or curriculum text.');
      return;
    }

    try {
      setLoading(true);
      let result;
      if (inputMode === 'file') {
        result = await apiClient.auditSyllabusFile(file, targetRole);
      } else {
        result = await apiClient.auditSyllabusText(rawText, targetRole);
      }
      setAuditResult(result);
    } catch (err) {
      setError(err.message || 'Failed to complete syllabus audit.');
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
            Accreditation & Curriculum Audit
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-zinc-100">
          Syllabus Skill Gap Analysis
        </h1>
        <p className="text-xs sm:text-sm text-zinc-400 mt-1">
          Audits university curricula against live hiring taxonomies and accreditation criteria via FastAPI.
        </p>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: Input Card */}
        <div className="lg:col-span-8 bg-zinc-900/50 border border-zinc-800/80 rounded-xl p-6 space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-zinc-800/80">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-zinc-400" />
              <h2 className="text-sm font-semibold text-zinc-100">
                Document Ingestion
              </h2>
            </div>

            {/* Toggle File / Direct Text */}
            <div className="flex bg-zinc-950 p-1 rounded-lg border border-zinc-800 text-xs">
              <button
                onClick={() => setInputMode('file')}
                className={`px-3 py-1 rounded-md font-medium transition ${
                  inputMode === 'file' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
                }`}
              >
                Upload PDF
              </button>
              <button
                onClick={() => setInputMode('text')}
                className={`px-3 py-1 rounded-md font-medium transition ${
                  inputMode === 'text' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
                }`}
              >
                Paste Text
              </button>
            </div>
          </div>

          <div className="space-y-4">
            {/* Target Role Input */}
            <div>
              <label className="block text-xs font-medium text-zinc-300 mb-1.5">
                Target Role Benchmark
              </label>
              <input
                type="text"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                placeholder="e.g. Software Engineer, AI Engineer, Cloud Architect"
                className="w-full px-3.5 py-2 rounded-lg bg-zinc-950 border border-zinc-800 text-zinc-100 placeholder-zinc-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition"
              />
            </div>

            {/* Ingestion Mode */}
            {inputMode === 'file' ? (
              <div>
                <label className="block text-xs font-medium text-zinc-300 mb-1.5">
                  University Syllabus (PDF)
                </label>
                <div className="relative border border-dashed border-zinc-700 hover:border-zinc-500 rounded-xl p-8 text-center bg-zinc-950/40 transition">
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  <div className="flex flex-col items-center justify-center space-y-2 pointer-events-none">
                    <UploadCloud className="w-8 h-8 text-zinc-400" />
                    <p className="text-xs sm:text-sm font-medium text-zinc-200">
                      {file ? file.name : 'Select or drag & drop university syllabus PDF'}
                    </p>
                    <p className="text-[11px] text-zinc-500">
                      Standard university semester or multi-year PDF curriculum
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div>
                <label className="block text-xs font-medium text-zinc-300 mb-1.5">
                  Curriculum Module Text
                </label>
                <textarea
                  rows={6}
                  value={rawText}
                  onChange={(e) => setRawText(e.target.value)}
                  placeholder="Paste semester course units, subject descriptions, or core engineering curriculum..."
                  className="w-full px-3.5 py-2.5 rounded-lg bg-zinc-950 border border-zinc-800 text-zinc-100 placeholder-zinc-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition"
                />
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs">
                <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
                <span>{error}</span>
              </div>
            )}

            {/* Execute Button */}
            <button
              onClick={handleAudit}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Auditing against Industry Standards via Gemini...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-indigo-200" />
                  <span>Execute Gap Analysis</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right: Pipeline Info Card */}
        <div className="lg:col-span-4 space-y-4">
          <div className="bg-zinc-900/50 border border-zinc-800/80 rounded-xl p-5 space-y-3">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 text-zinc-400" />
              <span>Audit Architecture</span>
            </h3>

            <div className="space-y-2 text-xs">
              <div className="p-2.5 rounded-lg bg-zinc-950/60 border border-zinc-800/60">
                <strong className="text-zinc-200 font-medium">1. Text Ingestion:</strong>
                <p className="text-zinc-400 text-[11px] mt-0.5">Scans binary PDF text streams via backend `pypdf` abstraction.</p>
              </div>
              <div className="p-2.5 rounded-lg bg-zinc-950/60 border border-zinc-800/60">
                <strong className="text-zinc-200 font-medium">2. Taxonomy Mapping:</strong>
                <p className="text-zinc-400 text-[11px] mt-0.5">Cross-references live market frameworks and requirements.</p>
              </div>
              <div className="p-2.5 rounded-lg bg-zinc-950/60 border border-zinc-800/60">
                <strong className="text-zinc-200 font-medium">3. LLM Audit Engine:</strong>
                <p className="text-zinc-400 text-[11px] mt-0.5">Identifies obsolete vs missing modules via Gemini.</p>
              </div>
              <div className="p-2.5 rounded-lg bg-zinc-950/60 border border-zinc-800/60">
                <strong className="text-zinc-200 font-medium">4. Accreditation Output:</strong>
                <p className="text-zinc-400 text-[11px] mt-0.5">Formats verified competencies for NAAC/NBA reviews.</p>
              </div>
            </div>
          </div>
        </div>

      </div>

      {/* Results Card */}
      {auditResult && (
        <div className="bg-zinc-900/50 border border-zinc-800/80 rounded-xl p-6 sm:p-8 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-zinc-800/80">
            <div>
              <span className="text-xs font-mono text-zinc-500">Benchmark Evaluated</span>
              <h3 className="text-xl font-bold text-zinc-100">{auditResult.target_role}</h3>
            </div>
            <span className="text-xs font-mono text-zinc-400 px-2.5 py-1 rounded bg-zinc-950 border border-zinc-800 self-start sm:self-auto">
              Source: {auditResult.source === 'gemini' ? 'Gemini 3.6 Flash' : 'Baseline Cache'}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
            {/* Score Donut */}
            <div className="md:col-span-4 flex flex-col items-center justify-center p-6 rounded-xl bg-zinc-950/60 border border-zinc-800/80">
              <DonutChart score={auditResult.alignment_score} label="Alignment Score" size={150} />
              <p className="text-xs text-zinc-500 text-center mt-2">
                Industry-Academic Taxonomy Convergence
              </p>
            </div>

            {/* Breakdown */}
            <div className="md:col-span-8 space-y-5">
              <div className="p-3.5 rounded-lg bg-zinc-950/60 border border-zinc-800/80">
                <span className="text-xs font-medium text-zinc-400 block mb-1">Executive Summary</span>
                <p className="text-xs sm:text-sm text-zinc-200 leading-relaxed">
                  {auditResult.summary}
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Verified Competencies */}
                <div className="space-y-2">
                  <h4 className="text-xs font-semibold text-emerald-400 flex items-center gap-1.5 uppercase tracking-wider">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Verified Competencies</span>
                  </h4>
                  <ul className="space-y-1.5 text-xs text-zinc-300">
                    {auditResult.verified_competencies?.map((item, idx) => (
                      <li key={idx} className="p-2.5 rounded-lg bg-zinc-950/50 border border-zinc-800/60 flex items-start gap-2">
                        <span className="text-emerald-400 font-bold">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Critical Deficits */}
                <div className="space-y-2">
                  <h4 className="text-xs font-semibold text-rose-400 flex items-center gap-1.5 uppercase tracking-wider">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    <span>Critical Deficits</span>
                  </h4>
                  <ul className="space-y-1.5 text-xs text-zinc-300">
                    {auditResult.critical_deficits?.map((item, idx) => (
                      <li key={idx} className="p-2.5 rounded-lg bg-zinc-950/50 border border-zinc-800/60 flex items-start gap-2">
                        <span className="text-rose-400 font-bold">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
