const BASE_URL = 'http://localhost:8000';
const API_V1 = `${BASE_URL}/api/v1`;

export const apiClient = {
  /**
   * Health check to detect backend connectivity
   */
  async checkHealth() {
    try {
      const res = await fetch(`${BASE_URL}/health`, { method: 'GET' });
      if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn('Backend offline:', err);
      return null;
    }
  },

  /**
   * Mode 1: Audit syllabus by uploading a PDF file
   */
  async auditSyllabusFile(file, targetRole = 'Software Engineer') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_role', targetRole);

    const res = await fetch(`${API_V1}/gap-analysis/audit-file`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Audit failed (${res.status}): ${errText}`);
    }
    return await res.json();
  },

  /**
   * Mode 1: Audit syllabus via raw text
   */
  async auditSyllabusText(syllabusText, targetRole = 'Software Engineer') {
    const res = await fetch(`${API_V1}/gap-analysis/audit-text`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        syllabus_text: syllabusText,
        target_role: targetRole,
      }),
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Text audit failed (${res.status}): ${errText}`);
    }
    return await res.json();
  },

  /**
   * Mode 2: Macro telemetry overview
   */
  async getTelemetry() {
    const res = await fetch(`${API_V1}/intelligence/telemetry`, {
      method: 'GET',
    });

    if (!res.ok) {
      throw new Error(`Failed to load telemetry data (${res.status})`);
    }
    return await res.json();
  },

  /**
   * Mode 2: District cluster policy lookup
   */
  async getClusterPolicy(clusterName) {
    const res = await fetch(`${API_V1}/intelligence/cluster/${encodeURIComponent(clusterName)}`, {
      method: 'GET',
    });

    if (!res.ok) {
      throw new Error(`Failed to load cluster policy (${res.status})`);
    }
    return await res.json();
  },

  /**
   * Mode 3: Personalized career trajectory recommendation
   */
  async generateCareerTrajectory(currentSkills, targetCareer) {
    const res = await fetch(`${API_V1}/recommendations/trajectory`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        current_skills: currentSkills,
        target_career: targetCareer,
      }),
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Career trajectory failed (${res.status}): ${errText}`);
    }
    return await res.json();
  },
};
