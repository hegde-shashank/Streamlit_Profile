import streamlit as st
import json
import os
import base64
from pathlib import Path
from datetime import datetime

# ─── Page Config ───
st.set_page_config(
    page_title="Shashank Hegde | Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Data Persistence ───
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def load_data(key, default=None):
    path = DATA_DIR / f"{key}.json"
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return default if default is not None else []

def save_data(key, data):
    with open(DATA_DIR / f"{key}.json", "w") as f:
        json.dump(data, f, indent=2)

def save_uploaded_file(uploaded_file, category):
    cat_dir = UPLOAD_DIR / category
    cat_dir.mkdir(exist_ok=True)
    file_path = cat_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(file_path)

def get_uploaded_files(category):
    cat_dir = UPLOAD_DIR / category
    if cat_dir.exists():
        return [str(p) for p in cat_dir.iterdir() if p.is_file()]
    return []

def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

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

/* Global */
.stApp {
    font-family: 'Outfit', sans-serif !important;
}

.block-container {
    padding-top: 1rem !important;
    max-width: 1200px !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* ─── Navigation Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--bg-secondary);
    border-radius: 16px;
    padding: 6px;
    border: 1px solid var(--border);
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.6rem 1.2rem;
    border-radius: 12px;
    color: var(--text-secondary);
    background: transparent;
    border: none;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: var(--gradient-1) !important;
    color: white !important;
    font-weight: 600;
    box-shadow: 0 4px 15px var(--accent-glow);
}

/* ─── Hero Section ─── */
.hero-container {
    position: relative;
    padding: 3rem 2.5rem;
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.08), rgba(139, 92, 246, 0.08));
    border: 1px solid var(--border);
    border-radius: 24px;
    margin-bottom: 2rem;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(14, 165, 233, 0.1), transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-name {
    font-family: 'Outfit', sans-serif !important;
    font-size: 3.2rem;
    font-weight: 900;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.3rem 0;
    line-height: 1.1;
}

.hero-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    color: var(--accent);
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
}

.hero-bio {
    font-size: 1.05rem;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 700px;
}

/* ─── Stat Cards ─── */
.stat-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}

.stat-card {
    flex: 1;
    min-width: 140px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(14, 165, 233, 0.15);
}

.stat-number {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 0.8rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.3rem;
}

/* ─── Section Title ─── */
.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 2rem 0 1.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.section-title .icon {
    font-size: 1.5rem;
}

.section-subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-top: -1rem;
    margin-bottom: 1.5rem;
}

/* ─── Experience / Timeline Cards ─── */
.timeline-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.timeline-card:hover {
    border-color: var(--accent);
    box-shadow: 0 8px 30px rgba(14, 165, 233, 0.1);
}

.timeline-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--gradient-1);
    border-radius: 4px 0 0 4px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.8rem;
}

.card-role {
    font-family: 'Outfit', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
}

.card-company {
    font-size: 0.95rem;
    color: var(--accent);
    font-weight: 500;
}

.card-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted);
    background: rgba(14, 165, 233, 0.1);
    padding: 0.3rem 0.8rem;
    border-radius: 8px;
    white-space: nowrap;
}

.card-desc {
    color: var(--text-secondary);
    font-size: 0.92rem;
    line-height: 1.6;
}

.card-skills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.8rem;
}

.skill-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--accent);
    background: rgba(14, 165, 233, 0.1);
    border: 1px solid rgba(14, 165, 233, 0.2);
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
}

/* ─── Education Card ─── */
.edu-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.2rem;
    transition: all 0.3s ease;
}

.edu-card:hover {
    border-color: var(--accent-2);
    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.1);
}

.edu-degree {
    font-family: 'Outfit', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    background: var(--gradient-2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.edu-school {
    font-size: 1rem;
    color: var(--text-primary);
    font-weight: 500;
    margin: 0.3rem 0;
}

.edu-details {
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ─── Award Badge ─── */
.award-card {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), rgba(239, 68, 68, 0.05));
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.award-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.15);
}

.award-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #f59e0b;
}

.award-desc {
    color: var(--text-secondary);
    font-size: 0.88rem;
    margin-top: 0.3rem;
}

/* ─── Publication Card ─── */
.pub-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.pub-card:hover {
    border-color: var(--accent-3);
}

.pub-title {
    font-weight: 700;
    color: var(--text-primary);
    font-size: 1rem;
}

