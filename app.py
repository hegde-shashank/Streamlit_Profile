import streamlit as st
import json
import os
from pathlib import Path

# ─── Page Config ───
st.set_page_config(
    page_title="Shashank Hegde | Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════
# IMAGE MANAGEMENT — SECURE LOCAL FOLDER SYSTEM
# ════════════════════════════════════════════════
# Images are loaded from a local folder structure.
# Only YOU (the repo owner) can add images by placing
# them in the correct folder and pushing to GitHub.
#
# Folder structure:
#   assets/
#   ├── profile/          → Your profile photo
#   ├── achievements/     → Achievement/award photos
#   ├── certificates/     → Certificate scans
#   ├── experience/       → Workplace photos
#   ├── education/        → Degree certificates
#   ├── products/         → Product/build photos
#   └── academics/        → Project/conference photos
#
# To add images:
#   1. Drop .jpg/.jpeg/.png files into the right folder
#   2. git add, commit, push
#   3. Streamlit Cloud auto-redeploys
# ════════════════════════════════════════════════

ASSETS_DIR = Path("assets")

CATEGORIES = [
    "profile", "achievements", "certificates",
    "experience", "education", "products", "academics"
]
for cat in CATEGORIES:
    (ASSETS_DIR / cat).mkdir(parents=True, exist_ok=True)


def get_images(category: str) -> list[str]:
    """Get sorted image paths from a category folder."""
    cat_dir = ASSETS_DIR / category
    if not cat_dir.exists():
        return []
    extensions = {".jpg", ".jpeg", ".png", ".webp"}
    return [
        str(p) for p in sorted(cat_dir.iterdir())
        if p.suffix.lower() in extensions
    ]


# ─── Custom CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-card: #1e293b;
    --accent: #0ea5e9;
    --accent-glow: rgba(14, 165, 233, 0.3);
    --accent-2: #8b5cf6;
    --accent-3: #10b981;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #334155;
    --gradient-1: linear-gradient(135deg, #0ea5e9, #8b5cf6);
    --gradient-2: linear-gradient(135deg, #8b5cf6, #ec4899);
    --gradient-3: linear-gradient(135deg, #10b981, #0ea5e9);
}

.stApp { font-family: 'Outfit', sans-serif !important; }
.block-container { padding-top: 1rem !important; max-width: 1200px !important; }
h1, h2, h3, h4, h5, h6 { font-family: 'Outfit', sans-serif !important; font-weight: 700 !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: var(--bg-secondary); border-radius: 16px;
    padding: 6px; border: 1px solid var(--border); margin-bottom: 2rem;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif !important; font-weight: 500; font-size: 0.9rem;
    padding: 0.6rem 1.2rem; border-radius: 12px; color: var(--text-secondary);
    background: transparent; border: none; transition: all 0.3s ease;
}
.stTabs [aria-selected="true"] {
    background: var(--gradient-1) !important; color: white !important;
    font-weight: 600; box-shadow: 0 4px 15px var(--accent-glow);
}

.hero-container {
    position: relative; padding: 3rem 2.5rem;
    background: linear-gradient(135deg, rgba(14,165,233,0.08), rgba(139,92,246,0.08));
    border: 1px solid var(--border); border-radius: 24px; margin-bottom: 2rem; overflow: hidden;
}
.hero-container::before {
    content: ''; position: absolute; top: -50%; right: -20%; width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(14,165,233,0.1), transparent 70%);
    border-radius: 50%; pointer-events: none;
}
.hero-name {
    font-family: 'Outfit', sans-serif !important; font-size: 3.2rem; font-weight: 900;
    background: var(--gradient-1); -webkit-background-clip: text;
    -webkit-text-fill-color: transparent; margin: 0 0 0.3rem 0; line-height: 1.1;
}
.hero-title {
    font-family: 'JetBrains Mono', monospace; font-size: 1rem;
    color: var(--accent); margin-bottom: 1rem; letter-spacing: 0.5px;
}
.hero-bio { font-size: 1.05rem; color: var(--text-secondary); line-height: 1.7; max-width: 700px; }

.stat-row { display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 140px; background: var(--bg-secondary); border: 1px solid var(--border);
    border-radius: 16px; padding: 1.2rem; text-align: center; transition: all 0.3s ease;
}
.stat-card:hover { border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 25px rgba(14,165,233,0.15); }
.stat-number {
    font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800;
    background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-label { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-top: 0.3rem; }

.section-title {
    font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800;
    color: var(--text-primary); margin: 2rem 0 1.5rem 0; display: flex; align-items: center; gap: 0.75rem;
}
.section-title .icon { font-size: 1.5rem; }
.section-subtitle { color: var(--text-muted); font-size: 0.95rem; margin-top: -1rem; margin-bottom: 1.5rem; }

.timeline-card {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px;
    padding: 1.8rem; margin-bottom: 1.2rem; position: relative; overflow: hidden; transition: all 0.3s ease;
}
.timeline-card:hover { border-color: var(--accent); box-shadow: 0 8px 30px rgba(14,165,233,0.1); }
.timeline-card::before {
    content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%;
    background: var(--gradient-1); border-radius: 4px 0 0 4px;
}
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.8rem; }
.card-role { font-family: 'Outfit', sans-serif; font-size: 1.2rem; font-weight: 700; color: var(--text-primary); }
.card-company { font-size: 0.95rem; color: var(--accent); font-weight: 500; }
.card-date {
    font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--text-muted);
    background: rgba(14,165,233,0.1); padding: 0.3rem 0.8rem; border-radius: 8px; white-space: nowrap;
}
.card-desc { color: var(--text-secondary); font-size: 0.92rem; line-height: 1.6; }
.card-skills { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.8rem; }
.skill-tag {
    font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--accent);
    background: rgba(14,165,233,0.1); border: 1px solid rgba(14,165,233,0.2);
    padding: 0.25rem 0.6rem; border-radius: 6px;
}

