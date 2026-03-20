import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Shashank Hegde | Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════
# IMAGE SYSTEM — Local folders only, no public uploads
# ════════════════════════════════════════════════
ASSETS_DIR = Path("assets")
for cat in ["profile","achievements","certificates","experience","education","products","academics"]:
    (ASSETS_DIR / cat).mkdir(parents=True, exist_ok=True)

def get_images(category: str) -> list[str]:
    cat_dir = ASSETS_DIR / category
    if not cat_dir.exists():
        return []
    return [str(p) for p in sorted(cat_dir.iterdir()) if p.suffix.lower() in {".jpg",".jpeg",".png",".webp"}]


# ─── Single-image slideshow with arrows ───
def slideshow(category: str, key: str, height: int = 420):
    """Render one image at a time with ◀ ▶ navigation arrows."""
    images = get_images(category)
    if not images:
        st.info(f"No images yet — add files to `assets/{category}/` and redeploy.")
        return

    idx_key = f"slide_{key}"
    if idx_key not in st.session_state:
        st.session_state[idx_key] = 0

    total = len(images)
    idx = st.session_state[idx_key] % total

    col_left, col_img, col_right = st.columns([0.6, 10, 0.6])

    with col_left:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        if st.button("◀", key=f"{key}_prev", help="Previous"):
            st.session_state[idx_key] = (idx - 1) % total
            st.rerun()

    with col_img:
        caption = Path(images[idx]).stem.replace("_", " ").replace("-", " ")
        st.image(images[idx], use_container_width=True)
        st.markdown(
            f'<p style="text-align:center;color:#64748b;font-size:0.85rem;margin-top:0.3rem;">'
            f'{caption} &nbsp;·&nbsp; {idx + 1} / {total}</p>',
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        if st.button("▶", key=f"{key}_next", help="Next"):
            st.session_state[idx_key] = (idx + 1) % total
            st.rerun()


# ─── CSS — Light, professional, clean ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ─ Global ─ */
:root {
    --blue: #2563eb;
    --blue-light: #eff6ff;
    --blue-50: #dbeafe;
    --indigo: #4f46e5;
    --slate-50: #f8fafc;
    --slate-100: #f1f5f9;
    --slate-200: #e2e8f0;
    --slate-300: #cbd5e1;
    --slate-400: #94a3b8;
    --slate-500: #64748b;
    --slate-600: #475569;
    --slate-700: #334155;
    --slate-800: #1e293b;
    --slate-900: #0f172a;
    --emerald: #059669;
    --amber: #d97706;
    --rose: #e11d48;
}

.stApp {
    font-family: 'Source Sans 3', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: #ffffff;
}

.block-container {
    padding-top: 1.5rem !important;
    max-width: 1100px !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Source Sans 3', sans-serif !important;
    color: var(--slate-900) !important;
}

p, li, span, div { font-family: 'Source Sans 3', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─ Tabs ─ */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--slate-100);
    border-radius: 10px;
    padding: 4px;
    border: 1px solid var(--slate-200);
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 500;
    font-size: 0.88rem;
    padding: 0.55rem 1.1rem;
    border-radius: 8px;
    color: var(--slate-500);
    background: transparent;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: var(--blue) !important;
    font-weight: 600;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* ─ Hero ─ */
.hero-wrap {
    padding: 2.5rem 2rem;
    background: var(--slate-50);
    border: 1px solid var(--slate-200);
    border-radius: 16px;
    margin-bottom: 2rem;
}

.hero-name {
    font-size: 2.6rem;
    font-weight: 700;
    color: var(--slate-900);
    margin: 0 0 0.15rem 0;
    line-height: 1.15;
    letter-spacing: -0.5px;
}

.hero-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.88rem;
    color: var(--blue);
    margin-bottom: 0.8rem;
}

.hero-bio {
    font-size: 1rem;
    color: var(--slate-600);
    line-height: 1.7;
    max-width: 660px;
}