.pub-venue {
    font-size: 0.85rem;
    color: var(--accent-3);
    margin-top: 0.2rem;
}

.pub-desc {
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin-top: 0.5rem;
    line-height: 1.5;
}

/* ─── Gallery Grid ─── */
.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}

.gallery-item {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid var(--border);
    transition: all 0.3s ease;
}

.gallery-item:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 30px rgba(14, 165, 233, 0.15);
}

.gallery-item img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

/* ─── Contact Card ─── */
.contact-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.8rem 1.2rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 0.5rem;
    transition: all 0.2s ease;
}

.contact-item:hover {
    border-color: var(--accent);
}

.contact-icon {
    font-size: 1.2rem;
}

.contact-text {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.contact-text a {
    color: var(--accent);
    text-decoration: none;
}

/* ─── Image Carousel ─── */
.carousel-container {
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    border: 1px solid var(--border);
    margin: 1rem 0;
}

/* ─── Photo circle ─── */
.profile-photo {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    border: 3px solid var(--accent);
    object-fit: cover;
    box-shadow: 0 0 30px var(--accent-glow);
}

/* ─── Skill Bars ─── */
.skill-bar-container {
    margin-bottom: 0.8rem;
}

.skill-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 0.3rem;
}

.skill-bar-bg {
    height: 6px;
    background: var(--bg-primary);
    border-radius: 3px;
    overflow: hidden;
}

.skill-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 1s ease;
}

/* Streamlit overrides */
.stImage > img {
    border-radius: 12px;
}

div[data-testid="stFileUploader"] {
    border: 2px dashed var(--border) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
}

div[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
}

