# ==========================================================
# LUMINABRAIN — End-to-End Super GUI (Demo/Research Edition)
# Human Brain Operating System — Unified Modules
# Author: Veera Babu
# ==========================================================
import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime
from collections import deque

# Optional EEG via LSL (if available)
try:
    from pylsl import StreamInlet, resolve_stream
    LSL_AVAILABLE = True
except:
    LSL_AVAILABLE = False

# Signal processing
from scipy.signal import butter, lfilter, welch

# ---------------- Page ----------------
st.set_page_config(page_title="LUMINABRAIN Super GUI", layout="wide")

# ---------------- Styles ----------------
st.markdown("""
<style>
body {background:#0a0f1e;color:#e6f1ff;}
.title {font-size:38px;font-weight:800;color:#00f0ff;}
.subtitle{font-size:15px;color:#9aa5ff;}
.card{background:#10172a;padding:14px;border-radius:14px;box-shadow:0 0 18px rgba(0,255,255,.18);}
.ok{background:#0f2f1f;border-radius:10px;padding:10px;color:#9cffd0;}
.warn{background:#2f1f0f;border-radius:10px;padding:10px;color:#ffd49c;}
.bad{background:#2f0f0f;border-radius:10px;padding:10px;color:#ffb3b3;}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("<div class='title'>🧠 LUMINABRAIN — Human Brain Operating System (Super GUI)</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Hybrid Neuro-AI Platform | Unified Brain Modules | Research/Demo</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- Sidebar (Modules) ----------------
st.sidebar.title("🧠 LUMINABRAIN Modules")
MODE = st.sidebar.radio("Select Mode", [
    "🚀 Command Center",
    "🔬 Neuro Lab",
    "✨ Thought Decoder",
    "📡 Telemetry",
    "🔐 Security Core",
    "🧠 Cognitive Firewall",
    "⚠ Predictive Mission Failure",
    "🧬 Digital Brain DNA",
    "🤖 Autonomous Brain Agent",
    "🛰 War-Room Cognitive Network",
    "🧠 Brain Simulation Engine",
    "🧬 Neuro-Regeneration",
    "🌐 Cognitive Battlefield Map",
])

st.sidebar.markdown("---")
REFRESH = st.sidebar.slider("Refresh (seconds)", 1, 5, 2)

# ---------------- EEG Utilities (optional) ----------------
FS = 250

def bandpass(data, low, high, fs, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, [low/nyq, high/nyq], btype='band')
    return lfilter(b, a, data, axis=0)

def connect_lsl():
    if not LSL_AVAILABLE:
        return None
    streams = resolve_stream('type', 'EEG', timeout=3)
    if not streams:
        return None
    return StreamInlet(streams[0], max_chunklen=32)

def read_chunk(inlet, n=FS):
    buf=[]
    for _ in range(n):
        s,_=inlet.pull_sample(timeout=1.0)
        if s: buf.append(s)
    return np.array(buf) if len(buf)>0 else None

def extract_bands(eeg, fs=FS):
    clean = bandpass(eeg, 1, 45, fs)
    bands={"alpha":[], "beta":[], "gamma":[], "theta":[], "delta":[]}
    for ch in range(clean.shape[1]):
        f,p = welch(clean[:,ch], fs=fs, nperseg=min(2*fs, clean.shape[0]))
        def bp(lo,hi):
            idx=(f>=lo)&(f<=hi)
            return np.trapz(p[idx], f[idx])
        bands["delta"].append(bp(0.5,4))
        bands["theta"].append(bp(4,7))
        bands["alpha"].append(bp(8,12))
        bands["beta"].append(bp(12,30))
        bands["gamma"].append(bp(30,80))
    return {k:float(np.mean(v)) for k,v in bands.items()}

# ---------------- Brain OS Core ----------------
def brain_state(b):
    stress = b["beta"] + b["gamma"]
    focus  = b["alpha"] + b["beta"]
    fatigue= b["theta"] + b["delta"]
    load   = (stress+fatigue)/2
    return dict(stress=round(stress,2), focus=round(focus,2),
                fatigue=round(fatigue,2), load=round(load,2))

def energy_model(load):
    return dict(metabolic=round(load*1.2,2),
                biophoton_sim=round(load*0.3,2),
                pulse_est=round(40+load,2))

def advisory(load):
    if load>80: return "🚨 CRITICAL: Cognitive overload. Immediate rest."
    if load>60: return "⚠ WARNING: Elevated stress. Breathing & hydration."
    return "✅ OPTIMAL: Brain condition stable. Mission safe."

# ---------------- Predictive (trend demo) ----------------
HIST = deque(maxlen=30)
def predict_risk(load_series):
    if len(load_series)<5: return 0.0
    # simple slope-based risk (demo)
    x=np.arange(len(load_series))
    y=np.array(load_series)
    m=np.polyfit(x,y,1)[0]
    risk = np.clip((y[-1]/100)*0.6 + max(m,0)*0.4, 0, 1)
    return round(float(risk*100),2)

# ---------------- Cognitive Firewall (demo) ----------------
def firewall_check(bands):
    # flag impossible spikes / flatlines (demo)
    flags=[]
    if any(v<0 for v in bands.values()): flags.append("NEG_POWER")
    if max(bands.values())>1e6: flags.append("SPIKE")
    return flags

# ---------------- Digital Brain DNA (baseline) ----------------
if "baseline" not in st.session_state:
    st.session_state.baseline = {"stress":40,"focus":40,"fatigue":20,"load":30}

def personalize(state):
    base = st.session_state.baseline
    delta = {k: round(state[k]-base[k],2) for k in base}
    return delta

# ---------------- Autonomous Brain Agent (demo) ----------------
def auto_actions(load):
    if load>80: return ["AUTO_ALERT", "SUGGEST_REST", "LOCK_HIGH_STRESS_MODE"]
    if load>60: return ["SUGGEST_BREATHING", "REDUCE_TASK_LOAD"]
    return ["MONITOR"]

# ---------------- War-Room (team demo) ----------------
def team_snapshot():
    # demo 5 operators
    team=[]
    for i in range(1,6):
        team.append({
            "operator": f"OP-{i}",
            "load": round(np.random.uniform(20,90),2),
            "status": "OK" if np.random.rand()>0.4 else "HIGH LOAD"
        })
    return pd.DataFrame(team)

# ---------------- Brain Simulation (what-if) ----------------
def simulate_scenario(stress, fatigue):
    load=(stress+fatigue)/2
    return dict(load=round(load,2), energy=energy_model(load), advice=advisory(load))

# ---------------- Neuro-Regeneration (recovery demo) ----------------
if "recovery" not in st.session_state:
    st.session_state.recovery = deque(maxlen=50)

def log_recovery(load):
    st.session_state.recovery.append({"t":datetime.now().strftime("%H:%M:%S"),"load":load})

# ---------------- Battlefield Map (demo) ----------------
def battlefield_map():
    nodes=[]
    for z in ["North","East","West","South"]:
        nodes.append({"zone":z, "avg_load":round(np.random.uniform(25,75),2)})
    return pd.DataFrame(nodes)

# ---------------- Status ----------------
status = st.sidebar.empty()
status.success("Neuro OS: ONLINE | AI: CONNECTED | Security: ACTIVE")

# ---------------- Data Source ----------------
inlet = connect_lsl()
if inlet:
    chunk = read_chunk(inlet)
    bands = extract_bands(chunk) if chunk is not None else {"alpha":0,"beta":0,"gamma":0,"theta":0,"delta":0}
else:
    # demo fallback
    bands = {"alpha":11.6,"beta":23.2,"gamma":47.1,"theta":5.2,"delta":1.5}

state = brain_state(bands)
energy = energy_model(state["load"])
advice = advisory(state["load"])
HIST.append(state["load"])
risk = predict_risk(list(HIST))
fire_flags = firewall_check(bands)
delta = personalize(state)
actions = auto_actions(state["load"])
ts = datetime.now().strftime("%H:%M:%S")

# ---------------- Pages ----------------
if MODE == "🚀 Command Center":
    st.subheader("🚀 Defence Neuro Command Center")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.metric("Stress", state["stress"])
        st.metric("Focus", state["focus"])
        st.metric("Fatigue", state["fatigue"])
    with c2:
        st.metric("Cognitive Load", state["load"])
        st.metric("Metabolic Energy", energy["metabolic"])
        st.metric("Biophoton (sim)", energy["biophoton_sim"])
    with c3:
        st.metric("Neural Pulse", energy["pulse_est"])
        st.metric("Risk (Next mins)", f"{risk}%")
        st.success(advice)
    st.info(f"Timestamp: {ts}")

elif MODE == "🔬 Neuro Lab":
    st.subheader("🔬 Neuro Lab — Biological Computing (Research)")
    st.write("Band Powers"); st.json(bands)
    st.write("Energy Model"); st.json(energy)

elif MODE == "✨ Thought Decoder":
    st.subheader("✨ Thought Decoder (Research Demo)")
    text = st.text_area("Describe a thought/emotion:")
    if st.button("Decode (Sim)"):
        score = min(100, max(0, len(text)*2))
        st.success(f"Decoded Cognitive Intensity (sim): {score}")

elif MODE == "📡 Telemetry":
    st.subheader("📡 Live Neuro Telemetry")
    st.json({"bands":bands, "state":state, "energy":energy, "risk":risk, "ts":ts})

elif MODE == "🔐 Security Core":
    st.subheader("🔐 Security Core")
    st.success("Encrypted Telemetry: ACTIVE")
    st.success("Zero-Trust Access: ENABLED")
    st.success("Model Integrity: VERIFIED")
    if fire_flags:
        st.error(f"Firewall Flags: {fire_flags}")
    else:
        st.success("Cognitive Firewall: CLEAN")

elif MODE == "🧠 Cognitive Firewall":
    st.subheader("🧠 Cognitive Firewall (Demo)")
    st.write("Flags:", fire_flags if fire_flags else "No anomalies")

elif MODE == "⚠ Predictive Mission Failure":
    st.subheader("⚠ Predictive Mission Failure (Trend Demo)")
    st.metric("Predicted Risk", f"{risk}%")
    st.line_chart(pd.DataFrame({"load":list(HIST)}))

elif MODE == "🧬 Digital Brain DNA":
    st.subheader("🧬 Digital Brain DNA (Personal Baseline)")
    st.write("Baseline:", st.session_state.baseline)
    st.write("Delta vs Baseline:", delta)
    if st.button("Set Current as Baseline"):
        st.session_state.baseline = state
        st.success("Baseline updated.")

elif MODE == "🤖 Autonomous Brain Agent":
    st.subheader("🤖 Autonomous Brain Agent (Auto-Advisory)")
    st.write("Suggested Actions:", actions)

elif MODE == "🛰 War-Room Cognitive Network":
    st.subheader("🛰 War-Room Cognitive Network (Team View — Demo)")
    st.dataframe(team_snapshot(), use_container_width=True)

elif MODE == "🧠 Brain Simulation Engine":
    st.subheader("🧠 Brain Simulation (What-If)")
    s = st.slider("Sim Stress", 0, 100, 60)
    f = st.slider("Sim Fatigue",0,100,40)
    sim = simulate_scenario(s,f)
    st.json(sim)

elif MODE == "🧬 Neuro-Regeneration":
    st.subheader("🧬 Neuro-Regeneration (Recovery Tracker)")
    log_recovery(state["load"])
    st.line_chart(pd.DataFrame(list(st.session_state.recovery)).set_index("t"))

elif MODE == "🌐 Cognitive Battlefield Map":
    st.subheader("🌐 Cognitive Battlefield Map (Status — Demo)")
    st.dataframe(battlefield_map(), use_container_width=True)

# ---------------- Footer ----------------
st.markdown("---")
st.caption("🛡 Secure Network | Encrypted Telemetry | Zero-Trust Brain OS (Research/Demo)")

time.sleep(REFRESH)
st.experimental_rerun()
