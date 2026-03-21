import streamlit as st
from pathlib import Path
import base64

st.set_page_config(page_title="Shashank Hegde | Portfolio", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

if "dark_mode" not in st.session_state: st.session_state.dark_mode = True
hc = st.columns([10, 1])
with hc[1]:
    if st.button("☀️" if st.session_state.dark_mode else "🌙", key="tt", help="Toggle theme"):
        st.session_state.dark_mode = not st.session_state.dark_mode; st.rerun()
DARK = st.session_state.dark_mode

A = Path("assets")
for d in ["profile","certificates","experience","education","products","academics","projects","robotics_club","docs"]:
    (A/d).mkdir(parents=True, exist_ok=True)

def pdf_to_png_b64(filepath, page=0, dpi=150):
    try:
        import fitz
        doc = fitz.open(str(filepath))
        total = len(doc)
        if page >= total: page = 0
        pix = doc[page].get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        b = pix.tobytes("png")
        doc.close()
        return base64.b64encode(b).decode(), total
    except:
        try:
            import fitz
            doc = fitz.Document(str(filepath))
            total = doc.page_count
            pix = doc.load_page(min(page, total-1)).get_pixmap(dpi=dpi)
            b = pix.tobytes("png")
            doc.close()
            return base64.b64encode(b).decode(), total
        except:
            return None, 0

def b64(path):
    with open(path,"rb") as f: return base64.b64encode(f.read()).decode()

def mime(path):
    ext = Path(path).suffix.lower().replace(".","")
    return {"jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png","webp":"image/webp"}.get(ext,"image/png")

def render_file(filepath):
    p = Path(filepath); ext = p.suffix.lower()
    if ext in {".jpg",".jpeg",".png",".webp"}:
        st.markdown(f'<div style="max-width:720px;margin:0 auto;border-radius:12px;overflow:hidden;border:1px solid {BD}"><img src="data:{mime(filepath)};base64,{b64(filepath)}" style="width:100%;display:block"/></div>', unsafe_allow_html=True)
    elif ext == ".pdf":
        img_b64, _ = pdf_to_png_b64(filepath)
        if img_b64:
            st.markdown(f'<div style="max-width:720px;margin:0 auto;border-radius:12px;overflow:hidden;border:1px solid {BD}"><img src="data:image/png;base64,{img_b64}" style="width:100%;display:block"/></div>', unsafe_allow_html=True)
        else:
            with open(filepath,"rb") as f: st.download_button(f"⬇ {p.name}",f.read(),file_name=p.name,mime="application/pdf")
    elif ext in {".mp4",".mov",".webm"}:
        st.video(filepath)

def get_files(cat):
    d=A/cat
    return [str(p) for p in sorted(d.iterdir()) if p.suffix.lower() in {".jpg",".jpeg",".png",".webp",".pdf"}] if d.exists() else []

def get_media(cat):
    d=A/cat
    return [str(p) for p in sorted(d.iterdir()) if p.suffix.lower() in {".jpg",".jpeg",".png",".webp",".pdf",".mp4",".mov",".webm"}] if d.exists() else []

def slideshow(cat, key, use_media=False):
    files = get_media(cat) if use_media else get_files(cat)
    if not files: st.info(f"No files yet — add to `assets/{cat}/` and redeploy."); return
    k=f"s_{key}"
    if k not in st.session_state: st.session_state[k]=0
    t=len(files); i=st.session_state[k]%t
    render_file(files[i])
    st.markdown(f'<p style="text-align:center;color:{T4};font-size:.82rem;margin:4px 0 2px">{Path(files[i]).stem.replace("_"," ").replace("-"," ")} · {i+1}/{t}</p>',unsafe_allow_html=True)
    _,bp,_,bn,_=st.columns([3,1.2,2,1.2,3])
    with bp:
        if st.button("← Prev",key=f"{key}_p",use_container_width=True): st.session_state[k]=(i-1)%t; st.rerun()
    with bn:
        if st.button("Next →",key=f"{key}_n",use_container_width=True): st.session_state[k]=(i+1)%t; st.rerun()

def render_doc_readable(fname, label="Document"):
    """Render doc as paginated images — READ ONLY, no download."""
    p = A/"docs"/fname
    if not p.exists(): st.info(f"📄 Place `{fname}` in `assets/docs/` and redeploy."); return
    if p.suffix.lower() != ".pdf": st.info(f"Unsupported format: {p.suffix}"); return
    pk=f"doc_{fname}"
    if pk not in st.session_state: st.session_state[pk]=0
    img_b64, total = pdf_to_png_b64(str(p), st.session_state[pk])
    if img_b64 and total > 0:
        pg = st.session_state[pk] % total
        st.markdown(f'<div style="border-radius:12px;overflow:hidden;border:1px solid {BD}"><img src="data:image/png;base64,{img_b64}" style="width:100%;display:block"/></div>',unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center;color:{T4};font-size:.8rem;margin:4px 0">Page {pg+1} / {total}</p>',unsafe_allow_html=True)
        if total > 1:
            _,b1,_,b2,_=st.columns([3,1.2,2,1.2,3])
            with b1:
                if st.button("← Prev",key=f"d{fname}_p",use_container_width=True): st.session_state[pk]=(pg-1)%total; st.rerun()
            with b2:
                if st.button("Next →",key=f"d{fname}_n",use_container_width=True): st.session_state[pk]=(pg+1)%total; st.rerun()
    else:
        st.warning(f"Could not render `{fname}`. Ensure PyMuPDF is installed.")

def yt(url, h=330):
    vid=""
    if "watch?v=" in url: vid=url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url: vid=url.split("youtu.be/")[1].split("?")[0]
    if vid: st.markdown(f'<iframe width="100%" height="{h}" src="https://www.youtube.com/embed/{vid}" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen style="border-radius:10px;border:1px solid {BD}"></iframe>',unsafe_allow_html=True)

# ═══ THEME ═══
if DARK:
    BG="#0f172a";BG2="#1e293b";CD="#1e293b";TX="#f1f5f9";T2="#cbd5e1";T3="#94a3b8";T4="#64748b"
    BD="#334155";AC="#3b82f6";A2="#8b5cf6";A3="#10b981";AMB="#fbbf24";AMBBG="rgba(245,158,11,.1)";AMBBD="rgba(245,158,11,.3)"
    TBG="#1e293b";TSBG="#3b82f6";TSTX="#fff";HBG="linear-gradient(135deg,rgba(59,130,246,.08),rgba(139,92,246,.08))"
    TAGBG="rgba(59,130,246,.12)";TAGBD="rgba(59,130,246,.25)";GL="rgba(59,130,246,.2)";BARBG="#1e293b"
    TL_IMG="gantt_dark.png"; VTL_IMG="timeline_dark.png"
else:
    BG="#ffffff";BG2="#f8fafc";CD="#ffffff";TX="#0f172a";T2="#334155";T3="#475569";T4="#64748b"
    BD="#e2e8f0";AC="#2563eb";A2="#4f46e5";A3="#059669";AMB="#92400e";AMBBG="#fffbeb";AMBBD="#fde68a"
    TBG="#f1f5f9";TSBG="#ffffff";TSTX="#2563eb";HBG="linear-gradient(135deg,rgba(37,99,235,.04),rgba(79,70,229,.04))"
    TAGBG="#eff6ff";TAGBD="#dbeafe";GL="rgba(37,99,235,.12)";BARBG="#e2e8f0"
    TL_IMG="gantt_light.png"; VTL_IMG="timeline_light.png"

BAR_COLORS={1:"#94a3b8",2:"#64748b",3:"#0891b2",4:"#0d9488",5:"#059669",6:"#16a34a",7:"#2563eb",8:"#4f46e5",9:"#7c3aed",10:"#8b5cf6"}
def skill_bar(name,level):
    color=BAR_COLORS.get(level,AC)
    st.markdown(f'<div style="margin-bottom:.45rem"><div style="display:flex;justify-content:space-between;margin-bottom:2px"><span style="font-family:DM Mono,monospace;font-size:.72rem;color:{T3}">{name}</span><span style="font-family:DM Mono,monospace;font-size:.63rem;color:{T4}">{level}/10</span></div><div style="height:5px;background:{BARBG};border-radius:3px;overflow:hidden"><div style="width:{level*10}%;height:100%;background:{color};border-radius:3px;transition:width .6s cubic-bezier(.34,1.56,.64,1)"></div></div></div>',unsafe_allow_html=True)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');
@keyframes fadeInUp{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes slideL{{from{{opacity:0;transform:translateX(-18px)}}to{{opacity:1;transform:translateX(0)}}}}
@keyframes popIn{{from{{opacity:0;transform:scale(.92)}}to{{opacity:1;transform:scale(1)}}}}
.au{{animation:fadeInUp .5s ease-out both}}.af{{animation:fadeIn .4s ease-out both}}.al{{animation:slideL .45s ease-out both}}.ap{{animation:popIn .35s cubic-bezier(.34,1.56,.64,1) both}}
.d1{{animation-delay:.06s}}.d2{{animation-delay:.12s}}.d3{{animation-delay:.18s}}.d4{{animation-delay:.24s}}.d5{{animation-delay:.3s}}
.stApp{{font-family:'Source Sans 3',-apple-system,sans-serif!important;background:{BG}!important;color:{TX}!important}}
.block-container{{padding-top:.5rem!important;max-width:1100px!important}}
h1,h2,h3,h4,h5,h6{{font-family:'Source Sans 3',sans-serif!important;color:{TX}!important}}
p,li,span,div,label{{color:{T2}}}
#MainMenu,footer,header{{visibility:hidden}}.stDeployButton{{display:none}}
.stTabs [data-baseweb="tab-list"]{{gap:2px;background:{TBG};border-radius:10px;padding:4px;border:1px solid {BD};margin-bottom:1.5rem}}
.stTabs [data-baseweb="tab"]{{font-family:'Source Sans 3',sans-serif!important;font-weight:500;font-size:.84rem;padding:.5rem .95rem;border-radius:8px;color:{T4};background:transparent;border:none;transition:all .25s}}
.stTabs [aria-selected="true"]{{background:{TSBG}!important;color:{TSTX}!important;font-weight:600;box-shadow:0 1px 6px rgba(0,0,0,.08)}}
.hero{{padding:2rem 1.8rem;background:{HBG};border:1px solid {BD};border-radius:16px;margin-bottom:1.2rem;min-height:180px}}
.hero-name{{font-size:2.4rem;font-weight:800;color:{TX};line-height:1.15;letter-spacing:-.4px}}
.hero-sub{{font-family:'DM Mono',monospace;font-size:.84rem;color:{AC};margin:.15rem 0 .6rem}}
.hero-bio{{font-size:.96rem;color:{T3};line-height:1.7;max-width:640px}}
.pfp{{width:180px;height:180px;border-radius:50%;object-fit:cover;border:3px solid {AC};box-shadow:0 0 20px {GL};transition:all .35s}}.pfp:hover{{transform:scale(1.06);box-shadow:0 0 30px {GL}}}
.srow{{display:flex;gap:.65rem;margin:1rem 0;flex-wrap:wrap}}
.scard{{flex:1;min-width:110px;background:{BG2};border:1px solid {BD};border-radius:12px;padding:.8rem;text-align:center;transition:all .3s cubic-bezier(.34,1.56,.64,1)}}.scard:hover{{border-color:{AC};transform:translateY(-4px) scale(1.03);box-shadow:0 8px 22px {GL}}}
.snum{{font-size:1.6rem;font-weight:700;color:{AC};line-height:1.2}}.slbl{{font-size:.67rem;color:{T4};text-transform:uppercase;letter-spacing:.7px;margin-top:.05rem}}
.sdiv{{width:100%;height:1px;background:{BD};margin:2.5rem 0 1.5rem}}
.stitle{{font-size:1.4rem;font-weight:700;color:{TX};margin:0 0 .3rem;letter-spacing:-.2px}}.ssub{{color:{T4};font-size:.86rem;margin-bottom:1.2rem}}
.tc{{background:{CD};border:1px solid {BD};border-radius:14px;padding:1.2rem 1.2rem 1.2rem 1.5rem;margin-bottom:.8rem;border-left:3px solid {AC};transition:all .3s cubic-bezier(.25,.46,.45,.94)}}.tc:hover{{box-shadow:0 8px 22px rgba(59,130,246,.07);transform:translateY(-2px)}}
.th_{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.35rem}}
.tr{{font-size:1rem;font-weight:600;color:{TX}}}.tr a{{color:{TX};text-decoration:none;border-bottom:1px dashed {AC};transition:color .2s}}.tr a:hover{{color:{AC}}}
.tco{{font-size:.84rem;color:{AC};font-weight:500}}.tdt{{font-family:'DM Mono',monospace;font-size:.71rem;color:{T4};background:{BG2};padding:.18rem .5rem;border-radius:6px;border:1px solid {BD};white-space:nowrap}}
.td{{color:{T3};font-size:.84rem;line-height:1.6}}.td ul{{margin:.2rem 0;padding-left:1rem}}.td li{{margin-bottom:.1rem;color:{T3}}}
.tsk{{display:flex;flex-wrap:wrap;gap:.28rem;margin-top:.5rem}}.sk{{font-family:'DM Mono',monospace;font-size:.66rem;color:{AC};background:{TAGBG};border:1px solid {TAGBD};padding:.15rem .45rem;border-radius:5px;transition:all .2s}}.sk:hover{{transform:translateY(-1px);box-shadow:0 2px 6px rgba(59,130,246,.08)}}
.ec{{background:{CD};border:1px solid {BD};border-radius:14px;padding:1.2rem;margin-bottom:.8rem;transition:all .3s}}.ec:hover{{box-shadow:0 8px 22px rgba(79,70,229,.06);transform:translateY(-2px)}}
.edeg{{font-size:1.08rem;font-weight:700;color:{A2}}}.esch{{font-size:.88rem;color:{T2};font-weight:500}}.edet{{color:{T3};font-size:.83rem;line-height:1.6;margin-top:.35rem}}
.pc{{background:{CD};border:1px solid {BD};border-left:3px solid {A3};border-radius:12px;padding:1rem 1.1rem;margin-bottom:.6rem;transition:all .3s}}.pc:hover{{box-shadow:0 5px 16px rgba(16,185,129,.07);transform:translateY(-2px)}}
.pt{{font-weight:600;color:{TX};font-size:.9rem}}.pt a{{color:{TX};text-decoration:none;border-bottom:1px dashed {A3}}}.pt a:hover{{color:{A3}}}.pv{{font-size:.76rem;color:{A3};margin-top:.08rem}}.pd_{{color:{T4};font-size:.8rem;margin-top:.2rem;line-height:1.5}}
.ci{{display:flex;align-items:center;gap:.55rem;padding:.55rem .85rem;background:{BG2};border:1px solid {BD};border-radius:10px;margin-bottom:.28rem;font-size:.84rem;color:{T3};transition:all .2s}}.ci:hover{{border-color:{AC};transform:translateX(3px)}}.ci a{{color:{AC};text-decoration:none}}
.ps{{background:{BG2};border:1px solid {BD};border-radius:14px;padding:1.2rem;margin-bottom:.9rem;transition:box-shadow .3s}}.ps:hover{{box-shadow:0 4px 14px rgba(59,130,246,.05)}}.pst{{font-size:1.02rem;font-weight:700;color:{TX};margin-bottom:.5rem}}
.db{{display:inline-flex;align-items:center;gap:.35rem;padding:.35rem .8rem;border-radius:8px;font-size:.8rem;font-weight:500;background:{TAGBG};border:1px solid {TAGBD};color:{AC};text-decoration:none;transition:all .25s;margin-right:.4rem;margin-top:.35rem}}.db:hover{{background:{AC};color:#fff;border-color:{AC};transform:translateY(-1px)}}
.stImage>img{{border-radius:10px}}
.stButton>button{{border-radius:8px!important;font-family:'Source Sans 3',sans-serif!important;font-weight:600!important;font-size:.86rem!important;padding:.32rem .95rem!important;background:{CD}!important;color:{T3}!important;border:1px solid {BD}!important;transition:all .25s cubic-bezier(.34,1.56,.64,1)!important}}.stButton>button:hover{{border-color:{AC}!important;color:{AC}!important;transform:translateY(-2px)!important;box-shadow:0 4px 12px {GL}!important}}
hr{{border-color:{BD}!important}}
</style>
""",unsafe_allow_html=True)

tabs = st.tabs(["About Me","Academics","Conferences & Awards","Projects & Videos","Contact"])

# ══ ABOUT ME ══
with tabs[0]:
    cp,ci=st.columns([1.2,3.2],gap="large")
    with cp:
        pf=[str(p) for p in sorted((A/"profile").iterdir()) if p.suffix.lower() in {".jpg",".jpeg",".png",".webp"}]
        if pf: st.markdown(f'<img src="data:{mime(pf[0])};base64,{b64(pf[0])}" class="pfp ap">',unsafe_allow_html=True)
        else: st.markdown(f'<div class="ap" style="width:180px;height:180px;border-radius:50%;background:{AC};display:flex;align-items:center;justify-content:center;font-size:3rem;color:#fff;font-weight:700;border:3px solid {AC};box-shadow:0 0 20px {GL}">SH</div>',unsafe_allow_html=True); st.caption("Add photo → `assets/profile/`")
    with ci:
        st.markdown(f'<div class="hero au"><div class="hero-name">Shashank Hegde</div><div class="hero-sub">Embedded-ML Electronics Engineer · Lead Product R&D</div><div class="hero-bio">Lead R&D Engineer and TUM graduate with 5+ years across Robert Bosch and high-growth startups. Owns embedded and ML-based healthcare systems end-to-end — from firmware and edge ML to cloud inference pipelines.</div></div>',unsafe_allow_html=True)

    st.markdown(f'<div class="srow au d2"><div class="scard ap d1"><div class="snum">5+</div><div class="slbl">Years Experience</div></div><div class="scard ap d2"><div class="snum">5+</div><div class="slbl">Product Deployments</div></div><div class="scard ap d3"><div class="snum">3</div><div class="slbl">Publications</div></div><div class="scard ap d4"><div class="snum">5</div><div class="slbl">Awards</div></div><div class="scard ap d5"><div class="snum">2</div><div class="slbl">Degrees</div></div></div>',unsafe_allow_html=True)

    # Vertical timeline infographic
    st.markdown(f'<div class="stitle af d3">Career Timeline</div>',unsafe_allow_html=True)
    vtl=A/"docs"/VTL_IMG
    if vtl.exists(): st.markdown(f'<div style="max-width:900px;margin:0 auto;border-radius:14px;overflow:hidden;border:1px solid {BD}"><img src="data:image/png;base64,{b64(str(vtl))}" style="width:100%;display:block"/></div>',unsafe_allow_html=True)

    # Horizontal Gantt timeline
    st.markdown(f'<div class="stitle af d4">Experience & Education</div>',unsafe_allow_html=True)
    gtl=A/"docs"/TL_IMG
    if gtl.exists(): st.markdown(f'<div style="max-width:1050px;margin:0 auto;border-radius:14px;overflow:hidden;border:1px solid {BD}"><img src="data:image/png;base64,{b64(str(gtl))}" style="width:100%;display:block"/></div>',unsafe_allow_html=True)

    # Skills
    st.markdown(f'<div class="stitle af d5">Core skills</div>',unsafe_allow_html=True)
    skills={"Embedded & IoT":[("Edge ML",9),("Arduino",8),("Raspberry Pi",8),("STM32",9),("Firmware",9),("IoT Security",7),("CAN",8),("V2V",7)],"AI / ML":[("ASR",8),("NLP",8),("RAG",7),("Model Compression",8),("TensorRT",7),("GPU Accel.",7),("Computer Vision",6)],"Programming":[("Python",9),("C",8),("C++",8),("Java",6),("CAPL",7),("ROS",6)],"Platforms":[("Linux/RHEL",8),("CUDA",7),("NVIDIA Jetson",8),("Docker",7),("Git",9)]}
    c1,c2=st.columns(2)
    for i,(cat,sk) in enumerate(skills.items()):
        with c1 if i%2==0 else c2:
            st.markdown(f'<p style="font-weight:600;color:{TX};margin-bottom:.3rem;font-size:.95rem">{cat}</p>',unsafe_allow_html=True)
            for n,l in sk: skill_bar(n,l)
            st.markdown("")

    # Experience — NO photo upload section
    st.markdown(f'<div class="sdiv"></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="stitle au">Work Experience</div>',unsafe_allow_html=True)
    for idx,(role,co,dt,bul,sk) in enumerate([
        ("Lead R&D Product Engineer","O-Health · Bangalore & Boston","Jan 2025 – Present",["Improved ASR accuracy — reduced WER by 40% for Standard Hindi on edge","Reduced inference latency by 50% via distillation, quantization, pruning","Built medical RAG pipeline with hallucination-free cross-LLM consensus","Optimized GPU inference on H200 — CUDA, TensorRT, async threading","Led end-to-end health-band development with MIT CSAIL"],["ASR","NLP","RAG","Linux","Edge ML","GPU Accel.","Health-tech"]),
        ("Werkstudent Embedded IoT Engineer","Würth Elektronik eiSoS · Munich","May 2022 – Jan 2025",["Optimized AT-command interfaces and multi-threaded buffer management","Designed LTE-M / NB-IoT firmware drivers with robust state machines","Ensured reliable high-frequency IoT data transmission"],["LTE-M","NB-IoT","Firmware","Multithreading","ARM","Edge ML"]),
        ("Embedded Software Engineer","Robert Bosch · Bangalore","Jan 2021 – Sep 2021",["Implemented ECU security algorithms per customer specifications","Developed SecOC tool for secure ECU-to-ECU communication over CAN"],["ECU Security","CAN","CAPL","CANoe","XCP"]),
        ("Embedded Software Developer","AmberFlux EdgeAI · Hyderabad","Nov 2020 – Jan 2021",["Integrated sensors on RPi, STM32 and Xtensa for real-time positioning","Optimized embedded AI models for edge devices"],["Raspberry Pi","STM32","Real-time","Embedded AI"]),
        ("Product Verification Intern","Tejas Networks · Bangalore","Jan 2020 – Jul 2020",["Automated Layer-2 product verification for optical communication","Developed test-automation scripts in Python and TCL"],["Layer-2","Test Automation","Python","TCL"]),
    ]):
        bl="".join(f"<li>{b}</li>" for b in bul); tg="".join(f'<span class="sk">{s}</span>' for s in sk)
        st.markdown(f'<div class="tc au d{min(idx%3+1,3)}"><div class="th_"><div><div class="tr">{role}</div><div class="tco">{co}</div></div><span class="tdt">{dt}</span></div><div class="td"><ul>{bl}</ul></div><div class="tsk">{tg}</div></div>',unsafe_allow_html=True)

    # Education
    st.markdown(f'<div class="sdiv"></div><div class="stitle au">Education</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="ec au d1"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><div class="edeg">M.Sc. Communication Engineering</div><div class="esch">Technical University of Munich (TUM) — Germany</div></div><span class="tdt">Oct 2021 – Oct 2024</span></div><div class="edet"><strong style="color:{T2}">Grade:</strong> 2.1 · <strong style="color:{T2}">Thesis:</strong> Lane-Free Traffic Control on Connected Mini Automated Vehicles <em>(1.0)</em><br><strong style="color:{T2}">Focus:</strong> Embedded Systems & Security, IoT, SoC, Data Networks · <strong style="color:{T2}">Extra:</strong> 6G Business Modeling Lab (TUM CDTM)</div></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="ec au d2"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><div class="edeg">B.E. Electronics & Communication</div><div class="esch">National Institute of Engineering — Mysore, India</div></div><span class="tdt">Aug 2016 – Oct 2020</span></div><div class="edet"><strong style="color:{T2}">Grade:</strong> 1.6 · <strong style="color:{T2}">Thesis:</strong> Data Analysis from Sensors via DSP and WSN <em>(1.0)</em><br><strong style="color:{T2}">Focus:</strong> Digital Electronics, Embedded Systems, Network Security, C++</div></div>',unsafe_allow_html=True)
    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.95rem;margin:1rem 0 .4rem">Online courses</p>',unsafe_allow_html=True)
    for c in ["IoT Wireless & Cloud Computing — Yonsei University (Coursera)","Embedded Hardware & Operating Systems — EIT Digital (Coursera)","Computer Networks & IP Protocol — IIT Kharagpur (NPTEL)","Python for Computer Vision with OpenCV & Deep Learning (Udemy)"]:
        st.markdown(f'<div class="ci af">{c}</div>',unsafe_allow_html=True)
    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.95rem;margin:1rem 0 .4rem">Degree certificates</p>',unsafe_allow_html=True)
    slideshow("education",key="eds")

    # Products
    st.markdown(f'<div class="sdiv"></div><div class="stitle au">Products & Builds</div>',unsafe_allow_html=True)
    prods=[("Health Band — O-Health","Production-grade wearable with custom sensors, BLE, and cloud ML. Collaborating with MIT CSAIL.",["Hardware","Firmware","ML","BLE","Healthcare"],None),("ASR Engine for Hindi","Edge-optimized ASR. 40% WER improvement, 50% latency reduction. 30,000+ clinical consultations.",["ASR","Edge ML","Compression","NLP"],None),("Medical RAG Pipeline","Hallucination-free medical info extraction via cross-LLM consensus.",["RAG","LLM","Healthcare","NLP"],None),("Retrofittable E-Bike Auto Shifter","IoT-enabled rear-derailleur shifting. IEEE ICCE 2024 Best Presentation.",["IoT","Mechatronics","Sensors","IEEE"],"https://ieeexplore.ieee.org/document/10444469"),("SecOC Tool — Bosch","Automated ECU data encryption for CAN bus.",["Automotive","Security","CAN","CAPL"],None),("Autonomous Mini Vehicle — TUM","Lane-free traffic control with V2V and sensor fusion.",["Autonomous","V2V","ROS","Sensor Fusion"],None)]
    for i in range(0,len(prods),2):
        cols=st.columns(2)
        for j in range(2):
            if i+j<len(prods):
                nm,desc,tags,lnk=prods[i+j]; tg="".join(f'<span class="sk">{t}</span>' for t in tags)
                thtml=f'<a href="{lnk}" target="_blank">{nm}</a>' if lnk else nm
                lhtml=f'<div style="font-family:DM Mono,monospace;font-size:.7rem;margin-top:.15rem"><a href="{lnk}" target="_blank" style="color:{AC};text-decoration:none">📄 View paper</a></div>' if lnk else ""
                with cols[j]: st.markdown(f'<div class="tc ap d{j+1}" style="min-height:145px"><div class="tr">{thtml}</div><div class="td" style="margin:.3rem 0">{desc}</div>{lhtml}<div class="tsk">{tg}</div></div>',unsafe_allow_html=True)
    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.95rem;margin:1rem 0 .4rem">Product gallery</p>',unsafe_allow_html=True)
    slideshow("products",key="prs",use_media=True)

# ══ ACADEMICS ══
with tabs[1]:
    st.markdown(f'<div class="stitle au">Academic Work</div>',unsafe_allow_html=True)
    st.markdown(f'<p style="font-weight:600;font-size:1.05rem;color:{TX};margin:1.2rem 0 .5rem">Research projects</p>',unsafe_allow_html=True)
    for title,venue,date,desc,skills,doc_id,btns in [
        ("Lane-Free Traffic Control for Connected Mini-Automated Vehicles","Master's Thesis — TU München","Feb – Oct 2024","Designed and implemented lane-free control strategies for connected autonomous vehicles using V2V communication.",["Vehicle Control","V2V","Sensor Fusion","Autonomous"],"lane-free-docs",[("📄 Thesis PDF","lane-free-docs"),("📊 Presentation","lane-free-docs")]),
        ("Cellular IoT Cloud Connectivity","Würth Elektronik eiSoS — TU München","2022 – 2024","Plug-and-play system for sensor-to-cloud via Adrastea-I in LTE-CAT-M and NB-IoT with PSM power saving and digital certificate security.",["LTE-M","NB-IoT","PSM","Cloud IoT","Digital Certificates","Adrastea-I"],"cellular-iot-docs",[("📄 PDF","cellular-iot-docs")]),
        ("3D Manoeuverable Solar Retrofittable System","Academic Project","Project","3D manoeuverable solar panel system retrofittable onto existing structures for optimal sun tracking.",["Solar Energy","Mechatronics","Retrofittable","3D Tracking"],"solar-docs",[("📄 PDF / Presentation","solar-docs")]),
        ("Wireless Sensor Network for Data Extraction","Academic Project","Project","WSN system for environmental data extraction and processing using distributed sensor nodes.",["WSN","Sensor Networks","Data Extraction","Embedded"],"wsn-docs",[("📄 PDF / Presentation","wsn-docs")]),
    ]:
        sk="".join(f'<span class="sk">{s}</span>' for s in skills)
        btn_html="".join(f'<a class="db" href="#{href}">{lbl}</a>' for lbl,href in btns)
        st.markdown(f'<div class="tc au"><div class="th_"><div><div class="tr"><a href="#{doc_id}">{title}</a></div><div class="tco">{venue}</div></div><span class="tdt">{date}</span></div><div class="td">{desc}</div><div class="tsk">{sk}</div><div>{btn_html}</div></div>',unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;font-size:1.05rem;color:{TX};margin:1.5rem 0 .5rem">Publications</p>',unsafe_allow_html=True)
    for t,v,u,d in [
        ("Retrofittable Automatic Shifter of Rear-Derailleur with Mode-Based Transmission and IoT","IEEE ICCE 2024","https://ieeexplore.ieee.org/document/10444469","Retrofittable shifting for E-bikes with IoT and adaptive riding modes."),
        ("Remote Monitoring Robot with Voice Control and Image Analysis","IJAST 2020","http://sersc.org/journals/index.php/IJAST/article/view/21218","Surveillance robot with image processing, voice control, and MQTT."),
        ("Data Extraction with Signal Comparison for Forest Logging Prevention","IJERT · NCCDS 2020","https://www.ijert.org/data-extraction-with-signal-comparison-for-forest-logging-prevention","WSN for illegal logging detection via FFT-based signal processing."),
    ]:
        st.markdown(f'<div class="pc af"><div class="pt"><a href="{u}" target="_blank">{t}</a></div><div class="pv">{v}</div><div class="pd_">{d}</div></div>',unsafe_allow_html=True)

    st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.95rem;margin:1rem 0 .4rem">Academic gallery</p>',unsafe_allow_html=True)
    slideshow("academics",key="acs")

    # READ-ONLY document embeds
    st.markdown("---")
    st.markdown(f'<div id="lane-free-docs"></div><div class="stitle au">📄 Lane-Free Traffic Control</div>',unsafe_allow_html=True)
    dc1,dc2=st.columns(2)
    with dc1: st.markdown(f'<p style="font-weight:600;color:{TX}">Thesis</p>',unsafe_allow_html=True); render_doc_readable("lane_free_thesis.pdf","Thesis")
    with dc2: st.markdown(f'<p style="font-weight:600;color:{TX}">Presentation</p>',unsafe_allow_html=True); render_doc_readable("lane_free_presentation.pdf","Presentation")
    for anchor,title,fname in [("cellular-iot-docs","Cellular IoT","cellular_iot.pdf"),("solar-docs","3D Solar System","solar_system.pdf"),("wsn-docs","Wireless Sensor Network","wsn_data_extraction.pdf")]:
        st.markdown(f'---<div id="{anchor}"></div><div class="stitle au">📄 {title}</div>',unsafe_allow_html=True)
        render_doc_readable(fname,title)

# ══ CONFERENCES & AWARDS ══
with tabs[2]:
    st.markdown(f'<div class="stitle au">Conferences & Awards</div>',unsafe_allow_html=True)
    certs=[
        ("Best Session Presentation — IEEE ICCE 2024","Las Vegas · Jan 2024","Award",AMB if DARK else "#d97706"),
        ("Best Session Presentation — IEEE ICCE 2024","Las Vegas · Jan 2024","Conference",AC),
        ("Best Paper — ICICEE 2020","Remote Monitoring · Tumkur","Award",AMB if DARK else "#d97706"),
        ("Bravo Award — Robert Bosch","SecOC tool · Aug 2021","Award",AMB if DARK else "#d97706"),
        ("UnternehmerTUM MakerSpace Scholarship","Munich · Feb 2024","Award",AMB if DARK else "#d97706"),
        ("Bosch Future Mobility Challenge","TUMAVERICK — Semi-finalist · Cluj 2023","Conference","#fb7185" if DARK else "#e11d48"),
        ("NCCDS 2020","Forest Logging Prevention · Mysuru","Conference",AC),
        ("ANKURA'19","National Paper Presentation · Mysore","Conference",AC),
        ("Tejas Networks Internship","Product verification · 2020","Internship",A3),
        ("NIE Summer of Code 5.0","Hardware Track · 2018","Workshop","#22d3ee" if DARK else "#0891b2"),
        ("Adroit'18 Appreciation","IEEE NIE volunteering · Oct 2018","Volunteering","#a78bfa" if DARK else "#7c3aed"),
    ]
    cats=sorted(set(c[2] for c in certs))
    sel=st.multiselect("Filter",cats,default=cats,key="cf")
    for idx,(ti,de,ca,co) in enumerate(certs):
        if ca in sel:
            st.markdown(f'<div class="tc al d{min(idx%3+1,3)}" style="border-left-color:{co}"><div class="th_"><div><div class="tr">{ti}</div><div class="td">{de}</div></div><span class="tdt">{ca}</span></div></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div class="stitle">Certificate scans</div>',unsafe_allow_html=True)
    slideshow("certificates",key="cs")

# ══ PROJECTS & VIDEOS ══
with tabs[3]:
    st.markdown(f'<div class="stitle au">Projects & Videos</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="ps au d1"><div class="pst">🌲 Illegal Forest Logging Prevention — STM32</div><div class="td">Bachelor thesis — WSN for illegal logging detection via FFT audio analysis on STM32.</div><div style="font-family:DM Mono,monospace;font-size:.7rem;margin-top:.4rem"><a href="https://www.ijert.org/data-extraction-with-signal-comparison-for-forest-logging-prevention" target="_blank" style="color:{AC};text-decoration:none">📄 Read the paper</a></div></div>',unsafe_allow_html=True)
    v1,v2=st.columns(2)
    with v1: st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.92rem">Project demo</p>',unsafe_allow_html=True); yt("https://www.youtube.com/watch?v=g9tRZPRJfYs")
    with v2: st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.92rem">Cooja simulator</p>',unsafe_allow_html=True); yt("https://www.youtube.com/watch?v=wczmB9WR8O4")
    st.markdown("---")
    st.markdown(f'<div class="ps au d2"><div class="pst">🐛 Pest Detection Using ML on Edge Devices</div><div class="td">ML pest detection on edge devices for real-time agricultural monitoring.</div><div style="font-family:DM Mono,monospace;font-size:.7rem;margin-top:.4rem"><a href="https://resources.mouser.com/explore-all/pest-detection-using-machine-learning-on-edge-devices" target="_blank" style="color:{AC};text-decoration:none">📄 View on Mouser</a></div></div>',unsafe_allow_html=True)
    slideshow("projects",key="pjs")
    st.markdown("---")
    st.markdown(f'<div class="ps au d3"><div class="pst">🤖 TUM Robotics Club</div><div class="td">Activities, competitions, and collaborative engineering.</div></div>',unsafe_allow_html=True)
    slideshow("robotics_club",key="rbs")
    robotics_club_videos=[]
    if robotics_club_videos:
        for ti,ur in robotics_club_videos: st.markdown(f'<p style="font-weight:600;color:{TX};font-size:.88rem">{ti}</p>',unsafe_allow_html=True); yt(ur)
    else: st.markdown(f'<div style="background:{BG2};border:1px dashed {BD};border-radius:10px;padding:.7rem;margin-top:.5rem"><p style="color:{T4};font-size:.8rem;margin:0">📹 Add YouTube links to <code>robotics_club_videos</code> in <code>app.py</code>.</p></div>',unsafe_allow_html=True)

# ══ CONTACT ══
with tabs[4]:
    st.markdown(f'<div class="stitle au">Get in touch</div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown(f'<div class="ci al d1">📞 +49 176 71095238</div><div class="ci al d2">📧 <a href="mailto:shashankv099@gmail.com">shashankv099@gmail.com</a></div><div class="ci al d3">💼 <a href="https://www.linkedin.com/in/shashank-hegde98" target="_blank">linkedin.com/in/shashank-hegde98</a></div><div class="ci al d4">🌍 Bangalore, India & Munich, Germany</div><div class="ci al d5">🇺🇸 Nationality: United States of America</div>',unsafe_allow_html=True)
        st.markdown(f'<p style="font-weight:600;color:{TX};margin-top:.8rem">Languages</p>',unsafe_allow_html=True)
        st.markdown(f'<div class="ci af">English — C2 · German — A2 (learning B1)</div>',unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="hero ap" style="padding:1.3rem"><div style="font-size:1rem;font-weight:600;color:{TX};margin-bottom:.3rem">Open to opportunities</div><div class="hero-bio" style="font-size:.87rem">Interested in Embedded ML, Edge AI, Healthcare Technology, and IoT. Reach out via email or LinkedIn.</div></div>',unsafe_allow_html=True)

st.markdown("---")
st.markdown(f'<p style="text-align:center;color:{T4};font-size:.78rem">Shashank Hegde · Embedded-ML Electronics Engineer · © 2025</p>',unsafe_allow_html=True)