/* ─ Stats ─ */
.stat-row { display: flex; gap: 0.75rem; margin: 1.5rem 0; flex-wrap: wrap; }

.stat-card {
    flex: 1; min-width: 120px;
    background: #fff;
    border: 1px solid var(--slate-200);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: var(--blue); }

.stat-num {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--blue);
    line-height: 1.2;
}

.stat-lbl {
    font-size: 0.72rem;
    color: var(--slate-400);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 0.15rem;
}

/* ─ Section Headings ─ */
.sec-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--slate-900);
    margin: 2rem 0 0.4rem 0;
    letter-spacing: -0.3px;
}

.sec-sub {
    color: var(--slate-400);
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

/* ─ Timeline Card ─ */
.t-card {
    background: #fff;
    border: 1px solid var(--slate-200);
    border-radius: 14px;
    padding: 1.5rem 1.5rem 1.5rem 1.8rem;
    margin-bottom: 1rem;
    border-left: 3px solid var(--blue);
    transition: box-shadow 0.2s;
}
.t-card:hover { box-shadow: 0 4px 16px rgba(37,99,235,0.07); }

.t-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; }

.t-role {
    font-size: 1.08rem;
    font-weight: 600;
    color: var(--slate-800);
}

.t-company {
    font-size: 0.9rem;
    color: var(--blue);
    font-weight: 500;
}

.t-date {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--slate-400);
    background: var(--slate-50);
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    border: 1px solid var(--slate-200);
    white-space: nowrap;
}

.t-desc {
    color: var(--slate-600);
    font-size: 0.9rem;
    line-height: 1.65;
}

.t-desc ul { margin: 0.3rem 0; padding-left: 1.1rem; }
.t-desc li { margin-bottom: 0.2rem; }

.t-skills { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.7rem; }

.sk {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--blue);
    background: var(--blue-light);
    border: 1px solid var(--blue-50);
    padding: 0.2rem 0.55rem;
    border-radius: 5px;
}

/* ─ Education Card ─ */
.edu-card {
    background: #fff;
    border: 1px solid var(--slate-200);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.edu-card:hover { box-shadow: 0 4px 16px rgba(79,70,229,0.06); }

.edu-deg {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--indigo);
}

.edu-school {
    font-size: 0.95rem;
    color: var(--slate-700);
    font-weight: 500;
}

.edu-det {
    color: var(--slate-600);
    font-size: 0.88rem;
    line-height: 1.65;
    margin-top: 0.5rem;
}

/* ─ Award Card ─ */
.aw-card {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.75rem;
}
.aw-card:hover { border-color: var(--amber); }

.aw-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #92400e;
}

.aw-desc {
    color: #78716c;
    font-size: 0.85rem;
    margin-top: 0.2rem;
}

/* ─ Publication Card ─ */
.pub-card {
    background: #fff;
    border: 1px solid var(--slate-200);
    border-left: 3px solid var(--emerald);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.75rem;
}

.pub-title { font-weight: 600; color: var(--slate-800); font-size: 0.95rem; }
.pub-venue { font-size: 0.82rem; color: var(--emerald); margin-top: 0.15rem; }
.pub-desc { color: var(--slate-500); font-size: 0.85rem; margin-top: 0.35rem; line-height: 1.55; }

/* ─ Contact row ─ */
.c-item {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.7rem 1rem;
    background: var(--slate-50);
    border: 1px solid var(--slate-200);
    border-radius: 10px;
    margin-bottom: 0.4rem;
    font-size: 0.9rem;
    color: var(--slate-600);
}
.c-item:hover { border-color: var(--blue); }
.c-item a { color: var(--blue); text-decoration: none; }

/* ─ Profile photo ─ */
.stImage > img { border-radius: 10px; }

/* ─ Buttons ─ */
.stButton > button {
    border-radius: 8px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    min-width: 44px !important;
    padding: 0.3rem 0.8rem !important;
}