.edu-card {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px;
    padding: 2rem; margin-bottom: 1.2rem; transition: all 0.3s ease;
}
.edu-card:hover { border-color: var(--accent-2); box-shadow: 0 8px 30px rgba(139,92,246,0.1); }
.edu-degree {
    font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 700;
    background: var(--gradient-2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.edu-school { font-size: 1rem; color: var(--text-primary); font-weight: 500; margin: 0.3rem 0; }
.edu-details { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6; }

.award-card {
    background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(239,68,68,0.05));
    border: 1px solid rgba(245,158,11,0.25); border-radius: 20px; padding: 1.5rem;
    margin-bottom: 1rem; transition: all 0.3s ease;
}
.award-card:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(245,158,11,0.15); }
.award-title { font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 700; color: #f59e0b; }
.award-desc { color: var(--text-secondary); font-size: 0.88rem; margin-top: 0.3rem; }

.pub-card {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px;
    padding: 1.5rem; margin-bottom: 1rem; transition: all 0.3s ease;
}
.pub-card:hover { border-color: var(--accent-3); }
.pub-title { font-weight: 700; color: var(--text-primary); font-size: 1rem; }
.pub-venue { font-size: 0.85rem; color: var(--accent-3); margin-top: 0.2rem; }
.pub-desc { color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.5rem; line-height: 1.5; }

.contact-item {
    display: flex; align-items: center; gap: 0.75rem; padding: 0.8rem 1.2rem;
    background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px;
    margin-bottom: 0.5rem; transition: all 0.2s ease;
}
.contact-item:hover { border-color: var(--accent); }
.contact-icon { font-size: 1.2rem; }
.contact-text { color: var(--text-secondary); font-size: 0.9rem; }
.contact-text a { color: var(--accent); text-decoration: none; }

.profile-photo {
    width: 140px; height: 140px; border-radius: 50%; border: 3px solid var(--accent);
    object-fit: cover; box-shadow: 0 0 30px var(--accent-glow);
}

.stImage > img { border-radius: 12px; }
.stButton > button {
    border-radius: 12px !important; font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important; padding: 0.5rem 1.5rem !important; transition: all 0.3s ease !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 15px var(--accent-glow) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Gallery helpers ───
def render_gallery(category: str, cols: int = 3):
    images = get_images(category)
    if not images:
        st.caption(f"No images yet — add `.jpg`/`.png` files to `assets/{category}/` and redeploy.")
        return
    columns = st.columns(cols)
    for i, img_path in enumerate(images):
        with columns[i % cols]:
            st.image(img_path, caption=Path(img_path).stem.replace("_", " ").replace("-", " "), use_container_width=True)


def render_carousel(category: str, items_per_page: int = 3, key_prefix: str = "carousel"):
    images = get_images(category)
    if not images:
        st.caption(f"No images yet — add files to `assets/{category}/` and redeploy.")
        return
    page_key = f"{key_prefix}_page"
    if page_key not in st.session_state:
        st.session_state[page_key] = 0
    total_pages = max(1, (len(images) + items_per_page - 1) // items_per_page)
    n1, n2, n3 = st.columns([1, 4, 1])
    with n1:
        if st.button("◀ Prev", key=f"{key_prefix}_prev"):
            st.session_state[page_key] = (st.session_state[page_key] - 1) % total_pages
    with n3:
        if st.button("Next ▶", key=f"{key_prefix}_next"):
            st.session_state[page_key] = (st.session_state[page_key] + 1) % total_pages
    with n2:
        st.caption(f"Page {st.session_state[page_key] + 1} of {total_pages}")
    start = st.session_state[page_key] * items_per_page
    end = min(start + items_per_page, len(images))
    cols = st.columns(items_per_page)
    for i, img_path in enumerate(images[start:end]):
        with cols[i]:
            st.image(img_path, use_container_width=True,
                     caption=Path(img_path).stem.replace("_", " ").replace("-", " "))


# ═══════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════
tabs = st.tabs(["🏠 Home", "🏆 Certificates", "💼 Experience", "🎓 Education", "🔧 Products", "📚 Academics", "📬 Contact"])

# ── TAB 1: HOME ──
with tabs[0]:
    col_photo, col_info = st.columns([1, 3], gap="large")
    with col_photo:
        profile_images = get_images("profile")
        if profile_images:
            st.image(profile_images[0], width=140)
        else:
            st.markdown('<div style="width:140px;height:140px;border-radius:50%;background:linear-gradient(135deg,#0ea5e9,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:3rem;color:white;border:3px solid #0ea5e9;box-shadow:0 0 30px rgba(14,165,233,0.3);">SH</div>', unsafe_allow_html=True)
    with col_info:
        st.markdown("""
        <div class="hero-container">
            <div class="hero-name">Shashank Hegde</div>
            <div class="hero-title">Embedded-ML Electronics Engineer | Lead Product R&D</div>
            <div class="hero-bio">Lead Product R&D Engineer and TUM graduate, working in a startup since inception with ownership of embedded and ML-based healthcare systems, including edge ML, wireless sensor connectivity, and product-grade system development. Over 5 years of experience across MNCs like Robert Bosch and high-growth startups.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
        <div class="stat-card"><div class="stat-number">5+</div><div class="stat-label">Years Experience</div></div>
        <div class="stat-card"><div class="stat-number">30K+</div><div class="stat-label">Clinical Consults</div></div>
        <div class="stat-card"><div class="stat-number">3</div><div class="stat-label">Publications</div></div>
        <div class="stat-card"><div class="stat-number">5</div><div class="stat-label">Awards</div></div>
        <div class="stat-card"><div class="stat-number">2</div><div class="stat-label">Degrees</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title"><span class="icon">🏅</span> Highlights & Achievements</div>', unsafe_allow_html=True)
    render_carousel("achievements", items_per_page=3, key_prefix="ach")

    st.markdown("""
    <div class="award-card"><div class="award-title">🏆 Best Presentation Award — IEEE ICCE 2024, Las Vegas</div><div class="award-desc">Presented research on IoT-enabled automatic gear shifting for E-bikes. Awarded best presentation among 50+ papers.</div></div>
    <div class="award-card"><div class="award-title">🏆 Bosch Future Mobility Challenge — Semi-Finalist, Cluj Romania</div><div class="award-desc">Represented Germany among 100+ international teams. Led embedded sensor fusion on NVIDIA Jetson Xavier.</div></div>
    <div class="award-card"><div class="award-title">🏆 Bravo Award — Robert Bosch</div><div class="award-desc">Recognized for successful and timely delivery of a SecOC tool in ECU security.</div></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title"><span class="icon">⚡</span> Core Competencies</div>', unsafe_allow_html=True)
    skills_data = {
        "Embedded Systems & IoT": ["Edge ML", "Arduino", "Raspberry Pi", "STM32", "Firmware Dev", "IoT Security", "CAN", "V2V"],
        "AI & Machine Learning": ["ASR", "NLP", "RAG", "Model Compression", "TensorRT", "GPU Acceleration", "Computer Vision"],
        "Programming": ["Python", "C", "C++", "CAPL", "ROS"],
        "Tools & Platforms": ["Linux/RHEL", "CUDA", "NVIDIA Jetson", "Docker", "Git"],
    }
    c1, c2 = st.columns(2)
    for idx, (cat, skills) in enumerate(skills_data.items()):
        with c1 if idx % 2 == 0 else c2:
            st.markdown(f"**{cat}**")
            st.markdown('<div class="card-skills">' + "".join([f'<span class="skill-tag">{s}</span>' for s in skills]) + '</div>', unsafe_allow_html=True)
            st.markdown("")

# ── TAB 2: CERTIFICATES ──
with tabs[1]:
    st.markdown('<div class="section-title"><span class="icon">🏆</span> Certificates & Awards</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">A collection of certificates, awards, and recognitions.</p>', unsafe_allow_html=True)

    default_certs = [
        {"title": "Best Session Presentation Award — IEEE ICCE 2024", "desc": "Las Vegas, USA | January 2024", "category": "Award"},
        {"title": "Certificate of Participation — IEEE ICCE 2024", "desc": "Retrofittable Automatic Shifter of Rear-Derailleur with Mode-Based Transmission and IoT", "category": "Conference"},
        {"title": "Best Paper Award — ICICEE 2020", "desc": "Remote Monitoring with Voice Command Control and Image Analysis | Tumkur, India", "category": "Award"},
        {"title": "Bravo Award — Robert Bosch", "desc": "Recognized for SecOC tool delivery in ECU security | August 2021", "category": "Corporate"},
        {"title": "Bosch Future Mobility Challenge", "desc": "Team TUMAVERICK — Semi-finalist | Cluj, Romania 2023", "category": "Competition"},
        {"title": "Tejas Networks Internship Certificate", "desc": "Product verification and test automation | Jan–May 2020", "category": "Internship"},
        {"title": "NCCDS 2020 Participation", "desc": "Data Extraction with Signal Comparison for Forest Logging Prevention", "category": "Conference"},
        {"title": "NIE IEEE Biblus — Paper Presentation", "desc": "ANKURA'19 National Level Paper Presentation", "category": "Conference"},
        {"title": "NIE Summer of Code 5.0", "desc": "Hardware Track | June 2018", "category": "Workshop"},
        {"title": "Adroit'18 — Certificate of Appreciation", "desc": "IEEE NIE Student Branch volunteering | October 2018", "category": "Volunteering"},
        {"title": "Texas Instruments Innovation Challenge 2019", "desc": "DST & TI India Innovation Challenge Design Contest", "category": "Competition"},
    ]
    categories = sorted(set(c["category"] for c in default_certs))
    selected_cat = st.multiselect("Filter by category", categories, default=categories, key="cert_filter")
    for cert in [c for c in default_certs if c["category"] in selected_cat]:
        color = {"Award":"#f59e0b","Conference":"#0ea5e9","Corporate":"#8b5cf6","Competition":"#ec4899","Internship":"#10b981","Workshop":"#06b6d4","Volunteering":"#a78bfa"}.get(cert["category"],"#0ea5e9")
        st.markdown(f'<div class="timeline-card" style="border-left:4px solid {color};"><div class="card-header"><div><div class="card-role">{cert["title"]}</div><div class="card-desc">{cert["desc"]}</div></div><span class="card-date">{cert["category"]}</span></div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📎 Certificate Scans")
    render_gallery("certificates", cols=3)

# ── TAB 3: EXPERIENCE ──
with tabs[2]:
    st.markdown('<div class="section-title"><span class="icon">💼</span> Work Experience</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">From embedded systems at Bosch to leading R&D at a healthtech startup.</p>', unsafe_allow_html=True)

    experiences = [
        {"role":"Lead R&D Product Engineer","company":"O-Health | Bangalore, India & Boston, USA","date":"Jan 2025 – Present",
         "highlights":["Improved ASR accuracy by reducing WER by 40% for Standard Hindi on edge models","Reduced inference latency by 50% via multi-stage model compression","Developed medical info extraction pipeline using RAG with hallucination-free outputs","Optimized GPU inference on H200 clusters using CUDA, TensorRT, batch processing","Led end-to-end health band development, collaborating with MIT CSAIL"],
         "skills":["ASR","NLP","RAG","Linux","Edge ML","GPU Acceleration","Health-tech"]},
        {"role":"Werkstudent Embedded IoT Engineer","company":"Würth Elektronik eiSoS | Munich, Germany","date":"May 2022 – Jan 2025",
         "highlights":["Optimized AT-command interfaces and multi-threaded buffer management","Designed low-level LTE-M / NB-IoT firmware drivers with robust state machines","Ensured reliable high-frequency IoT data transmission under variable conditions"],
         "skills":["LTE-M","NB-IoT","Firmware","Multithreading","ARM","Network Security","Edge ML"]},
        {"role":"Embedded Software Engineer","company":"Robert Bosch | Bangalore, India","date":"Jan 2021 – Sep 2021",
         "highlights":["Implemented ECU security algorithms based on customer requirements","Developed SecOC tool for automated data transmission between ECUs over CAN bus"],
         "skills":["ECU Security","CAN","CAPL","CANoe","XCP"]},
        {"role":"Embedded Software Developer","company":"AmberFlux EdgeAI | Hyderabad, India","date":"Nov 2020 – Jan 2021",
         "highlights":["Integrated sensors on Raspberry Pi, STM32 and Xtensa chips for real-time positioning","Implemented and optimized embedded AI models for edge devices"],
         "skills":["Sensor Integration","Raspberry Pi","Real-time Processing","Embedded AI"]},
        {"role":"Product Verification Engineer Intern","company":"Tejas Networks | Bangalore, India","date":"Jan 2020 – Jul 2020",
         "highlights":["Automated product verification and testing of Layer-2 systems","Designed test scenarios and developed automation scripts using Python and TCL"],
         "skills":["Layer-2 Networking","Test Automation","Python","TCL"]},
    ]
    for exp in experiences:
        hl = "".join([f"<li>{h}</li>" for h in exp["highlights"]])
        sk = "".join([f'<span class="skill-tag">{s}</span>' for s in exp["skills"]])
        st.markdown(f'<div class="timeline-card"><div class="card-header"><div><div class="card-role">{exp["role"]}</div><div class="card-company">{exp["company"]}</div></div><span class="card-date">{exp["date"]}</span></div><div class="card-desc"><ul style="margin:0.5rem 0;padding-left:1.2rem;">{hl}</ul></div><div class="card-skills">{sk}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📸 Work Experience Photos")
    render_gallery("experience", cols=3)

# ── TAB 4: EDUCATION ──
with tabs[3]:
    st.markdown('<div class="section-title"><span class="icon">🎓</span> Education</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="edu-card"><div style="display:flex;justify-content:space-between;align-items:flex-start;"><div><div class="edu-degree">M.Sc. Communication Engineering (MSCE)</div><div class="edu-school">Technical University of Munich (TUM) — Munich, Germany</div></div><span class="card-date">Oct 2021 – Oct 2024</span></div><div class="edu-details" style="margin-top:0.8rem;"><strong>Grade:</strong> 2.1<br><strong>Master Thesis:</strong> "Implementation of Lane-Free Traffic Control strategies on Connected Mini Automated Vehicles" <em>(Grade: 1.0)</em><br><strong>Focus:</strong> Embedded Systems & Security, IoT, System-on-Chip, Data Networks<br><strong>Extra:</strong> 6G Business Modeling & Prototyping Lab (TUM CDTM)</div></div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="edu-card"><div style="display:flex;justify-content:space-between;align-items:flex-start;"><div><div class="edu-degree">B.E. Electronics & Communication Engineering</div><div class="edu-school">National Institute of Engineering — Mysore, India</div></div><span class="card-date">Aug 2016 – Oct 2020</span></div><div class="edu-details" style="margin-top:0.8rem;"><strong>Grade:</strong> 1.6<br><strong>Bachelor Thesis:</strong> Data Analysis from Sensors utilizing Digital Signal Processors and Wireless Sensor Networks <em>(Grade: 1.0)</em><br><strong>Focus:</strong> Digital Electronics, Embedded Systems, Network Security, C++, Microcontrollers</div></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size:1.3rem;"><span class="icon">📜</span> Online Courses</div>', unsafe_allow_html=True)
    for course in ["IoT Wireless & Cloud Computing – Yonsei University (Coursera)","Embedded Hardware & Operating Systems – EIT Digital (Coursera)","Computer Networks & IP Protocol – IIT Kharagpur (NPTEL)","Python for Computer Vision with OpenCV and Deep Learning (Udemy)"]:
        st.markdown(f'<div class="contact-item"><span class="contact-icon">📘</span><span class="contact-text">{course}</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📎 Degree Certificates")
    render_gallery("education", cols=2)

# ── TAB 5: PRODUCTS ──
with tabs[4]:
    st.markdown('<div class="section-title"><span class="icon">🔧</span> Products & Builds</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Hardware, software, and everything in between.</p>', unsafe_allow_html=True)

    products = [
        {"name":"Health Band — O-Health","desc":"Production-grade health monitoring wearable developed in Munich, collaborating with MIT CSAIL. 30,000+ clinical consultations.","tags":["Hardware","Firmware","ML","BLE","Healthcare"]},
        {"name":"ASR Engine for Hindi — Edge","desc":"ASR optimized for Standard Hindi on edge devices. 40% WER improvement, 50% latency reduction.","tags":["ASR","Edge ML","Model Compression","NLP"]},
        {"name":"Medical RAG Pipeline","desc":"Retrieval-Augmented Generation for medical info extraction with hallucination-free outputs.","tags":["RAG","LLM","Healthcare","NLP"]},
        {"name":"Retrofittable E-Bike Auto Shifter","desc":"IoT-enabled automatic rear-derailleur shifting. IEEE ICCE 2024 Best Presentation Award.","tags":["IoT","Mechatronics","Sensors","IEEE"]},
        {"name":"SecOC Tool — Robert Bosch","desc":"Automated ECU data encryption and secure communication tool for CAN bus.","tags":["Automotive","Security","CAN","CAPL"]},
        {"name":"Autonomous Mini Vehicle — TUM","desc":"Connected mini automated vehicle with lane-free traffic control and V2V communication.","tags":["Autonomous","V2V","ROS","Sensor Fusion"]},
    ]
    for i in range(0, len(products), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(products):
                p = products[i+j]
                tk = "".join([f'<span class="skill-tag">{t}</span>' for t in p["tags"]])
                with cols[j]:
                    st.markdown(f'<div class="timeline-card" style="min-height:180px;"><div class="card-role">{p["name"]}</div><div class="card-desc" style="margin:0.5rem 0;">{p["desc"]}</div><div class="card-skills">{tk}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📸 Product Gallery")
    render_gallery("products", cols=3)

# ── TAB 6: ACADEMICS ──
with tabs[5]:
    st.markdown('<div class="section-title"><span class="icon">📚</span> Academic Work</div>', unsafe_allow_html=True)

    st.markdown("### 🔬 Research Projects")
    for proj in [
        {"title":"Lane-Free Traffic Control for Connected Mini-Automated Vehicles","venue":"Master's Thesis — TU München","date":"Feb–Oct 2024","desc":"Lane-free control strategies for connected autonomous vehicles using V2V communication.","skills":["Vehicle Control","V2V","Sensor Fusion","Autonomous Systems"]},
        {"title":"Embedded Development for E-Bike","venue":"EMotorad India","date":"Jun 2023 – Feb 2024","desc":"Sensor fusion algorithms and mechatronics for automatic pedal-assist with wireless integration.","skills":["Embedded Systems","Sensor Fusion","IoT","Mechatronics"]},
    ]:
        sk = "".join([f'<span class="skill-tag">{s}</span>' for s in proj["skills"]])
        st.markdown(f'<div class="timeline-card"><div class="card-header"><div><div class="card-role">{proj["title"]}</div><div class="card-company">{proj["venue"]}</div></div><span class="card-date">{proj["date"]}</span></div><div class="card-desc">{proj["desc"]}</div><div class="card-skills">{sk}</div></div>', unsafe_allow_html=True)

    st.markdown("### 📄 Publications")
    for pub in [
        {"title":"Retrofittable Automatic Shifter of Rear-Derailleur with Mode-Based Transmission and IoT","venue":"IEEE ICCE 2024","desc":"Retrofittable automatic rear-derailleur shifting for E-bikes with IoT and adaptive riding modes."},
        {"title":"Remote Monitoring Robot with Voice Control and Image Analysis","venue":"Scopus-indexed Journal (IJAST)","desc":"Intelligent surveillance robot with real-time image processing, voice control, and MQTT communication."},
        {"title":"Data Extraction with Signal Comparison for Forest Logging Prevention","venue":"IJERT | NCCDS 2020","desc":"Wireless sensor network for illegal forest logging detection using FFT-based signal processing."},
    ]:
        st.markdown(f'<div class="pub-card"><div class="pub-title">{pub["title"]}</div><div class="pub-venue">{pub["venue"]}</div><div class="pub-desc">{pub["desc"]}</div></div>', unsafe_allow_html=True)

    st.markdown("### 🎤 Conferences")
    for conf in [
        {"name":"IEEE ICCE 2024","location":"Las Vegas, USA","note":"Best Presentation Award"},
        {"name":"Bosch Future Mobility Challenge 2023","location":"Cluj, Romania","note":"Semi-finalist"},
        {"name":"ICICEE 2020","location":"Tumkur, India","note":"Best Paper Award"},
        {"name":"NCCDS 2020","location":"Mysuru, India","note":"Paper Presentation"},
        {"name":"ANKURA'19","location":"Mysore, India","note":"National Paper Presentation"},
        {"name":"TI Innovation Challenge 2019","location":"India","note":"Design Contest"},
    ]:
        st.markdown(f'<div class="contact-item"><span class="contact-icon">🎙️</span><span class="contact-text"><strong>{conf["name"]}</strong> — {conf["location"]} <em>({conf["note"]})</em></span></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📸 Academic Gallery")
    render_gallery("academics", cols=3)

# ── TAB 7: CONTACT ──
with tabs[6]:
    st.markdown('<div class="section-title"><span class="icon">📬</span> Get In Touch</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="contact-item"><span class="contact-icon">📞</span><span class="contact-text">+49 176 71095238</span></div>
        <div class="contact-item"><span class="contact-icon">📧</span><span class="contact-text"><a href="mailto:shashankv099@gmail.com">shashankv099@gmail.com</a></span></div>
        <div class="contact-item"><span class="contact-icon">💼</span><span class="contact-text"><a href="https://www.linkedin.com/in/shashank-hegde98" target="_blank">linkedin.com/in/shashank-hegde98</a></span></div>
        <div class="contact-item"><span class="contact-icon">🌍</span><span class="contact-text">Bangalore, India & Munich, Germany</span></div>
        <div class="contact-item"><span class="contact-icon">🇺🇸</span><span class="contact-text">Nationality: United States of America</span></div>
        """, unsafe_allow_html=True)
        st.markdown("")
        st.markdown("#### 🌐 Languages")
        st.markdown("""
        <div class="contact-item"><span class="contact-icon">🇬🇧</span><span class="contact-text">English — C2 (Proficient)</span></div>
        <div class="contact-item"><span class="contact-icon">🇩🇪</span><span class="contact-text">German — A2 (Learning B1)</span></div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="hero-container" style="padding:2rem;"><div style="font-size:1.1rem;font-weight:600;color:var(--text-primary);margin-bottom:0.5rem;">Open to Opportunities</div><div class="hero-bio" style="font-size:0.95rem;">Interested in roles involving Embedded ML, Edge AI, Healthcare Technology, and IoT systems. Feel free to reach out via email or LinkedIn.</div></div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<div style="text-align:center;padding:1rem;color:var(--text-muted);font-size:0.85rem;"><span style="background:var(--gradient-1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;">Shashank Hegde</span> · Embedded-ML Electronics Engineer · © 2025</div>', unsafe_allow_html=True)
