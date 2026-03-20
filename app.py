import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(
    page_title="Shashank Hegde | Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════
# DARK / LIGHT MODE
# ════════════════════════════════════════════════
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

head_cols = st.columns([10, 1])
with head_cols[1]:
    icon = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(icon, key="theme_toggle", help="Toggle dark/light mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

DARK = st.session_state.dark_mode

# ════════════════════════════════════════════════
# IMAGES & DOCS
# ════════════════════════════════════════════════
ASSETS = Path("assets")
for d in ["profile","achievements","certificates","experience","education",
          "products","academics","projects","robotics_club","docs"]:
    (ASSETS / d).mkdir(parents=True, exist_ok=True)

def get_images(cat):
    d = ASSETS / cat
    return [str(p) for p in sorted(d.iterdir()) if p.suffix.lower() in {".jpg",".jpeg",".png",".webp"}] if d.exists() else []

def get_doc(filename):
    """Return path if doc exists in assets/docs/"""
    p = ASSETS / "docs" / filename
    return str(p) if p.exists() else None

def embed_pdf(filepath, height=600):
    """Embed a PDF inline using base64."""
    p = Path(filepath)
    if p.exists() and p.suffix.lower() == ".pdf":
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" '
            f'width="100%" height="{height}px" style="border:1px solid {BORDER};border-radius:10px;"></iframe>',
            unsafe_allow_html=True,
        )
    else:
        st.info(f"📄 Place `{p.name}` in `assets/docs/` and redeploy to view it here.")

def embed_ppt_or_pdf(filename, label="Document", height=600):
    """Show PDF inline or show placeholder for PPT."""
    p = ASSETS / "docs" / filename
    if p.exists():
        if p.suffix.lower() == ".pdf":
            embed_pdf(str(p), height)
        else:
            # For pptx, offer download
            with open(p, "rb") as f:
                data = f.read()
            st.download_button(f"⬇ Download {label}", data, file_name=filename, mime="application/octet-stream")
    else:
        st.info(f"📄 Place `{filename}` in `assets/docs/` and redeploy to view it here.")


# ════════════════════════════════════════════════
# SLIDESHOW — Centered arrows, smooth transitions
# ════════════════════════════════════════════════
def slideshow(category, key):
    images = get_images(category)
    if not images:
        st.info(f"No images yet — add files to `assets/{category}/` and redeploy.")
        return
    idx_key = f"slide_{key}"
    if idx_key not in st.session_state:
        st.session_state[idx_key] = 0
    total = len(images)
    idx = st.session_state[idx_key] % total
    cap = Path(images[idx]).stem.replace("_"," ").replace("-"," ")

    # Render using HTML/CSS for centered arrows and smooth feel
    with open(images[idx], "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    ext = Path(images[idx]).suffix.lower().replace(".","")
    mime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"

    st.markdown(f"""
    <div style="position:relative;width:100%;max-width:750px;margin:0 auto 0.5rem auto;
        border-radius:12px;overflow:hidden;border:1px solid {BORDER};
        animation:fadeIn 0.4s ease-out;">
        <img src="data:{mime};base64,{img_b64}" style="width:100%;display:block;
            transition:opacity 0.3s ease;" />
    </div>
    <p style="text-align:center;color:{TXT4};font-size:0.82rem;margin:0 0 0.3rem 0;">
        {cap} &nbsp;·&nbsp; {idx+1} / {total}
    </p>
    """, unsafe_allow_html=True)

    # Arrow buttons centered below image
    spacer1, btn_prev, counter, btn_next, spacer2 = st.columns([3, 1, 2, 1, 3])
    with btn_prev:
        if st.button("← Prev", key=f"{key}_p", use_container_width=True):
            st.session_state[idx_key] = (idx - 1) % total
            st.rerun()
    with btn_next:
        if st.button("Next →", key=f"{key}_n", use_container_width=True):
            st.session_state[idx_key] = (idx + 1) % total
            st.rerun()


# ════════════════════════════════════════════════
# THEME VARIABLES
# ════════════════════════════════════════════════
if DARK:
    BG="#0f172a"; BG2="#1e293b"; CARD="#1e293b"; TXT="#f1f5f9"; TXT2="#cbd5e1"
    TXT3="#94a3b8"; TXT4="#64748b"; BORDER="#334155"; ACCENT="#3b82f6"
    ACCENT2="#8b5cf6"; ACCENT3="#10b981"; AMBER_BG="rgba(245,158,11,0.1)"
    AMBER_BD="rgba(245,158,11,0.3)"; AMBER_TXT="#fbbf24"
    TAG_BG="rgba(59,130,246,0.12)"; TAG_BD="rgba(59,130,246,0.25)"
    TAB_BG="#1e293b"; TAB_SEL_BG="#3b82f6"; TAB_SEL_TXT="#fff"
    HERO_BG="linear-gradient(135deg,rgba(59,130,246,0.08),rgba(139,92,246,0.08))"
    STAT_BG="#1e293b"; PUB_LEFT="#10b981"
    GLASS="rgba(30,41,59,0.85)"; GLASS_BD="rgba(148,163,184,0.15)"
else:
    BG="#ffffff"; BG2="#f8fafc"; CARD="#ffffff"; TXT="#0f172a"; TXT2="#334155"
    TXT3="#475569"; TXT4="#64748b"; BORDER="#e2e8f0"; ACCENT="#2563eb"
    ACCENT2="#4f46e5"; ACCENT3="#059669"; AMBER_BG="#fffbeb"
    AMBER_BD="#fde68a"; AMBER_TXT="#92400e"
    TAG_BG="#eff6ff"; TAG_BD="#dbeafe"
    TAB_BG="#f1f5f9"; TAB_SEL_BG="#ffffff"; TAB_SEL_TXT="#2563eb"
    HERO_BG="linear-gradient(135deg,rgba(37,99,235,0.04),rgba(79,70,229,0.04))"
    STAT_BG="#f8fafc"; PUB_LEFT="#059669"
    GLASS="rgba(255,255,255,0.85)"; GLASS_BD="rgba(0,0,0,0.06)"

# ════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&family=DM+Mono:wght@400;500&display=swap');

@keyframes fadeInUp {{ from{{opacity:0;transform:translateY(20px)}} to{{opacity:1;transform:translateY(0)}} }}
@keyframes fadeIn {{ from{{opacity:0}} to{{opacity:1}} }}
@keyframes slideLeft {{ from{{opacity:0;transform:translateX(-20px)}} to{{opacity:1;transform:translateX(0)}} }}
@keyframes scaleIn {{ from{{opacity:0;transform:scale(0.94)}} to{{opacity:1;transform:scale(1)}} }}
@keyframes popIn {{ from{{opacity:0;transform:scale(0.8)}} to{{opacity:1;transform:scale(1)}} }}
@keyframes glowPulse {{
    0%,100%{{box-shadow:0 0 0 0 rgba(59,130,246,0)}}
    50%{{box-shadow:0 0 20px 4px rgba(59,130,246,0.15)}}
}}

.anim-up {{ animation:fadeInUp 0.55s ease-out both; }}
.anim-fade {{ animation:fadeIn 0.45s ease-out both; }}
.anim-left {{ animation:slideLeft 0.5s ease-out both; }}
.anim-scale {{ animation:scaleIn 0.4s ease-out both; }}
.anim-pop {{ animation:popIn 0.35s cubic-bezier(0.34,1.56,0.64,1) both; }}
.d1{{animation-delay:.08s}} .d2{{animation-delay:.16s}} .d3{{animation-delay:.24s}}
.d4{{animation-delay:.32s}} .d5{{animation-delay:.4s}} .d6{{animation-delay:.48s}}

.stApp {{ font-family:'Source Sans 3',-apple-system,sans-serif!important; background:{BG}!important; color:{TXT}!important; }}
.block-container {{ padding-top:0.5rem!important; max-width:1100px!important; }}
h1,h2,h3,h4,h5,h6 {{ font-family:'Source Sans 3',sans-serif!important; color:{TXT}!important; }}
p,li,span,div,label {{ color:{TXT2}; }}
#MainMenu,footer,header {{ visibility:hidden; }}
.stDeployButton {{ display:none; }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap:2px; background:{TAB_BG}; border-radius:10px;
    padding:4px; border:1px solid {BORDER}; margin-bottom:1.8rem;
}}
.stTabs [data-baseweb="tab"] {{
    font-family:'Source Sans 3',sans-serif!important; font-weight:500;
    font-size:0.84rem; padding:0.5rem 0.9rem; border-radius:8px;
    color:{TXT4}; background:transparent; border:none; transition:all 0.25s ease;
}}
.stTabs [aria-selected="true"] {{
    background:{TAB_SEL_BG}!important; color:{TAB_SEL_TXT}!important;
    font-weight:600; box-shadow:0 1px 6px rgba(0,0,0,0.08);
}}

/* Hero */
.hero-wrap {{
    padding:2.2rem 2rem; background:{HERO_BG};
    border:1px solid {BORDER}; border-radius:16px; margin-bottom:1.5rem;
}}
.hero-name {{ font-size:2.5rem; font-weight:800; color:{TXT}; margin:0 0 0.1rem; line-height:1.15; letter-spacing:-0.5px; }}
.hero-title {{ font-family:'DM Mono',monospace; font-size:0.85rem; color:{ACCENT}; margin-bottom:0.7rem; }}
.hero-bio {{ font-size:0.98rem; color:{TXT3}; line-height:1.7; max-width:640px; }}

/* Stats — clickable interactive cards */
.stat-row {{ display:flex; gap:0.7rem; margin:1.2rem 0; flex-wrap:wrap; }}
.stat-card {{
    flex:1; min-width:120px; background:{STAT_BG};
    border:1px solid {BORDER}; border-radius:12px; padding:0.85rem; text-align:center;
    transition:all 0.3s cubic-bezier(0.34,1.56,0.64,1); cursor:default;
}}
.stat-card:hover {{
    border-color:{ACCENT}; transform:translateY(-4px) scale(1.03);
    box-shadow:0 8px 24px rgba(59,130,246,0.12);
}}
.stat-card:active {{ transform:translateY(-1px) scale(0.98); }}
.stat-num {{ font-size:1.65rem; font-weight:700; color:{ACCENT}; line-height:1.2; }}
.stat-lbl {{ font-size:0.68rem; color:{TXT4}; text-transform:uppercase; letter-spacing:0.8px; margin-top:0.1rem; }}

/* Section */
.sec-title {{ font-size:1.45rem; font-weight:700; color:{TXT}; margin:1.8rem 0 0.35rem; }}
.sec-sub {{ color:{TXT4}; font-size:0.88rem; margin-bottom:1.3rem; }}

/* Timeline card */
.t-card {{
    background:{CARD}; border:1px solid {BORDER}; border-radius:14px;
    padding:1.3rem 1.3rem 1.3rem 1.6rem; margin-bottom:0.85rem;
    border-left:3px solid {ACCENT};
    transition:all 0.3s cubic-bezier(0.25,0.46,0.45,0.94);
}}
.t-card:hover {{ box-shadow:0 8px 24px rgba(59,130,246,0.08); transform:translateY(-3px); }}
.t-header {{ display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem; }}
.t-role {{ font-size:1.02rem; font-weight:600; color:{TXT}; }}
.t-role a {{ color:{TXT}; text-decoration:none; border-bottom:1px dashed {ACCENT}; transition:color 0.2s; }}
.t-role a:hover {{ color:{ACCENT}; }}
.t-company {{ font-size:0.86rem; color:{ACCENT}; font-weight:500; }}
.t-date {{
    font-family:'DM Mono',monospace; font-size:0.72rem; color:{TXT4};
    background:{BG2}; padding:0.2rem 0.55rem; border-radius:6px;
    border:1px solid {BORDER}; white-space:nowrap;
}}
.t-desc {{ color:{TXT3}; font-size:0.86rem; line-height:1.6; }}
.t-desc ul {{ margin:0.25rem 0; padding-left:1.05rem; }}
.t-desc li {{ margin-bottom:0.12rem; color:{TXT3}; }}
.t-skills {{ display:flex; flex-wrap:wrap; gap:0.3rem; margin-top:0.55rem; }}
.sk {{
    font-family:'DM Mono',monospace; font-size:0.67rem; color:{ACCENT};
    background:{TAG_BG}; border:1px solid {TAG_BD};
    padding:0.17rem 0.48rem; border-radius:5px; transition:all 0.2s;
}}
.sk:hover {{ transform:translateY(-1px); box-shadow:0 2px 8px rgba(59,130,246,0.1); }}

/* Edu */
.edu-card {{
    background:{CARD}; border:1px solid {BORDER}; border-radius:14px;
    padding:1.3rem; margin-bottom:0.85rem;
    transition:all 0.3s cubic-bezier(0.25,0.46,0.45,0.94);
}}
.edu-card:hover {{ box-shadow:0 8px 24px rgba(79,70,229,0.07); transform:translateY(-3px); }}
.edu-deg {{ font-size:1.1rem; font-weight:700; color:{ACCENT2}; }}
.edu-school {{ font-size:0.9rem; color:{TXT2}; font-weight:500; }}
.edu-det {{ color:{TXT3}; font-size:0.84rem; line-height:1.6; margin-top:0.4rem; }}

/* Award */
.aw-card {{
    background:{AMBER_BG}; border:1px solid {AMBER_BD}; border-radius:12px;
    padding:1rem 1.2rem; margin-bottom:0.65rem;
    transition:all 0.3s cubic-bezier(0.34,1.56,0.64,1);
}}
.aw-card:hover {{ transform:translateY(-3px); box-shadow:0 6px 18px rgba(245,158,11,0.1); }}
.aw-title {{ font-size:0.9rem; font-weight:600; color:{AMBER_TXT}; }}
.aw-desc {{ color:{TXT3}; font-size:0.82rem; margin-top:0.12rem; }}

/* Publication */
.pub-card {{
    background:{CARD}; border:1px solid {BORDER}; border-left:3px solid {PUB_LEFT};
    border-radius:12px; padding:1.1rem 1.2rem; margin-bottom:0.65rem;
    transition:all 0.3s ease;
}}
.pub-card:hover {{ box-shadow:0 6px 18px rgba(16,185,129,0.08); transform:translateY(-2px); }}
.pub-title {{ font-weight:600; color:{TXT}; font-size:0.92rem; }}
.pub-title a {{ color:{TXT}; text-decoration:none; border-bottom:1px dashed {ACCENT3}; }}
.pub-title a:hover {{ color:{ACCENT3}; }}
.pub-venue {{ font-size:0.78rem; color:{ACCENT3}; margin-top:0.1rem; }}
.pub-link {{ font-family:'DM Mono',monospace; font-size:0.72rem; margin-top:0.18rem; }}
.pub-link a {{ color:{ACCENT}; text-decoration:none; }}
.pub-link a:hover {{ text-decoration:underline; }}
.pub-desc {{ color:{TXT4}; font-size:0.82rem; margin-top:0.25rem; line-height:1.5; }}

/* Contact */
.c-item {{
    display:flex; align-items:center; gap:0.6rem; padding:0.6rem 0.9rem;
    background:{BG2}; border:1px solid {BORDER}; border-radius:10px;
    margin-bottom:0.3rem; font-size:0.86rem; color:{TXT3}; transition:all 0.2s;
}}
.c-item:hover {{ border-color:{ACCENT}; transform:translateX(3px); }}
.c-item a {{ color:{ACCENT}; text-decoration:none; }}

/* Video */
.vid-title {{ font-size:0.95rem; font-weight:600; color:{TXT}; margin-bottom:0.5rem; }}

/* Project section */
.proj-section {{
    background:{BG2}; border:1px solid {BORDER}; border-radius:14px;
    padding:1.3rem; margin-bottom:1rem;
    transition:all 0.3s ease;
}}
.proj-section:hover {{ box-shadow:0 4px 16px rgba(59,130,246,0.06); }}
.proj-section-title {{ font-size:1.05rem; font-weight:700; color:{TXT}; margin-bottom:0.6rem; }}

/* Doc link buttons */
.doc-btn {{
    display:inline-flex; align-items:center; gap:0.4rem;
    padding:0.4rem 0.9rem; border-radius:8px; font-size:0.82rem; font-weight:500;
    background:{TAG_BG}; border:1px solid {TAG_BD}; color:{ACCENT};
    text-decoration:none; transition:all 0.25s; margin-right:0.5rem; margin-top:0.4rem;
}}
.doc-btn:hover {{ background:{ACCENT}; color:#fff; border-color:{ACCENT}; transform:translateY(-1px); }}

/* Profile photo */
.profile-photo {{
    width:140px; height:140px; border-radius:50%; object-fit:cover;
    border:3px solid {ACCENT}; box-shadow:0 0 24px rgba(59,130,246,0.2);
    transition:all 0.4s ease;
}}
.profile-photo:hover {{ transform:scale(1.05); box-shadow:0 0 32px rgba(59,130,246,0.3); }}

/* Misc */
.stImage>img {{ border-radius:10px; }}
.stButton>button {{
    border-radius:8px!important; font-family:'Source Sans 3',sans-serif!important;
    font-weight:600!important; font-size:0.88rem!important;
    padding:0.35rem 1rem!important;
    background:{CARD}!important; color:{TXT3}!important;
    border:1px solid {BORDER}!important;
    transition:all 0.25s cubic-bezier(0.34,1.56,0.64,1)!important;
}}
.stButton>button:hover {{ border-color:{ACCENT}!important; color:{ACCENT}!important; transform:translateY(-2px)!important; box-shadow:0 4px 12px rgba(59,130,246,0.1)!important; }}
.stButton>button:active {{ transform:translateY(0)!important; }}
hr {{ border-color:{BORDER}!important; }}
</style>
""", unsafe_allow_html=True)


# ─── YouTube embed ───
def yt_embed(url, height=340):
    vid = ""
    if "watch?v=" in url: vid = url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url: vid = url.split("youtu.be/")[1].split("?")[0]
    if vid:
        st.markdown(
            f'<iframe width="100%" height="{height}" src="https://www.youtube.com/embed/{vid}" '
            f'frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;'
            f'gyroscope;picture-in-picture" allowfullscreen style="border-radius:10px;border:1px solid {BORDER};"></iframe>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════
# TAB ORDER: Home, Experience, Education, Products, Academics, Certificates, Projects & Videos, Contact
# ═══════════════════════════════════════════
tabs = st.tabs(["Home","Experience","Education","Products","Academics","Certificates","Projects & Videos","Contact"])


# ══════════════════ HOME ══════════════════
with tabs[0]:
    col_photo, col_info = st.columns([1, 3.5], gap="large")
    with col_photo:
        profile = get_images("profile")
        if profile:
            with open(profile[0],"rb") as f:
                pb64 = base64.b64encode(f.read()).decode()
            ext = Path(profile[0]).suffix.lower().replace(".","")
            pmime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"
            st.markdown(f'<img src="data:{pmime};base64,{pb64}" class="profile-photo anim-pop">', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="anim-pop" style="width:140px;height:140px;border-radius:50%;'
                f'background:{ACCENT};display:flex;align-items:center;justify-content:center;'
                f'font-size:2.5rem;color:#fff;font-weight:700;border:3px solid {ACCENT};'
                f'box-shadow:0 0 24px rgba(59,130,246,0.2);">SH</div>',
                unsafe_allow_html=True,
            )
            st.caption("Add your photo to `assets/profile/`")

    with col_info:
        st.markdown(f"""
        <div class="hero-wrap anim-up">
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
    <div class="stat-row anim-up d2">
        <div class="stat-card anim-pop d1"><div class="stat-num">5+</div><div class="stat-lbl">Years Experience</div></div>
        <div class="stat-card anim-pop d2"><div class="stat-num">5+</div><div class="stat-lbl">Product Deployments</div></div>
        <div class="stat-card anim-pop d3"><div class="stat-num">3</div><div class="stat-lbl">Publications</div></div>
        <div class="stat-card anim-pop d4"><div class="stat-num">5</div><div class="stat-lbl">Awards</div></div>
        <div class="stat-card anim-pop d5"><div class="stat-num">2</div><div class="stat-lbl">Degrees</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sec-title anim-fade d3">Highlights</div>', unsafe_allow_html=True)
    slideshow("achievements", key="home_ach")

    st.markdown(f"""
    <div class="aw-card anim-left d1"><div class="aw-title">Best Presentation Award — IEEE ICCE 2024, Las Vegas</div><div class="aw-desc">IoT-enabled automatic gear shifting for E-bikes. Best among 50+ papers.</div></div>
    <div class="aw-card anim-left d2"><div class="aw-title">Bosch Future Mobility Challenge — Semi-Finalist, Cluj Romania</div><div class="aw-desc">Represented Germany among 100+ teams. Led sensor fusion on NVIDIA Jetson Xavier.</div></div>
    <div class="aw-card anim-left d3"><div class="aw-title">Bravo Award — Robert Bosch</div><div class="aw-desc">Recognized for SecOC tool delivery in ECU security.</div></div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sec-title anim-fade d4">Core skills</div>', unsafe_allow_html=True)
    skills = {
        "Embedded & IoT":["Edge ML","Arduino","Raspberry Pi","STM32","Firmware","IoT Security","CAN","V2V"],
        "AI / ML":["ASR","NLP","RAG","Model Compression","TensorRT","GPU Accel.","Computer Vision"],
        "Programming":["Python","C","C++","CAPL","ROS"],
        "Platforms":["Linux/RHEL","CUDA","NVIDIA Jetson","Docker","Git"],
    }
    c1,c2 = st.columns(2)
    for i,(cat,sk) in enumerate(skills.items()):
        with c1 if i%2==0 else c2:
            st.markdown(f'<p style="font-weight:600;color:{TXT};margin-bottom:0.2rem;">{cat}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="t-skills anim-fade d{i+1}">'+"".join(f'<span class="sk">{s}</span>' for s in sk)+'</div>', unsafe_allow_html=True)
            st.markdown("")


# ══════════════════ EXPERIENCE ══════════════════
with tabs[1]:
    st.markdown(f'<div class="sec-title anim-up">Work Experience</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-sub">From embedded systems at Bosch to leading R&D at a healthtech startup.</div>', unsafe_allow_html=True)

    exps = [
        ("Lead R&D Product Engineer","O-Health · Bangalore & Boston","Jan 2025 – Present",
         ["Improved ASR accuracy — reduced WER by 40% for Standard Hindi on edge models",
          "Reduced inference latency by 50% via knowledge distillation, quantization, weight pruning",
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
    for idx,(role,company,date,bullets,sk) in enumerate(exps):
        bl="".join(f"<li>{b}</li>" for b in bullets)
        tags="".join(f'<span class="sk">{s}</span>' for s in sk)
        st.markdown(
            f'<div class="t-card anim-up d{min(idx%3+1,3)}"><div class="t-header"><div>'
            f'<div class="t-role">{role}</div><div class="t-company">{company}</div></div>'
            f'<span class="t-date">{date}</span></div>'
            f'<div class="t-desc"><ul>{bl}</ul></div>'
            f'<div class="t-skills">{tags}</div></div>',
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div class="sec-title">Workplace photos</div>', unsafe_allow_html=True)
    slideshow("experience", key="exp_s")


# ══════════════════ EDUCATION ══════════════════
with tabs[2]:
    st.markdown(f'<div class="sec-title anim-up">Education</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="edu-card anim-up d1">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div><div class="edu-deg">M.Sc. Communication Engineering</div>
            <div class="edu-school">Technical University of Munich (TUM) — Germany</div></div>
            <span class="t-date">Oct 2021 – Oct 2024</span>
        </div>
        <div class="edu-det">
            <strong style="color:{TXT2}">Grade:</strong> 2.1 ·
            <strong style="color:{TXT2}">Thesis:</strong> Lane-Free Traffic Control on Connected Mini Automated Vehicles <em>(1.0)</em><br>
            <strong style="color:{TXT2}">Focus:</strong> Embedded Systems & Security, IoT, SoC, Data Networks<br>
            <strong style="color:{TXT2}">Extra:</strong> 6G Business Modeling Lab (TUM CDTM)
        </div>
    </div>
    <div class="edu-card anim-up d2">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div><div class="edu-deg">B.E. Electronics & Communication</div>
            <div class="edu-school">National Institute of Engineering — Mysore, India</div></div>
            <span class="t-date">Aug 2016 – Oct 2020</span>
        </div>
        <div class="edu-det">
            <strong style="color:{TXT2}">Grade:</strong> 1.6 ·
            <strong style="color:{TXT2}">Thesis:</strong> Data Analysis from Sensors via DSP and WSN <em>(1.0)</em><br>
            <strong style="color:{TXT2}">Focus:</strong> Digital Electronics, Embedded Systems, Network Security, C++
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sec-title" style="font-size:1.15rem;">Online courses</div>', unsafe_allow_html=True)
    for c in ["IoT Wireless & Cloud Computing — Yonsei University (Coursera)",
              "Embedded Hardware & Operating Systems — EIT Digital (Coursera)",
              "Computer Networks & IP Protocol — IIT Kharagpur (NPTEL)",
              "Python for Computer Vision with OpenCV & Deep Learning (Udemy)"]:
        st.markdown(f'<div class="c-item anim-fade">{c}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div class="sec-title">Degree certificates</div>', unsafe_allow_html=True)
    slideshow("education", key="edu_s")


# ══════════════════ PRODUCTS ══════════════════
with tabs[3]:
    st.markdown(f'<div class="sec-title anim-up">Products & Builds</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-sub">Hardware, software, and everything in between.</div>', unsafe_allow_html=True)

    products = [
        ("Health Band — O-Health","Production-grade wearable with custom sensors, BLE, and cloud ML. 30,000+ clinical consultations.",
         ["Hardware","Firmware","ML","BLE","Healthcare"], None),
        ("ASR Engine for Hindi","Edge-optimized ASR. 40% WER improvement, 50% latency reduction.",
         ["ASR","Edge ML","Compression","NLP"], None),
        ("Medical RAG Pipeline","Hallucination-free medical info extraction via cross-LLM consensus.",
         ["RAG","LLM","Healthcare","NLP"], None),
        ("Retrofittable E-Bike Auto Shifter",
         "IoT-enabled rear-derailleur shifting with mode-based transmission and adaptive riding. IEEE ICCE 2024 Best Presentation.",
         ["IoT","Mechatronics","Sensors","IEEE"],
         "https://ieeexplore.ieee.org/document/10444469"),
        ("SecOC Tool — Bosch","Automated ECU data encryption for CAN bus.",
         ["Automotive","Security","CAN","CAPL"], None),
        ("Autonomous Mini Vehicle — TUM","Lane-free traffic control with V2V and sensor fusion.",
         ["Autonomous","V2V","ROS","Sensor Fusion"], None),
    ]
    for i in range(0,len(products),2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(products):
                name,desc,tags,link = products[i+j]
                tk = "".join(f'<span class="sk">{t}</span>' for t in tags)
                title_html = f'<a href="{link}" target="_blank">{name}</a>' if link else name
                link_html = f'<div class="pub-link"><a href="{link}" target="_blank">📄 View paper</a></div>' if link else ""
                with cols[j]:
                    st.markdown(
                        f'<div class="t-card anim-scale d{j+1}" style="min-height:160px;">'
                        f'<div class="t-role">{title_html}</div>'
                        f'<div class="t-desc" style="margin:0.3rem 0;">{desc}</div>'
                        f'{link_html}'
                        f'<div class="t-skills">{tk}</div></div>',
                        unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div class="sec-title">Product gallery</div>', unsafe_allow_html=True)
    slideshow("products", key="prod_s")


# ══════════════════ ACADEMICS ══════════════════
with tabs[4]:
    st.markdown(f'<div class="sec-title anim-up">Academic Work</div>', unsafe_allow_html=True)

    # ── Research Projects ──
    st.markdown(f'<p style="font-weight:600;font-size:1.08rem;color:{TXT};margin:1.3rem 0 0.5rem;">Research projects</p>', unsafe_allow_html=True)

    # 1) Lane-Free Traffic — clickable, scrolls to docs below
    st.markdown(f"""
    <div class="t-card anim-up d1">
        <div class="t-header"><div>
            <div class="t-role"><a href="#lane-free-docs">Lane-Free Traffic Control for Connected Mini-Automated Vehicles</a></div>
            <div class="t-company">Master's Thesis — TU München</div>
        </div><span class="t-date">Feb – Oct 2024</span></div>
        <div class="t-desc">Designed and implemented lane-free control strategies for connected autonomous vehicles using V2V communication. Defined control loops and boundary conditions.</div>
        <div class="t-skills">
            <span class="sk">Vehicle Control</span><span class="sk">V2V</span>
            <span class="sk">Sensor Fusion</span><span class="sk">Autonomous Systems</span>
        </div>
        <div style="margin-top:0.6rem;">
            <a class="doc-btn" href="#lane-free-docs">📄 PDF (Thesis)</a>
            <a class="doc-btn" href="#lane-free-docs">📊 Presentation</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2) Cellular IoT Cloud Connectivity
    st.markdown(f"""
    <div class="t-card anim-up d2">
        <div class="t-header"><div>
            <div class="t-role"><a href="#cellular-iot-docs">Cellular IoT Cloud Connectivity</a></div>
            <div class="t-company">Würth Elektronik eiSoS — TU München</div>
        </div><span class="t-date">2022 – 2024</span></div>
        <div class="t-desc">Designed a plug-and-play system enabling seamless communication between the sensor module and cellular Adrastea-I, transmitting data to the cloud in secure mode via digital certificates in both LTE-CAT-M and NB-IoT modes with PSM power saving.</div>
        <div class="t-skills">
            <span class="sk">LTE-M</span><span class="sk">NB-IoT</span>
            <span class="sk">PSM</span><span class="sk">Cloud IoT</span>
            <span class="sk">Digital Certificates</span><span class="sk">Adrastea-I</span>
        </div>
        <div style="margin-top:0.6rem;">
            <a class="doc-btn" href="#cellular-iot-docs">📄 PDF</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Publications ──
    st.markdown(f'<p style="font-weight:600;font-size:1.08rem;color:{TXT};margin:1.5rem 0 0.5rem;">Publications</p>', unsafe_allow_html=True)

    pubs = [
        ("Retrofittable Automatic Shifter of Rear-Derailleur with Mode-Based Transmission and IoT",
         "IEEE ICCE 2024","https://ieeexplore.ieee.org/document/10444469",
         "Retrofittable shifting for E-bikes with IoT and adaptive riding modes."),
        ("Remote Monitoring Robot with Voice Control and Image Analysis",
         "Scopus-indexed — IJAST","http://sersc.org/journals/index.php/IJAST/article/view/21218",
         "Surveillance robot with image processing, voice control, and MQTT."),
        ("Data Extraction with Signal Comparison for Forest Logging Prevention",
         "IJERT · NCCDS 2020","https://www.ijert.org/data-extraction-with-signal-comparison-for-forest-logging-prevention",
         "WSN for illegal logging detection via FFT-based signal processing."),
    ]
    for t,v,u,d in pubs:
        st.markdown(
            f'<div class="pub-card anim-fade">'
            f'<div class="pub-title"><a href="{u}" target="_blank">{t}</a></div>'
            f'<div class="pub-venue">{v}</div>'
            f'<div class="pub-link"><a href="{u}" target="_blank">📄 {u}</a></div>'
            f'<div class="pub-desc">{d}</div></div>',
            unsafe_allow_html=True)

    # ── Conferences ──
    st.markdown(f'<p style="font-weight:600;font-size:1.08rem;color:{TXT};margin:1.5rem 0 0.5rem;">Conferences</p>', unsafe_allow_html=True)
    for n,l,note in [
        ("IEEE ICCE 2024","Las Vegas","Best Presentation"),
        ("Bosch Future Mobility 2023","Cluj, Romania","Semi-finalist"),
        ("ICICEE 2020","Tumkur","Best Paper"),
        ("NCCDS 2020","Mysuru","Paper Presentation"),
        ("ANKURA'19","Mysore","National Paper Presentation"),
        ("TI Innovation Challenge 2019","India","Design Contest"),
    ]:
        st.markdown(f'<div class="c-item anim-fade"><strong>{n}</strong>&nbsp;— {l} &nbsp;<em>({note})</em></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div class="sec-title">Academic gallery</div>', unsafe_allow_html=True)
    slideshow("academics", key="acad_s")

    # ── DOCUMENT EMBEDS ──
    st.markdown("---")
    st.markdown(f'<div id="lane-free-docs"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-title anim-up">📄 Lane-Free Traffic Control — Documents</div>', unsafe_allow_html=True)

    doc_c1, doc_c2 = st.columns(2)
    with doc_c1:
        st.markdown(f'<p style="font-weight:600;color:{TXT};">Thesis PDF</p>', unsafe_allow_html=True)
        embed_ppt_or_pdf("lane_free_thesis.pdf", "Lane-Free Thesis PDF")
    with doc_c2:
        st.markdown(f'<p style="font-weight:600;color:{TXT};">Presentation</p>', unsafe_allow_html=True)
        embed_ppt_or_pdf("lane_free_presentation.pdf", "Lane-Free Presentation")

    st.markdown("---")
    st.markdown(f'<div id="cellular-iot-docs"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-title anim-up">📄 Cellular IoT Cloud Connectivity — Document</div>', unsafe_allow_html=True)
    embed_ppt_or_pdf("cellular_iot.pdf", "Cellular IoT PDF")


# ══════════════════ CERTIFICATES ══════════════════
with tabs[5]:
    st.markdown(f'<div class="sec-title anim-up">Certificates & Awards</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-sub">Filtered by category. Scanned copies below.</div>', unsafe_allow_html=True)

    certs = [
        ("Best Session Presentation — IEEE ICCE 2024","Las Vegas · Jan 2024","Award",AMBER_TXT),
        ("Certificate of Participation — IEEE ICCE 2024","Retrofittable Auto Shifter","Conference",ACCENT),
        ("Best Paper — ICICEE 2020","Remote Monitoring with Voice Control · Tumkur","Award",AMBER_TXT),
        ("Bravo Award — Robert Bosch","SecOC tool delivery · Aug 2021","Corporate",ACCENT2),
        ("Bosch Future Mobility Challenge","TUMAVERICK — Semi-finalist · Cluj 2023","Competition","#fb7185" if DARK else "#e11d48"),
        ("Tejas Networks Internship","Product verification · 2020","Internship",ACCENT3),
        ("NCCDS 2020","Forest Logging Prevention","Conference",ACCENT),
        ("NIE IEEE Biblus — ANKURA'19","National Paper Presentation","Conference",ACCENT),
        ("NIE Summer of Code 5.0","Hardware Track · 2018","Workshop","#22d3ee" if DARK else "#0891b2"),
        ("Adroit'18 Appreciation","IEEE NIE volunteering · Oct 2018","Volunteering","#a78bfa" if DARK else "#7c3aed"),
        ("Texas Instruments Innovation 2019","DST & TI Design Contest","Competition","#fb7185" if DARK else "#e11d48"),
    ]
    all_cats = sorted(set(c[2] for c in certs))
    sel = st.multiselect("Filter",all_cats,default=all_cats,key="cf")
    for idx,(title,desc,cat,color) in enumerate(certs):
        if cat in sel:
            st.markdown(
                f'<div class="t-card anim-left d{min(idx%3+1,3)}" style="border-left-color:{color};">'
                f'<div class="t-header"><div><div class="t-role">{title}</div>'
                f'<div class="t-desc">{desc}</div></div>'
                f'<span class="t-date">{cat}</span></div></div>',
                unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div class="sec-title">Certificate scans</div>', unsafe_allow_html=True)
    slideshow("certificates", key="cert_s")


# ══════════════════ PROJECTS & VIDEOS ══════════════════
with tabs[6]:
    st.markdown(f'<div class="sec-title anim-up">Projects & Videos</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-sub">Demo videos, project walkthroughs, and builds.</div>', unsafe_allow_html=True)

    # Forest Logging
    st.markdown(f"""
    <div class="proj-section anim-up d1">
        <div class="proj-section-title">🌲 Illegal Forest Logging Prevention — STM32 Wireless Nodes</div>
        <div class="t-desc">Bachelor thesis — wireless sensor network for detecting illegal logging via FFT-based audio analysis on STM32 microcontrollers.</div>
        <div class="pub-link" style="margin-top:0.4rem;">
            <a href="https://www.ijert.org/data-extraction-with-signal-comparison-for-forest-logging-prevention" target="_blank">📄 Read the paper (IJERT)</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    vc1,vc2 = st.columns(2)
    with vc1:
        st.markdown(f'<div class="vid-title">Project demo</div>', unsafe_allow_html=True)
        yt_embed("https://www.youtube.com/watch?v=g9tRZPRJfYs")
    with vc2:
        st.markdown(f'<div class="vid-title">Cooja simulator</div>', unsafe_allow_html=True)
        yt_embed("https://www.youtube.com/watch?v=wczmB9WR8O4")

    st.markdown("---")

    # Pest Detection
    st.markdown(f"""
    <div class="proj-section anim-up d2">
        <div class="proj-section-title">🐛 Pest Detection Using ML on Edge Devices</div>
        <div class="t-desc">Machine learning-based pest detection running on edge devices for real-time agricultural monitoring.</div>
        <div class="pub-link" style="margin-top:0.4rem;">
            <a href="https://resources.mouser.com/explore-all/pest-detection-using-machine-learning-on-edge-devices" target="_blank">📄 View on Mouser</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<p style="font-weight:600;color:{TXT};font-size:0.95rem;margin:0.5rem 0;">Project photos</p>', unsafe_allow_html=True)
    slideshow("projects", key="proj_s")

    st.markdown("---")

    # TUM Robotics Club
    st.markdown(f"""
    <div class="proj-section anim-up d3">
        <div class="proj-section-title">🤖 TUM Robotics Club</div>
        <div class="t-desc">Activities, competitions, and collaborative engineering with the TUM Robotics Club.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;color:{TXT};font-size:0.95rem;margin:0.5rem 0;">Photos</p>', unsafe_allow_html=True)
    slideshow("robotics_club", key="robo_s")

    # Robotics videos provision
    robotics_club_videos = [
        # ("Title", "https://www.youtube.com/watch?v=XXXXX"),
    ]
    if robotics_club_videos:
        st.markdown(f'<p style="font-weight:600;color:{TXT};font-size:0.95rem;margin:1rem 0 0.5rem;">Videos</p>', unsafe_allow_html=True)
        for title, url in robotics_club_videos:
            st.markdown(f'<div class="vid-title">{title}</div>', unsafe_allow_html=True)
            yt_embed(url)
    else:
        st.markdown(f"""
        <div style="background:{BG2};border:1px dashed {BORDER};border-radius:10px;padding:0.8rem;margin-top:0.6rem;">
            <p style="color:{TXT4};font-size:0.82rem;margin:0;">
                📹 Add YouTube links to <code>robotics_club_videos</code> list in <code>app.py</code> to embed here.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════ CONTACT ══════════════════
with tabs[7]:
    st.markdown(f'<div class="sec-title anim-up">Get in touch</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="c-item anim-left d1">📞 &nbsp; +49 176 71095238</div>
        <div class="c-item anim-left d2">📧 &nbsp; <a href="mailto:shashankv099@gmail.com">shashankv099@gmail.com</a></div>
        <div class="c-item anim-left d3">💼 &nbsp; <a href="https://www.linkedin.com/in/shashank-hegde98" target="_blank">linkedin.com/in/shashank-hegde98</a></div>
        <div class="c-item anim-left d4">🌍 &nbsp; Bangalore, India & Munich, Germany</div>
        <div class="c-item anim-left d5">🇺🇸 &nbsp; Nationality: United States of America</div>
        """, unsafe_allow_html=True)
        st.markdown("")
        st.markdown(f'<p style="font-weight:600;color:{TXT};">Languages</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="c-item anim-fade">English — C2 · German — A2 (learning B1)</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="hero-wrap anim-scale" style="padding:1.4rem;">
            <div style="font-size:1rem;font-weight:600;color:{TXT};margin-bottom:0.3rem;">Open to opportunities</div>
            <div class="hero-bio" style="font-size:0.88rem;">
                Interested in Embedded ML, Edge AI, Healthcare Technology, and IoT systems.
                Reach out via email or LinkedIn.
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f'<p style="text-align:center;color:{TXT4};font-size:0.8rem;">Shashank Hegde · Embedded-ML Electronics Engineer · © 2025</p>', unsafe_allow_html=True)