/* ─ Divider ─ */
hr { border-color: var(--slate-200) !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════
tabs = st.tabs(["Home", "Certificates", "Experience", "Education", "Products", "Academics", "Contact"])

# ══ HOME ══
with tabs[0]:
    col_photo, col_info = st.columns([1, 3.5], gap="large")
    with col_photo:
        profile = get_images("profile")
        if profile:
            st.image(profile[0], width=150)
        else:
            st.markdown(
                '<div style="width:130px;height:130px;border-radius:50%;background:#2563eb;'
                'display:flex;align-items:center;justify-content:center;font-size:2.5rem;'
                'color:#fff;font-weight:700;">SH</div>',
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown("""
        <div class="hero-wrap">
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

    st.markdown("""
    <div class="stat-row">
        <div class="stat-card"><div class="stat-num">5+</div><div class="stat-lbl">Years Experience</div></div>
        <div class="stat-card"><div class="stat-num">30K+</div><div class="stat-lbl">Clinical Consults</div></div>
        <div class="stat-card"><div class="stat-num">3</div><div class="stat-lbl">Publications</div></div>
        <div class="stat-card"><div class="stat-num">5</div><div class="stat-lbl">Awards</div></div>
        <div class="stat-card"><div class="stat-num">2</div><div class="stat-lbl">Degrees</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Achievement slideshow
    st.markdown('<div class="sec-title">Highlights</div>', unsafe_allow_html=True)
    slideshow("achievements", key="home_ach")

    st.markdown("""
    <div class="aw-card"><div class="aw-title">Best Presentation Award — IEEE ICCE 2024, Las Vegas</div><div class="aw-desc">IoT-enabled automatic gear shifting for E-bikes. Best presentation among 50+ papers.</div></div>
    <div class="aw-card"><div class="aw-title">Bosch Future Mobility Challenge — Semi-Finalist, Cluj Romania</div><div class="aw-desc">Represented Germany among 100+ international teams. Led sensor fusion on NVIDIA Jetson Xavier.</div></div>
    <div class="aw-card"><div class="aw-title">Bravo Award — Robert Bosch</div><div class="aw-desc">Recognized for successful delivery of a SecOC tool in ECU security.</div></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Core skills</div>', unsafe_allow_html=True)
    skills_data = {
        "Embedded & IoT": ["Edge ML","Arduino","Raspberry Pi","STM32","Firmware","IoT Security","CAN","V2V"],
        "AI / ML": ["ASR","NLP","RAG","Model Compression","TensorRT","GPU Accel.","Computer Vision"],
        "Programming": ["Python","C","C++","CAPL","ROS"],
        "Platforms": ["Linux/RHEL","CUDA","NVIDIA Jetson","Docker","Git"],
    }
    c1, c2 = st.columns(2)
    for i, (cat, sk) in enumerate(skills_data.items()):
        with c1 if i % 2 == 0 else c2:
            st.markdown(f"**{cat}**")
            st.markdown('<div class="t-skills">' + "".join(f'<span class="sk">{s}</span>' for s in sk) + '</div>', unsafe_allow_html=True)
            st.markdown("")


# ══ CERTIFICATES ══
with tabs[1]:
    st.markdown('<div class="sec-title">Certificates & Awards</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Filtered by category. Scanned copies below.</div>', unsafe_allow_html=True)

    certs = [
        ("Best Session Presentation — IEEE ICCE 2024","Las Vegas, USA · Jan 2024","Award","#d97706"),
        ("Certificate of Participation — IEEE ICCE 2024","Retrofittable Automatic Shifter of Rear-Derailleur","Conference","#2563eb"),
        ("Best Paper — ICICEE 2020","Remote Monitoring with Voice Control · Tumkur","Award","#d97706"),
        ("Bravo Award — Robert Bosch","SecOC tool delivery in ECU security · Aug 2021","Corporate","#4f46e5"),
        ("Bosch Future Mobility Challenge","Team TUMAVERICK — Semi-finalist · Cluj 2023","Competition","#e11d48"),
        ("Tejas Networks Internship","Product verification & test automation · Jan–May 2020","Internship","#059669"),
        ("NCCDS 2020","Signal Comparison for Forest Logging Prevention","Conference","#2563eb"),
        ("NIE IEEE Biblus — ANKURA'19","National Level Paper Presentation","Conference","#2563eb"),
        ("NIE Summer of Code 5.0","Hardware Track · June 2018","Workshop","#0891b2"),
        ("Adroit'18 Appreciation","IEEE NIE Student Branch volunteering · Oct 2018","Volunteering","#7c3aed"),
        ("Texas Instruments Innovation Challenge 2019","DST & TI India Design Contest","Competition","#e11d48"),
    ]

    all_cats = sorted(set(c[2] for c in certs))
    sel = st.multiselect("Filter", all_cats, default=all_cats, key="cf")
    for title, desc, cat, color in certs:
        if cat in sel:
            st.markdown(
                f'<div class="t-card" style="border-left-color:{color};">'
                f'<div class="t-header"><div><div class="t-role">{title}</div>'
                f'<div class="t-desc">{desc}</div></div>'
                f'<span class="t-date">{cat}</span></div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown('<div class="sec-title">Certificate scans</div>', unsafe_allow_html=True)
    slideshow("certificates", key="cert_slide")


# ══ EXPERIENCE ══
with tabs[2]:
    st.markdown('<div class="sec-title">Work Experience</div>', unsafe_allow_html=True)
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
          "Ensured reliable high-frequency IoT data transmission under variable signal conditions"],
         ["LTE-M","NB-IoT","Firmware","Multithreading","ARM","Edge ML"]),
        ("Embedded Software Engineer","Robert Bosch · Bangalore","Jan 2021 – Sep 2021",
         ["Implemented ECU security algorithms per customer specifications",
          "Developed SecOC tool for secure data transmission between ECUs over CAN bus"],
         ["ECU Security","CAN","CAPL","CANoe","XCP"]),
        ("Embedded Software Developer","AmberFlux EdgeAI · Hyderabad","Nov 2020 – Jan 2021",
         ["Integrated sensors on Raspberry Pi, STM32 and Xtensa for real-time positioning",
          "Optimized embedded AI models for edge devices"],
         ["Raspberry Pi","STM32","Real-time Processing","Embedded AI"]),
        ("Product Verification Intern","Tejas Networks · Bangalore","Jan 2020 – Jul 2020",
         ["Automated Layer-2 product verification for optical communication systems",
          "Developed test-automation scripts in Python and TCL"],
         ["Layer-2","Test Automation","Python","TCL"]),
    ]

    for role, company, date, bullets, skills in exps:
        bl = "".join(f"<li>{b}</li>" for b in bullets)
        sk = "".join(f'<span class="sk">{s}</span>' for s in skills)
        st.markdown(
            f'<div class="t-card"><div class="t-header"><div>'
            f'<div class="t-role">{role}</div><div class="t-company">{company}</div></div>'
            f'<span class="t-date">{date}</span></div>'
            f'<div class="t-desc"><ul>{bl}</ul></div>'
            f'<div class="t-skills">{sk}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown('<div class="sec-title">Workplace photos</div>', unsafe_allow_html=True)
    slideshow("experience", key="exp_slide")


# ══ EDUCATION ══
with tabs[3]:
    st.markdown('<div class="sec-title">Education</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="edu-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div><div class="edu-deg">M.Sc. Communication Engineering</div>
            <div class="edu-school">Technical University of Munich (TUM) — Germany</div></div>
            <span class="t-date">Oct 2021 – Oct 2024</span>
        </div>
        <div class="edu-det">
            <strong>Grade:</strong> 2.1 &nbsp;·&nbsp;
            <strong>Thesis:</strong> Lane-Free Traffic Control on Connected Mini Automated Vehicles <em>(1.0)</em><br>
            <strong>Focus:</strong> Embedded Systems & Security, IoT, SoC, Data Networks<br>
            <strong>Extra:</strong> 6G Business Modeling Lab (TUM CDTM) — interdisciplinary prototyping
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="edu-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div><div class="edu-deg">B.E. Electronics & Communication</div>
            <div class="edu-school">National Institute of Engineering — Mysore, India</div></div>
            <span class="t-date">Aug 2016 – Oct 2020</span>
        </div>
        <div class="edu-det">
            <strong>Grade:</strong> 1.6 &nbsp;·&nbsp;
            <strong>Thesis:</strong> Data Analysis from Sensors via DSP and Wireless Sensor Networks <em>(1.0)</em><br>
            <strong>Focus:</strong> Digital Electronics, Embedded Systems, Network Security, C++
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title" style="font-size:1.2rem;">Online courses</div>', unsafe_allow_html=True)
    for c in [
        "IoT Wireless & Cloud Computing — Yonsei University (Coursera)",
        "Embedded Hardware & Operating Systems — EIT Digital (Coursera)",
        "Computer Networks & IP Protocol — IIT Kharagpur (NPTEL)",
        "Python for Computer Vision with OpenCV & Deep Learning (Udemy)",
    ]:
        st.markdown(f'<div class="c-item">{c}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sec-title">Degree certificates</div>', unsafe_allow_html=True)
    slideshow("education", key="edu_slide")


# ══ PRODUCTS ══
with tabs[4]:
    st.markdown('<div class="sec-title">Products & Builds</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Hardware, software, and everything in between.</div>', unsafe_allow_html=True)

    products = [
        ("Health Band — O-Health","Production-grade wearable with custom sensors, BLE, and cloud ML. 30 000+ clinical consultations.",["Hardware","Firmware","ML","BLE","Healthcare"]),
        ("ASR Engine for Hindi","Edge-optimized ASR. 40 % WER improvement, 50 % latency reduction via distillation & quantization.",["ASR","Edge ML","Compression","NLP"]),
        ("Medical RAG Pipeline","Hallucination-free medical info extraction via cross-LLM consensus and verified ontologies.",["RAG","LLM","Healthcare","NLP"]),
        ("E-Bike Auto Shifter","IoT-enabled rear-derailleur shifting. IEEE ICCE 2024 Best Presentation.",["IoT","Mechatronics","Sensors","IEEE"]),
        ("SecOC Tool — Bosch","Automated ECU data encryption for CAN bus communication.",["Automotive","Security","CAN","CAPL"]),
        ("Autonomous Mini Vehicle — TUM","Lane-free traffic control with V2V communication and sensor fusion.",["Autonomous","V2V","ROS","Sensor Fusion"]),
    ]

    for i in range(0, len(products), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(products):
                name, desc, tags = products[i + j]
                tk = "".join(f'<span class="sk">{t}</span>' for t in tags)
                with cols[j]:
                    st.markdown(
                        f'<div class="t-card" style="min-height:160px;">'
                        f'<div class="t-role">{name}</div>'
                        f'<div class="t-desc" style="margin:0.4rem 0;">{desc}</div>'
                        f'<div class="t-skills">{tk}</div></div>',
                        unsafe_allow_html=True,
                    )

    st.markdown("---")
    st.markdown('<div class="sec-title">Product gallery</div>', unsafe_allow_html=True)
    slideshow("products", key="prod_slide")


# ══ ACADEMICS ══
with tabs[5]:
    st.markdown('<div class="sec-title">Academic Work</div>', unsafe_allow_html=True)

    st.markdown("#### Research projects")
    for title, venue, date, desc, skills in [
        ("Lane-Free Traffic Control for Connected Mini-Automated Vehicles","Master's Thesis — TU München","Feb–Oct 2024",
         "Lane-free control strategies for connected autonomous vehicles using V2V communication.",
         ["Vehicle Control","V2V","Sensor Fusion","Autonomous"]),
        ("Embedded Development for E-Bike","EMotorad India","Jun 2023 – Feb 2024",
         "Sensor fusion algorithms and mechatronics for automatic pedal-assist with wireless integration.",
         ["Embedded","Sensor Fusion","IoT","Mechatronics"]),
    ]:
        sk = "".join(f'<span class="sk">{s}</span>' for s in skills)
        st.markdown(
            f'<div class="t-card"><div class="t-header"><div>'
            f'<div class="t-role">{title}</div><div class="t-company">{venue}</div></div>'
            f'<span class="t-date">{date}</span></div>'
            f'<div class="t-desc">{desc}</div><div class="t-skills">{sk}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### Publications")
    for title, venue, desc in [
        ("Retrofittable Automatic Shifter of Rear-Derailleur with Mode-Based Transmission and IoT",
         "IEEE ICCE 2024",
         "Retrofittable automatic shifting for E-bikes with IoT and adaptive riding modes."),
        ("Remote Monitoring Robot with Voice Control and Image Analysis",
         "Scopus-indexed — IJAST",
         "Surveillance robot with real-time image processing, voice control, and MQTT communication."),
        ("Data Extraction with Signal Comparison for Forest Logging Prevention",
         "IJERT · NCCDS 2020",
         "Wireless sensor network for illegal logging detection using FFT-based signal processing."),
    ]:
        st.markdown(
            f'<div class="pub-card"><div class="pub-title">{title}</div>'
            f'<div class="pub-venue">{venue}</div>'
            f'<div class="pub-desc">{desc}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### Conferences & presentations")
    for name, loc, note in [
        ("IEEE ICCE 2024","Las Vegas, USA","Best Presentation Award"),
        ("Bosch Future Mobility Challenge 2023","Cluj, Romania","Semi-finalist"),
        ("ICICEE 2020","Tumkur, India","Best Paper Award"),
        ("NCCDS 2020","Mysuru, India","Paper Presentation"),
        ("ANKURA'19","Mysore, India","National Paper Presentation"),
        ("TI Innovation Challenge 2019","India","Design Contest"),
    ]:
        st.markdown(f'<div class="c-item"><strong>{name}</strong>&nbsp;— {loc} &nbsp;<em>({note})</em></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sec-title">Academic gallery</div>', unsafe_allow_html=True)
    slideshow("academics", key="acad_slide")


# ══ CONTACT ══
with tabs[6]:
    st.markdown('<div class="sec-title">Get in touch</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="c-item">📞 &nbsp; +49 176 71095238</div>
        <div class="c-item">📧 &nbsp; <a href="mailto:shashankv099@gmail.com">shashankv099@gmail.com</a></div>
        <div class="c-item">💼 &nbsp; <a href="https://www.linkedin.com/in/shashank-hegde98" target="_blank">linkedin.com/in/shashank-hegde98</a></div>
        <div class="c-item">🌍 &nbsp; Bangalore, India & Munich, Germany</div>
        <div class="c-item">🇺🇸 &nbsp; Nationality: United States of America</div>
        """, unsafe_allow_html=True)
        st.markdown("")
        st.markdown("**Languages**")
        st.markdown("""
        <div class="c-item">English — C2 &nbsp;·&nbsp; German — A2 (learning B1)</div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="hero-wrap" style="padding:1.5rem;">
            <div style="font-size:1.05rem;font-weight:600;color:#1e293b;margin-bottom:0.4rem;">Open to opportunities</div>
            <div class="hero-bio" style="font-size:0.9rem;">
                Interested in Embedded ML, Edge AI, Healthcare Technology, and IoT systems.
                Reach out via email or LinkedIn — happy to connect.
            </div>
        </div>
        """, unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#94a3b8;font-size:0.82rem;">'
    'Shashank Hegde · Embedded-ML Electronics Engineer · © 2025</p>',
    unsafe_allow_html=True,
)
