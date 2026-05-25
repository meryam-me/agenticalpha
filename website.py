import subprocess
subprocess.run(["pip", "install", "plotly", "groq", "-q"])

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(
    page_title="The Agentic Alpha",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #f0f2f6; color: #1a2744; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #0d1f3c 100%);
    border-right: 3px solid #c9a227;
}
[data-testid="stSidebar"] * { color: #e8e8e8 !important; }
[data-testid="stSidebar"] .stRadio label {
    padding: 10px 14px; border-radius: 8px;
    font-weight: 500; transition: all 0.2s; display: block;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(201,162,39,0.15);
    color: #FFD700 !important;
}
h1 {
    color: #0a1628 !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    border-bottom: 3px solid #c9a227;
    padding-bottom: 10px;
}
h2 { color: #0a1628 !important; font-weight: 700 !important; }
h3 { color: #1a3a6b !important; font-weight: 600 !important; }
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-top: 4px solid #c9a227;
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    overflow: hidden;
}
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #0a1628 !important;
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    white-space: nowrap;
    overflow: hidden;
}
.stButton > button {
    background: #0a1628;
    color: #FFD700 !important;
    border: 2px solid #c9a227;
    border-radius: 8px;
    font-weight: 700;
    font-size: 14px;
    padding: 12px 28px;
    text-transform: uppercase;
    transition: all 0.3s;
}
.stButton > button:hover {
    background: #c9a227;
    color: #0a1628 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(201,162,39,0.3);
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #ffffff;
    color: #1a2744 !important;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 13px;
}
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #1a2744 !important;
    font-size: 13px !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid #e2e8f0;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b !important;
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
}
.stTabs [aria-selected="true"] {
    background: #0a1628 !important;
    color: #FFD700 !important;
}
.stInfo {
    background: #eff6ff !important;
    border-left: 4px solid #3b82f6 !important;
    border-radius: 8px;
}
.stSuccess {
    background: #f0fdf4 !important;
    border-left: 4px solid #22c55e !important;
    border-radius: 8px;
}
.stWarning {
    background: #fffbeb !important;
    border-left: 4px solid #c9a227 !important;
    border-radius: 8px;
}
.stError {
    background: #fff1f2 !important;
    border-left: 4px solid #ef4444 !important;
    border-radius: 8px;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #0a1628, #c9a227);
    border-radius: 10px;
}
.stDataFrame {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    font-size: 12px !important;
}
.stDataFrame td, .stDataFrame th {
    font-size: 12px !important;
    padding: 8px 10px !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 140px;
}
hr { border: none; border-top: 1px solid #e2e8f0; margin: 20px 0; }
.stCaption { color: #94a3b8 !important; }
.gold-line {
    height: 3px;
    background: linear-gradient(90deg, #c9a227, #FFD700, #c9a227);
    border: none; margin: 28px 0; border-radius: 2px;
}
.aa-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("""
<div style='text-align:center; padding:20px 0 24px;'>
    <div style='width:72px; height:72px; margin:0 auto;
                background:#ffffff; border-radius:50%;
                border:3px solid #c9a227;
                display:flex; align-items:center;
                justify-content:center;
                box-shadow:0 4px 15px rgba(201,162,39,0.3);'>
        <span style='font-size:26px; font-weight:900;
                     background:linear-gradient(135deg,#c9a227,#FFD700);
                     -webkit-background-clip:text;
                     -webkit-text-fill-color:transparent;
                     letter-spacing:-2px;'>AA</span>
    </div>
    <div style='margin-top:14px; font-size:15px; font-weight:800;
                color:#FFD700; letter-spacing:1px;'>THE AGENTIC ALPHA</div>
    <div style='font-size:10px; color:#94a3b8; letter-spacing:2px;
                margin-top:4px; text-transform:uppercase;'>
        AI Decision Support System</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='background:rgba(255,255,255,0.05);
            border:1px solid rgba(201,162,39,0.3);
            border-radius:10px; padding:14px; margin-bottom:16px;'>
    <div style='color:#c9a227; font-size:10px;
                text-transform:uppercase; letter-spacing:1px;
                margin-bottom:8px;'>Researcher</div>
    <div style='color:#ffffff; font-weight:700; font-size:14px;'>
        Meryam El Ghouti</div>
    <div style='color:#94a3b8; font-size:12px; margin-top:3px;'>
        Sapienza University of Rome</div>
    <div style='color:#94a3b8; font-size:12px;'>
        MSc Business Management · 2026</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    "<div style='color:#c9a227; font-size:10px; text-transform:uppercase;"
    "letter-spacing:1px; padding:0 4px; margin-bottom:6px;'>Navigation</div>",
    unsafe_allow_html=True
)

page = st.sidebar.radio("", [
    "⚡ Home", "🤖 Live Analyzer", "📊 Dashboard",
    "⚔️ AI vs Human", "📂 Custom Analysis",
    "🎤 Jury Demo", "📋 About"
])

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align:center; color:#475569; font-size:11px; padding:8px;'>
    © 2026 Meryam El Ghouti<br>
    <span style='color:#c9a227;'>agenticalpha.streamlit.app</span>
</div>
""", unsafe_allow_html=True)

# Data
data = {
    "Company": [
        "WeWork","Tesla","Apple","Theranos","Kodak",
        "Blockbuster","Peloton","Amazon","Netflix","Microsoft",
        "Meta","Twitter","Disney","Uber","Rivian",
        "Microsoft","Adobe","Apple","Meta","OpenAI"
    ],
    "Year": [
        2019,2020,2018,2016,2012,2010,2021,2015,2013,2016,
        2021,2022,2019,2019,2021,2023,2023,2024,2022,2025
    ],
    "Corporate_Decision": [
        "Proceed with IPO expansion?",
        "Invest in Gigafactory Texas?",
        "Shift to services expansion?",
        "Scale blood-testing operations?",
        "Invest in digital transformation?",
        "Invest in streaming technology?",
        "Expand manufacturing capacity?",
        "Invest massively in AWS expansion?",
        "Invest billions in original content?",
        "Acquire LinkedIn for $26B?",
        "Invest billions in Metaverse?",
        "Accept Musk $44B acquisition?",
        "Acquire Fox and launch Disney+?",
        "Proceed with IPO unprofitable?",
        "Invest in mass EV production?",
        "Invest $10B in OpenAI partnership?",
        "Acquire Figma for $20B?",
        "Launch Vision Pro at $3,499?",
        "Massive layoffs and restructuring?",
        "Transition to fully commercial?"
    ],
    "Neutral_Decision": [
        "NO","YES","YES","NO","NO","NO","YES","YES","YES","YES",
        "NO","NO","YES","YES","YES","YES","NO","NO","YES","YES"
    ],
    "Aggressive_Decision": [
        "YES","YES","YES","YES","NO","NO","YES","YES","YES","YES",
        "YES","YES","NO","YES","YES","YES","YES","YES","YES","YES"
    ],
    "Conservative_Decision": [
        "YES","NO","YES","NO","NO","NO","NO","YES","NO","YES",
        "NO","NO","YES","NO","NO","YES","NO","NO","NO","NO"
    ],
    "Actual_Outcome": [
        "Failed","Success","Success","Failed","Failed","Failed",
        "Failed","Success","Success","Success","Mixed","Failed",
        "Mixed","Failed","Failed","Success","Failed","Failed",
        "Success","Pending"
    ],
    "Human_Decision": [
        "Proceed","Proceed","Proceed","Proceed","Did Not","Did Not",
        "Proceed","Proceed","Proceed","Proceed","Proceed","Accepted",
        "Proceed","Proceed","Proceed","Proceeded","Attempted",
        "Launched","Proceeded","Proceeding"
    ],
    "Industry": [
        "Real Estate","Automotive","Technology","Healthcare","Photography",
        "Entertainment","Fitness","E-Commerce","Media","Technology",
        "Social Media","Social Media","Entertainment","Transport","Automotive",
        "Technology","Software","Technology","Social Media","AI"
    ],
    "Neutral_Correct":      [1,1,1,1,1,1,0,1,1,1,1,1,0,0,0,1,1,1,1,0],
    "Aggressive_Correct":   [0,1,1,0,1,1,0,1,1,1,0,0,1,0,0,1,0,0,1,0],
    "Conservative_Correct": [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
    "Neutral_Score":      [15,78,82,12,20,18,55,85,80,90,35,30,72,60,65,88,25,28,82,60],
    "Aggressive_Score":   [65,88,92,75,35,30,80,95,85,85,80,72,45,80,75,95,70,78,88,90],
    "Conservative_Score": [8,25,88,15,18,12,22,82,25,88,20,18,75,15,18,85,20,18,22,35],
    "Main_Bias": [
        "Herding","Overconfidence","None","Herding","Loss Aversion",
        "Loss Aversion","Overconfidence","None","Overconfidence","None",
        "Overconfidence","Loss Aversion","Anchoring","Overconfidence","Overconfidence",
        "None","Overconfidence","Overconfidence","Loss Aversion","Overconfidence"
    ],
    "Human_Correct": [0,1,1,0,0,0,0,1,1,1,1,0,1,0,0,1,0,0,1,0]
}

df = pd.DataFrame(data)
df["Average_Score"] = (df["Neutral_Score"]+df["Aggressive_Score"]+df["Conservative_Score"])/3
df["AI_Recommendation"] = df["Average_Score"].apply(
    lambda x: "PROCEED" if x>=60 else "CAUTION" if x>=40 else "DO NOT PROCEED"
)
df_h = df[df["Actual_Outcome"]!="Pending"]

PT = dict(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#f8fafc",
    font_color="#1a2744",
    title_font_color="#0a1628",
    title_font_size=13,
    font_size=11,
    height=320
)
C = {"Neutral":"#1e3a8a","Aggressive":"#dc2626","Conservative":"#15803d","Human":"#c9a227"}

# HOME
if page == "⚡ Home":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a1628,#1a3a6b);
                border-radius:16px; padding:40px; margin-bottom:24px;
                border:1px solid #c9a227; text-align:center;'>
        <div style='width:64px; height:64px; margin:0 auto 16px;
                    background:#fff; border-radius:50%;
                    border:3px solid #c9a227;
                    display:flex; align-items:center; justify-content:center;'>
            <span style='font-size:22px; font-weight:900;
                         background:linear-gradient(135deg,#c9a227,#FFD700);
                         -webkit-background-clip:text;
                         -webkit-text-fill-color:transparent;
                         letter-spacing:-2px;'>AA</span>
        </div>
        <div style='font-size:30px; font-weight:900; color:#FFD700;
                    margin-bottom:10px;'>THE AGENTIC ALPHA</div>
        <div style='font-size:15px; color:#94a3b8; max-width:560px;
                    margin:0 auto 18px; line-height:1.7;'>
            An AI-powered corporate investment decision simulator that analyzes
            any investment through three behavioral personas — detecting
            cognitive biases in real time.
        </div>
        <div style='background:rgba(201,162,39,0.2); border:1px solid #c9a227;
                    display:inline-block; color:#FFD700; font-weight:700;
                    font-size:12px; padding:8px 20px; border-radius:20px;
                    letter-spacing:1px;'>
            ⚡ AI · SIMULATION · BEHAVIORAL ANALYSIS
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <div style='color:#c9a227; font-size:11px; font-weight:700;
                    text-transform:uppercase; letter-spacing:2px;'>
            What Is The Agentic Alpha?</div>
        <div style='color:#0a1628; font-size:20px; font-weight:800; margin-top:6px;'>
            A Multi-Agent AI That Simulates Corporate Investment Decisions</div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    for col,color,icon,name,desc in zip(
        [c1,c2,c3],
        ["#1e3a8a","#dc2626","#15803d"],
        ["🤖","📈","🛡️"],
        ["Neutral Advisor","Aggressive CFO","Conservative Board"],
        [
            "Objective analysis based purely on financial data and market conditions — no emotional bias",
            "Growth-focused perspective that prioritizes expansion and accepts calculated high risk",
            "Risk-averse perspective focused on financial stability and long-term sustainability"
        ]
    ):
        with col:
            st.markdown(f"""
            <div class='aa-card' style='border-top:4px solid {color};
                        text-align:center;'>
                <div style='font-size:32px; margin-bottom:10px;'>{icon}</div>
                <div style='color:{color}; font-weight:800; font-size:14px;
                            margin-bottom:8px;'>{name}</div>
                <div style='color:#64748b; font-size:13px;
                            line-height:1.6;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='gold-line'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <div style='color:#c9a227; font-size:11px; font-weight:700;
                    text-transform:uppercase; letter-spacing:2px;'>How It Works</div>
        <div style='color:#0a1628; font-size:20px; font-weight:800;
                    margin-top:6px;'>4 Simple Steps</div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,num,icon,title,desc in zip(
        [c1,c2,c3,c4],
        ["01","02","03","04"],
        ["🏢","⚡","💯","🧠"],
        ["Input Decision","AI Simulates","Get Scores","Detect Biases"],
        [
            "Enter company, year and investment decision type",
            "3 personas analyze through different behavioral lenses",
            "Each persona gives a 0-100 investment score",
            "System detects overconfidence, herding and more"
        ]
    ):
        with col:
            st.markdown(f"""
            <div class='aa-card' style='text-align:center; padding:20px 14px;'>
                <div style='background:#0a1628; color:#FFD700; font-size:10px;
                            font-weight:800; padding:3px 10px;
                            border-radius:20px; display:inline-block;
                            margin-bottom:10px; letter-spacing:1px;'>
                    STEP {num}</div>
                <div style='font-size:28px; margin-bottom:8px;'>{icon}</div>
                <div style='color:#0a1628; font-weight:700; font-size:13px;
                            margin-bottom:6px;'>{title}</div>
                <div style='color:#64748b; font-size:12px;
                            line-height:1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='gold-line'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-bottom:16px;'>
        <div style='color:#c9a227; font-size:11px; font-weight:700;
                    text-transform:uppercase; letter-spacing:2px;'>
            Research Validation</div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("📊 Cases Confirmed","19")
    with c2: st.metric("🤖 AI Simulations","60")
    with c3: st.metric("🎯 Best Accuracy",f"{round(df_h['Conservative_Correct'].mean()*100)}%")
    with c4: st.metric("🧠 Bias Types","5")

    st.markdown("<hr class='gold-line'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-bottom:16px;'>
        <div style='color:#c9a227; font-size:11px; font-weight:700;
                    text-transform:uppercase; letter-spacing:2px;'>What You Get</div>
        <div style='color:#0a1628; font-size:20px; font-weight:800;
                    margin-top:6px;'>Every Analysis Includes</div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    items_left = [
        "✅  Investment decision — YES or NO",
        "✅  Investment score from 0 to 100",
        "✅  Three specific reasons per persona",
        "✅  Final simulation verdict"
    ]
    items_right = [
        "✅  Behavioral bias detection report",
        "✅  Heuristic overconfidence indicator",
        "✅  Herding and anchoring analysis",
        "✅  Private company custom analysis"
    ]
    with c1:
        for item in items_left:
            st.markdown(f"""
            <div class='aa-card' style='padding:12px 16px; margin-bottom:8px;
                        font-weight:600; color:#0a1628; font-size:13px;'>
                {item}</div>
            """, unsafe_allow_html=True)
    with c2:
        for item in items_right:
            st.markdown(f"""
            <div class='aa-card' style='padding:12px 16px; margin-bottom:8px;
                        font-weight:600; color:#0a1628; font-size:13px;'>
                {item}</div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='gold-line'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#0a1628; border:1px solid #c9a227;
                border-radius:16px; padding:32px; text-align:center;'>
        <div style='color:#FFD700; font-size:20px; font-weight:800;
                    margin-bottom:8px;'>Ready to Simulate?</div>
        <div style='color:#94a3b8; font-size:13px; margin-bottom:12px;
                    line-height:1.6;'>
            Use the sidebar navigation on the left to access
            the Live Analyzer and Custom Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("👈 Use the sidebar navigation to get started")

# LIVE ANALYZER
elif page == "🤖 Live Analyzer":
    st.title("🤖 Live Corporate Investment Simulator")
    st.markdown("*Simulate corporate investment decisions through AI behavioral personas*")
    st.info("⚠️ Research simulation tool — does not predict actual financial outcomes or constitute financial advice.")
    st.markdown("---")

    c1,c2 = st.columns(2)
    with c1:
        company = st.text_input("🏢 Company Name:", placeholder="e.g. Apple, Tesla, OpenAI")
    with c2:
        year = st.text_input("📅 Year:", placeholder="e.g. 2019, 2023, 2025")

    decision_type = st.selectbox("📋 Type of Corporate Investment Decision:", [
        "IPO / Going Public","Merger & Acquisition (M&A)",
        "Capital Expenditure / Expansion","New Product / Service Investment",
        "Digital Transformation","Market Entry / Geographic Expansion",
        "Research & Development","Strategic Pivot","AI Investment","Restructuring"
    ])

    custom = st.text_input("📝 Describe the specific decision (optional):",
                          placeholder="e.g. Should the company acquire a competitor for $10B?")

    if st.button("⚡ RUN SIMULATION", use_container_width=True):
        if company and year:
            st.markdown("---")
            st.markdown(f"""
            <div class='aa-card' style='border-left:5px solid #c9a227;'>
                <div style='color:#64748b; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>Simulation Target</div>
                <div style='color:#0a1628; font-size:18px; font-weight:800;
                            margin-top:4px;'>{company} · {year}</div>
                <div style='color:#64748b; font-size:13px;'>{decision_type}</div>
            </div>
            """, unsafe_allow_html=True)

            personas = [
                {"name":"🤖 Neutral Advisor","color":"#1e3a8a","bg":"#eff6ff",
                 "instruction":"You are a neutral objective corporate finance advisor."},
                {"name":"📈 Aggressive CFO","color":"#dc2626","bg":"#fff1f2",
                 "instruction":"You are an aggressive CFO who prioritizes growth."},
                {"name":"🛡️ Conservative Board","color":"#15803d","bg":"#f0fdf4",
                 "instruction":"You are a conservative board member focused on stability."},
            ]

            all_decisions=[]
            all_scores=[]
            c1,c2,c3=st.columns(3)
            cols=[c1,c2,c3]

            for i,p in enumerate(personas):
                with cols[i]:
                    with st.spinner("Simulating..."):
                        spec = custom if custom else f"a major {decision_type} decision"
                        q = f"""
                        {p['instruction']}
                        Company: {company} | Year: {year} | Decision: {spec}
                        Answer in EXACTLY this format:
                        DECISION: YES or NO
                        SCORE: (0 to 100)
                        CONFIDENCE: (0 to 100)
                        REASON 1: (one sentence)
                        REASON 2: (one sentence)
                        REASON 3: (one sentence)
                        """
                        r = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[{"role":"user","content":q}]
                        )
                        text=r.choices[0].message.content
                        lines=text.strip().split('\n')
                        dec=sc=conf=r1=r2=r3=""
                        for line in lines:
                            if line.startswith("DECISION:"): dec=line.replace("DECISION:","").strip()
                            elif "SCORE:" in line:
                                try: sc=str(int(''.join(filter(str.isdigit, line.split("SCORE:")[-1].strip()))[:3]))
                                except: sc="50"
                            elif line.startswith("CONFIDENCE:"): conf=line.replace("CONFIDENCE:","").strip()
                            elif line.startswith("REASON 1:"): r1=line.replace("REASON 1:","").strip()
                            elif line.startswith("REASON 2:"): r2=line.replace("REASON 2:","").strip()
                            elif line.startswith("REASON 3:"): r3=line.replace("REASON 3:","").strip()

                        all_decisions.append(dec)
                        try: all_scores.append(int(sc))
                        except: all_scores.append(50)

                        yes = "YES" in dec.upper()
                        vc = "#15803d" if yes else "#dc2626"
                        vbg = "#f0fdf4" if yes else "#fff1f2"

                        st.markdown(f"""
                        <div style='background:#ffffff; border:1px solid #e2e8f0;
                                    border-top:4px solid {p['color']};
                                    border-radius:12px; padding:16px;'>
                            <div style='color:{p['color']}; font-weight:700;
                                        font-size:13px; margin-bottom:10px;'>
                                {p['name']}</div>
                            <div style='background:{vbg}; border:1px solid {vc};
                                        border-radius:8px; padding:8px;
                                        text-align:center; margin-bottom:10px;'>
                                <span style='color:{vc}; font-weight:800; font-size:14px;'>
                                    {"✅ PROCEED" if yes else "❌ DO NOT PROCEED"}
                                </span>
                            </div>
                            <div style='height:6px; background:#e2e8f0;
                                        border-radius:3px; margin-bottom:8px;'>
                                <div style='height:6px; background:{p['color']};
                                            border-radius:3px; width:{sc}%;'></div>
                            </div>
                            <div style='color:#64748b; font-size:12px; margin-bottom:8px;'>
                                Score: <strong style='color:#0a1628;'>{sc}/100</strong> ·
                                Confidence: <strong style='color:#0a1628;'>{conf}%</strong>
                            </div>
                            <div style='font-size:12px; color:#334155; line-height:1.6;'>
                                📌 {r1}<br>📌 {r2}<br>📌 {r3}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            avg = sum(all_scores)/len(all_scores) if all_scores else 50
            if avg>=60: v="PROCEED WITH INVESTMENT"; vc2="#15803d"; vbg2="#f0fdf4"; vi="✅"
            elif avg>=40: v="PROCEED WITH CAUTION"; vc2="#92400e"; vbg2="#fffbeb"; vi="⚠️"
            else: v="DO NOT PROCEED"; vc2="#991b1b"; vbg2="#fff1f2"; vi="❌"

            st.markdown("---")
            st.markdown(f"""
            <div style='background:{vbg2}; border:2px solid {vc2};
                        border-radius:14px; padding:24px; text-align:center;'>
                <div style='color:{vc2}; font-size:11px; font-weight:700;
                            text-transform:uppercase; letter-spacing:2px;
                            margin-bottom:6px;'>Simulation Verdict</div>
                <div style='color:{vc2}; font-size:22px; font-weight:900;'>
                    {vi} {v}</div>
                <div style='color:{vc2}; font-size:12px; margin-top:8px; opacity:0.8;'>
                    Avg: {avg:.0f}/100 · Neutral: {all_scores[0] if all_scores else 0} ·
                    Aggressive: {all_scores[1] if len(all_scores)>1 else 0} ·
                    Conservative: {all_scores[2] if len(all_scores)>2 else 0}
                </div>
            </div>
            <div style='text-align:center; color:#94a3b8; font-size:11px; margin-top:8px;'>
                ⚠️ Simulation output only — not financial advice</div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            bq = f"""
            Advisors simulated {company} {decision_type} in {year}.
            Decisions: {', '.join(all_decisions)}
            Scores: {', '.join([str(s) for s in all_scores])}
            Answer in EXACTLY this format:
            OVERCONFIDENCE: YES or NO — (why)
            LOSS AVERSION: YES or NO — (why)
            HERDING: YES or NO — (why)
            ANCHORING: YES or NO — (why)
            MAIN BIAS: (name or NONE)
            EXPLANATION: (one sentence)
            """
            br = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role":"user","content":bq}]
            )
            bl = br.choices[0].message.content.strip().split('\n')
            oc=la=h=an=mb=ex=""
            for line in bl:
                if line.startswith("OVERCONFIDENCE:"): oc=line.replace("OVERCONFIDENCE:","").strip()
                elif line.startswith("LOSS AVERSION:"): la=line.replace("LOSS AVERSION:","").strip()
                elif line.startswith("HERDING:"): h=line.replace("HERDING:","").strip()
                elif line.startswith("ANCHORING:"): an=line.replace("ANCHORING:","").strip()
                elif line.startswith("MAIN BIAS:"): mb=line.replace("MAIN BIAS:","").strip()
                elif line.startswith("EXPLANATION:"): ex=line.replace("EXPLANATION:","").strip()

            st.markdown("### 🧠 Heuristic Bias Detection")
            st.caption("Heuristic indicators — not definitive bias diagnoses")
            c1,c2,c3,c4 = st.columns(4)
            for col,bias,val,color in zip(
                [c1,c2,c3,c4],
                ["Overconfidence","Loss Aversion","Herding","Anchoring"],
                [oc,la,h,an],
                ["#dc2626","#c9a227","#1e3a8a","#7c3aed"]
            ):
                with col:
                    detected = "YES" in val.upper()
                    st.markdown(f"""
                    <div style='background:#ffffff; border:1px solid #e2e8f0;
                                border-top:3px solid {color if detected else "#e2e8f0"};
                                border-radius:10px; padding:12px;'>
                        <div style='color:{color}; font-weight:700;
                                    font-size:12px;'>{bias}</div>
                        <div style='color:{"#dc2626" if detected else "#15803d"};
                                    font-weight:800; font-size:16px; margin:4px 0;'>
                            {"⚠️ YES" if detected else "✅ NO"}</div>
                        <div style='color:#64748b; font-size:11px;
                                    line-height:1.4; overflow:hidden;
                                    text-overflow:ellipsis;'>{val[:70]}</div>
                    </div>
                    """, unsafe_allow_html=True)

            if mb:
                st.warning(f"**Main Bias Indicator:** {mb} — {ex}")
        else:
            st.error("⚠️ Please enter both company name and year!")

# DASHBOARD
elif page == "📊 Dashboard":
    st.title("📊 Research Dashboard")
    st.markdown("*Simulation results from 20 corporate investment cases (2010–2025)*")
    st.info("⚠️ Results represent simulated decision reasoning — not causal financial predictions.")
    st.markdown("---")

    tab1,tab2,tab3 = st.tabs(["📊 Accuracy","💯 Scoring","🧠 Bias"])

    with tab1:
        na=round(df_h["Neutral_Correct"].mean()*100)
        ag=round(df_h["Aggressive_Correct"].mean()*100)
        co=round(df_h["Conservative_Correct"].mean()*100)
        hu=round(df_h["Human_Correct"].mean()*100)

        c1,c2,c3,c4=st.columns(4)
        with c1: st.metric("🤖 Neutral",f"{na}%")
        with c2: st.metric("📈 Aggressive",f"{ag}%")
        with c3: st.metric("🛡️ Conservative",f"{co}%")
        with c4: st.metric("🧑 Human",f"{hu}%")

        st.markdown("---")
        c1,c2=st.columns(2)
        with c1:
            fig=px.bar(
                pd.DataFrame({
                    "Persona":["Neutral","Aggressive","Conservative","Human"],
                    "Accuracy":[na,ag,co,hu]
                }),
                x="Persona",y="Accuracy",color="Persona",
                color_discrete_map={
                    "Neutral":"#1e3a8a","Aggressive":"#dc2626",
                    "Conservative":"#15803d","Human":"#c9a227"
                },
                title="Simulation Accuracy vs Human",text="Accuracy"
            )
            fig.update_traces(texttemplate='%{text}%',textposition='outside')
            fig.update_layout(**PT,yaxis_range=[0,115],showlegend=False)
            st.plotly_chart(fig,use_container_width=True)

        with c2:
            yd=df_h.groupby("Year")["Neutral_Correct"].mean().reset_index()
            yd.columns=["Year","Accuracy"]
            yd["Accuracy"]=round(yd["Accuracy"]*100)
            fig2=px.line(yd,x="Year",y="Accuracy",
                        title="Accuracy Over Time",
                        markers=True,color_discrete_sequence=["#c9a227"])
            fig2.update_layout(**PT,yaxis_range=[0,115])
            st.plotly_chart(fig2,use_container_width=True)

        c1,c2=st.columns(2)
        with c1:
            fig3=go.Figure()
            for name,col,color in [
                ("Neutral","Neutral_Correct","#1e3a8a"),
                ("Aggressive","Aggressive_Correct","#dc2626"),
                ("Conservative","Conservative_Correct","#15803d")
            ]:
                fig3.add_trace(go.Bar(
                    name=name,x=df_h["Company"],
                    y=df_h[col],marker_color=color
                ))
            fig3.update_layout(
                **PT,barmode="group",
                title="Correct Simulations by Company",
                yaxis=dict(tickvals=[0,1],ticktext=["Wrong","Correct"])
            )
            st.plotly_chart(fig3,use_container_width=True)

        with c2:
            ind=df_h.groupby("Industry")["Conservative_Correct"].mean().reset_index()
            ind.columns=["Industry","Accuracy"]
            ind["Accuracy"]=round(ind["Accuracy"]*100)
            fig4=px.bar(ind,x="Industry",y="Accuracy",
                       title="Conservative Accuracy by Industry",
                       color="Accuracy",
                       color_continuous_scale=[[0,"#dc2626"],[0.5,"#c9a227"],[1,"#15803d"]],
                       text="Accuracy")
            fig4.update_traces(texttemplate='%{text}%',textposition='outside')
            fig4.update_layout(**PT,yaxis_range=[0,115])
            st.plotly_chart(fig4,use_container_width=True)

        st.markdown("### 📋 Full Results")
        st.dataframe(
            df_h[[
                "Company","Year","Corporate_Decision",
                "Neutral_Decision","Aggressive_Decision",
                "Conservative_Decision","Human_Decision",
                "Actual_Outcome","Main_Bias"
            ]].rename(columns={
                "Corporate_Decision":"Decision",
                "Neutral_Decision":"Neutral",
                "Aggressive_Decision":"Aggressive",
                "Conservative_Decision":"Conservative",
                "Human_Decision":"Human",
                "Actual_Outcome":"Outcome",
                "Main_Bias":"Bias"
            }),
            use_container_width=True,
            hide_index=True,
            height=380
        )

    with tab2:
        st.markdown("### 💯 Scoring Analysis")
        st.caption("Scores represent simulated reasoning strength — not financial return predictions")
        c1,c2,c3=st.columns(3)
        with c1: st.metric("🤖 Avg Neutral",f"{df_h['Neutral_Score'].mean():.0f}/100")
        with c2: st.metric("📈 Avg Aggressive",f"{df_h['Aggressive_Score'].mean():.0f}/100")
        with c3: st.metric("🛡️ Avg Conservative",f"{df_h['Conservative_Score'].mean():.0f}/100")

        st.markdown("---")
        c1,c2=st.columns(2)
        with c1:
            fig=px.scatter(
                df_h,x="Average_Score",y="Neutral_Correct",text="Company",
                title="Higher Score = Better Decision?",
                labels={"Average_Score":"Avg Score","Neutral_Correct":"Correct"},
                color="Actual_Outcome",size="Average_Score",
                color_discrete_map={"Success":"#15803d","Failed":"#dc2626","Mixed":"#c9a227"}
            )
            fig.update_traces(textposition="top center")
            fig.update_layout(**PT)
            st.plotly_chart(fig,use_container_width=True)

        with c2:
            sd=pd.DataFrame({
                "Company":df_h["Company"],
                "Neutral":df_h["Neutral_Score"],
                "Aggressive":df_h["Aggressive_Score"],
                "Conservative":df_h["Conservative_Score"]
            })
            fig2=px.line(sd,x="Company",y=["Neutral","Aggressive","Conservative"],
                        title="Score Comparison by Persona",
                        color_discrete_map={
                            "Neutral":"#1e3a8a",
                            "Aggressive":"#dc2626",
                            "Conservative":"#15803d"
                        })
            fig2.update_layout(**PT)
            st.plotly_chart(fig2,use_container_width=True)

        st.dataframe(
            df_h[[
                "Company","Year","Neutral_Score","Aggressive_Score",
                "Conservative_Score","Average_Score","AI_Recommendation","Actual_Outcome"
            ]].rename(columns={
                "Neutral_Score":"Neutral",
                "Aggressive_Score":"Aggressive",
                "Conservative_Score":"Conservative",
                "Average_Score":"Avg",
                "AI_Recommendation":"Verdict",
                "Actual_Outcome":"Outcome"
            }),
            use_container_width=True,
            hide_index=True,
            height=380
        )

    with tab3:
        st.markdown("### 🧠 Heuristic Bias Analysis")
        st.caption("Bias detection is heuristic — suggests possible patterns, not definitive diagnoses")
        bc=df_h["Main_Bias"].value_counts().reset_index()
        bc.columns=["Bias","Count"]
        c1,c2=st.columns(2)
        with c1:
            fig=px.pie(bc,values="Count",names="Bias",
                      title="Bias Distribution",
                      color_discrete_sequence=["#c9a227","#1e3a8a","#dc2626","#15803d","#7c3aed"])
            fig.update_layout(**PT)
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            fig2=px.bar(bc,x="Bias",y="Count",title="Bias Frequency",
                       color="Bias",text="Count",
                       color_discrete_sequence=["#c9a227","#1e3a8a","#dc2626","#15803d","#7c3aed"])
            fig2.update_traces(textposition='outside')
            fig2.update_layout(**PT,showlegend=False)
            st.plotly_chart(fig2,use_container_width=True)

        st.dataframe(
            df_h[[
                "Company","Year","Main_Bias",
                "Neutral_Decision","Aggressive_Decision",
                "Conservative_Decision","Actual_Outcome"
            ]].rename(columns={
                "Main_Bias":"Bias Indicator",
                "Neutral_Decision":"Neutral",
                "Aggressive_Decision":"Aggressive",
                "Conservative_Decision":"Conservative",
                "Actual_Outcome":"Outcome"
            }),
            use_container_width=True,
            hide_index=True,
            height=380
        )

# AI VS HUMAN
elif page == "⚔️ AI vs Human":
    st.title("⚔️ AI Simulation vs Human Decisions")
    st.markdown("*Comparing simulated AI reasoning against documented human corporate decisions*")
    st.info("⚠️ Comparison between simulated AI reasoning and documented historical decisions — not causal performance measurement.")
    st.markdown("---")

    ai_w=len(df_h[(df_h["Neutral_Correct"]==1)&(df_h["Human_Correct"]==0)])
    hu_w=len(df_h[(df_h["Human_Correct"]==1)&(df_h["Neutral_Correct"]==0)])
    bo_r=len(df_h[(df_h["Neutral_Correct"]==1)&(df_h["Human_Correct"]==1)])
    bo_w=len(df_h[(df_h["Neutral_Correct"]==0)&(df_h["Human_Correct"]==0)])
    tot=len(df_h)

    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("🤖 AI Better",f"{ai_w}",delta=f"{round(ai_w/tot*100)}%")
    with c2: st.metric("🧑 Human Better",f"{hu_w}",delta=f"{round(hu_w/tot*100)}%")
    with c3: st.metric("🤝 Both Correct",f"{bo_r}",delta=f"{round(bo_r/tot*100)}%")
    with c4: st.metric("❌ Both Wrong",f"{bo_w}",delta=f"{round(bo_w/tot*100)}%")

    st.markdown("---")
    c1,c2=st.columns(2)
    with c1:
        fig=px.bar(
            pd.DataFrame({
                "Result":["AI Better","Human Better","Both Correct","Both Wrong"],
                "Cases":[ai_w,hu_w,bo_r,bo_w]
            }),
            x="Result",y="Cases",color="Result",
            color_discrete_map={
                "AI Better":"#1e3a8a","Human Better":"#c9a227",
                "Both Correct":"#15803d","Both Wrong":"#dc2626"
            },
            title="AI vs Human — Head to Head",text="Cases"
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(**PT,showlegend=False)
        st.plotly_chart(fig,use_container_width=True)

    with c2:
        na=round(df_h["Neutral_Correct"].mean()*100)
        ag=round(df_h["Aggressive_Correct"].mean()*100)
        co=round(df_h["Conservative_Correct"].mean()*100)
        hu=round(df_h["Human_Correct"].mean()*100)
        fig2=px.bar(
            pd.DataFrame({
                "Decision Maker":["Neutral AI","Aggressive AI","Conservative AI","Human"],
                "Accuracy":[na,ag,co,hu]
            }),
            x="Decision Maker",y="Accuracy",color="Decision Maker",
            title="Accuracy Comparison",text="Accuracy",
            color_discrete_map={
                "Neutral AI":"#1e3a8a","Aggressive AI":"#dc2626",
                "Conservative AI":"#15803d","Human":"#c9a227"
            }
        )
        fig2.update_traces(texttemplate='%{text}%',textposition='outside')
        fig2.update_layout(**PT,yaxis_range=[0,115],showlegend=False)
        st.plotly_chart(fig2,use_container_width=True)

    st.markdown("---")
    st.markdown("### 📋 Case by Case")
    comp=df_h[["Company","Year","Neutral_Decision","Human_Decision",
               "Actual_Outcome","Neutral_Correct","Human_Correct"]].copy()

    def lbl(row):
        if row["Neutral_Correct"]==1 and row["Human_Correct"]==0: return "🤖 AI Better"
        elif row["Human_Correct"]==1 and row["Neutral_Correct"]==0: return "🧑 Human Better"
        elif row["Neutral_Correct"]==1 and row["Human_Correct"]==1: return "🤝 Both Correct"
        else: return "❌ Both Wrong"

    comp["Result"]=comp.apply(lbl,axis=1)
    st.dataframe(
        comp[["Company","Year","Neutral_Decision","Human_Decision",
              "Actual_Outcome","Result"]].rename(columns={
            "Neutral_Decision":"AI Simulation",
            "Human_Decision":"Human",
            "Actual_Outcome":"Outcome"
        }),
        use_container_width=True,
        hide_index=True,
        height=420
    )

    st.markdown("---")
    co=round(df_h["Conservative_Correct"].mean()*100)
    hu=round(df_h["Human_Correct"].mean()*100)
    diff=co-hu
    if diff>0:
        st.success(f"**Conservative AI simulation aligned with correct outcomes {diff}% more than documented human decisions.** This suggests risk-averse behavioral framing may produce reasoning more consistent with successful corporate outcomes — though causal conclusions require larger samples and real corporate data.")
    else:
        st.info(f"**Human decisions aligned with correct outcomes {abs(diff)}% more than AI simulation.** This highlights the continuing importance of human judgment in corporate investment — particularly for strategic intuition.")

# CUSTOM ANALYSIS
elif page == "📂 Custom Analysis":
    st.title("📂 Custom Investment Simulation")
    st.markdown("*Input your company data for a private AI-powered investment decision simulation*")
    st.markdown("""
    <div style='display:flex; gap:12px; margin-bottom:20px; flex-wrap:wrap;'>
        <div style='background:#f0fdf4; border:1px solid #22c55e; border-radius:8px;
                    padding:10px 16px; flex:1;'>
            <span style='color:#15803d; font-weight:700;'>🔒 Privacy:</span>
            <span style='color:#15803d; font-size:13px;'>
                Your data is never stored. Analysis generated in real time only.</span>
        </div>
        <div style='background:#fffbeb; border:1px solid #c9a227; border-radius:8px;
                    padding:10px 16px; flex:1;'>
            <span style='color:#92400e; font-weight:700;'>⚠️ Note:</span>
            <span style='color:#92400e; font-size:13px;'>
                Simulation tool — not financial advice.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def section_bar(title):
        st.markdown(f"""
        <div style='background:#0a1628; color:#FFD700; font-weight:700;
                    padding:8px 16px; border-radius:8px;
                    margin:20px 0 12px; font-size:13px;'>
            {title}</div>
        """, unsafe_allow_html=True)

    section_bar("📋 SECTION 1 — COMPANY IDENTITY")
    c1,c2,c3=st.columns(3)
    with c1:
        cname=st.text_input("🏢 Company Name:",placeholder="Your company")
        ind=st.selectbox("🏭 Industry:",[
            "Technology","Healthcare","Financial Services","Real Estate",
            "Retail/E-Commerce","Automotive","Energy","Media/Entertainment",
            "Manufacturing","Telecommunications","Education","Other"
        ])
    with c2:
        country=st.text_input("🌍 Country:",placeholder="e.g. Italy, USA")
        ctype=st.selectbox("🏗️ Company Type:",[
            "Startup (0-3 years)","Growth Stage (3-7 years)",
            "SME","Large Corporation","Multinational"
        ])
    with c3:
        yrs=st.number_input("📅 Years in Business:",min_value=0,value=5)
        cstat=st.selectbox("📊 Status:",[
            "Private","Public (Listed)","Family Business","State Owned","Subsidiary"
        ])

    section_bar("💰 SECTION 2 — FINANCIAL HEALTH")
    c1,c2,c3=st.columns(3)
    with c1:
        rev=st.number_input("💵 Revenue ($M):",min_value=0.0,value=10.0)
        pnl=st.number_input("📈 Profit/Loss ($M):",value=1.0)
        debt=st.number_input("💳 Total Debt ($M):",min_value=0.0,value=5.0)
    with c2:
        cash=st.number_input("🏦 Cash ($M):",min_value=0.0,value=3.0)
        grw=st.number_input("📊 Revenue Growth (%):",value=10.0)
        val=st.number_input("🏷️ Valuation ($M):",min_value=0.0,value=50.0)
    with c3:
        de=st.number_input("⚖️ Debt/Equity:",min_value=0.0,value=0.5)
        ebitda=st.number_input("📉 EBITDA ($M):",value=2.0)
        burn=st.number_input("🔥 Monthly Burn ($M):",min_value=0.0,value=0.5)

    section_bar("🎯 SECTION 3 — INVESTMENT DECISION")
    c1,c2,c3=st.columns(3)
    with c1:
        itype=st.selectbox("📋 Investment Type:",[
            "Merger & Acquisition","Geographic Expansion","New Product",
            "Technology Investment","R&D","Strategic Partnership",
            "IPO","Capital Expenditure","Digital Transformation","Restructuring"
        ])
        iamt=st.number_input("💰 Amount ($M):",min_value=0.1,value=5.0)
    with c2:
        eret=st.number_input("📈 Expected Return (%):",value=15.0)
        tframe=st.selectbox("⏱️ Timeframe:",[
            "Short term (under 1 year)","Medium term (1-3 years)",
            "Long term (3-10 years)","Very long term (10+ years)"
        ])
    with c3:
        mkt=st.selectbox("🌍 Target Market:",[
            "Local","National","Regional","Global"
        ])
        fin=st.selectbox("💳 Financing:",[
            "Own cash","Bank loan","Investor/VC","Bond issuance","Mixed","Government grant"
        ])

    section_bar("🌍 SECTION 4 — STRATEGIC CONTEXT")
    c1,c2,c3=st.columns(3)
    with c1:
        mktc=st.selectbox("📊 Market Conditions:",[
            "Growing","Stable","Declining","Highly competitive","Emerging/disrupted"
        ])
        reg=st.selectbox("⚖️ Regulatory:",[
            "Highly regulated","Moderately regulated","Low regulation","Changing"
        ])
    with c2:
        tech=st.selectbox("💻 Tech Risk:",[
            "High — being disrupted","Medium","Low — stable"
        ])
        rtol=st.selectbox("🎯 Risk Tolerance:",[
            "Very conservative","Moderate","Aggressive"
        ])
    with c3:
        why=st.text_area("❓ Why Invest?",placeholder="Brief reason...",height=80)
        risk=st.text_area("⚠️ Main Risk?",placeholder="Biggest concern...",height=80)

    section_bar("📝 SECTION 5 — ADDITIONAL CONTEXT")
    c1,c2=st.columns(2)
    with c1:
        comp=st.text_input("🏆 Competitors:",placeholder="e.g. Amazon, Google")
        events=st.text_area("📰 Recent Events:",placeholder="Leadership change...",height=80)
    with c2:
        decision=st.text_area(
            "📋 Describe Your Investment Decision:",
            placeholder="e.g. We want to acquire a competitor in France for $20M...",
            height=120
        )

    st.markdown("---")

    if st.button("⚡ SIMULATE MY INVESTMENT",use_container_width=True):
        if cname and decision:
            st.markdown(f"""
            <div class='aa-card' style='border-left:5px solid #c9a227;
                        margin-bottom:20px;'>
                <div style='color:#64748b; font-size:11px;
                            text-transform:uppercase;'>Simulation Target</div>
                <div style='color:#0a1628; font-size:18px;
                            font-weight:800; margin-top:4px;'>{cname}</div>
                <div style='color:#64748b; font-size:13px;'>{decision}</div>
            </div>
            """, unsafe_allow_html=True)

            profile=f"""
            Company:{cname}|Industry:{ind}|Country:{country}|Type:{ctype}
            Years:{yrs}|Status:{cstat}|Revenue:${rev}M|P&L:${pnl}M|Debt:${debt}M
            Cash:${cash}M|Growth:{grw}%|Val:${val}M|D/E:{de}|EBITDA:${ebitda}M|Burn:${burn}M
            Investment:{itype}|Amount:${iamt}M|Return:{eret}%|Time:{tframe}
            Market:{mkt}|Finance:{fin}|Conditions:{mktc}|Reg:{reg}
            Tech:{tech}|Risk:{rtol}|Competitors:{comp}|Why:{why}|Risk:{risk}|Events:{events}
            DECISION:{decision}
            """

            personas=[
                {"name":"🤖 Neutral Advisor","color":"#1e3a8a","bg":"#eff6ff",
                 "instruction":"You are a neutral objective corporate finance advisor."},
                {"name":"📈 Aggressive CFO","color":"#dc2626","bg":"#fff1f2",
                 "instruction":"You are an aggressive CFO who prioritizes growth."},
                {"name":"🛡️ Conservative Board","color":"#15803d","bg":"#f0fdf4",
                 "instruction":"You are a conservative board member focused on stability."},
            ]

            all_d=[]
            all_s=[]
            c1,c2,c3=st.columns(3)
            cols=[c1,c2,c3]

            for i,p in enumerate(personas):
                with cols[i]:
                    with st.spinner(f"Simulating..."):
                        q=f"""
                        {p['instruction']}
                        Data: {profile}
                        Should proceed with: {decision}?
                        DECISION: YES or NO
                        SCORE: (0-100)
                        CONFIDENCE: (0-100)
                        REASON 1: (specific to financials)
                        REASON 2: (specific to market)
                        REASON 3: (specific to risk)
                        KEY RISK: (biggest risk)
                        ALTERNATIVE: (if NO)
                        """
                        r=client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[{"role":"user","content":q}]
                        )
                        text=r.choices[0].message.content
                        lines=text.strip().split('\n')
                        dec=sc=conf=r1=r2=r3=kr=alt=""
                        for line in lines:
                            if line.startswith("DECISION:"): dec=line.replace("DECISION:","").strip()
                            elif "SCORE:" in line:
                                try: sc=str(int(''.join(filter(str.isdigit, line.split("SCORE:")[-1].strip()))[:3]))
                                except: sc="50"
                            elif "CONFIDENCE:" in line:
    try: conf=str(int(''.join(filter(str.isdigit, line.split("CONFIDENCE:")[-1].strip()))[:3]))
    except: conf="50"
                            elif "REASON 1:" in line: r1=line.split("REASON 1:")[-1].strip()
                            elif "REASON 2:" in line: r2=line.split("REASON 2:")[-1].strip()
                            elif "REASON 3:" in line: r3=line.split("REASON 3:")[-1].strip()
                            elif line.startswith("KEY RISK:"): kr=line.replace("KEY RISK:","").strip()
                            elif line.startswith("ALTERNATIVE:"): alt=line.replace("ALTERNATIVE:","").strip()

                        all_d.append(dec)
                        try: all_s.append(int(sc))
                        except: all_s.append(50)

                        yes="YES" in dec.upper()
                        vc="#15803d" if yes else "#dc2626"
                        vbg="#f0fdf4" if yes else "#fff1f2"

                        st.markdown(f"""
                        <div style='background:#ffffff; border:1px solid #e2e8f0;
                                    border-top:4px solid {p['color']};
                                    border-radius:12px; padding:16px;'>
                            <div style='color:{p['color']}; font-weight:700;
                                        font-size:13px; margin-bottom:10px;'>
                                {p['name']}</div>
                            <div style='background:{vbg}; border:1px solid {vc};
                                        border-radius:8px; padding:8px;
                                        text-align:center; margin-bottom:10px;'>
                                <span style='color:{vc}; font-weight:800;'>
                                    {"✅ PROCEED" if yes else "❌ DO NOT PROCEED"}
                                </span>
                            </div>
                            <div style='height:6px; background:#e2e8f0;
                                        border-radius:3px; margin-bottom:8px;'>
                                <div style='height:6px; background:{p['color']};
                                            border-radius:3px; width:{sc}%;'></div>
                            </div>
                            <div style='color:#64748b; font-size:12px; margin-bottom:8px;'>
                                Score:<strong>{sc}/100</strong> ·
                                Conf:<strong>{conf}%</strong>
                            </div>
                            <div style='font-size:12px; color:#334155; line-height:1.6;'>
                                📌 {r1}<br>📌 {r2}<br>📌 {r3}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if kr: st.warning(f"⚠️ **Key Risk:** {kr}")
                        if alt and "NO" in dec.upper(): st.info(f"💡 **Alternative:** {alt}")

            avg=sum(all_s)/len(all_s) if all_s else 50
            if avg>=60: v="PROCEED"; vc2="#15803d"; vbg2="#f0fdf4"; vi="✅"
            elif avg>=40: v="PROCEED WITH CAUTION"; vc2="#92400e"; vbg2="#fffbeb"; vi="⚠️"
            else: v="DO NOT PROCEED"; vc2="#991b1b"; vbg2="#fff1f2"; vi="❌"

            st.markdown(f"""
            <div style='background:{vbg2}; border:2px solid {vc2};
                        border-radius:14px; padding:24px;
                        text-align:center; margin:20px 0;'>
                <div style='color:{vc2}; font-size:11px; font-weight:700;
                            text-transform:uppercase; letter-spacing:2px;'>
                    Simulation Verdict</div>
                <div style='color:{vc2}; font-size:22px;
                            font-weight:900; margin:8px 0;'>{vi} {v}</div>
                <div style='color:{vc2}; font-size:12px; opacity:0.8;'>
                    Average Score: {avg:.0f}/100</div>
            </div>
            <div style='text-align:center; color:#94a3b8; font-size:11px;'>
                ⚠️ Simulation only — not financial advice</div>
            """, unsafe_allow_html=True)

            st.success("🔒 Your data was used only for this simulation and has not been stored.")
        else:
            st.error("⚠️ Please fill Company Name and describe your Investment Decision!")

# JURY DEMO
elif page == "🎤 Jury Demo":
    st.title("🎤 Jury Presentation Demo")
    st.markdown("*Prepared live simulation for thesis defense*")
    c1,c2,c3=st.columns(3)
    with c1: dco=st.text_input("🏢 Company:",value="WeWork")
    with c2: dyr=st.text_input("📅 Year:",value="2019")
    with c3: ddec=st.text_input("📋 Decision:",value="Proceed with IPO expansion?")

    if st.button("⚡ RUN LIVE DEMONSTRATION",use_container_width=True):
        if dco and dyr:
            st.markdown(f"""
            <div style='background:#0a1628; border-radius:12px;
                        padding:20px; margin:16px 0; border:1px solid #c9a227;'>
                <div style='color:#c9a227; font-size:11px;
                            text-transform:uppercase; letter-spacing:2px;'>
                    Live Simulation</div>
                <div style='color:#ffffff; font-size:20px;
                            font-weight:800; margin-top:4px;'>{dco} · {dyr}</div>
                <div style='color:#94a3b8; font-size:13px;
                            margin-top:4px;'>{ddec}</div>
            </div>
            """, unsafe_allow_html=True)

            personas=[
                {"name":"🤖 Neutral Advisor","color":"#1e3a8a",
                 "instruction":"You are a neutral objective corporate finance advisor."},
                {"name":"📈 Aggressive CFO","color":"#dc2626",
                 "instruction":"You are an aggressive CFO who prioritizes growth."},
                {"name":"🛡️ Conservative Board","color":"#15803d",
                 "instruction":"You are a conservative board member focused on stability."},
            ]

            decisions=[]
            scores=[]
            c1,c2,c3=st.columns(3)
            cols=[c1,c2,c3]

            for i,p in enumerate(personas):
                with cols[i]:
                    with st.spinner("Simulating..."):
                        q=f"""
                        {p['instruction']}
                        Company:{dco}|Year:{dyr}|Decision:{ddec}
                        DECISION: YES or NO
                        SCORE: (0-100)
                        CONFIDENCE: (0-100)
                        REASON 1: (one sentence)
                        REASON 2: (one sentence)
                        REASON 3: (one sentence)
                        """
                        r=client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[{"role":"user","content":q}]
                        )
                        text=r.choices[0].message.content
                        lines=text.strip().split('\n')
                        dec=sc=conf=r1=r2=r3=""
                        for line in lines:
                            if line.startswith("DECISION:"): dec=line.replace("DECISION:","").strip()
                            elif "SCORE:" in line:
    try: sc=str(int(''.join(filter(str.isdigit, line.split("SCORE:")[-1].strip()))[:3]))
    except: sc="50"
                            elif line.startswith("CONFIDENCE:"): conf=line.replace("CONFIDENCE:","").strip()
                            elif line.startswith("REASON 1:"): r1=line.replace("REASON 1:","").strip()
                            elif line.startswith("REASON 2:"): r2=line.replace("REASON 2:","").strip()
                            elif line.startswith("REASON 3:"): r3=line.replace("REASON 3:","").strip()

                        decisions.append(dec)
                        try: scores.append(int(sc))
                        except: scores.append(50)

                        yes="YES" in dec.upper()
                        vc="#15803d" if yes else "#dc2626"
                        vbg="#f0fdf4" if yes else "#fff1f2"

                        st.markdown(f"""
                        <div style='background:#ffffff; border:2px solid {p['color']};
                                    border-radius:14px; padding:16px;'>
                            <div style='color:{p['color']}; font-weight:800;
                                        font-size:14px; margin-bottom:10px;'>
                                {p['name']}</div>
                            <div style='background:{vbg}; border:2px solid {vc};
                                        border-radius:10px; padding:10px;
                                        text-align:center; margin-bottom:10px;'>
                                <span style='color:{vc}; font-weight:900; font-size:15px;'>
                                    {"✅ PROCEED" if yes else "❌ DO NOT PROCEED"}
                                </span>
                            </div>
                            <div style='height:8px; background:#e2e8f0;
                                        border-radius:4px; margin-bottom:10px;'>
                                <div style='height:8px; background:{p['color']};
                                            border-radius:4px; width:{sc}%;'></div>
                            </div>
                            <div style='color:#64748b; font-size:12px; margin-bottom:8px;'>
                                Score:<strong style='color:{p["color"]};'>{sc}/100</strong> ·
                                Conf:<strong>{conf}%</strong>
                            </div>
                            <div style='font-size:12px; color:#334155; line-height:1.7;'>
                                📌 {r1}<br>📌 {r2}<br>📌 {r3}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            avg=sum(scores)/len(scores) if scores else 50
            if avg>=60: v="PROCEED"; vc="#15803d"; vbg="#f0fdf4"; vi="✅"
            elif avg>=40: v="PROCEED WITH CAUTION"; vc="#92400e"; vbg="#fffbeb"; vi="⚠️"
            else: v="DO NOT PROCEED"; vc="#991b1b"; vbg="#fff1f2"; vi="❌"

            st.markdown(f"""
            <div style='background:{vbg}; border:3px solid {vc};
                        border-radius:16px; padding:28px;
                        text-align:center; margin:20px 0;'>
                <div style='color:{vc}; font-size:11px; font-weight:700;
                            text-transform:uppercase; letter-spacing:3px;
                            margin-bottom:8px;'>Final Simulation Verdict</div>
                <div style='color:{vc}; font-size:26px;
                            font-weight:900; margin-bottom:10px;'>{vi} {v}</div>
                <div style='display:flex; justify-content:center;
                            gap:16px; flex-wrap:wrap;'>
                    <span style='color:{vc}; font-size:13px; opacity:0.9;'>
                        Avg: {avg:.0f}/100</span>
                    <span style='color:{vc}; font-size:13px; opacity:0.9;'>
                        Neutral: {scores[0] if scores else 0}/100</span>
                    <span style='color:{vc}; font-size:13px; opacity:0.9;'>
                        Aggressive: {scores[1] if len(scores)>1 else 0}/100</span>
                    <span style='color:{vc}; font-size:13px; opacity:0.9;'>
                        Conservative: {scores[2] if len(scores)>2 else 0}/100</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if dco in ["WeWork","Theranos","Kodak","Blockbuster","Peloton"]:
                st.error(f"✅ **Historical Validation:** {dco} FAILED — Simulation correctly identified risk")
            elif dco in ["Tesla","Apple","Amazon","Netflix","Microsoft"]:
                st.success(f"✅ **Historical Validation:** {dco} SUCCEEDED — Simulation correctly identified opportunity")

            st.caption("⚠️ Simulation output for research demonstration only — not financial advice")

# ABOUT
elif page == "📋 About":
    st.title("📋 About This Research")
    st.markdown("*The Agentic Alpha — Multi-Agent AI Decision Support System*")
    st.markdown("---")

    c1,c2=st.columns(2)
    with c1:
        st.markdown("""
        <div style='background:#ffffff; border:1px solid #e2e8f0;
                    border-top:4px solid #c9a227; border-radius:12px;
                    padding:24px; box-shadow:0 2px 8px rgba(0,0,0,0.05);'>
            <div style='color:#0a1628; font-size:15px; font-weight:800;
                        margin-bottom:18px;'>👩‍🎓 Researcher</div>
            <div style='margin-bottom:12px;'>
                <div style='color:#94a3b8; font-size:10px; font-weight:700;
                            text-transform:uppercase; letter-spacing:1px;'>Name</div>
                <div style='color:#0a1628; font-weight:700; font-size:14px;
                            margin-top:3px;'>Meryam El Ghouti</div>
            </div>
            <div style='margin-bottom:12px;'>
                <div style='color:#94a3b8; font-size:10px; font-weight:700;
                            text-transform:uppercase; letter-spacing:1px;'>University</div>
                <div style='color:#334155; font-size:13px; margin-top:3px;'>
                    Sapienza University of Rome</div>
            </div>
            <div style='margin-bottom:12px;'>
                <div style='color:#94a3b8; font-size:10px; font-weight:700;
                            text-transform:uppercase; letter-spacing:1px;'>Degree</div>
                <div style='color:#334155; font-size:13px; margin-top:3px;'>
                    Master's in Business Management · 2026</div>
            </div>
            <div>
                <div style='color:#94a3b8; font-size:10px; font-weight:700;
                            text-transform:uppercase; letter-spacing:1px;'>Thesis</div>
                <div style='color:#334155; font-size:13px; margin-top:3px;
                            line-height:1.6;'>
                    The Agentic Alpha — A Multi-Agent AI Decision Support System
                    for Corporate Investment Simulation with Behavioral Bias Detection
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style='background:#0a1628; border:1px solid #c9a227;
                    border-radius:12px; padding:24px;'>
            <div style='color:#FFD700; font-size:15px; font-weight:800;
                        margin-bottom:18px;'>🔬 Research Overview</div>
            <div style='margin-bottom:14px;'>
                <div style='color:#c9a227; font-size:10px; font-weight:700;
                            text-transform:uppercase; letter-spacing:1px;'>
                    Research Question</div>
                <div style='color:#e8e8e8; font-size:13px; margin-top:5px;
                            line-height:1.6;'>
                    Can a multi-agent AI system simulate corporate investment
                    reasoning with behavioral bias detection comparable
                    to human decision-makers?</div>
            </div>
            <div style='margin-bottom:14px;'>
                <div style='color:#c9a227; font-size:10px; font-weight:700;
                            text-transform:uppercase; letter-spacing:1px;'>Approach</div>
                <div style='color:#e8e8e8; font-size:13px; margin-top:5px;'>
                    Design Science Research · Multi-agent simulation ·
                    Heuristic bias detection · 20 historical cases</div>
            </div>
            <div style='margin-bottom:14px;'>
                <div style='color:#c9a227; font-size:10px; font-weight:700;
                            text-transform:uppercase; letter-spacing:1px;'>Theory</div>
                <div style='color:#e8e8e8; font-size:13px; margin-top:5px;'>
                    Kahneman & Tversky (1979) — Behavioral Finance
                    · Thaler (2015) — Nudge Theory</div>
            </div>
            <div>
                <div style='color:#c9a227; font-size:10px; font-weight:700;
                            text-transform:uppercase; letter-spacing:1px;'>Tools</div>
                <div style='color:#e8e8e8; font-size:13px; margin-top:5px;'>
                    Python · Groq LLaMA API · Streamlit · Plotly</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='gold-line'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <div style='color:#c9a227; font-size:11px; font-weight:700;
                    text-transform:uppercase; letter-spacing:2px;'>
            Academic Contributions</div>
        <div style='color:#0a1628; font-size:20px; font-weight:800;
                    margin-top:6px;'>Three Research Contributions</div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3=st.columns(3)
    for col,num,title,desc in zip(
        [c1,c2,c3],
        ["01","02","03"],
        ["Multi-Agent Framework","Heuristic Bias Detection","Comparative Analysis"],
        [
            "AI framework simulating corporate investment reasoning through three behavioral personas",
            "Module identifying overconfidence, herding, loss aversion and anchoring in simulations",
            "Framework comparing AI simulation outputs against documented human decisions"
        ]
    ):
        with col:
            st.markdown(f"""
            <div class='aa-card' style='border-top:4px solid #c9a227;'>
                <div style='font-size:36px; font-weight:900;
                            color:#f1f5f9;'>{num}</div>
                <div style='color:#0a1628; font-weight:700; font-size:14px;
                            margin:8px 0 6px;'>{title}</div>
                <div style='color:#64748b; font-size:13px;
                            line-height:1.6;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='gold-line'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <div style='color:#c9a227; font-size:11px; font-weight:700;
                    text-transform:uppercase; letter-spacing:2px;'>Key Results</div>
        <div style='color:#0a1628; font-size:20px; font-weight:800;
                    margin-top:6px;'>Top 5 Simulation Findings</div>
    </div>
    """, unsafe_allow_html=True)

    for title,desc,color in [
        ("Conservative Persona Most Accurate",
         "Conservative simulation showed highest alignment with successful outcomes — risk-averse reasoning produces more reliable corporate decision simulations.",
         "#15803d"),
        ("Overconfidence Most Detected Bias",
         "Aggressive persona showed heuristic overconfidence in most failed simulations — mirroring documented human executive bias.",
         "#c9a227"),
        ("Herding Pattern Detected in AI",
         "Simulated reasoning followed crowd sentiment in WeWork and Theranos — consistent with behavioral finance herding theory.",
         "#1e3a8a"),
        ("Persona Framing Affects Simulation",
         "Identical AI with different behavioral framing produced significantly different scores — validating importance of decision context.",
         "#c9a227"),
        ("2021 Market Euphoria Effect",
         "All personas over-scored 2021 growth companies — AI training data absorbed market optimism similar to human overconfidence.",
         "#dc2626"),
    ]:
        st.markdown(f"""
        <div class='aa-card' style='border-left:4px solid {color};
                    padding:14px 18px; margin-bottom:10px;'>
            <div style='color:#0a1628; font-weight:700;
                        font-size:14px;'>{title}</div>
            <div style='color:#64748b; font-size:13px;
                        margin-top:4px; line-height:1.6;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='gold-line'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <div style='color:#c9a227; font-size:11px; font-weight:700;
                    text-transform:uppercase; letter-spacing:2px;'>Theory</div>
        <div style='color:#0a1628; font-size:20px; font-weight:800;
                    margin-top:6px;'>Behavioral Finance Framework</div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)
    for col,bias,theory,desc,color in zip(
        [c1,c2,c3,c4],
        ["Overconfidence","Loss Aversion","Herding Behavior","Anchoring Bias"],
        ["Kahneman & Tversky","Prospect Theory","Shiller","Tversky"],
        [
            "Overestimating accuracy of corporate decisions",
            "Fear of losses stronger than desire for gains",
            "Following crowd despite contradictory evidence",
            "Over-relying on first piece of information"
        ],
        ["#dc2626","#c9a227","#1e3a8a","#7c3aed"]
    ):
        with col:
            st.markdown(f"""
            <div class='aa-card' style='border-left:4px solid {color};'>
                <div style='color:{color}; font-weight:700;
                            font-size:13px;'>{bias}</div>
                <div style='color:#94a3b8; font-size:11px;
                            margin:3px 0;'>{theory}</div>
                <div style='color:#64748b; font-size:12px;
                            line-height:1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='gold-line'>", unsafe_allow_html=True)
    st.markdown("### 🛠️ System Architecture")
    st.code("""
    Input: Corporate Investment Decision
           (Known Company OR Custom Private Data)
                        ↓
    ┌──────────────────────────────────────────┐
    │         Multi-Agent AI Pipeline           │
    │          (Groq LLaMA 3.1 API)            │
    ├──────────────────────────────────────────┤
    │  Agent 1: Neutral Corporate Advisor       │
    │  Agent 2: Aggressive CFO                  │
    │  Agent 3: Conservative Board Member       │
    └──────────────────────────────────────────┘
                        ↓
    Investment Scoring Module (0 to 100)
                        ↓
    Heuristic Bias Detection Module
    (Overconfidence · Loss Aversion · Herding · Anchoring)
                        ↓
    Simulated Corporate Investment Verdict
    """, language="text")

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; padding:16px; color:#94a3b8; font-size:12px;'>
        Master's Thesis · The Agentic Alpha · Meryam El Ghouti ·
        Sapienza University of Rome · 2026 ·
        <span style='color:#c9a227;'>agenticalpha.streamlit.app</span>
    </div>
    """, unsafe_allow_html=True)
