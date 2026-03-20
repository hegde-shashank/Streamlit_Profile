import streamlit as st
from pathlib import Path
import base64

st.set_page_config(page_title="Shashank Hegde | Portfolio", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# ═══ DARK / LIGHT ═══
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
head = st.columns([10, 1])
with head[1]:
    if st.button("☀️" if st.session_state.dark_mode else "🌙", key="tt", help="Toggle theme"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
DARK = st.session_state.dark_mode

# ═══ ASSETS ═══
A = Path("assets")
for d in ["profile","achievements","certificates","experience","education","products","academics","projects","robotics_club","docs"]:
    (A/d).mkdir(parents=True, exist_ok=True)

def imgs(cat):
    d=A/cat
    return [str(p) for p in sorted(d.iterdir()) if p.suffix.lower() in {".jpg",".jpeg",".png",".webp"}] if d.exists() else []

def b64img(path):
    with open(path,"rb") as f: return base64.b64encode(f.read()).decode()

def mimetype(path):
    ext=Path(path).suffix.lower().replace(".","")
    return f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"

def slideshow(cat, key):
    images=imgs(cat)
    if not images:
        st.info(f"No images yet — add files to `assets/{cat}/` and redeploy.")
        return
    k=f"s_{key}"
    if k not in st.session_state: st.session_state[k]=0
    t=len(images); i=st.session_state[k]%t
    cap=Path(images[i]).stem.replace("_"," ").replace("-"," ")
    st.markdown(f"""
    <div style="position:relative;max-width:720px;margin:0 auto;border-radius:12px;overflow:hidden;border:1px solid {BD};animation:fadeIn .4s ease-out;">
        <img src="data:{mimetype(images[i])};base64,{b64img(images[i])}" style="width:100%;display:block;"/>
    </div>
    <p style="text-align:center;color:{T4};font-size:.82rem;margin:4px 0 2px;">{cap} · {i+1}/{t}</p>
    """, unsafe_allow_html=True)
    _,bp,_,bn,_=st.columns([3,1.2,2,1.2,3])
    with bp:
        if st.button("← Prev",key=f"{key}_p",use_container_width=True):
            st.session_state[k]=(i-1)%t; st.rerun()
    with bn:
        if st.button("Next →",key=f"{key}_n",use_container_width=True):
            st.session_state[k]=(i+1)%t; st.rerun()

def embed_doc(fname, label="Document", h=550):
    p=A/"docs"/fname
    if p.exists() and p.suffix.lower()==".pdf":
        with open(p,"rb") as f: d=base64.b64encode(f.read()).decode()
        st.markdown(f'<iframe src="data:application/pdf;base64,{d}" width="100%" height="{h}px" style="border:1px solid {BD};border-radius:10px;"></iframe>',unsafe_allow_html=True)
    elif p.exists():
        with open(p,"rb") as f: data=f.read()
        st.download_button(f"⬇ Download {label}",data,file_name=fname)
    else:
        st.info(f"📄 Place `{fname}` in `assets/docs/` and redeploy.")

def yt(url, h=330):
    vid=""
    if "watch?v=" in url: vid=url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url: vid=url.split("youtu.be/")[1].split("?")[0]
    if vid:
        st.markdown(f'<iframe width="100%" height="{h}" src="https://www.youtube.com/embed/{vid}" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen style="border-radius:10px;border:1px solid {BD};"></iframe>',unsafe_allow_html=True)

# ═══ THEME ═══
if DARK:
    BG="#0f172a";BG2="#1e293b";CD="#1e293b";TX="#f1f5f9";T2="#cbd5e1";T3="#94a3b8";T4="#64748b"
    BD="#334155";AC="#3b82f6";A2="#8b5cf6";A3="#10b981";AMB="#fbbf24";AMBBG="rgba(245,158,11,.1)";AMBBD="rgba(245,158,11,.3)"
    TBG="#1e293b";TSBG="#3b82f6";TSTX="#fff";HBG="linear-gradient(135deg,rgba(59,130,246,.08),rgba(139,92,246,.08))"
    TAGBG="rgba(59,130,246,.12)";TAGBD="rgba(59,130,246,.25)";GL="rgba(59,130,246,.2)"
else:
    BG="#ffffff";BG2="#f8fafc";CD="#ffffff";TX="#0f172a";T2="#334155";T3="#475569";T4="#64748b"
    BD="#e2e8f0";AC="#2563eb";A2="#4f46e5";A3="#059669";AMB="#92400e";AMBBG="#fffbeb";AMBBD="#fde68a"
    TBG="#f1f5f9";TSBG="#ffffff";TSTX="#2563eb";HBG="linear-gradient(135deg,rgba(37,99,235,.04),rgba(79,70,229,.04))"
    TAGBG="#eff6ff";TAGBD="#dbeafe";GL="rgba(37,99,235,.12)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

@keyframes fadeInUp{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes slideL{{from{{opacity:0;transform:translateX(-18px)}}to{{opacity:1;transform:translateX(0)}}}}
@keyframes popIn{{from{{opacity:0;transform:scale(.92)}}to{{opacity:1;transform:scale(1)}}}}

.au{{animation:fadeInUp .5s ease-out both}}.af{{animation:fadeIn .4s ease-out both}}
.al{{animation:slideL .45s ease-out both}}.ap{{animation:popIn .35s cubic-bezier(.34,1.56,.64,1) both}}
.d1{{animation-delay:.06s}}.d2{{animation-delay:.12s}}.d3{{animation-delay:.18s}}
.d4{{animation-delay:.24s}}.d5{{animation-delay:.3s}}.d6{{animation-delay:.36s}}

.stApp{{font-family:'Source Sans 3',-apple-system,sans-serif!important;background:{BG}!important;color:{TX}!important}}
.block-container{{padding-top:.5rem!important;max-width:1100px!important}}
h1,h2,h3,h4,h5,h6{{font-family:'Source Sans 3',sans-serif!important;color:{TX}!important}}
p,li,span,div,label{{color:{T2}}}
#MainMenu,footer,header{{visibility:hidden}}.stDeployButton{{display:none}}

.stTabs [data-baseweb="tab-list"]{{gap:2px;background:{TBG};border-radius:10px;padding:4px;border:1px solid {BD};margin-bottom:1.5rem}}
.stTabs [data-baseweb="tab"]{{font-family:'Source Sans 3',sans-serif!important;font-weight:500;font-size:.84rem;padding:.5rem .95rem;border-radius:8px;color:{T4};background:transparent;border:none;transition:all .25s}}
.stTabs [aria-selected="true"]{{background:{TSBG}!important;color:{TSTX}!important;font-weight:600;box-shadow:0 1px 6px rgba(0,0,0,.08)}}

/* Hero */
.hero{{padding:2rem 1.8rem;background:{HBG};border:1px solid {BD};border-radius:16px;margin-bottom:1.2rem}}
.hero-name{{font-size:2.4rem;font-weight:800;color:{TX};line-height:1.15;letter-spacing:-.4px}}
.hero-sub{{font-family:'DM Mono',monospace;font-size:.84rem;color:{AC};margin:.15rem 0 .6rem}}
.hero-bio{{font-size:.96rem;color:{T3};line-height:1.7;max-width:640px}}
.pfp{{width:130px;height:130px;border-radius:50%;object-fit:cover;border:3px solid {AC};box-shadow:0 0 20px {GL};transition:all .35s}}
.pfp:hover{{transform:scale(1.06);box-shadow:0 0 30px {GL}}}

/* Stats */
.srow{{display:flex;gap:.65rem;margin:1rem 0;flex-wrap:wrap}}
.scard{{flex:1;min-width:110px;background:{BG2};border:1px solid {BD};border-radius:12px;padding:.8rem;text-align:center;transition:all .3s cubic-bezier(.34,1.56,.64,1)}}
.scard:hover{{border-color:{AC};transform:translateY(-4px) scale(1.03);box-shadow:0 8px 22px {GL}}}
.snum{{font-size:1.6rem;font-weight:700;color:{AC};line-height:1.2}}
.slbl{{font-size:.67rem;color:{T4};text-transform:uppercase;letter-spacing:.7px;margin-top:.05rem}}

/* Section divider */
.sdiv{{width:100%;height:1px;background:{BD};margin:2.5rem 0 1.5rem}}
.stitle{{font-size:1.4rem;font-weight:700;color:{TX};margin:0 0 .3rem;letter-spacing:-.2px}}
.ssub{{color:{T4};font-size:.86rem;margin-bottom:1.2rem}}

/* Card */
.tc{{background:{CD};border:1px solid {BD};border-radius:14px;padding:1.2rem 1.2rem 1.2rem 1.5rem;margin-bottom:.8rem;border-left:3px solid {AC};transition:all .3s cubic-bezier(.25,.46,.45,.94)}}
.tc:hover{{box-shadow:0 8px 22px rgba(59,130,246,.07);transform:translateY(-2px)}}
.th_{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.35rem}}
.tr{{font-size:1rem;font-weight:600;color:{TX}}}
.tr a{{color:{TX};text-decoration:none;border-bottom:1px dashed {AC};transition:color .2s}}
.tr a:hover{{color:{AC}}}
.tco{{font-size:.84rem;color:{AC};font-weight:500}}
.tdt{{font-family:'DM Mono',monospace;font-size:.71rem;color:{T4};background:{BG2};padding:.18rem .5rem;border-radius:6px;border:1px solid {BD};white-space:nowrap}}
.td{{color:{T3};font-size:.84rem;line-height:1.6}}
.td ul{{margin:.2rem 0;padding-left:1rem}}.td li{{margin-bottom:.1rem;color:{T3}}}
.tsk{{display:flex;flex-wrap:wrap;gap:.28rem;margin-top:.5rem}}
.sk{{font-family:'DM Mono',monospace;font-size:.66rem;color:{AC};background:{TAGBG};border:1px solid {TAGBD};padding:.15rem .45rem;border-radius:5px;transition:all .2s}}
.sk:hover{{transform:translateY(-1px);box-shadow:0 2px 6px rgba(59,130,246,.08)}}

/* Edu */
.ec{{background:{CD};border:1px solid {BD};border-radius:14px;padding:1.2rem;margin-bottom:.8rem;transition:all .3s cubic-bezier(.25,.46,.45,.94)}}
.ec:hover{{box-shadow:0 8px 22px rgba(79,70,229,.06);transform:translateY(-2px)}}
.edeg{{font-size:1.08rem;font-weight:700;color:{A2}}}.esch{{font-size:.88rem;color:{T2};font-weight:500}}
.edet{{color:{T3};font-size:.83rem;line-height:1.6;margin-top:.35rem}}

/* Award */
.aw{{background:{AMBBG};border:1px solid {AMBBD};border-radius:12px;padding:.95rem 1.1rem;margin-bottom:.6rem;transition:all .3s cubic-bezier(.34,1.56,.64,1)}}
.aw:hover{{transform:translateY(-2px);box-shadow:0 5px 16px rgba(245,158,11,.08)}}
.awt{{font-size:.88rem;font-weight:600;color:{AMB}}}.awd{{color:{T3};font-size:.8rem;margin-top:.1rem}}

/* Pub */
.pc{{background:{CD};border:1px solid {BD};border-left:3px solid {A3};border-radius:12px;padding:1rem 1.1rem;margin-bottom:.6rem;transition:all .3s}}
.pc:hover{{box-shadow:0 5px 16px rgba(16,185,129,.07);transform:translateY(-2px)}}
.pt{{font-weight:600;color:{TX};font-size:.9rem}}.pt a{{color:{TX};text-decoration:none;border-bottom:1px dashed {A3}}}.pt a:hover{{color:{A3}}}
.pv{{font-size:.76rem;color:{A3};margin-top:.08rem}}.pl{{font-family:'DM Mono',monospace;font-size:.7rem;margin-top:.15rem}}.pl a{{color:{AC};text-decoration:none}}.pl a:hover{{text-decoration:underline}}
.pd{{color:{T4};font-size:.8rem;margin-top:.2rem;line-height:1.5}}

/* Contact */
.ci{{display:flex;align-items:center;gap:.55rem;padding:.55rem .85rem;background:{BG2};border:1px solid {BD};border-radius:10px;margin-bottom:.28rem;font-size:.84rem;color:{T3};transition:all .2s}}
.ci:hover{{border-color:{AC};transform:translateX(3px)}}.ci a{{color:{AC};text-decoration:none}}

/* Project */
.ps{{background:{BG2};border:1px solid {BD};border-radius:14px;padding:1.2rem;margin-bottom:.9rem;transition:box-shadow .3s}}
.ps:hover{{box-shadow:0 4px 14px rgba(59,130,246,.05)}}
.pst{{font-size:1.02rem;font-weight:700;color:{TX};margin-bottom:.5rem}}

/* Doc btn */
.db{{display:inline-flex;align-items:center;gap:.35rem;padding:.35rem .8rem;border-radius:8px;font-size:.8rem;font-weight:500;background:{TAGBG};border:1px solid {TAGBD};color:{AC};text-decoration:none;transition:all .25s;margin-right:.4rem;margin-top:.35rem}}
.db:hover{{background:{AC};color:#fff;border-color:{AC};transform:translateY(-1px)}}

/* Misc */
.stImage>img{{border-radius:10px}}
.stButton>button{{border-radius:8px!important;font-family:'Source Sans 3',sans-serif!important;font-weight:600!important;font-size:.86rem!important;padding:.32rem .95rem!important;background:{CD}!important;color:{T3}!important;border:1px solid {BD}!important;transition:all .25s cubic-bezier(.34,1.56,.64,1)!important}}
.stButton>button:hover{{border-color:{AC}!important;color:{AC}!important;transform:translateY(-2px)!important;box-shadow:0 4px 12px {GL}!important}}
hr{{border-color:{BD}!important}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TABS:  About Me (merged)  |  Academics  |  Certificates  |  Projects & Videos  |  Contact
# ══════════════════════════════════════════════════════════════════
tabs = st.tabs(["About Me", "Academics", "Certificates", "Projects & Videos", "Contact"])


# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 1 — ABOUT ME  (Home + Experience + Education + Products) ║
# ╚══════════════════════════════════════════════════════════════╝
with tabs[0]:

    # ───────── HERO ─────────
    cp, ci = st.columns([1, 3.5], gap="large")
    with cp:
        pf=imgs("profile")
        if pf:
            st.markdown(f'<img src="data:{mimetype(pf[0])};base64,{b64img(pf[0])}" class="pfp ap">', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ap" style="width:130px;height:130px;border-radius:50%;background:{AC};display:flex;align-items:center;justify-content:center;font-size:2.4rem;color:#fff;font-weight:700;border:3px solid {AC};box-shadow:0 0 20px {GL}">SH</div>', unsafe_allow_html=True)
            st.caption("Add photo → `assets/profile/`")
    with ci:
        st.markdown(f"""
        <div class="hero au">
            <div class="hero-name">Shashank Hegde</div>
            <div class="hero-sub">Embedded-ML Electronics Engineer · Lead Product R&D</div>
            <div class="hero-bio">Lead R&D Engineer and TUM graduate with 5+ years across Robert Bosch and high-growth startups. Owns embedded and ML-based healthcare systems end-to-end — from firmware and edge ML to cloud inference pipelines — with production software active in 30,000+ clinical consultations worldwide.</div>
        </div>
        """, unsafe_allow_html=True)

    # Stats
    st.markdown(f"""
    <div class="srow au d2">
        <div class="scard ap d1"><div class="snum">5+</div><div class="slbl">Years Experience</div></div>
        <div class="scard ap d2"><div class="snum">5+</div><div class="slbl">Product Deployments</div></div>
        <div class="scard ap d3"><div class="snum">3</div><div class="slbl">Publications</div></div>
        <div class="scard ap d4"><div class="snum">5</div><div class="slbl">Awards</div></div>
        <div class="scard ap d5"><div class="snum">2</div><div class="slbl">Degrees</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Highlights
    st.markdown(f'<div class="stitle af d3">Highlights</div>', unsafe_allow_html=True)
    slideshow("achievements", key="hach")
    st.markdown(f"""
    <div class="aw al d1"><div class="awt">Best Presentation Award — IEEE ICCE 2024, Las Vegas</div><div class="awd">IoT-enabled automatic gear shifting for E-bikes. Best among 50+ papers.</div></div>
    <div class="aw al d2"><div class="awt">Bosch Future Mobility Challenge — Semi-Finalist, Cluj Romania</div><div class="awd">Represented Germany among 100+ teams. Led sensor fusion on NVIDIA Jetson Xavier.</div></div>
    <div class="aw al d3"><div class="awt">Bravo Award — Robert Bosch</div><div class="awd">Recognized for SecOC tool delivery in ECU security.</div></div>
    """, unsafe_allow_html=True)

    # Skills
    st.markdown(f'<div class="stitle af d4">Core skills</div>', unsafe_allow_html=True)
    sk_data={"Embedded & IoT":["Edge ML","Arduino","Raspberry Pi","STM32","Firmware","IoT Security","CAN","V2V"],"AI / ML":["ASR","NLP","RAG","Model Compression","TensorRT","GPU Accel.","Computer Vision"],"Programming":["Python","C","C++","CAPL","ROS"],"Platforms":["Linux/RHEL","CUDA","NVIDIA Jetson","Docker","Git"]}
    c1,c2=st.columns(2)
    for i,(cat,sk) in enumerate(sk_data.items()):
        with c1 if i%2==0 else c2:
            st.markdown(f'<p style="font-weight:600;color:{TX};margin-bottom:.2rem;font-size:.92rem;">{cat}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="tsk af d{i+1}">'+"".join(f'<span class="sk">{s}</span>' for s in sk)+'</div>', unsafe_allow_html=True)
            st.markdown("")

    # ───────── DIVIDER: EXPERIENCE ─────────
    st.markdown(f'<div class="sdiv"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stitle au">Work Experience</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ssub">From embedded systems at Bosch to leading R&D at a healthtech startup.</div>', unsafe_allow_html=True)

    exps=[
        ("Lead R&D Product Engineer","O-Health · Bangalore & Boston","Jan 2025 – Present",
         ["Improved ASR accuracy — reduced WER by 40% for Standard Hindi on edge models","Reduced inference latency by 50% via knowledge distillation, quantization, weight pruning","Built medical RAG pipeline with hallucination-free outputs via cross-LLM consensus","Optimized GPU inference on H200 clusters — CUDA, TensorRT, async multi-threading","Led end-to-end health-band development with MIT CSAIL"],
         ["ASR","NLP","RAG","Linux","Edge ML","GPU Accel.","Health-tech"]),
        ("Werkstudent Embedded IoT Engineer","Würth Elektronik eiSoS · Munich","May 2022 – Jan 2025",
         ["Optimized AT-command interfaces and multi-threaded buffer management","Designed low-level LTE-M / NB-IoT firmware drivers with robust state machines","Ensured reliable high-frequency IoT data transmission under variable conditions"],
         ["LTE-M","NB-IoT","Firmware","Multithreading","ARM","Edge ML"]),
        ("Embedded Software Engineer","Robert Bosch · Bangalore","Jan 2021 – Sep 2021",
         ["Implemented ECU security algorithms per customer specifications","Developed SecOC tool for secure data transmission between ECUs over CAN bus"],
         ["ECU Security","CAN","CAPL","CANoe","XCP"]),
        ("Embedded Software Developer","AmberFlux EdgeAI · Hyderabad","Nov 2020 – Jan 2021",
         ["Integrated sensors on RPi, STM32 and Xtensa for real-time positioning","Optimized embedded AI models for edge devices"],
         ["Raspberry Pi","STM32","Real-time","Embedded AI"]),
        ("Product Verification Intern","Tejas Networks · Bangalore","Jan 2020 – Jul 2020",
         ["Automated Layer-2 product verification for optical communication","Developed test-automation scripts in Python and TCL"],
         ["Layer-2","Test Automation","Python","TCL"]),
    ]
    for idx,(role,co,dt,bul,sk) in enumerate(exps):
        bl="".join(f"<li>{b}</li>" for b in bul)
        tg="".join(f'<span class="sk">{s}</span>' for s in sk)
        st.markdown(f'<div class="tc au d{min(idx%3+1,3)}"><div class="th_"><div><div class="tr">{role}</div><div class="tco">{co}</div></div><span class="tdt">{dt}</span></div><div class="td"><ul>{bl}</ul></div><div class="tsk">{tg}</div></div>',unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.95rem;margin:1rem 0 .4rem;">Workplace photos</p>', unsafe_allow_html=True)
    slideshow("experience", key="exs")

    # ───────── DIVIDER: EDUCATION ─────────
    st.markdown(f'<div class="sdiv"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stitle au">Education</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ec au d1"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><div class="edeg">M.Sc. Communication Engineering</div><div class="esch">Technical University of Munich (TUM) — Germany</div></div><span class="tdt">Oct 2021 – Oct 2024</span></div>
    <div class="edet"><strong style="color:{T2}">Grade:</strong> 2.1 · <strong style="color:{T2}">Thesis:</strong> Lane-Free Traffic Control on Connected Mini Automated Vehicles <em>(1.0)</em><br><strong style="color:{T2}">Focus:</strong> Embedded Systems & Security, IoT, SoC, Data Networks · <strong style="color:{T2}">Extra:</strong> 6G Business Modeling Lab (TUM CDTM)</div></div>
    <div class="ec au d2"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><div class="edeg">B.E. Electronics & Communication</div><div class="esch">National Institute of Engineering — Mysore, India</div></div><span class="tdt">Aug 2016 – Oct 2020</span></div>
    <div class="edet"><strong style="color:{T2}">Grade:</strong> 1.6 · <strong style="color:{T2}">Thesis:</strong> Data Analysis from Sensors via DSP and WSN <em>(1.0)</em><br><strong style="color:{T2}">Focus:</strong> Digital Electronics, Embedded Systems, Network Security, C++</div></div>
    """, unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.95rem;margin:1rem 0 .4rem;">Online courses</p>', unsafe_allow_html=True)
    for c in ["IoT Wireless & Cloud Computing — Yonsei University (Coursera)","Embedded Hardware & Operating Systems — EIT Digital (Coursera)","Computer Networks & IP Protocol — IIT Kharagpur (NPTEL)","Python for Computer Vision with OpenCV & Deep Learning (Udemy)"]:
        st.markdown(f'<div class="ci af">{c}</div>',unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.95rem;margin:1rem 0 .4rem;">Degree certificates</p>', unsafe_allow_html=True)
    slideshow("education", key="eds")

    # ───────── DIVIDER: PRODUCTS ─────────
    st.markdown(f'<div class="sdiv"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stitle au">Products & Builds</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ssub">Hardware, software, and everything in between.</div>', unsafe_allow_html=True)

    prods=[
        ("Health Band — O-Health","Production-grade wearable with custom sensors, BLE, and cloud ML. 30,000+ clinical consultations.",["Hardware","Firmware","ML","BLE","Healthcare"],None),
        ("ASR Engine for Hindi","Edge-optimized ASR. 40% WER improvement, 50% latency reduction.",["ASR","Edge ML","Compression","NLP"],None),
        ("Medical RAG Pipeline","Hallucination-free medical info extraction via cross-LLM consensus.",["RAG","LLM","Healthcare","NLP"],None),
        ("Retrofittable E-Bike Auto Shifter","IoT-enabled rear-derailleur shifting with mode-based transmission. IEEE ICCE 2024 Best Presentation.",["IoT","Mechatronics","Sensors","IEEE"],"https://ieeexplore.ieee.org/document/10444469"),
        ("SecOC Tool — Bosch","Automated ECU data encryption for CAN bus.",["Automotive","Security","CAN","CAPL"],None),
        ("Autonomous Mini Vehicle — TUM","Lane-free traffic control with V2V and sensor fusion.",["Autonomous","V2V","ROS","Sensor Fusion"],None),
    ]
    for i in range(0,len(prods),2):
        cols=st.columns(2)
        for j in range(2):
            if i+j<len(prods):
                nm,desc,tags,lnk=prods[i+j]
                tg="".join(f'<span class="sk">{t}</span>' for t in tags)
                thtml=f'<a href="{lnk}" target="_blank">{nm}</a>' if lnk else nm
                lhtml=f'<div class="pl"><a href="{lnk}" target="_blank">📄 View paper</a></div>' if lnk else ""
                with cols[j]:
                    st.markdown(f'<div class="tc ap d{j+1}" style="min-height:145px"><div class="tr">{thtml}</div><div class="td" style="margin:.3rem 0">{desc}</div>{lhtml}<div class="tsk">{tg}</div></div>',unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.95rem;margin:1rem 0 .4rem;">Product gallery</p>', unsafe_allow_html=True)
    slideshow("products", key="prs")


# ╔══════════════════════════════════╗
# ║  TAB 2 — ACADEMICS               ║
# ╚══════════════════════════════════╝
with tabs[1]:
    st.markdown(f'<div class="stitle au">Academic Work</div>', unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;font-size:1.05rem;color:{TX};margin:1.2rem 0 .5rem">Research projects</p>', unsafe_allow_html=True)

    # Lane-Free
    st.markdown(f"""
    <div class="tc au d1"><div class="th_"><div>
        <div class="tr"><a href="#lane-free-docs">Lane-Free Traffic Control for Connected Mini-Automated Vehicles</a></div>
        <div class="tco">Master's Thesis — TU München</div>
    </div><span class="tdt">Feb – Oct 2024</span></div>
    <div class="td">Designed and implemented lane-free control strategies for connected autonomous vehicles using V2V communication.</div>
    <div class="tsk"><span class="sk">Vehicle Control</span><span class="sk">V2V</span><span class="sk">Sensor Fusion</span><span class="sk">Autonomous</span></div>
    <div><a class="db" href="#lane-free-docs">📄 Thesis PDF</a><a class="db" href="#lane-free-docs">📊 Presentation</a></div></div>
    """, unsafe_allow_html=True)

    # Cellular IoT
    st.markdown(f"""
    <div class="tc au d2"><div class="th_"><div>
        <div class="tr"><a href="#cellular-iot-docs">Cellular IoT Cloud Connectivity</a></div>
        <div class="tco">Würth Elektronik eiSoS — TU München</div>
    </div><span class="tdt">2022 – 2024</span></div>
    <div class="td">Designed a plug-and-play system enabling seamless communication between the sensor module and cellular Adrastea-I, transmitting data to the cloud in secure mode via digital certificates in both LTE-CAT-M and NB-IoT modes with PSM power saving.</div>
    <div class="tsk"><span class="sk">LTE-M</span><span class="sk">NB-IoT</span><span class="sk">PSM</span><span class="sk">Cloud IoT</span><span class="sk">Digital Certificates</span><span class="sk">Adrastea-I</span></div>
    <div><a class="db" href="#cellular-iot-docs">📄 PDF</a></div></div>
    """, unsafe_allow_html=True)

    # Publications
    st.markdown(f'<p style="font-weight:600;font-size:1.05rem;color:{TX};margin:1.5rem 0 .5rem">Publications</p>', unsafe_allow_html=True)
    for t,v,u,d in [
        ("Retrofittable Automatic Shifter of Rear-Derailleur with Mode-Based Transmission and IoT","IEEE ICCE 2024","https://ieeexplore.ieee.org/document/10444469","Retrofittable shifting for E-bikes with IoT and adaptive riding modes."),
        ("Remote Monitoring Robot with Voice Control and Image Analysis","Scopus — IJAST","http://sersc.org/journals/index.php/IJAST/article/view/21218","Surveillance robot with image processing, voice control, and MQTT."),
        ("Data Extraction with Signal Comparison for Forest Logging Prevention","IJERT · NCCDS 2020","https://www.ijert.org/data-extraction-with-signal-comparison-for-forest-logging-prevention","WSN for illegal logging detection via FFT-based signal processing."),
    ]:
        st.markdown(f'<div class="pc af"><div class="pt"><a href="{u}" target="_blank">{t}</a></div><div class="pv">{v}</div><div class="pl"><a href="{u}" target="_blank">📄 {u}</a></div><div class="pd">{d}</div></div>',unsafe_allow_html=True)

    # Conferences
    st.markdown(f'<p style="font-weight:600;font-size:1.05rem;color:{TX};margin:1.5rem 0 .5rem">Conferences</p>', unsafe_allow_html=True)
    for n,l,note in [("IEEE ICCE 2024","Las Vegas","Best Presentation"),("Bosch Future Mobility 2023","Cluj, Romania","Semi-finalist"),("ICICEE 2020","Tumkur","Best Paper"),("NCCDS 2020","Mysuru","Paper Presentation"),("ANKURA'19","Mysore","National Paper Presentation"),("TI Innovation Challenge 2019","India","Design Contest")]:
        st.markdown(f'<div class="ci af"><strong>{n}</strong>&nbsp;— {l} &nbsp;<em>({note})</em></div>',unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.95rem;margin:1rem 0 .4rem;">Academic gallery</p>', unsafe_allow_html=True)
    slideshow("academics", key="acs")

    # ── Documents ──
    st.markdown("---")
    st.markdown(f'<div id="lane-free-docs"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stitle au">📄 Lane-Free Traffic Control — Documents</div>', unsafe_allow_html=True)
    dc1,dc2=st.columns(2)
    with dc1:
        st.markdown(f'<p style="font-weight:600;color:{TX};">Thesis PDF</p>', unsafe_allow_html=True)
        embed_doc("lane_free_thesis.pdf","Thesis")
    with dc2:
        st.markdown(f'<p style="font-weight:600;color:{TX};">Presentation</p>', unsafe_allow_html=True)
        embed_doc("lane_free_presentation.pdf","Presentation")

    st.markdown("---")
    st.markdown(f'<div id="cellular-iot-docs"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stitle au">📄 Cellular IoT Cloud Connectivity — Document</div>', unsafe_allow_html=True)
    embed_doc("cellular_iot.pdf","Cellular IoT")


# ╔══════════════════════════════════╗
# ║  TAB 3 — CERTIFICATES            ║
# ╚══════════════════════════════════╝
with tabs[2]:
    st.markdown(f'<div class="stitle au">Certificates & Awards</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ssub">Filtered by category.</div>', unsafe_allow_html=True)

    certs=[
        ("Best Session Presentation — IEEE ICCE 2024","Las Vegas · Jan 2024","Award",AMB),
        ("Certificate of Participation — IEEE ICCE 2024","Retrofittable Auto Shifter","Conference",AC),
        ("Best Paper — ICICEE 2020","Remote Monitoring · Tumkur","Award",AMB),
        ("Bravo Award — Robert Bosch","SecOC tool · Aug 2021","Corporate",A2),
        ("Bosch Future Mobility Challenge","TUMAVERICK — Semi-finalist · Cluj 2023","Competition","#fb7185" if DARK else "#e11d48"),
        ("Tejas Networks Internship","Product verification · 2020","Internship",A3),
        ("NCCDS 2020","Forest Logging Prevention","Conference",AC),
        ("NIE IEEE Biblus — ANKURA'19","National Paper Presentation","Conference",AC),
        ("NIE Summer of Code 5.0","Hardware Track · 2018","Workshop","#22d3ee" if DARK else "#0891b2"),
        ("Adroit'18 Appreciation","IEEE NIE volunteering · Oct 2018","Volunteering","#a78bfa" if DARK else "#7c3aed"),
        ("Texas Instruments Innovation 2019","DST & TI Design Contest","Competition","#fb7185" if DARK else "#e11d48"),
    ]
    cats=sorted(set(c[2] for c in certs))
    sel=st.multiselect("Filter",cats,default=cats,key="cf")
    for idx,(ti,de,ca,co) in enumerate(certs):
        if ca in sel:
            st.markdown(f'<div class="tc al d{min(idx%3+1,3)}" style="border-left-color:{co}"><div class="th_"><div><div class="tr">{ti}</div><div class="td">{de}</div></div><span class="tdt">{ca}</span></div></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div class="stitle">Certificate scans</div>', unsafe_allow_html=True)
    slideshow("certificates", key="cs")


# ╔══════════════════════════════════╗
# ║  TAB 4 — PROJECTS & VIDEOS       ║
# ╚══════════════════════════════════╝
with tabs[3]:
    st.markdown(f'<div class="stitle au">Projects & Videos</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ssub">Demo videos, project walkthroughs, and builds.</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="ps au d1"><div class="pst">🌲 Illegal Forest Logging Prevention — STM32 Wireless Nodes</div><div class="td">Bachelor thesis — wireless sensor network for detecting illegal logging via FFT-based audio analysis on STM32 microcontrollers.</div><div class="pl" style="margin-top:.4rem"><a href="https://www.ijert.org/data-extraction-with-signal-comparison-for-forest-logging-prevention" target="_blank">📄 Read the paper (IJERT)</a></div></div>',unsafe_allow_html=True)
    v1,v2=st.columns(2)
    with v1:
        st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.92rem;">Project demo</p>',unsafe_allow_html=True)
        yt("https://www.youtube.com/watch?v=g9tRZPRJfYs")
    with v2:
        st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.92rem;">Cooja simulator</p>',unsafe_allow_html=True)
        yt("https://www.youtube.com/watch?v=wczmB9WR8O4")

    st.markdown("---")
    st.markdown(f'<div class="ps au d2"><div class="pst">🐛 Pest Detection Using ML on Edge Devices</div><div class="td">Machine learning pest detection on edge devices for real-time agricultural monitoring.</div><div class="pl" style="margin-top:.4rem"><a href="https://resources.mouser.com/explore-all/pest-detection-using-machine-learning-on-edge-devices" target="_blank">📄 View on Mouser</a></div></div>',unsafe_allow_html=True)
    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.92rem;margin:.5rem 0 .3rem">Project photos</p>',unsafe_allow_html=True)
    slideshow("projects", key="pjs")

    st.markdown("---")
    st.markdown(f'<div class="ps au d3"><div class="pst">🤖 TUM Robotics Club</div><div class="td">Activities, competitions, and collaborative engineering.</div></div>',unsafe_allow_html=True)
    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.92rem;margin:.3rem 0">Photos</p>',unsafe_allow_html=True)
    slideshow("robotics_club", key="rbs")

    robotics_club_videos = [
        # ("Title", "https://www.youtube.com/watch?v=XXXXX"),
    ]
    if robotics_club_videos:
        st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.92rem;margin:.8rem 0 .4rem">Videos</p>',unsafe_allow_html=True)
        for ti,ur in robotics_club_videos:
            st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.88rem">{ti}</p>',unsafe_allow_html=True)
            yt(ur)
    else:
        st.markdown(f'<div style="background:{BG2};border:1px dashed {BD};border-radius:10px;padding:.7rem;margin-top:.5rem"><p style="color:{T4};font-size:.8rem;margin:0">📹 Add YouTube links to <code>robotics_club_videos</code> in <code>app.py</code>.</p></div>',unsafe_allow_html=True)


# ╔══════════════════════════════════╗
# ║  TAB 5 — CONTACT                  ║
# ╚══════════════════════════════════╝
with tabs[4]:
    st.markdown(f'<div class="stitle au">Get in touch</div>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="ci al d1">📞 &nbsp;+49 176 71095238</div>
        <div class="ci al d2">📧 &nbsp;<a href="mailto:shashankv099@gmail.com">shashankv099@gmail.com</a></div>
        <div class="ci al d3">💼 &nbsp;<a href="https://www.linkedin.com/in/shashank-hegde98" target="_blank">linkedin.com/in/shashank-hegde98</a></div>
        <div class="ci al d4">🌍 &nbsp;Bangalore, India & Munich, Germany</div>
        <div class="ci al d5">🇺🇸 &nbsp;Nationality: United States of America</div>
        """, unsafe_allow_html=True)
        st.markdown("")
        st.markdown(f'<p style="font-weight:600;color:{TX}">Languages</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="ci af">English — C2 · German — A2 (learning B1)</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="hero ap" style="padding:1.3rem"><div style="font-size:1rem;font-weight:600;color:{TX};margin-bottom:.3rem">Open to opportunities</div><div class="hero-bio" style="font-size:.87rem">Interested in Embedded ML, Edge AI, Healthcare Technology, and IoT. Reach out via email or LinkedIn.</div></div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f'<p style="text-align:center;color:{T4};font-size:.78rem">Shashank Hegde · Embedded-ML Electronics Engineer · © 2025</p>', unsafe_allow_html=True)
