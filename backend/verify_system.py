import requests

def main():
    print("=" * 60)
    print("END-TO-END SYSTEM INTEGRATION VERIFICATION")
    print("=" * 60)

    # 1. Backend health
    h = requests.get("http://127.0.0.1:8000/health", timeout=5).json()
    print(f"[1] Backend Health: {h['status']} | Model: {h['model']} | Records: {h['telemetry_records']}")
    assert h["status"] == "healthy"

    # 2. Mode 2: Telemetry
    t = requests.get("http://127.0.0.1:8000/api/v1/intelligence/telemetry", timeout=5).json()
    print(f"[2] Mode 2 Telemetry: {len(t['roles'])} roles loaded, {len(t['national_deficits'])} national deficits")
    assert len(t["roles"]) >= 5

    # 3. Mode 2: Cluster Lookup
    c = requests.get("http://127.0.0.1:8000/api/v1/intelligence/cluster/Bengaluru (Karnataka)", timeout=5).json()
    print(f"[3] Mode 2 Cluster: {c['cluster_name']} -> {c['cluster_focus']}")
    assert "Bengaluru" in c["cluster_name"]

    # 4. Mode 3: Trajectory
    r = requests.post(
        "http://127.0.0.1:8000/api/v1/recommendations/trajectory",
        json={"current_skills": "html, css, python", "target_career": "Full Stack Developer"},
        timeout=30
    ).json()
    print(f"[4] Mode 3 Trajectory: Match {r['employability_match']}% | Pathways: {len(r['government_pathways'])} mapped")
    assert 0 <= r["employability_match"] <= 100

    # 5. Frontend Streamlit HTTP
    s = requests.get("http://localhost:8501", timeout=5)
    print(f"[5] Streamlit UI: HTTP {s.status_code} OK")
    assert s.status_code == 200

    print("=" * 60)
    print("ALL SYSTEM INTEGRATION CHECKS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
