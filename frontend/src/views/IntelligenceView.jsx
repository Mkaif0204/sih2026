import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  MapPin, 
  BarChart3, 
  Table as TableIcon, 
  TrendingUp, 
  AlertOctagon, 
  Building2, 
  Loader2 
} from 'lucide-react';
import { apiClient } from '../api/client';
import MetricCard from '../components/MetricCard';

export default function IntelligenceView({ backendStatus }) {
  const [telemetry, setTelemetry] = useState(null);
  const [selectedCluster, setSelectedCluster] = useState('Hyderabad (Telangana)');
  const [clusterPolicy, setClusterPolicy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('geospatial'); // 'geospatial' | 'dataset'

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const data = await apiClient.getTelemetry();
        setTelemetry(data);
        if (data.available_clusters && data.available_clusters.length > 0) {
          const initCluster = data.available_clusters[0];
          setSelectedCluster(initCluster);
          const pol = await apiClient.getClusterPolicy(initCluster);
          setClusterPolicy(pol);
        }
      } catch (err) {
        setError(err.message || 'Failed to load telemetry data.');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleClusterChange = async (clusterName) => {
    setSelectedCluster(clusterName);
    try {
      const pol = await apiClient.getClusterPolicy(clusterName);
      setClusterPolicy(pol);
    } catch (err) {
      console.warn('Failed to load cluster policy:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] space-y-3">
        <Loader2 className="w-6 h-6 text-zinc-400 animate-spin" />
        <p className="text-xs font-mono text-zinc-500">Loading National Industry Telemetry...</p>
      </div>
    );
  }

  const metrics = telemetry?.metrics || {
    high_demand_skills: { label: 'High-Demand Skills', value: '186', delta: '↑ 12.4% MoM' },
    identified_deficits: { label: 'Identified Deficits', value: '72', delta: '↓ 4.8% YoY' },
    indexed_syllabi: { label: 'Indexed Syllabi', value: '128', delta: 'Active Nodes' },
    emerging_vectors: { label: 'Emerging Vectors', value: '34', delta: 'Industry 4.0' },
  };

  const roles = telemetry?.roles || [];
  const deficits = telemetry?.national_deficits || [];
  const clusters = telemetry?.available_clusters || [
    'Hyderabad (Telangana)',
    'Bengaluru (Karnataka)',
    'Pune (Maharashtra)',
    'Chennai (Tamil Nadu)',
    'Noida (UP)'
  ];

  const maxOpenRoles = Math.max(...roles.map(r => r.open_roles), 1);

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-[11px] font-mono text-indigo-400">
            Industry & Telemetry Engine
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-zinc-100">
          National Industry Skill Intelligence
        </h1>
        <p className="text-xs sm:text-sm text-zinc-400 mt-1">
          Macro telemetry connecting regional industry requirements with curriculum policies and hiring trends.
        </p>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          label={metrics.high_demand_skills.label}
          value={metrics.high_demand_skills.value}
          delta={metrics.high_demand_skills.delta}
          icon={TrendingUp}
        />
        <MetricCard
          label={metrics.identified_deficits.label}
          value={metrics.identified_deficits.value}
          delta={metrics.identified_deficits.delta}
          icon={AlertOctagon}
        />
        <MetricCard
          label={metrics.indexed_syllabi.label}
          value={metrics.indexed_syllabi.value}
          delta={metrics.indexed_syllabi.delta}
          icon={Building2}
        />
        <MetricCard
          label={metrics.emerging_vectors.label}
          value={metrics.emerging_vectors.value}
          delta={metrics.emerging_vectors.delta}
          icon={Activity}
        />
      </div>

      {/* Clean Tabs */}
      <div className="flex border-b border-zinc-800/80 gap-6 text-sm font-medium">
        <button
          onClick={() => setActiveTab('geospatial')}
          className={`pb-3 flex items-center gap-2 border-b-2 transition-colors duration-150 ${
            activeTab === 'geospatial'
              ? 'border-indigo-500 text-white'
              : 'border-transparent text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <MapPin className="w-4 h-4" />
          <span>Regional Cluster Policies</span>
        </button>
        <button
          onClick={() => setActiveTab('dataset')}
          className={`pb-3 flex items-center gap-2 border-b-2 transition-colors duration-150 ${
            activeTab === 'dataset'
              ? 'border-indigo-500 text-white'
              : 'border-transparent text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <TableIcon className="w-4 h-4" />
          <span>Demand Dataset</span>
        </button>
      </div>

      {/* Tab 1: Geospatial */}
      {activeTab === 'geospatial' && (
        <div className="space-y-6 animate-in fade-in duration-150">
          
          {/* Cluster Selection & Policy */}
          <div className="bg-zinc-900/50 border border-zinc-800/80 rounded-xl p-6 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
                  <Building2 className="w-4 h-4 text-zinc-400" />
                  <span>Industrial Cluster Policy Focus</span>
                </h3>
                <p className="text-xs text-zinc-400 mt-0.5">
                  Select an industrial cluster to review targeted institutional intervention policies.
                </p>
              </div>

              <select
                value={selectedCluster}
                onChange={(e) => handleClusterChange(e.target.value)}
                className="px-3.5 py-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-zinc-200 text-xs font-medium focus:outline-none focus:border-indigo-500"
              >
                {clusters.map((c) => (
                  <option key={c} value={c} className="bg-zinc-900 text-zinc-200">
                    {c}
                  </option>
                ))}
              </select>
            </div>

            {clusterPolicy && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
                <div className="p-4 rounded-lg bg-zinc-950/60 border border-zinc-800/80 space-y-1">
                  <span className="text-[11px] font-mono text-zinc-400 uppercase tracking-wider">
                    Cluster Focus • {clusterPolicy.cluster_name}
                  </span>
                  <p className="text-xs sm:text-sm text-zinc-200 font-medium">
                    {clusterPolicy.cluster_focus}
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-zinc-950/60 border border-zinc-800/80 space-y-1">
                  <span className="text-[11px] font-mono text-indigo-400 uppercase tracking-wider">
                    Recommended Policy Intervention
                  </span>
                  <p className="text-xs sm:text-sm text-zinc-200 font-medium">
                    {clusterPolicy.policy_intervention}
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Role Bars & National Deficits */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* Left: Role Availability */}
            <div className="lg:col-span-8 bg-zinc-900/50 border border-zinc-800/80 rounded-xl p-6 space-y-5">
              <div className="flex items-center justify-between pb-3 border-b border-zinc-800/80">
                <h3 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-zinc-400" />
                  <span>Role Availability by Domain</span>
                </h3>
                <span className="text-[11px] font-mono text-zinc-500">Active Open Roles</span>
              </div>

              <div className="space-y-4">
                {roles.map((r, idx) => {
                  const pct = Math.round((r.open_roles / maxOpenRoles) * 100);
                  return (
                    <div key={idx} className="space-y-1.5">
                      <div className="flex justify-between text-xs">
                        <span className="text-zinc-200 font-medium flex items-center gap-2">
                          <span>{r.job_role}</span>
                          <span className="text-[10px] font-mono text-zinc-400 px-1.5 py-0.5 rounded bg-zinc-950 border border-zinc-800">
                            {r.top_skill}
                          </span>
                        </span>
                        <span className="text-zinc-400 font-mono">
                          {r.open_roles.toLocaleString()} roles
                        </span>
                      </div>

                      <div className="w-full bg-zinc-950 rounded-full h-2 overflow-hidden border border-zinc-800/60">
                        <div
                          className="bg-indigo-500 h-full rounded-full transition-all duration-500"
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Right: National Deficits */}
            <div className="lg:col-span-4 bg-zinc-900/50 border border-zinc-800/80 rounded-xl p-6 space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-zinc-800/80">
                <AlertOctagon className="w-4 h-4 text-zinc-400" />
                <h3 className="text-sm font-semibold text-zinc-100">
                  Critical National Deficits
                </h3>
              </div>

              <div className="space-y-3">
                {deficits.map((d, idx) => (
                  <div key={idx} className="p-3 rounded-lg bg-zinc-950/60 border border-zinc-800/60 space-y-1.5">
                    <div className="flex justify-between items-center text-xs">
                      <span className="text-zinc-200 font-medium">{d.domain}</span>
                      <span className="text-rose-400 font-mono text-[11px]">{d.unmet_percentage}% unmet</span>
                    </div>
                    
                    <div className="w-full bg-zinc-900 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-rose-500/80 h-full rounded-full"
                        style={{ width: `${d.unmet_percentage}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              <p className="text-[11px] text-zinc-500 pt-1">
                Data synthesized from national enterprise surveys across Tier-1 and Tier-2 clusters.
              </p>
            </div>

          </div>

        </div>
      )}

      {/* Tab 2: Dataset */}
      {activeTab === 'dataset' && (
        <div className="bg-zinc-900/50 border border-zinc-800/80 rounded-xl overflow-hidden animate-in fade-in duration-150">
          <div className="p-4 border-b border-zinc-800/80 flex justify-between items-center">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-300">
              National Skill Demand Dataset
            </h3>
            <span className="text-xs font-mono text-zinc-500">Source: industry_data.csv</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-zinc-950/60 border-b border-zinc-800/80 text-zinc-400 font-medium uppercase tracking-wider">
                  <th className="py-3 px-4">Job Role</th>
                  <th className="py-3 px-4">Top Demanded Skill</th>
                  <th className="py-3 px-4">Avg Salary</th>
                  <th className="py-3 px-4">Open Positions</th>
                  <th className="py-3 px-4">Projected Growth</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/60">
                {roles.map((r, idx) => (
                  <tr key={idx} className="hover:bg-zinc-800/20 transition-colors">
                    <td className="py-3 px-4 text-zinc-200 font-medium">{r.job_role}</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded bg-zinc-950 border border-zinc-800 text-zinc-300 font-mono">
                        {r.top_skill}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono text-zinc-300">₹{r.avg_salary_lpa} LPA</td>
                    <td className="py-3 px-4 font-mono text-zinc-300">{r.open_roles.toLocaleString()}</td>
                    <td className="py-3 px-4 font-mono text-indigo-400">+{r.growth_projected_2026_pct}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
}