.stButton > button {
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px var(--accent-glow) !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Tab Navigation ───
tabs = st.tabs([
    "🏠 Home",
    "🏆 Certificates",
    "💼 Experience",
    "🎓 Education",
    "🔧 Products",
    "📚 Academics",
    "📬 Contact",
])

# ════════════════════════════════════════════════
# TAB 1: HOME
# ════════════════════════════════════════════════
with tabs[0]:

    # Hero Section
    col_photo, col_info = st.columns([1, 3], gap="large")

    with col_photo:
        profile_photos = get_uploaded_files("profile")
        if profile_photos:
            st.markdown(f'<img src="data:image/png;base64,{get_image_base64(profile_photos[0])}" class="profile-photo">', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="width:140px;height:140px;border-radius:50%;background:linear-gradient(135deg,#0ea5e9,#8b5cf6);
            display:flex;align-items:center;justify-content:center;font-size:3rem;color:white;
            border:3px solid #0ea5e9;box-shadow:0 0 30px rgba(14,165,233,0.3);">SH</div>
            """, unsafe_allow_html=True)

        with st.expander("📷 Upload Profile Photo"):
            photo = st.file_uploader("Choose photo", type=["jpg", "jpeg", "png"], key="profile_photo")
            if photo:
                save_uploaded_file(photo, "profile")
                st.success("Uploaded!")
                st.rerun()

    with col_info:
        st.markdown("""
        <div class="hero-container">
            <div class="hero-name">Shashank Hegde</div>
            <div class="hero-title">Embedded-ML Electronics Engineer | Lead Product R&D</div>
            <div class="hero-bio">
                Lead Product R&D Engineer and TUM graduate, working in a startup since inception 
                with ownership of embedded and ML-based healthcare systems, including edge ML, 
                wireless sensor connectivity, and product-grade system development. Over 5 years 
                of experience across MNCs like Robert Bosch and high-growth startups, with a unique 
                blend of theoretical research and production-level deployment.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Stats
    st.markdown("""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-number">5+</div>
            <div class="stat-label">Years Experience</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">30K+</div>
            <div class="stat-label">Clinical Consults</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">3</div>
            <div class="stat-label">Publications</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">5</div>
            <div class="stat-label">Awards</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">2</div>
            <div class="stat-label">Degrees</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Achievements Carousel
    st.markdown('<div class="section-title"><span class="icon">🏅</span> Highlights & Achievements</div>', unsafe_allow_html=True)

    achievement_images = get_uploaded_files("achievements")
    if achievement_images:
        # Slidable carousel using columns
        items_per_page = 3
        if "ach_page" not in st.session_state:
            st.session_state.ach_page = 0

        total_pages = max(1, (len(achievement_images) + items_per_page - 1) // items_per_page)

        nav_col1, nav_col2, nav_col3 = st.columns([1, 4, 1])
        with nav_col1:
            if st.button("◀ Prev", key="ach_prev"):
                st.session_state.ach_page = (st.session_state.ach_page - 1) % total_pages
        with nav_col3:
            if st.button("Next ▶", key="ach_next"):
                st.session_state.ach_page = (st.session_state.ach_page + 1) % total_pages
        with nav_col2:
            st.caption(f"Page {st.session_state.ach_page + 1} of {total_pages}")

        start = st.session_state.ach_page * items_per_page
        end = min(start + items_per_page, len(achievement_images))
        cols = st.columns(items_per_page)
        for i, img_path in enumerate(achievement_images[start:end]):
            with cols[i]:
                st.image(img_path, use_container_width=True)
    else:
        st.info("No achievement images uploaded yet. Add them below!")

    with st.expander("➕ Add Achievement Images"):
        ach_files = st.file_uploader(
            "Upload achievement photos", type=["jpg", "jpeg", "png"],
            accept_multiple_files=True, key="ach_upload"
        )
        if ach_files:
            for f in ach_files:
                save_uploaded_file(f, "achievements")
            st.success(f"Uploaded {len(ach_files)} image(s)!")
            st.rerun()

    # Key Highlights
    st.markdown("""
    <div class="award-card">
        <div class="award-title">🏆 Best Presentation Award — IEEE ICCE 2024, Las Vegas</div>
        <div class="award-desc">Presented research on IoT-enabled automatic gear shifting for E-bikes at the IEEE International Conference on Consumer Electronics. Awarded best presentation among 50+ papers.</div>
    </div>
    <div class="award-card">
        <div class="award-title">🏆 Bosch Future Mobility Challenge — Semi-Finalist, Cluj Romania</div>
        <div class="award-desc">Represented Germany among 100+ international teams. Led embedded sensor fusion on NVIDIA Jetson Xavier for autonomous vehicle navigation.</div>
    </div>
    <div class="award-card">
        <div class="award-title">🏆 Bravo Award — Robert Bosch</div>
        <div class="award-desc">Recognized for successful and timely delivery of a SecOC tool in ECU security, demonstrating exceptional commitment as a fresher.</div>
    </div>
    """, unsafe_allow_html=True)

    # Skills Section
    st.markdown('<div class="section-title"><span class="icon">⚡</span> Core Competencies</div>', unsafe_allow_html=True)

    skills_data = {
        "Embedded Systems & IoT": ["Edge ML", "Arduino", "Raspberry Pi", "STM32", "Firmware Dev", "IoT Security", "CAN", "V2V"],
        "AI & Machine Learning": ["ASR", "NLP", "RAG", "Model Compression", "TensorRT", "GPU Acceleration", "Computer Vision"],
        "Programming": ["Python", "C", "C++", "CAPL", "ROS"],
        "Tools & Platforms": ["Linux/RHEL", "CUDA", "NVIDIA Jetson", "Docker", "Git"],
    }

    col1, col2 = st.columns(2)
    for idx, (category, skills) in enumerate(skills_data.items()):
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"**{category}**")
            tags_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
            st.markdown(f'<div class="card-skills">{tags_html}</div>', unsafe_allow_html=True)
            st.markdown("")


# ════════════════════════════════════════════════
# TAB 2: CERTIFICATES
# ════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-title"><span class="icon">🏆</span> Certificates & Awards</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">A collection of certificates, awards, and recognitions earned throughout my career.</p>', unsafe_allow_html=True)

    # Default certificates info
    default_certs = [
        {"title": "Best Session Presentation Award — IEEE ICCE 2024", "desc": "Las Vegas, USA | January 2024", "category": "Award"},
        {"title": "Certificate of Participation — IEEE ICCE 2024", "desc": "Retrofittable Automatic Shifter of Rear-Derailleur with Mode-Based Transmission and IoT", "category": "Conference"},
        {"title": "Best Paper Award — ICICEE 2020", "desc": "Remote Monitoring with Voice Command Control and Image Analysis | Tumkur, India", "category": "Award"},
        {"title": "Bravo Award — Robert Bosch", "desc": "Recognized for SecOC tool delivery in ECU security | August 2021", "category": "Corporate"},
        {"title": "Bosch Future Mobility Challenge", "desc": "Team TUMAVERICK — Semi-finalist representing TU Munich | Cluj, Romania 2023", "category": "Competition"},
        {"title": "Tejas Networks Internship Certificate", "desc": "Product verification and test automation | January–May 2020", "category": "Internship"},
        {"title": "NCCDS 2020 Participation", "desc": "Data Extraction with Signal Comparison for Forest Logging Prevention", "category": "Conference"},
        {"title": "NIE IEEE Biblus — Paper Presentation", "desc": "ANKURA'19 National Level Paper Presentation", "category": "Conference"},
        {"title": "NIE Summer of Code 5.0", "desc": "Hardware Track | June 2018", "category": "Workshop"},
        {"title": "Adroit'18 — Certificate of Appreciation", "desc": "IEEE NIE Student Branch volunteering | October 2018", "category": "Volunteering"},
        {"title": "Texas Instruments Innovation Challenge 2019", "desc": "DST & TI India Innovation Challenge Design Contest", "category": "Competition"},
    ]

    # Filter by category
    categories = sorted(set(c["category"] for c in default_certs))
    selected_cat = st.multiselect("Filter by category", categories, default=categories, key="cert_filter")

    filtered = [c for c in default_certs if c["category"] in selected_cat]

    for cert in filtered:
        cat_colors = {
            "Award": "#f59e0b",
            "Conference": "#0ea5e9",
            "Corporate": "#8b5cf6",
            "Competition": "#ec4899",
            "Internship": "#10b981",
            "Workshop": "#06b6d4",
            "Volunteering": "#a78bfa",
        }
        color = cat_colors.get(cert["category"], "#0ea5e9")
        st.markdown(f"""
        <div class="timeline-card" style="border-left:4px solid {color};">
            <div class="card-header">
                <div>
                    <div class="card-role">{cert["title"]}</div>
                    <div class="card-desc">{cert["desc"]}</div>
                </div>
                <span class="card-date">{cert["category"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Upload certificates
    st.markdown("---")
    st.markdown("#### 📎 Upload Certificate Images")
    cert_images = get_uploaded_files("certificates")

    if cert_images:
        cols = st.columns(3)
        for i, img_path in enumerate(cert_images):
            with cols[i % 3]:
                st.image(img_path, caption=Path(img_path).stem, use_container_width=True)

    cert_files = st.file_uploader(
        "Upload certificate images", type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True, key="cert_upload"
    )
    if cert_files:
        for f in cert_files:
            save_uploaded_file(f, "certificates")
        st.success(f"Uploaded {len(cert_files)} certificate(s)!")
        st.rerun()


# ════════════════════════════════════════════════
# TAB 3: EXPERIENCE
# ════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-title"><span class="icon">💼</span> Work Experience</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">From embedded systems at Bosch to leading R&D at a healthtech startup.</p>', unsafe_allow_html=True)

    experiences = [
        {
            "role": "Lead R&D Product Engineer",
            "company": "O-Health | Bangalore, India & Boston, USA",
            "date": "Jan 2025 – Present",
            "highlights": [
                "Improved ASR accuracy by reducing Word Error Rate by 40% for Standard Hindi on edge models",
                "Reduced inference latency by 50% via multi-stage model compression pipeline",
                "Developed medical info extraction pipeline using RAG with hallucination-free outputs",
                "Optimized GPU inference on H200 clusters using CUDA, TensorRT, and batch processing",
                "Led end-to-end health band development, collaborating with MIT CSAIL",
            ],
            "skills": ["ASR", "NLP", "RAG", "Linux", "Edge ML", "GPU Acceleration", "Health-tech"],
        },
        {
            "role": "Werkstudent Embedded IoT Engineer",
            "company": "Würth Elektronik eiSoS | Munich, Germany",
            "date": "May 2022 – Jan 2025",
            "highlights": [
                "Optimized AT-command interfaces and multi-threaded buffer management in firmware",
                "Designed low-level LTE-M / NB-IoT firmware drivers with robust state machines",
                "Ensured reliable high-frequency IoT data transmission under variable signal conditions",
            ],
            "skills": ["LTE-M", "NB-IoT", "Firmware", "Multithreading", "ARM", "Network Security", "Edge ML"],
        },
        {
            "role": "Embedded Software Engineer",
            "company": "Robert Bosch Business & Solutions | Bangalore, India",
            "date": "Jan 2021 – Sep 2021",
            "highlights": [
                "Implemented ECU security algorithms based on customer requirements",
                "Developed SecOC tool for automated data transmission between ECUs over CAN bus",
            ],
            "skills": ["ECU Security", "CAN", "CAPL", "CANoe", "XCP"],
        },
        {
            "role": "Embedded Software Developer",
            "company": "AmberFlux EdgeAI Private Limited | Hyderabad, India",
            "date": "Nov 2020 – Jan 2021",
            "highlights": [
                "Integrated sensors on Raspberry Pi, STM32 and Xtensa chips for real-time positioning",
                "Implemented and optimized embedded AI models for edge devices",
            ],
            "skills": ["Sensor Integration", "Raspberry Pi", "Real-time Processing", "Embedded AI"],
        },
        {
            "role": "Product Verification Engineer Intern",
            "company": "Tejas Networks | Bangalore, India",
            "date": "Jan 2020 – Jul 2020",
            "highlights": [
                "Automated product verification and testing of Layer-2 systems for optical comms",
                "Designed test scenarios and developed automation scripts using Python and TCL",
            ],
            "skills": ["Layer-2 Networking", "Test Automation", "Python", "TCL"],
        },
    ]

    for exp in experiences:
        highlights_html = "".join([f"<li>{h}</li>" for h in exp["highlights"]])
        skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in exp["skills"]])

        st.markdown(f"""
        <div class="timeline-card">
            <div class="card-header">
                <div>
                    <div class="card-role">{exp["role"]}</div>
                    <div class="card-company">{exp["company"]}</div>
                </div>
                <span class="card-date">{exp["date"]}</span>
            </div>
            <div class="card-desc"><ul style="margin:0.5rem 0;padding-left:1.2rem;">{highlights_html}</ul></div>
            <div class="card-skills">{skills_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # Upload work experience images
    st.markdown("---")
    st.markdown("#### 📸 Work Experience Photos")
    exp_images = get_uploaded_files("experience")
    if exp_images:
        cols = st.columns(3)
        for i, img_path in enumerate(exp_images):
            with cols[i % 3]:
                st.image(img_path, caption=Path(img_path).stem, use_container_width=True)

    exp_files = st.file_uploader(
        "Upload work experience images", type=["jpg", "jpeg", "png"],
        accept_multiple_files=True, key="exp_upload"
    )
    if exp_files:
        for f in exp_files:
            save_uploaded_file(f, "experience")
        st.success(f"Uploaded {len(exp_files)} image(s)!")
        st.rerun()


# ════════════════════════════════════════════════
# TAB 4: EDUCATION
# ════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-title"><span class="icon">🎓</span> Education</div>', unsafe_allow_html=True)

    # TUM
    st.markdown("""
    <div class="edu-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                <div class="edu-degree">M.Sc. Communication Engineering (MSCE)</div>
                <div class="edu-school">Technical University of Munich (TUM) — Munich, Germany</div>
            </div>
            <span class="card-date">Oct 2021 – Oct 2024</span>
        </div>
        <div class="edu-details" style="margin-top:0.8rem;">
            <strong>Grade:</strong> 2.1<br>
            <strong>Master Thesis:</strong> "Implementation of Lane-Free Traffic Control strategies on Connected Mini Automated Vehicles" at the Chair of Traffic Engineering and Control <em>(Grade: 1.0)</em><br>
            <strong>Focus:</strong> Embedded Systems & Security, IoT, System-on-Chip, Data Networks<br>
            <strong>Extra:</strong> 6G Business Modeling & Prototyping Lab (TUM CDTM) — interdisciplinary projects on technology research, use-case development and prototyping
        </div>
    </div>
    """, unsafe_allow_html=True)

    # NIE
    st.markdown("""
    <div class="edu-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                <div class="edu-degree">B.E. Electronics & Communication Engineering</div>
                <div class="edu-school">National Institute of Engineering — Mysore, India</div>
            </div>
            <span class="card-date">Aug 2016 – Oct 2020</span>
        </div>
        <div class="edu-details" style="margin-top:0.8rem;">
            <strong>Grade:</strong> 1.6<br>
            <strong>Bachelor Thesis:</strong> Data Analysis from Sensors utilizing Digital Signal Processors and Wireless Sensor Networks <em>(Grade: 1.0)</em><br>
            <strong>Focus:</strong> Digital Electronics, Embedded Systems, Network Security, C++, Microcontrollers
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Online certs
    st.markdown('<div class="section-title" style="font-size:1.3rem;"><span class="icon">📜</span> Online Courses & Certifications</div>', unsafe_allow_html=True)

    online_courses = [
        "IoT Wireless & Cloud Computing – Emerging Technologies, Yonsei University (Coursera)",
        "Embedded Hardware & Operating Systems, EIT Digital (Coursera)",
        "Computer Networks & IP Protocol, IIT Kharagpur (NPTEL)",
        "Python for Computer Vision with OpenCV and Deep Learning (Udemy)",
    ]
    for course in online_courses:
        st.markdown(f"""
        <div class="contact-item">
            <span class="contact-icon">📘</span>
            <span class="contact-text">{course}</span>
        </div>
        """, unsafe_allow_html=True)

    # Upload degree certificates
    st.markdown("---")
    st.markdown("#### 📎 Upload Degree Certificates")
    edu_images = get_uploaded_files("education")
    if edu_images:
        cols = st.columns(2)
        for i, img_path in enumerate(edu_images):
            with cols[i % 2]:
                st.image(img_path, caption=Path(img_path).stem, use_container_width=True)

    edu_files = st.file_uploader(
        "Upload degree certificates", type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True, key="edu_upload"
    )
    if edu_files:
        for f in edu_files:
            save_uploaded_file(f, "education")
        st.success(f"Uploaded {len(edu_files)} certificate(s)!")
        st.rerun()


# ════════════════════════════════════════════════
# TAB 5: PRODUCTS
# ════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-title"><span class="icon">🔧</span> Products & Builds</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Hardware, software, and everything in between — things I\'ve built and shipped.</p>', unsafe_allow_html=True)

    # Default products
    products = [
        {
            "name": "Health Band — O-Health",
            "desc": "Production-grade health monitoring wearable developed in Munich, collaborating with MIT CSAIL. Integrates custom sensors, BLE connectivity, and cloud-based ML for clinical use in 30,000+ consultations worldwide.",
            "tags": ["Hardware", "Firmware", "ML", "BLE", "Healthcare"],
        },
        {
            "name": "ASR Engine for Hindi — Edge Deployed",
            "desc": "Automatic Speech Recognition system optimized for Standard Hindi running on edge devices. Achieved 40% WER improvement with 50% latency reduction through knowledge distillation, quantization, and weight pruning.",
            "tags": ["ASR", "Edge ML", "Model Compression", "NLP"],
        },
        {
            "name": "Medical RAG Pipeline",
            "desc": "Retrieval-Augmented Generation pipeline for medical information extraction with hallucination-free outputs, validated using cross-LLM consensus and verified medical ontologies.",
            "tags": ["RAG", "LLM", "Healthcare", "NLP"],
        },
        {
            "name": "Retrofittable E-Bike Auto Shifter",
            "desc": "IoT-enabled automatic rear-derailleur shifting system for E-bikes with mode-based transmission. Published at IEEE ICCE 2024 and won Best Presentation Award.",
            "tags": ["IoT", "Mechatronics", "Sensors", "IEEE Publication"],
        },
        {
            "name": "SecOC Tool — Robert Bosch",
            "desc": "Automated ECU data encryption and secure communication tool for CAN bus, ensuring secure data transmission between Electronic Control Units.",
            "tags": ["Automotive", "Security", "CAN", "CAPL"],
        },
        {
            "name": "Autonomous Mini Vehicle — TUM",
            "desc": "Connected mini automated vehicle with lane-free traffic control. V2V communication, sensor fusion, and control loop design for autonomous navigation.",
            "tags": ["Autonomous Systems", "V2V", "ROS", "Sensor Fusion"],
        },
    ]

    for i in range(0, len(products), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(products):
                p = products[i + j]
                tags_html = "".join([f'<span class="skill-tag">{t}</span>' for t in p["tags"]])
                with cols[j]:
                    st.markdown(f"""
                    <div class="timeline-card" style="min-height:200px;">
                        <div class="card-role">{p["name"]}</div>
                        <div class="card-desc" style="margin:0.5rem 0;">{p["desc"]}</div>
                        <div class="card-skills">{tags_html}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # Upload product images
    st.markdown("---")
    st.markdown("#### 📸 Product Gallery")
    prod_images = get_uploaded_files("products")
    if prod_images:
        cols = st.columns(3)
        for i, img_path in enumerate(prod_images):
            with cols[i % 3]:
                st.image(img_path, caption=Path(img_path).stem, use_container_width=True)

    prod_files = st.file_uploader(
        "Upload product / build images", type=["jpg", "jpeg", "png"],
        accept_multiple_files=True, key="prod_upload"
    )
    if prod_files:
        for f in prod_files:
            save_uploaded_file(f, "products")
        st.success(f"Uploaded {len(prod_files)} image(s)!")
        st.rerun()

    # Custom product entry
    with st.expander("➕ Add Custom Product"):
        custom_products = load_data("custom_products", [])
        p_name = st.text_input("Product Name", key="cp_name")
        p_desc = st.text_area("Description", key="cp_desc")
        p_tags = st.text_input("Tags (comma separated)", key="cp_tags")
        if st.button("Add Product", key="add_product"):
            if p_name:
                custom_products.append({
                    "name": p_name,
                    "desc": p_desc,
                    "tags": [t.strip() for t in p_tags.split(",") if t.strip()],
                })
                save_data("custom_products", custom_products)
                st.success(f"Added '{p_name}'!")
                st.rerun()

    # Show custom products
    custom_products = load_data("custom_products", [])
    if custom_products:
        st.markdown("#### Your Added Products")
        for p in custom_products:
            tags_html = "".join([f'<span class="skill-tag">{t}</span>' for t in p.get("tags", [])])
            st.markdown(f"""
            <div class="timeline-card">
                <div class="card-role">{p["name"]}</div>
                <div class="card-desc">{p.get("desc", "")}</div>
                <div class="card-skills">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════
# TAB 6: ACADEMICS
# ════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-title"><span class="icon">📚</span> Academic Work</div>', unsafe_allow_html=True)

    # Projects
    st.markdown("### 🔬 Research Projects")

    projects = [
        {
            "title": "Lane-Free Traffic Control for Connected Mini-Automated Vehicles",
            "venue": "Master's Thesis — TU München",
            "date": "Feb 2024 – Oct 2024",
            "desc": "Designed and implemented lane-free control strategies for connected autonomous vehicles. Defined control loops and boundary conditions using V2V communication.",
            "skills": ["Vehicle Control", "V2V", "Sensor Fusion", "Autonomous Systems"],
        },
        {
            "title": "Embedded Development for E-Bike",
            "venue": "Project with EMotorad India",
            "date": "Jun 2023 – Feb 2024",
            "desc": "Developed sensor fusion algorithms and mechatronics systems for automatic pedal-assist. Contributed to embedded/PCB development and firmware with wireless sensor integration.",
            "skills": ["Embedded Systems", "Sensor Fusion", "IoT", "Mechatronics"],
        },
    ]

    for proj in projects:
        skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in proj["skills"]])
        st.markdown(f"""
        <div class="timeline-card">
            <div class="card-header">
                <div>
                    <div class="card-role">{proj["title"]}</div>
                    <div class="card-company">{proj["venue"]}</div>
                </div>
                <span class="card-date">{proj["date"]}</span>
            </div>
            <div class="card-desc">{proj["desc"]}</div>
            <div class="card-skills">{skills_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # Publications
    st.markdown("### 📄 Publications")

    publications = [
        {
            "title": "Retrofittable Automatic Shifter of Rear-Derailleur with Mode-Based Transmission and IoT",
            "venue": "IEEE ICCE 2024 | ieeexplore.ieee.org/document/10444469",
            "desc": "Developed a retrofittable automatic rear-derailleur shifting system for E-bikes with IoT connectivity, adaptive riding modes, and sensor-driven autonomous gear shifting.",
        },
        {
            "title": "Remote Monitoring Robot with Voice Control and Image Analysis",
            "venue": "Scopus-indexed Journal (IJAST) | Published Oct 2019 – Jun 2020",
            "desc": "Intelligent surveillance robot with real-time image processing, voice-based control, speech recognition for navigation, and MQTT-based distributed communication.",
        },
        {
            "title": "Data Extraction with Signal Comparison for Forest Logging Prevention",
            "venue": "IJERT | NCCDS 2020",
            "desc": "Wireless sensor network for illegal forest logging detection using FFT-based signal processing in MATLAB with STM32 implementation nodes.",
        },
    ]

    for pub in publications:
        st.markdown(f"""
        <div class="pub-card">
            <div class="pub-title">{pub["title"]}</div>
            <div class="pub-venue">{pub["venue"]}</div>
            <div class="pub-desc">{pub["desc"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # Conferences & Presentations
    st.markdown("### 🎤 Conferences & Presentations")

    conferences = [
        {"name": "IEEE ICCE 2024", "location": "Las Vegas, USA", "note": "Best Presentation Award"},
        {"name": "Bosch Future Mobility Challenge 2023", "location": "Cluj, Romania", "note": "Semi-finalist representing Germany"},
        {"name": "ICICEE 2020", "location": "Tumkur, India", "note": "Best Paper Award"},
        {"name": "NCCDS 2020", "location": "Mysuru, India", "note": "Paper Presentation"},
        {"name": "NIE IEEE Biblus — ANKURA'19", "location": "Mysore, India", "note": "National Level Paper Presentation"},
        {"name": "Texas Instruments Innovation Challenge 2019", "location": "India", "note": "Design Contest Participant"},
    ]

    for conf in conferences:
        st.markdown(f"""
        <div class="contact-item">
            <span class="contact-icon">🎙️</span>
            <span class="contact-text"><strong>{conf["name"]}</strong> — {conf["location"]} <em>({conf["note"]})</em></span>
        </div>
        """, unsafe_allow_html=True)

    # Upload academic images
    st.markdown("---")
    st.markdown("#### 📸 Academic Gallery")
    acad_images = get_uploaded_files("academics")
    if acad_images:
        cols = st.columns(3)
        for i, img_path in enumerate(acad_images):
            with cols[i % 3]:
                st.image(img_path, caption=Path(img_path).stem, use_container_width=True)

    acad_files = st.file_uploader(
        "Upload academic / project images", type=["jpg", "jpeg", "png"],
        accept_multiple_files=True, key="acad_upload"
    )
    if acad_files:
        for f in acad_files:
            save_uploaded_file(f, "academics")
        st.success(f"Uploaded {len(acad_files)} image(s)!")
        st.rerun()


# ════════════════════════════════════════════════
# TAB 7: CONTACT
# ════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-title"><span class="icon">📬</span> Get In Touch</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="contact-item">
            <span class="contact-icon">📞</span>
            <span class="contact-text">+49 176 71095238</span>
        </div>
        <div class="contact-item">
            <span class="contact-icon">📧</span>
            <span class="contact-text"><a href="mailto:shashankv099@gmail.com">shashankv099@gmail.com</a></span>
        </div>
        <div class="contact-item">
            <span class="contact-icon">💼</span>
            <span class="contact-text"><a href="https://www.linkedin.com/in/shashank-hegde98" target="_blank">linkedin.com/in/shashank-hegde98</a></span>
        </div>
        <div class="contact-item">
            <span class="contact-icon">🌍</span>
            <span class="contact-text">Bangalore, India & Munich, Germany</span>
        </div>
        <div class="contact-item">
            <span class="contact-icon">🇺🇸</span>
            <span class="contact-text">Nationality: United States of America</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("#### 🌐 Languages")
        st.markdown("""
        <div class="contact-item">
            <span class="contact-icon">🇬🇧</span>
            <span class="contact-text">English — C2 (Proficient)</span>
        </div>
        <div class="contact-item">
            <span class="contact-icon">🇩🇪</span>
            <span class="contact-text">German — A2 (Learning B1)</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 💌 Send a Message")
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            message = st.text_area("Message", height=150)
            submitted = st.form_submit_button("Send Message 🚀")
            if submitted:
                if name and email and message:
                    messages = load_data("messages", [])
                    messages.append({
                        "name": name,
                        "email": email,
                        "message": message,
                        "date": datetime.now().isoformat(),
                    })
                    save_data("messages", messages)
                    st.success("Message saved! Thank you for reaching out.")
                else:
                    st.warning("Please fill in all fields.")


# ─── Footer ───
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:1rem;color:var(--text-muted);font-size:0.85rem;">
    <span style="background:var(--gradient-1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;">
        Shashank Hegde
    </span> 
    · Embedded-ML Electronics Engineer · © 2025
</div>
""", unsafe_allow_html=True)
