import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Shashank Hegde | Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════
# DARK / LIGHT MODE TOGGLE
# ════════════════════════════════════════════════
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # default dark

# Toggle button top-right
head_cols = st.columns([10, 1])
with head_cols[1]:
    icon = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(icon, key="theme_toggle", help="Toggle dark/light mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

DARK = st.session_state.dark_mode

# ════════════════════════════════════════════════
# IMAGE SYSTEM
# ════════════════════════════════════════════════
ASSETS_DIR = Path("assets")
for cat in ["profile","achievements","certificates","experience","education","products","academics","projects","robotics_club"]:
    (ASSETS_DIR / cat).mkdir(parents=True, exist_ok=True)

def get_images(category: str) -> list[str]:
    cat_dir = ASSETS_DIR / category
    if not cat_dir.exists():
        return []
    return [str(p) for p in sorted(cat_dir.iterdir()) if p.suffix.lower() in {".jpg",".jpeg",".png",".webp"}]

def slideshow(category: str, key: str):
    images = get_images(category)
    if not images:
        st.info(f"No images yet — add files to `assets/{category}/` and redeploy.")
        return
    idx_key = f"slide_{key}"
    if idx_key not in st.session_state:
        st.session_state[idx_key] = 0
    total = len(images)
    idx = st.session_state[idx_key] % total
    lc, mc, rc = st.columns([0.5, 10, 0.5])
    with lc:
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
        if st.button("◀", key=f"{key}_p", help="Previous"):
            st.session_state[idx_key] = (idx - 1) % total
            st.rerun()
    with mc:
        cap = Path(images[idx]).stem.replace("_"," ").replace("-"," ")
        st.image(images[idx], use_container_width=True)
        tc = "color:#94a3b8;" if DARK else "color:#64748b;"
        st.markdown(f'<p style="text-align:center;{tc}font-size:0.85rem;margin-top:4px;">{cap} · {idx+1}/{total}</p>', unsafe_allow_html=True)
    with rc:
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
        if st.button("▶", key=f"{key}_n", help="Next"):
            st.session_state[idx_key] = (idx + 1) % total
            st.rerun()

# ─── Theme-aware CSS ───
if DARK:
    BG = "#0f172a"; BG2 = "#1e293b"; CARD = "#1e293b"
    TXT = "#f1f5f9"; TXT2 = "#cbd5e1"; TXT3 = "#94a3b8"; TXT4 = "#64748b"
    BORDER = "#334155"; ACCENT = "#3b82f6"; ACCENT2 = "#8b5cf6"
    ACCENT3 = "#10b981"; AMBER_BG = "rgba(245,158,11,0.1)"; AMBER_BD = "rgba(245,158,11,0.3)"
    AMBER_TXT = "#fbbf24"; TAG_BG = "rgba(59,130,246,0.12)"; TAG_BD = "rgba(59,130,246,0.25)"
    TAB_BG = "#1e293b"; TAB_SEL_BG = "#3b82f6"; TAB_SEL_TXT = "#ffffff"
    HERO_BG = "linear-gradient(135deg, rgba(59,130,246,0.08), rgba(139,92,246,0.08))"
    STAT_BG = "#1e293b"; PUB_LEFT = "#10b981"
else:
    BG = "#ffffff"; BG2 = "#f8fafc"; CARD = "#ffffff"
    TXT = "#0f172a"; TXT2 = "#334155"; TXT3 = "#475569"; TXT4 = "#64748b"
    BORDER = "#e2e8f0"; ACCENT = "#2563eb"; ACCENT2 = "#4f46e5"
    ACCENT3 = "#059669"; AMBER_BG = "#fffbeb"; AMBER_BD = "#fde68a"
    AMBER_TXT = "#92400e"; TAG_BG = "#eff6ff"; TAG_BD = "#dbeafe"
    TAB_BG = "#f1f5f9"; TAB_SEL_BG = "#ffffff"; TAB_SEL_TXT = "#2563eb"
    HERO_BG = "linear-gradient(135deg, rgba(37,99,235,0.04), rgba(79,70,229,0.04))"
    STAT_BG = "#f8fafc"; PUB_LEFT = "#059669"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&family=DM+Mono:wght@400;500&display=swap');

/* ── ANIMATIONS ── */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(24px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}
@keyframes slideInLeft {{
    from {{ opacity: 0; transform: translateX(-30px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes scaleIn {{
    from {{ opacity: 0; transform: scale(0.92); }}
    to {{ opacity: 1; transform: scale(1); }}
}}
@keyframes shimmer {{
    0% {{ background-position: -200% 0; }}
    100% {{ background-position: 200% 0; }}
}}

.animate-up {{ animation: fadeInUp 0.6s ease-out both; }}
.animate-fade {{ animation: fadeIn 0.5s ease-out both; }}
.animate-left {{ animation: slideInLeft 0.5s ease-out both; }}
.animate-scale {{ animation: scaleIn 0.4s ease-out both; }}

.delay-1 {{ animation-delay: 0.1s; }}
.delay-2 {{ animation-delay: 0.2s; }}
.delay-3 {{ animation-delay: 0.3s; }}
.delay-4 {{ animation-delay: 0.4s; }}
.delay-5 {{ animation-delay: 0.5s; }}

/* ── GLOBAL ── */
.stApp {{
    font-family: 'Source Sans 3', -apple-system, sans-serif !important;
    background: {BG} !important;
    color: {TXT} !important;
}}

.block-container {{ padding-top: 0.5rem !important; max-width: 1100px !important; }}
h1,h2,h3,h4,h5,h6 {{ font-family: 'Source Sans 3', sans-serif !important; color: {TXT} !important; }}
p, li, span, div, label {{ color: {TXT2}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px; background: {TAB_BG}; border-radius: 10px;
    padding: 4px; border: 1px solid {BORDER}; margin-bottom: 2rem;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'Source Sans 3', sans-serif !important; font-weight: 500;
    font-size: 0.85rem; padding: 0.5rem 1rem; border-radius: 8px;
    color: {TXT4}; background: transparent; border: none;
}}
.stTabs [aria-selected="true"] {{
    background: {TAB_SEL_BG} !important; color: {TAB_SEL_TXT} !important;
    font-weight: 600; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}}

/* ── HERO ── */
.hero-wrap {{
    padding: 2.5rem 2rem; background: {HERO_BG};
    border: 1px solid {BORDER}; border-radius: 16px; margin-bottom: 1.5rem;
}}
.hero-name {{
    font-size: 2.6rem; font-weight: 800; color: {TXT}; margin: 0 0 0.1rem 0;
    line-height: 1.15; letter-spacing: -0.5px;
}}
.hero-title {{
    font-family: 'DM Mono', monospace; font-size: 0.88rem;
    color: {ACCENT}; margin-bottom: 0.8rem;
}}
.hero-bio {{ font-size: 1rem; color: {TXT3}; line-height: 1.7; max-width: 660px; }}

/* ── STATS ── */
.stat-row {{ display: flex; gap: 0.75rem; margin: 1.2rem 0; flex-wrap: wrap; }}
.stat-card {{
    flex: 1; min-width: 115px; background: {STAT_BG};
    border: 1px solid {BORDER}; border-radius: 12px; padding: 0.9rem; text-align: center;
    transition: transform 0.25s ease, border-color 0.25s ease;
}}
.stat-card:hover {{ border-color: {ACCENT}; transform: translateY(-3px); }}
.stat-num {{ font-size: 1.7rem; font-weight: 700; color: {ACCENT}; line-height: 1.2; }}
.stat-lbl {{ font-size: 0.7rem; color: {TXT4}; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 0.1rem; }}

/* ── SECTION ── */
.sec-title {{ font-size: 1.5rem; font-weight: 700; color: {TXT}; margin: 2rem 0 0.4rem 0; }}
.sec-sub {{ color: {TXT4}; font-size: 0.9rem; margin-bottom: 1.4rem; }}

/* ── TIMELINE CARD ── */
.t-card {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 1.4rem 1.4rem 1.4rem 1.7rem; margin-bottom: 0.9rem;
    border-left: 3px solid {ACCENT};
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}}
.t-card:hover {{ box-shadow: 0 6px 20px rgba(59,130,246,0.08); transform: translateY(-2px); }}
.t-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem; }}
.t-role {{ font-size: 1.05rem; font-weight: 600; color: {TXT}; }}
.t-company {{ font-size: 0.88rem; color: {ACCENT}; font-weight: 500; }}
.t-date {{
    font-family: 'DM Mono', monospace; font-size: 0.73rem; color: {TXT4};
    background: {BG2}; padding: 0.2rem 0.6rem; border-radius: 6px;
    border: 1px solid {BORDER}; white-space: nowrap;
}}
.t-desc {{ color: {TXT3}; font-size: 0.88rem; line-height: 1.6; }}
.t-desc ul {{ margin: 0.3rem 0; padding-left: 1.1rem; }}
.t-desc li {{ margin-bottom: 0.15rem; color: {TXT3}; }}
.t-skills {{ display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.6rem; }}
.sk {{
    font-family: 'DM Mono', monospace; font-size: 0.68rem; color: {ACCENT};
    background: {TAG_BG}; border: 1px solid {TAG_BD};
    padding: 0.18rem 0.5rem; border-radius: 5px;
}}

/* ── EDU ── */
.edu-card {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 1.4rem; margin-bottom: 0.9rem;
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}}
.edu-card:hover {{ box-shadow: 0 6px 20px rgba(79,70,229,0.07); transform: translateY(-2px); }}
.edu-deg {{ font-size: 1.12rem; font-weight: 700; color: {ACCENT2}; }}
.edu-school {{ font-size: 0.92rem; color: {TXT2}; font-weight: 500; }}
.edu-det {{ color: {TXT3}; font-size: 0.86rem; line-height: 1.6; margin-top: 0.4rem; }}

/* ── AWARD ── */
.aw-card {{
    background: {AMBER_BG}; border: 1px solid {AMBER_BD}; border-radius: 12px;
    padding: 1.1rem 1.3rem; margin-bottom: 0.7rem;
    transition: transform 0.25s ease;
}}
.aw-card:hover {{ transform: translateY(-2px); }}
.aw-title {{ font-size: 0.93rem; font-weight: 600; color: {AMBER_TXT}; }}
.aw-desc {{ color: {TXT3}; font-size: 0.83rem; margin-top: 0.15rem; }}

/* ── PUBLICATION ── */
.pub-card {{
    background: {CARD}; border: 1px solid {BORDER};
    border-left: 3px solid {PUB_LEFT}; border-radius: 12px;
    padding: 1.2rem 1.3rem; margin-bottom: 0.7rem;
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}}
.pub-card:hover {{ box-shadow: 0 4px 14px rgba(16,185,129,0.08); transform: translateY(-2px); }}
.pub-title {{ font-weight: 600; color: {TXT}; font-size: 0.93rem; }}
.pub-title a {{ color: {TXT}; text-decoration: none; border-bottom: 1px dashed {ACCENT3}; }}
.pub-title a:hover {{ color: {ACCENT3}; }}
.pub-venue {{ font-size: 0.8rem; color: {ACCENT3}; margin-top: 0.12rem; }}
.pub-link {{ font-family: 'DM Mono', monospace; font-size: 0.73rem; margin-top: 0.2rem; }}
.pub-link a {{ color: {ACCENT}; text-decoration: none; }}
.pub-link a:hover {{ text-decoration: underline; }}
.pub-desc {{ color: {TXT4}; font-size: 0.83rem; margin-top: 0.3rem; line-height: 1.5; }}

/* ── CONTACT ── */
.c-item {{
    display: flex; align-items: center; gap: 0.65rem; padding: 0.65rem 1rem;
    background: {BG2}; border: 1px solid {BORDER}; border-radius: 10px;
    margin-bottom: 0.35rem; font-size: 0.88rem; color: {TXT3};
    transition: border-color 0.2s;
}}
.c-item:hover {{ border-color: {ACCENT}; }}
.c-item a {{ color: {ACCENT}; text-decoration: none; }}

/* ── VIDEO CARD ── */
.vid-card {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 1.2rem; margin-bottom: 1rem;
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}}
.vid-card:hover {{ box-shadow: 0 6px 20px rgba(59,130,246,0.07); transform: translateY(-2px); }}
.vid-title {{ font-size: 1rem; font-weight: 600; color: {TXT}; margin-bottom: 0.6rem; }}
.vid-link {{ font-family: 'DM Mono', monospace; font-size: 0.75rem; margin-top: 0.5rem; }}
.vid-link a {{ color: {ACCENT}; text-decoration: none; }}
.vid-link a:hover {{ text-decoration: underline; }}

/* ── PROJECT SECTION ── */
.proj-section {{
    background: {BG2}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 1.5rem; margin-bottom: 1.2rem;
}}
.proj-section-title {{ font-size: 1.1rem; font-weight: 700; color: {TXT}; margin-bottom: 0.8rem; }}

/* ── MISC ── */
.stImage > img {{ border-radius: 10px; }}
.stButton > button {{
    border-radius: 8px !important; font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important; font-size: 1.05rem !important;
    min-width: 42px !important; padding: 0.3rem 0.75rem !important;
    background: {BG2} !important; color: {TXT3} !important;
    border: 1px solid {BORDER} !important;
    transition: all 0.2s ease !important;
}}
.stButton > button:hover {{ border-color: {ACCENT} !important; color: {ACCENT} !important; }}
hr {{ border-color: {BORDER} !important; }}
</style>
""", unsafe_allow_html=True)


# ─── Helper: YouTube embed ───
def youtube_embed(url: str, height: int = 340):
    video_id = ""
    if "watch?v=" in url:
        video_id = url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
    if video_id:
        st.markdown(
            f'<iframe width="100%" height="{height}" src="https://www.youtube.com/embed/{video_id}" '
            f'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
            f'gyroscope; picture-in-picture" allowfullscreen style="border-radius:10px;"></iframe>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════
tabs = st.tabs(["Home", "Certificates", "Experience", "Education", "Products", "Academics", "Projects & Videos", "Contact"])

# ══════════════════ HOME ══════════════════
with tabs[0]:
    col_photo, col_info = st.columns([1, 3.5], gap="large")
    with col_photo:
        profile = get_images("profile")
        if profile:
            st.image(profile[0], width=150)
        else:
            st.markdown(
                f'<div class="animate-scale" style="width:130px;height:130px;border-radius:50%;'
                f'background:{ACCENT};display:flex;align-items:center;justify-content:center;'
                f'font-size:2.5rem;color:#fff;font-weight:700;">SH</div>',
                unsafe_allow_html=True,
            )
    with col_info:
        st.markdown(f"""
        <div class="hero-wrap animate-up">
            <div class="hero-name">Shashank Hegde</div>
            <div class="hero-title">Embedded-ML Electronics Engineer · Lead Product R&D</div>
            <div class="hero-bio">
                Lead R&D Engineer and TUM graduate with 5+ years across Robert Bosch and
                high-growth startups. Owns embedded and ML-based healthcare systems end-to-end —
                from firmware and edge ML to cloud inference pipelines — with production software
                active in 30,000+ clinical consultations worldwide.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-row animate-up delay-2">
        <div class="stat-card"><div class="stat-num">5+</div><div class="stat-lbl">Years Experience</div></div>
        <div class="stat-card"><div class="stat-num">30K+</div><div class="stat-lbl">Clinical Consults</div></div>
        <div class="stat-card"><div class="stat-num">3</div><div class="stat-lbl">Publications</div></div>
        <div class="stat-card"><div class="stat-num">5</div><div class="stat-lbl">Awards</div></div>
        <div class="stat-card"><div class="stat-num">2</div><div class="stat-lbl">Degrees</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title animate-fade delay-3">Highlights</div>', unsafe_allow_html=True)
    slideshow("achievements", key="home_ach")

    st.markdown(f"""
    <div class="aw-card animate-left delay-1"><div class="aw-title">Best Presentation Award — IEEE ICCE 2024, Las Vegas</div><div class="aw-desc">IoT-enabled automatic gear shifting for E-bikes. Best among 50+ papers.</div></div>
    <div class="aw-card animate-left delay-2"><div class="aw-title">Bosch Future Mobility Challenge — Semi-Finalist, Cluj Romania</div><div class="aw-desc">Represented Germany among 100+ teams. Led sensor fusion on NVIDIA Jetson Xavier.</div></div>
    <div class="aw-card animate-left delay-3"><div class="aw-title">Bravo Award — Robert Bosch</div><div class="aw-desc">Recognized for SecOC tool delivery in ECU security.</div></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title animate-fade delay-4">Core skills</div>', unsafe_allow_html=True)
    skills_data = {
        "Embedded & IoT": ["Edge ML","Arduino","Raspberry Pi","STM32","Firmware","IoT Security","CAN","V2V"],
        "AI / ML": ["ASR","NLP","RAG","Model Compression","TensorRT","GPU Accel.","Computer Vision"],
        "Programming": ["Python","C","C++","CAPL","ROS"],
        "Platforms": ["Linux/RHEL","CUDA","NVIDIA Jetson","Docker","Git"],
    }
    c1, c2 = st.columns(2)
    for i, (cat, sk) in enumerate(skills_data.items()):
        with c1 if i % 2 == 0 else c2:
            st.markdown(f'<p style="font-weight:600;color:{TXT};margin-bottom:0.3rem;">{cat}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="t-skills animate-fade delay-{i+1}">' + "".join(f'<span class="sk">{s}</span>' for s in sk) + '</div>', unsafe_allow_html=True)
            st.markdown("")


# ══════════════════ CERTIFICATES ══════════════════
with tabs[1]:
    st.markdown('<div class="sec-title animate-up">Certificates & Awards</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Filtered by category. Scanned copies below.</div>', unsafe_allow_html=True)

    certs = [
        ("Best Session Presentation — IEEE ICCE 2024","Las Vegas · Jan 2024","Award",AMBER_TXT),
        ("Certificate of Participation — IEEE ICCE 2024","Retrofittable Automatic Shifter","Conference",ACCENT),
        ("Best Paper — ICICEE 2020","Remote Monitoring with Voice Control · Tumkur","Award",AMBER_TXT),
        ("Bravo Award — Robert Bosch","SecOC tool delivery · Aug 2021","Corporate",ACCENT2),
        ("Bosch Future Mobility Challenge","Team TUMAVERICK — Semi-finalist · Cluj 2023","Competition","#e11d48" if not DARK else "#fb7185"),
        ("Tejas Networks Internship","Product verification & test automation · 2020","Internship",ACCENT3),
        ("NCCDS 2020","Signal Comparison for Forest Logging Prevention","Conference",ACCENT),
        ("NIE IEEE Biblus — ANKURA'19","National Level Paper Presentation","Conference",ACCENT),
        ("NIE Summer of Code 5.0","Hardware Track · June 2018","Workshop","#0891b2" if not DARK else "#22d3ee"),
        ("Adroit'18 Appreciation","IEEE NIE Student Branch volunteering · Oct 2018","Volunteering","#7c3aed" if not DARK else "#a78bfa"),
        ("Texas Instruments Innovation Challenge 2019","DST & TI India Design Contest","Competition","#e11d48" if not DARK else "#fb7185"),
    ]
    all_cats = sorted(set(c[2] for c in certs))
    sel = st.multiselect("Filter", all_cats, default=all_cats, key="cf")
    for idx, (title, desc, cat, color) in enumerate(certs):
        if cat in sel:
            st.markdown(
                f'<div class="t-card animate-left delay-{min(idx%3+1,3)}" style="border-left-color:{color};">'
                f'<div class="t-header"><div><div class="t-role">{title}</div>'
                f'<div class="t-desc">{desc}</div></div>'
                f'<span class="t-date">{cat}</span></div></div>',
                unsafe_allow_html=True,
            )
    st.markdown("---")
    st.markdown('<div class="sec-title">Certificate scans</div>', unsafe_allow_html=True)
    slideshow("certificates", key="cert_s")


# ══════════════════ EXPERIENCE ══════════════════
with tabs[2]:
    st.markdown('<div class="sec-title animate-up">Work Experience</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">From embedded systems at Bosch to leading R&D at a healthtech startup.</div>', unsafe_allow_html=True)

    exps = [
        ("Lead R&D Product Engineer","O-Health · Bangalore & Boston","Jan 2025 – Present",
         ["Improved ASR accuracy — reduced WER by 40 % for Standard Hindi on edge models",
          "Reduced inference latency by 50 % via knowledge distillation, quantization, weight pruning",
          "Built medical RAG pipeline with hallucination-free outputs via cross-LLM consensus",
          "Optimized GPU inference on H200 clusters — CUDA, TensorRT, async multi-threading",
          "Led end-to-end health-band development with MIT CSAIL"],
         ["ASR","NLP","RAG","Linux","Edge ML","GPU Accel.","Health-tech"]),
        ("Werkstudent Embedded IoT Engineer","Würth Elektronik eiSoS · Munich","May 2022 – Jan 2025",
         ["Optimized AT-command interfaces and multi-threaded buffer management",
          "Designed low-level LTE-M / NB-IoT firmware drivers with robust state machines",
          "Ensured reliable high-frequency IoT data transmission under variable conditions"],
         ["LTE-M","NB-IoT","Firmware","Multithreading","ARM","Edge ML"]),
        ("Embedded Software Engineer","Robert Bosch · Bangalore","Jan 2021 – Sep 2021",
         ["Implemented ECU security algorithms per customer specifications",
          "Developed SecOC tool for secure data transmission between ECUs over CAN bus"],
         ["ECU Security","CAN","CAPL","CANoe","XCP"]),
        ("Embedded Software Developer","AmberFlux EdgeAI · Hyderabad","Nov 2020 – Jan 2021",
         ["Integrated sensors on Raspberry Pi, STM32 and Xtensa for real-time positioning",
          "Optimized embedded AI models for edge devices"],
         ["Raspberry Pi","STM32","Real-time","Embedded AI"]),
        ("Product Verification Intern","Tejas Networks · Bangalore","Jan 2020 – Jul 2020",
         ["Automated Layer-2 product verification for optical communication",
          "Developed test-automation scripts in Python and TCL"],
         ["Layer-2","Test Automation","Python","TCL"]),
    ]
    for idx, (role, company, date, bullets, skills) in enumerate(exps):
        bl = "".join(f"<li>{b}</li>" for b in bullets)
        sk = "".join(f'<span class="sk">{s}</span>' for s in skills)
        st.markdown(
            f'<div class="t-card animate-up delay-{min(idx%3+1,3)}"><div class="t-header"><div>'
            f'<div class="t-role">{role}</div><div class="t-company">{company}</div></div>'
            f'<span class="t-date">{date}</span></div>'
            f'<div class="t-desc"><ul>{bl}</ul></div>'
            f'<div class="t-skills">{sk}</div></div>',
            unsafe_allow_html=True,
        )
    st.markdown("---")
    st.markdown('<div class="sec-title">Workplace photos</div>', unsafe_allow_html=True)
    slideshow("experience", key="exp_s")


# ══════════════════ EDUCATION ══════════════════
with tabs[3]:
    st.markdown('<div class="sec-title animate-up">Education</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="edu-card animate-up delay-1">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div><div class="edu-deg">M.Sc. Communication Engineering</div>
            <div class="edu-school">Technical University of Munich (TUM) — Germany</div></div>
            <span class="t-date">Oct 2021 – Oct 2024</span>
        </div>
        <div class="edu-det">
            <strong style="color:{TXT2}">Grade:</strong> 2.1 &nbsp;·&nbsp;
            <strong style="color:{TXT2}">Thesis:</strong> Lane-Free Traffic Control on Connected Mini Automated Vehicles <em>(1.0)</em><br>
            <strong style="color:{TXT2}">Focus:</strong> Embedded Systems & Security, IoT, SoC, Data Networks<br>
            <strong style="color:{TXT2}">Extra:</strong> 6G Business Modeling Lab (TUM CDTM) — interdisciplinary prototyping
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="edu-card animate-up delay-2">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div><div class="edu-deg">B.E. Electronics & Communication</div>
            <div class="edu-school">National Institute of Engineering — Mysore, India</div></div>
            <span class="t-date">Aug 2016 – Oct 2020</span>
        </div>
        <div class="edu-det">
            <strong style="color:{TXT2}">Grade:</strong> 1.6 &nbsp;·&nbsp;
            <strong style="color:{TXT2}">Thesis:</strong> Data Analysis from Sensors via DSP and Wireless Sensor Networks <em>(1.0)</em><br>
            <strong style="color:{TXT2}">Focus:</strong> Digital Electronics, Embedded Systems, Network Security, C++
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title" style="font-size:1.2rem;">Online courses</div>', unsafe_allow_html=True)
    for c in ["IoT Wireless & Cloud Computing — Yonsei University (Coursera)",
              "Embedded Hardware & Operating Systems — EIT Digital (Coursera)",
              "Computer Networks & IP Protocol — IIT Kharagpur (NPTEL)",
              "Python for Computer Vision with OpenCV & Deep Learning (Udemy)"]:
        st.markdown(f'<div class="c-item animate-fade">{c}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sec-title">Degree certificates</div>', unsafe_allow_html=True)
    slideshow("education", key="edu_s")


# ══════════════════ PRODUCTS ══════════════════
with tabs[4]:
    st.markdown('<div class="sec-title animate-up">Products & Builds</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Hardware, software, and everything in between.</div>', unsafe_allow_html=True)

    products = [
        ("Health Band — O-Health","Production-grade wearable with custom sensors, BLE, and cloud ML. 30,000+ clinical consultations.",["Hardware","Firmware","ML","BLE","Healthcare"]),
        ("ASR Engine for Hindi","Edge-optimized ASR. 40 % WER improvement, 50 % latency reduction.",["ASR","Edge ML","Compression","NLP"]),
        ("Medical RAG Pipeline","Hallucination-free medical info extraction via cross-LLM consensus.",["RAG","LLM","Healthcare","NLP"]),
        ("E-Bike Auto Shifter","IoT-enabled rear-derailleur shifting. IEEE ICCE 2024 Best Presentation.",["IoT","Mechatronics","Sensors","IEEE"]),
        ("SecOC Tool — Bosch","Automated ECU data encryption for CAN bus.",["Automotive","Security","CAN","CAPL"]),
        ("Autonomous Mini Vehicle — TUM","Lane-free traffic control with V2V and sensor fusion.",["Autonomous","V2V","ROS","Sensor Fusion"]),
    ]
    for i in range(0, len(products), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(products):
                name, desc, tags = products[i+j]
                tk = "".join(f'<span class="sk">{t}</span>' for t in tags)
                with cols[j]:
                    st.markdown(
                        f'<div class="t-card animate-scale delay-{j+1}" style="min-height:150px;">'
                        f'<div class="t-role">{name}</div>'
                        f'<div class="t-desc" style="margin:0.35rem 0;">{desc}</div>'
                        f'<div class="t-skills">{tk}</div></div>',
                        unsafe_allow_html=True,
                    )
    st.markdown("---")
    st.markdown('<div class="sec-title">Product gallery</div>', unsafe_allow_html=True)
    slideshow("products", key="prod_s")


# ══════════════════ ACADEMICS ══════════════════
with tabs[5]:
    st.markdown('<div class="sec-title animate-up">Academic Work</div>', unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;font-size:1.1rem;color:{TXT};margin:1.5rem 0 0.6rem;">Research projects</p>', unsafe_allow_html=True)
    for title, venue, date, desc, skills in [
        ("Lane-Free Traffic Control for Connected Mini-Automated Vehicles","Master's Thesis — TU München","Feb–Oct 2024",
         "Lane-free control strategies for connected autonomous vehicles using V2V communication.",
         ["Vehicle Control","V2V","Sensor Fusion","Autonomous"]),
        ("Embedded Development for E-Bike","EMotorad India","Jun 2023 – Feb 2024",
         "Sensor fusion algorithms and mechatronics for automatic pedal-assist.",
         ["Embedded","Sensor Fusion","IoT","Mechatronics"]),
    ]:
        sk = "".join(f'<span class="sk">{s}</span>' for s in skills)
        st.markdown(
            f'<div class="t-card animate-left"><div class="t-header"><div>'
            f'<div class="t-role">{title}</div><div class="t-company">{venue}</div></div>'
            f'<span class="t-date">{date}</span></div>'
            f'<div class="t-desc">{desc}</div><div class="t-skills">{sk}</div></div>',
            unsafe_allow_html=True,
        )

    # PUBLICATIONS WITH HYPERLINKS
    st.markdown(f'<p style="font-weight:600;font-size:1.1rem;color:{TXT};margin:1.5rem 0 0.6rem;">Publications</p>', unsafe_allow_html=True)

    pubs = [
        ("Retrofittable Automatic Shifter of Rear-Derailleur with Mode-Based Transmission and IoT",
         "IEEE ICCE 2024",
         "https://ieeexplore.ieee.org/document/10444469",
         "Retrofittable automatic shifting for E-bikes with IoT and adaptive riding modes."),
        ("Remote Monitoring Robot with Voice Control and Image Analysis",
         "Scopus-indexed — IJAST",
         "http://sersc.org/journals/index.php/IJAST/article/view/21218",
         "Surveillance robot with real-time image processing, voice control, and MQTT."),
        ("Data Extraction with Signal Comparison for Forest Logging Prevention",
         "IJERT · NCCDS 2020",
         "https://www.ijert.org/data-extraction-with-signal-comparison-for-forest-logging-prevention",
         "Wireless sensor network for illegal logging detection via FFT-based signal processing."),
    ]
    for title, venue, url, desc in pubs:
        st.markdown(
            f'<div class="pub-card animate-fade">'
            f'<div class="pub-title"><a href="{url}" target="_blank">{title}</a></div>'
            f'<div class="pub-venue">{venue}</div>'
            f'<div class="pub-link"><a href="{url}" target="_blank">📄 {url}</a></div>'
            f'<div class="pub-desc">{desc}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(f'<p style="font-weight:600;font-size:1.1rem;color:{TXT};margin:1.5rem 0 0.6rem;">Conferences & presentations</p>', unsafe_allow_html=True)
    for name, loc, note in [
        ("IEEE ICCE 2024","Las Vegas, USA","Best Presentation Award"),
        ("Bosch Future Mobility Challenge 2023","Cluj, Romania","Semi-finalist"),
        ("ICICEE 2020","Tumkur, India","Best Paper Award"),
        ("NCCDS 2020","Mysuru, India","Paper Presentation"),
        ("ANKURA'19","Mysore, India","National Paper Presentation"),
        ("TI Innovation Challenge 2019","India","Design Contest"),
    ]:
        st.markdown(f'<div class="c-item animate-fade"><strong>{name}</strong>&nbsp;— {loc} &nbsp;<em>({note})</em></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sec-title">Academic gallery</div>', unsafe_allow_html=True)
    slideshow("academics", key="acad_s")


# ══════════════════ PROJECTS & VIDEOS ══════════════════
with tabs[6]:
    st.markdown('<div class="sec-title animate-up">Projects & Videos</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Demo videos, project walkthroughs, and additional builds.</div>', unsafe_allow_html=True)

    # ── Section 1: Forest Logging Prevention ──
    st.markdown(f"""
    <div class="proj-section animate-up delay-1">
        <div class="proj-section-title">🌲 Illegal Forest Logging Prevention using STM32 Wireless Nodes</div>
        <div class="t-desc">Bachelor thesis project — wireless sensor network for detecting illegal logging activity using FFT-based audio signal analysis on STM32 microcontrollers.</div>
        <div class="pub-link" style="margin-top:0.5rem;"><a href="https://www.ijert.org/data-extraction-with-signal-comparison-for-forest-logging-prevention" target="_blank">📄 Read the paper (IJERT)</a></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="vid-title" style="color:{TXT};">Project demo</div>', unsafe_allow_html=True)
        youtube_embed("https://www.youtube.com/watch?v=g9tRZPRJfYs")
    with col2:
        st.markdown(f'<div class="vid-title" style="color:{TXT};">Cooja simulator</div>', unsafe_allow_html=True)
        youtube_embed("https://www.youtube.com/watch?v=wczmB9WR8O4")

    st.markdown("---")

    # ── Section 2: Pest Detection ──
    st.markdown(f"""
    <div class="proj-section animate-up delay-2">
        <div class="proj-section-title">🐛 Pest Detection Using Machine Learning on Edge Devices</div>
        <div class="t-desc">Machine learning-based pest detection system running on edge devices for real-time agricultural monitoring.</div>
        <div class="pub-link" style="margin-top:0.5rem;"><a href="https://resources.mouser.com/explore-all/pest-detection-using-machine-learning-on-edge-devices" target="_blank">📄 View on Mouser</a></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title" style="font-size:1.1rem;">Project photos</div>', unsafe_allow_html=True)
    slideshow("projects", key="proj_s")

    st.markdown("---")

    # ── Section 3: TUM Robotics Club ──
    st.markdown(f"""
    <div class="proj-section animate-up delay-3">
        <div class="proj-section-title">🤖 TUM Robotics Club</div>
        <div class="t-desc">Activities and projects from the TUM Robotics Club — hands-on experience with robotic systems, competitions, and collaborative engineering.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;color:{TXT};margin:0.5rem 0;">Photos</p>', unsafe_allow_html=True)
    slideshow("robotics_club", key="robo_photos")

    # Robotics club video links (provision for future)
    robo_videos = get_images("robotics_club")  # placeholder check
    st.markdown(f"""
    <div style="background:{BG2};border:1px dashed {BORDER};border-radius:10px;padding:1rem;margin-top:0.8rem;">
        <p style="color:{TXT4};font-size:0.85rem;margin:0;">
            📹 <strong>Videos:</strong> Add YouTube links to the <code>robotics_club_videos</code> list in <code>app.py</code> to embed them here.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Provision: add robotics club video URLs here
    robotics_club_videos = [
        # ("Video Title", "https://www.youtube.com/watch?v=XXXXX"),
    ]
    if robotics_club_videos:
        for title, url in robotics_club_videos:
            st.markdown(f'<div class="vid-title" style="color:{TXT};">{title}</div>', unsafe_allow_html=True)
            youtube_embed(url)


# ══════════════════ CONTACT ══════════════════
with tabs[7]:
    st.markdown('<div class="sec-title animate-up">Get in touch</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="c-item animate-left delay-1">📞 &nbsp; +49 176 71095238</div>
        <div class="c-item animate-left delay-2">📧 &nbsp; <a href="mailto:shashankv099@gmail.com">shashankv099@gmail.com</a></div>
        <div class="c-item animate-left delay-3">💼 &nbsp; <a href="https://www.linkedin.com/in/shashank-hegde98" target="_blank">linkedin.com/in/shashank-hegde98</a></div>
        <div class="c-item animate-left delay-4">🌍 &nbsp; Bangalore, India & Munich, Germany</div>
        <div class="c-item animate-left delay-5">🇺🇸 &nbsp; Nationality: United States of America</div>
        """, unsafe_allow_html=True)
        st.markdown("")
        st.markdown(f'<p style="font-weight:600;color:{TXT};">Languages</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="c-item animate-fade">English — C2 &nbsp;·&nbsp; German — A2 (learning B1)</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="hero-wrap animate-scale" style="padding:1.5rem;">
            <div style="font-size:1.05rem;font-weight:600;color:{TXT};margin-bottom:0.4rem;">Open to opportunities</div>
            <div class="hero-bio" style="font-size:0.9rem;">
                Interested in Embedded ML, Edge AI, Healthcare Technology, and IoT systems.
                Reach out via email or LinkedIn — happy to connect.
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    f'<p style="text-align:center;color:{TXT4};font-size:0.82rem;">'
    f'Shashank Hegde · Embedded-ML Electronics Engineer · © 2025</p>',
    unsafe_allow_html=True,
)
