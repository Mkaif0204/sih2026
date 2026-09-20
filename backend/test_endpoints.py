import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("RUNNING AUTOMATED FASTAPI ENDPOINT SUITE")
    print("=" * 60)
    
    # 1. Health check
    print("\n[1] Testing GET /health...")
    res = client.get("/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    health_data = res.json()
    print("   Response:", health_data)
    assert health_data["status"] == "healthy"
    print("   --> PASS")

    # 2. Mode 2: Telemetry Overview
    print("\n[2] Testing GET /api/v1/intelligence/telemetry...")
    res = client.get("/api/v1/intelligence/telemetry")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    telemetry = res.json()
    print(f"   Roles found: {len(telemetry['roles'])}")
    print(f"   National deficits found: {len(telemetry['national_deficits'])}")
    print(f"   Supported clusters: {telemetry['available_clusters']}")
    assert len(telemetry["roles"]) >= 5
    assert len(telemetry["national_deficits"]) >= 3
    print("   --> PASS")

    # 3. Mode 2: Cluster Recommendation
    print("\n[3] Testing GET /api/v1/intelligence/cluster/Hyderabad (Telangana)...")
    res = client.get("/api/v1/intelligence/cluster/Hyderabad (Telangana)")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    cluster_policy = res.json()
    print("   Cluster Focus:", cluster_policy["cluster_focus"])
    print("   Intervention:", cluster_policy["policy_intervention"])
    assert "Applied Data Science" in cluster_policy["policy_intervention"]
    print("   --> PASS")

    # 4. Mode 3: Career Trajectory & Government Pathways
    print("\n[4] Testing POST /api/v1/recommendations/trajectory...")
    req_body = {
        "current_skills": "python basics, html, css",
        "target_career": "Full Stack Developer"
    }
    res = client.post("/api/v1/recommendations/trajectory", json=req_body)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    traj = res.json()
    print(f"   Target Career: {traj['target_career']}")
    print(f"   Employability Match: {traj['employability_match']}%")
    print(f"   Deficits: {traj['technical_deficits']}")
    print(f"   Government Pathways: {traj['government_pathways']}")
    assert 0 <= traj["employability_match"] <= 100
    assert len(traj["technical_deficits"]) > 0
    assert len(traj["government_pathways"]) > 0
    print("   --> PASS")

    # 5. Mode 1: Syllabus Gap Audit (Text)
    print("\n[5] Testing POST /api/v1/gap-analysis/audit-text...")
    audit_req = {
        "target_role": "Software Engineer",
        "syllabus_text": "Semester 1: Data Structures, C Programming, Algorithms, Object Oriented Systems in Java, Database Management."
    }
    res = client.post("/api/v1/gap-analysis/audit-text", json=audit_req)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    gap_audit = res.json()
    print(f"   Target Role: {gap_audit['target_role']}")
    print(f"   Alignment Score: {gap_audit['alignment_score']}%")
    print(f"   Competencies: {gap_audit['verified_competencies']}")
    print(f"   Critical Deficits: {gap_audit['critical_deficits']}")
    assert 0 <= gap_audit["alignment_score"] <= 100
    assert len(gap_audit["verified_competencies"]) > 0
    assert len(gap_audit["critical_deficits"]) > 0
    print("   --> PASS")

    print("\n" + "=" * 60)
    print("ALL 5 ENDPOINT TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
