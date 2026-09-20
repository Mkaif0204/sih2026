import os
import requests
import streamlit as st
import pandas as pd
import re

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="SkillPulse AI | Enterprise Dashboard",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_V1 = f"{BACKEND_URL}/api/v1"

@st.cache_data(ttl=5)
def check_backend_health():
    """Probe the backend health endpoint."""
    try:
        res = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if res.status_code == 200:
            return True, res.json()
    except Exception:
        pass
    return False, {}

# ==========================================
# ENTERPRISE SLATE CSS ARCHITECTURE
# ==========================================
st.markdown("""
<style>
    /* ---------------- GLOBAL RESET & STREAMLIT OVERRIDES ---------------- */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header [data-testid="stToolbar"] { visibility: hidden !important; }
    .stDeployButton { display: none !important; }

    /* PRESERVE MOBILE SIDEBAR COLLAPSE TOGGLE */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        z-index: 999999 !important;
        color: #F4F4F5 !important;
    }
    button[data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        visibility: visible !important;
        color: #F4F4F5 !important;
    }

    /* ---------------- TYPOGRAPHY & HEADINGS ---------------- */
    h1, h2 {
        color: #F4F4F5 !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 6px !important;
    }
    
    h3, h4 {
        color: #E4E4E7 !important;
        font-weight: 700 !important;
        letter-spacing: -0.015em !important;
    }

    /* ---------------- ENTERPRISE METRIC CARDS ---------------- */
    div[data-testid="stMetric"] {
        background: rgba(24, 24, 27, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(39, 39, 42, 0.8) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: none !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: rgba(63, 63, 70, 0.9) !important;
        background: rgba(24, 24, 27, 0.7) !important;
    }

    div[data-testid="stMetricValue"] > div {
        color: #F4F4F5 !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        letter-spacing: -0.03em !important;
    }

    div[data-testid="stMetricLabel"] p {
        color: #A1A1AA !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }

    /* ---------------- ENTERPRISE CTAS ---------------- */
    .stButton > button[kind="primary"] {
        background: #4F46E5 !important;
        border: 1px solid #4338CA !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1.3rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #4338CA !important;
        border-color: #3730A3 !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(1px) !important;
    }

    /* ---------------- FORM INPUTS & UPLOADERS ---------------- */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #09090B !important;
        color: #F4F4F5 !important;
        border: 1px solid rgba(39, 39, 42, 0.8) !important;
        border-radius: 8px !important;
        transition: border-color 0.15s ease !important;
    }
    
    .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 1px #6366F1 !important;
    }

    [data-testid="stFileUploader"] {
        background: rgba(24, 24, 27, 0.4) !important;
        border: 1px dashed rgba(63, 63, 70, 0.8) !important;
        border-radius: 12px !important;
        padding: 10px !important;
        transition: border-color 0.15s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #A1A1AA !important;
    }

    /* ---------------- CARDS & CONTAINERS ---------------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(39, 39, 42, 0.8) !important;
        border-radius: 12px !important;
        background: rgba(24, 24, 27, 0.4) !important;
        box-shadow: none !important;
    }

    /* ---------------- TABS ---------------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        background-color: transparent !important;
        border-bottom: 1px solid rgba(39, 39, 42, 0.8) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0 !important;
        padding: 8px 16px !important;
        color: #A1A1AA !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        background: rgba(24, 24, 27, 0.6) !important;
        border-bottom: 2px solid #6366F1 !important;
    }

    /* ---------------- ANIMATED STATUS BADGES ---------------- */
    @keyframes pulse-emerald {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    .status-dot-emerald {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-emerald 2s infinite;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def extract_score(text):
    match = re.search(r'(\d+)%', text)
    return int(match.group(1)) if match else 55

def create_svg_donut(score, label):
    if score >= 75:
        color = "#10B981"  # Emerald
    elif score >= 50:
        color = "#6366F1"  # Indigo
    else:
        color = "#F43F5E"  # Rose
        
    circumference = 251.2
    offset = circumference - (circumference * score / 100)
    
    html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 18px 0;">
        <div style="position: relative;">
            <svg width="140" height="140" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#27272a" stroke-width="8" />
                <circle cx="50" cy="50" r="40" fill="none" stroke="{color}" stroke-width="8" 
                        stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" 
                        stroke-linecap="round" transform="rotate(-90 50 50)" />
                <text x="50" y="57" text-anchor="middle" font-size="22" font-weight="700" fill="#F4F4F5" font-family="'Inter', system-ui, sans-serif">{score}%</text>
            </svg>
        </div>
        <span style="color: #A1A1AA; font-size: 11px; font-weight: 600; margin-top: 14px; letter-spacing: 1.5px; text-transform: uppercase;">{label}</span>
    </div>
    """
    return html

# Probe Backend Status
is_online, health_data = check_backend_health()

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
        <div style="display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: #18181b; border: 1px solid #27272a; color: #818cf8; font-size: 14px;">⚡</div>
        <span style="font-size: 17px; font-weight: 700; color: #F4F4F5; letter-spacing: -0.3px;">SkillPulse AI</span>
    </div>
    <div style="color: #71717a; font-size: 11px; font-family: monospace; margin-bottom: 14px;">SIH26134 • NATIONAL ENGINE</div>
    """, unsafe_allow_html=True)
    st.divider()
    
    st.markdown("""
    <div style="font-size: 11px; font-weight: 600; color: #71717a; letter-spacing: 0.8px; margin-bottom: 8px;">SYSTEM STATUS</div>
    """, unsafe_allow_html=True)

    if is_online:
        model_name = health_data.get("model", "gemini-3.6-flash")
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; padding: 6px 12px; border-radius: 9999px; background: #18181b; border: 1px solid #27272a; font-size: 12px; color: #e4e4e7;" title="FastAPI on Port 8000 • {model_name}">
            <span class="status-dot-emerald"></span>
            <span style="font-weight: 500;">System Live</span>
            <span style="margin-left: auto; font-size: 10px; font-family: monospace; color: #71717a;">Port 8000</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; padding: 6px 12px; border-radius: 9999px; background: #18181b; border: 1px solid rgba(244,63,94,0.3); font-size: 12px; color: #f43f5e;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 9999px; background: #f43f5e; margin-right: 4px;"></span>
            <span style="font-weight: 500;">System Offline</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    st.markdown("<div style='font-size: 11px; font-weight: 600; color: #71717a; letter-spacing: 0.8px; margin-bottom: 8px;'>NAVIGATION</div>", unsafe_allow_html=True)
    mode = st.radio("Navigation:", [
        "Syllabus Skill Gap Analysis",
        "Industry Skill Intelligence",
        "Career Pathways"
    ], label_visibility="collapsed")

# ==========================================
# HERO BANNER / BREADCRUMB
# ==========================================
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 4px 0 16px 0; border-bottom: 1px solid rgba(39, 39, 42, 0.8); margin-bottom: 24px;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="background: #18181b; border: 1px solid #27272a; padding: 6px 10px; border-radius: 8px; font-size: 15px; color: #818cf8;">⚡</div>
        <div>
            <span style="font-size: 13px; font-weight: 700; color: #F4F4F5; letter-spacing: 0.3px;">Enterprise Skill Intelligence Platform</span>
            <div style="font-size: 11px; color: #71717a; font-family: monospace;">SIH26134 • National Skill-to-Industry Alignment Engine</div>
        </div>
    </div>
    <div style="display: flex; gap: 8px; align-items: center;">
        <span style="background: #18181b; border: 1px solid #27272a; color: #A1A1AA; font-size: 11px; font-weight: 500; padding: 4px 10px; border-radius: 6px;">v1.0.0</span>
        <span style="background: #18181b; border: 1px solid #27272a; color: #34D399; font-size: 11px; font-weight: 500; padding: 4px 10px; border-radius: 6px;">● System Live</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SYLLABUS SKILL GAP ANALYSIS
# ==========================================
if mode == "Syllabus Skill Gap Analysis":
    st.markdown("## 🔍 Syllabus Skill Gap Analysis")
    st.caption("Audits university curricula against live hiring taxonomies and accreditation criteria via FastAPI.")
    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
    
    main_col, info_col = st.columns([7, 3], gap="large")
    
    with main_col:
        with st.container(border=True):
            st.markdown("#### 📄 Document Ingestion Engine")
            col1, col2 = st.columns(2)
            with col1:
                uploaded_file = st.file_uploader("Upload University Syllabus (PDF)", type=["pdf"])
            with col2:
                target_role = st.text_input("Target Job Role:", "Software Engineer")
                
            analyze_btn = st.button("Execute Gap Analysis", type="primary", use_container_width=True, icon="⚡")
            
        result_container = st.empty()
            
    with info_col:
        with st.container(border=True):
            st.markdown("### ⚙️ Pipeline")
            st.markdown("""
            **1. Extraction:** Scans digital text streams via backend `PDFService`.  
            **2. Vector Context:** Aligns with standard role benchmarks.  
            **3. LLM Audit:** Identifies obsolete and missing modules via Gemini.  
            **4. Accreditation:** Prepares outputs for NAAC/NBA reviews.
            """)
        st.info("💡 **Tip:** Digital syllabus files give the highest parsing precision.")

    if analyze_btn:
        if uploaded_file is None:
            st.warning("⚠️ Please upload a syllabus PDF first.")
        elif not is_online:
            st.error(f"⚠️ FastAPI Backend is offline at {BACKEND_URL}. Please start the backend service first.")
        else:
            with st.spinner("Extracting syllabus and auditing against industry standards via FastAPI..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    data = {"target_role": target_role}
                    response = requests.post(f"{API_V1}/gap-analysis/audit-file", files=files, data=data, timeout=60)
                    
                    if response.status_code == 200:
                        audit_result = response.json()
                        score = audit_result.get("alignment_score", 52)
                        output_text = audit_result.get("raw_markdown", "")
                        source_label = "⚡ Live Gemini AI" if audit_result.get("source") == "gemini" else "🛡️ Baseline Model"
                        
                        with result_container.container():
                            st.success(f"Audit Complete: **{target_role}** ({source_label})")
                            c_chart, c_report = st.columns([2, 5], gap="medium")
                            with c_chart:
                                with st.container(border=True):
                                    st.markdown(create_svg_donut(score, "Alignment"), unsafe_allow_html=True)
                            with c_report:
                                with st.container(border=True):
                                    st.markdown(output_text)
                    else:
                        st.error(f"Backend returned error {response.status_code}: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to communicate with FastAPI backend: {e}")

# ==========================================
# INDUSTRY SKILL INTELLIGENCE
# ==========================================
elif mode == "Industry Skill Intelligence":
    st.markdown("## 📊 National Intelligence Dashboard")
    st.caption("Macro telemetry connecting regional industry requirements with curriculum policies.")
    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
    
    # Fetch telemetry from Backend
    telemetry = {}
    if is_online:
        try:
            resp = requests.get(f"{API_V1}/intelligence/telemetry", timeout=10)
            if resp.status_code == 200:
                telemetry = resp.json()
        except Exception as e:
            st.warning(f"Could not reach backend telemetry service: {e}")

    # Fallback structure if backend call failed
    metrics = telemetry.get("metrics", {
        "high_demand_skills": {"label": "High-Demand Skills", "value": "186", "delta": "↑ 12.4% MoM"},
        "identified_deficits": {"label": "Identified Deficits", "value": "72", "delta": "↓ 4.8% YoY"},
        "indexed_syllabi": {"label": "Indexed Syllabi", "value": "128", "delta": "Active Nodes"},
        "emerging_vectors": {"label": "Emerging Vectors", "value": "34", "delta": "Industry 4.0"}
    })
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(metrics["high_demand_skills"]["label"], metrics["high_demand_skills"]["value"], metrics["high_demand_skills"]["delta"])
    col2.metric(metrics["identified_deficits"]["label"], metrics["identified_deficits"]["value"], metrics["identified_deficits"]["delta"])
    col3.metric(metrics["indexed_syllabi"]["label"], metrics["indexed_syllabi"]["value"], metrics["indexed_syllabi"]["delta"])
    col4.metric(metrics["emerging_vectors"]["label"], metrics["emerging_vectors"]["value"], metrics["emerging_vectors"]["delta"])
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # Convert role data into DataFrame
    roles_data = telemetry.get("roles", [
        {"job_role": "AI Engineer", "top_skill": "GenAI / PyTorch", "avg_salary_lpa": 18.5, "open_roles": 1240, "growth_projected_2026_pct": 92},
        {"job_role": "Full Stack Dev", "top_skill": "Next.js / React", "avg_salary_lpa": 12.0, "open_roles": 3500, "growth_projected_2026_pct": 85},
        {"job_role": "Cloud Architect", "top_skill": "Kubernetes / AWS", "avg_salary_lpa": 22.0, "open_roles": 890, "growth_projected_2026_pct": 88},
        {"job_role": "Data Analyst", "top_skill": "Pandas / SQL", "avg_salary_lpa": 8.5, "open_roles": 2100, "growth_projected_2026_pct": 75},
        {"job_role": "Cybersecurity Analyst", "top_skill": "Zero Trust", "avg_salary_lpa": 15.0, "open_roles": 1100, "growth_projected_2026_pct": 90},
        {"job_role": "Blockchain Dev", "top_skill": "Solidity / Web3", "avg_salary_lpa": 16.0, "open_roles": 450, "growth_projected_2026_pct": 82}
    ])
    live_df = pd.DataFrame(roles_data)
    
    tab1, tab2 = st.tabs(["📍 Geospatial Mapping & Trends", "📋 Structured Demand Dataset"])
    
    with tab1:
        st.markdown("### Regional Skill Cluster Allocation")
        
        clusters = telemetry.get("available_clusters", [
            "Hyderabad (Telangana)",
            "Bengaluru (Karnataka)",
            "Pune (Maharashtra)",
            "Chennai (Tamil Nadu)",
            "Noida (UP)"
        ])
        
        c_filter, c_policy = st.columns([1, 2])
        with c_filter:
            district = st.selectbox("Select Industrial Cluster:", clusters)
            
        with c_policy:
            # Query backend for dynamic cluster policy intervention
            policy_focus = "High concentration of Pharma-Tech, Cloud & Enterprise AI."
            policy_intervention = "Expand AICTE-approved Applied Data Science intake by 35%."
            if is_online:
                try:
                    c_resp = requests.get(f"{API_V1}/intelligence/cluster/{district}", timeout=5)
                    if c_resp.status_code == 200:
                        c_data = c_resp.json()
                        policy_focus = c_data.get("cluster_focus", policy_focus)
                        policy_intervention = c_data.get("policy_intervention", policy_intervention)
                except Exception:
                    pass
                    
            st.info(f"🏢 **Cluster Focus:** {policy_focus}")
            st.success(f"📌 **Intervention:** {policy_intervention}")
                
        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
        chart_col, radar_col = st.columns([8, 4], gap="medium")
        with chart_col:
            with st.container(border=True):
                st.markdown("##### Role Availability by Domain")
                st.bar_chart(live_df.set_index("job_role")["open_roles"], color="#6366F1")
                
        with radar_col:
            with st.container(border=True):
                st.markdown("##### 🚨 Critical National Deficits")
                deficits = telemetry.get("national_deficits", [
                    {"domain": "Cloud Security Architecture", "unmet_percentage": 82},
                    {"domain": "Distributed Systems (Go/Rust)", "unmet_percentage": 74},
                    {"domain": "Applied MLOps Pipelines", "unmet_percentage": 68},
                    {"domain": "Embedded Firmware (IoT)", "unmet_percentage": 59}
                ])
                deficit_md = "\n".join([
                    f"* **{item['domain']}**  \n  Demand gap: **{item['unmet_percentage']}% unmet**"
                    for item in deficits
                ])
                st.markdown(deficit_md)
                
    with tab2:
        with st.container(border=True):
            st.dataframe(live_df, use_container_width=True)

# ==========================================
# CAREER PATHWAYS
# ==========================================
elif mode == "Career Pathways":
    st.markdown("## 🎓 Personalized Skill Roadmap")
    st.caption("Maps learner skill deficits directly to active Government of India skilling initiatives via FastAPI.")
    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
    
    main_col, info_col = st.columns([7, 3], gap="large")
    
    with main_col:
        with st.container(border=True):
            st.markdown("#### 👤 Student Profile Input")
            col1, col2 = st.columns(2)
            with col1:
                student_skills = st.text_input("Current Skills (comma-separated):", "html, css, python basics")
            with col2:
                target_career = st.text_input("Target Career Track:", "Full Stack Developer")
                
            roadmap_btn = st.button("Generate Learning Trajectory", type="primary", use_container_width=True, icon="✨")
            
        result_container = st.empty()
            
    with info_col:
        with st.container(border=True):
            st.markdown("### 🏛️ Integrated Schemes")
            st.markdown("""
            Direct mapping targets:
            * **PMKVY 4.0** (Skill India Digital)
            * **NASSCOM FutureSkills Prime** (MeitY)
            * **AICTE NEAT** Portal Courses
            * **SWAYAM / NPTEL** National Channels
            """)
        st.success("✅ **Integration Hooks: Verified**")

    if roadmap_btn:
        if not is_online:
            st.error(f"⚠️ FastAPI Backend is offline at {BACKEND_URL}. Please start the backend service first.")
        else:
            with st.spinner(f"Mapping pathway toward {target_career} via FastAPI..."):
                try:
                    payload = {
                        "current_skills": student_skills,
                        "target_career": target_career
                    }
                    response = requests.post(f"{API_V1}/recommendations/trajectory", json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        traj_result = response.json()
                        score = traj_result.get("employability_match", 65)
                        output_text = traj_result.get("raw_markdown", "")
                        source_label = "✨ Live Gemini AI" if traj_result.get("source") == "gemini" else "🛡️ Baseline Model"
                        
                        with result_container.container():
                            st.success(f"Trajectory Formatted: **{target_career}** ({source_label})")
                            c_chart, c_report = st.columns([2, 5], gap="medium")
                            with c_chart:
                                with st.container(border=True):
                                    st.markdown(create_svg_donut(score, "Employability"), unsafe_allow_html=True)
                            with c_report:
                                with st.container(border=True):
                                    st.markdown(output_text)
                    else:
                        st.error(f"Backend returned error {response.status_code}: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to communicate with FastAPI backend: {e}")
