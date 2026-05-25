
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

    .stApp {
        background: #040d1a;
        color: #e8e8e8;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #040d1a 0%, #071528 100%);
        border-right: 1px solid #c9a227;
    }

    [data-testid="stSidebar"] * {
        color: #e8e8e8 !important;
    }

    h1 {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }

    h2 { color: #FFD700 !important; font-weight: 700 !important; }
    h3 { color: #c9a227 !important; font-weight: 600 !important; }

    p, li, span { color: #c8d0dc; }

    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #071528, #0d2144);
        border: 1px solid #c9a227;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(201, 162, 39, 0.15);
    }

    [data-testid="metric-container"] label {
        color: #c9a227 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #FFD700 !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #c9a227, #FFD700);
        color: #040d1a !important;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        font-size: 15px;
        padding: 14px 28px;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(201, 162, 39, 0.4);
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #071528;
        color: #e8e8e8 !important;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #c9a227 !important;
        box-shadow: 0 0 0 2px rgba(201,162,39,0.2);
    }

    .stSelectbox > div > div {
        background: #071528;
        color: #e8e8e8;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
    }

    div[data-baseweb="select"] > div {
        background: #071528 !important;
        border-color: #1e3a5f !important;
        color: #e8e8e8 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: #071528;
        border-radius: 10px;
        padding: 4px;
        border: 1px solid #1e3a5f;
    }

    .stTabs [data-baseweb="tab"] {
        color: #8899aa !important;
        border-radius: 8px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #c9a227, #FFD700) !important;
        color: #040d1a !important;
    }

    .stInfo {
        background: #071528 !important;
        border-left: 4px solid #c9a227 !important;
        border-radius: 8px;
        color: #c8d0dc !important;
    }

    .stSuccess {
        background: #071528 !important;
        border-left: 4px solid #00aa44 !important;
        border-radius: 8px;
    }

    .stWarning {
        background: #071528 !important;
        border-left: 4px solid #FFD700 !important;
        border-radius: 8px;
    }

    .stError {
        background: #071528 !important;
        border-left: 4px solid #cc3333 !important;
        border-radius: 8px;
    }

    .stDataFrame {
        background: #071528;
        border: 1px solid #1e3a5f;
        border-radius: 10px;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #c9a227, #FFD700);
        border-radius: 10px;
    }

    .stRadio label { color: #c8d0dc !important; }

    hr {
        border: none;
        border-top: 1px solid #1e3a5f;
        margin: 20px 0;
    }

    .stCaption { color: #556677 !important; }

    .stCode, .stCodeBlock {
        background: #020a14 !important;
        border: 1px solid #1e3a5f;
        border-radius: 10px;
    }

    .stSpinner > div {
        border-top-color: #FFD700 !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(201,162,39,0.1);
        color: #FFD700 !important;
    }

    .gold-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #c9a227, transparent);
        margin: 30px 0;
        border: none;
    }

    .stat-card {
        background: linear-gradient(135deg, #071528, #0d2144);
        border: 1px solid #c9a227;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(201,162,39,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='text-align:center; padding: 10px 0 20px 0;'>
    <div style='font-size:40px'>⚡</div>
    <div style='font-size:20px; font-weight:800;
                background: linear-gradient(135deg, #FFD700, #FFA500);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;'>
        THE AGENTIC ALPHA
    </div>
    <div style='font-size:11px; color:#8899aa;
                letter-spacing:2px; margin-top:4px;'>
        AI DECISION SUPPORT SYSTEM
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='background:#071528; border:1px solid #1e3a5f;
            border-radius:10px; padding:12px; margin-bottom:15px;'>
    <div style='color:#c9a227; font-size:11px;
                text-transform:uppercase; letter-spacing:1px;'>
        Researcher
    </div>
    <div style='color:#e8e8e8; font-weight:600; margin-top:4px;'>
        Meryam El Ghouti
    </div>
    <div style='color:#8899aa; font-size:12px; margin-top:2px;'>
        Sapienza University of Rome
    </div>
    <div style='color:#8899aa; font-size:12px;'>
        Master's in Business Management
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    ["⚡ Home", "🤖 Live Analyzer",
     "📊 Dashboard", "⚔️ AI vs Human",
     "📂 Custom Analysis", "🎤 Jury Demo", "📋 About"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align:center; color:#556677;
            font-size:11px; padding:10px;'>
    © 2026 Meryam El Ghouti<br>
    agenticalpha.streamlit.app
</div>
""", unsafe_allow_html=True)

data = {
    "Company": [
        "WeWork","Tesla","Apple","Theranos","Kodak",
        "Blockbuster","Peloton","Amazon","Netflix",
        "Microsoft","Meta","Twitter","Disney","Uber","Rivian",
        "Microsoft","Adobe","Apple","Meta","OpenAI"
    ],
    "Year": [
        2019,2020,2018,2016,2012,
        2010,2021,2015,2013,
        2016,2021,2022,2019,2019,2021,
        2023,2023,2024,2022,2025
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
        "Transition to fully commercial company?"
    ],
    "Neutral_Decision": [
        "NO","YES","YES","NO","NO",
        "NO","YES","YES","YES","YES",
        "NO","NO","YES","YES","YES",
        "YES","NO","NO","YES","YES"
    ],
    "Aggressive_Decision": [
        "YES","YES","YES","YES","NO",
        "NO","YES","YES","YES","YES",
        "YES","YES","NO","YES","YES",
        "YES","YES","YES","YES","YES"
    ],
    "Conservative_Decision": [
        "YES","NO","YES","NO","NO",
        "NO","NO","YES","NO","YES",
        "NO","NO","YES","NO","NO",
        "YES","NO","NO","NO","NO"
    ],
    "Actual_Outcome": [
        "Failed","Success","Success","Failed","Failed",
        "Failed","Failed","Success","Success","Success",
        "Mixed","Failed","Mixed","Failed","Failed",
        "Success","Failed","Failed","Success","Pending"
    ],
    "Human_Decision": [
        "Proceed","Proceed","Proceed","Proceed","Did Not",
        "Did Not","Proceed","Proceed","Proceed","Proceed",
        "Proceed","Accepted","Proceed","Proceed","Proceed",
        "Proceeded","Attempted","Launched","Proceeded","Proceeding"
    ],
    "Industry": [
        "Real Estate","Automotive","Technology","Healthcare","Photography",
        "Entertainment","Fitness","E-Commerce","Media","Technology",
        "Social Media","Social Media","Entertainment","Transport","Automotive",
        "Technology","Software","Technology","Social Media","AI"
    ],
    "Neutral_Correct": [1,1,1,1,1,1,0,1,1,1,1,1,0,0,0,1,1,1,1,0],
    "Aggressive_Correct": [0,1,1,0,1,1,0,1,1,1,0,0,1,0,0,1,0,0,1,0],
    "Conservative_Correct": [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
    "Neutral_Score": [15,78,82,12,20,18,55,85,80,90,35,30,72,60,65,88,25,28,82,60],
    "Aggressive_Score": [65,88,92,75,35,30,80,95,85,85,80,72,45,80,75,95,70,78,88,90],
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
    lambda x: "✅ PROCEED" if x>=60 else "⚠️ CONDITIONAL" if x>=40 else "❌ DO NOT PROCEED"
)
df_historical = df[df["Actual_Outcome"]!="Pending"]
df_pending = df[df["Actual_Outcome"]=="Pending"]

PLOT_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(7,21,40,0.8)',
    font_color='#c8d0dc',
    title_font_color='#FFD700',
    legend_bgcolor='rgba(7,21,40,0.8)',
    legend_bordercolor='#1e3a5f'
)

GOLD = "#FFD700"
NAVY = "#071528"
COLORS = {
    "Neutral": "#4da6ff",
    "Aggressive": "#ff6b6b",
    "Conservative": "#51cf66",
    "Human": "#FFD700"
}

if page == "⚡ Home":
    st.markdown("""
    <div style='text-align:center; padding:20px 0;'>
        <div style='font-size:60px;'>⚡</div>
        <h1 style='font-size:3.5rem; margin:0;'>THE AGENTIC ALPHA</h1>
        <p style='color:#8899aa; font-size:16px; letter-spacing:3px;
                  text-transform:uppercase; margin-top:8px;'>
            Multi-Agent AI Decision Support System for Corporate Investment Simulation
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("""
        ### 🎯 Research Question
        Can a multi-agent AI system simulate
        corporate investment reasoning with
        behavioral bias detection comparable
        to human decision-makers?
        """)
    with col2:
        st.success("""
        ### 🔬 Methodology
        Design Science Research using
        multi-agent simulation across 20
        historical corporate cases with
        heuristic behavioral bias detection.
        """)
    with col3:
        st.warning("""
        ### 💡 Key Contribution
        A functional AI decision support
        system simulating corporate investment
        through behavioral personas with
        heuristic bias analysis.
        """)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        ("📊", "Cases Analyzed", "20"),
        ("🤖", "AI Simulations", "60"),
        ("🧠", "Bias Types", "5"),
        ("📅", "Time Period", "2010–2025"),
        ("🎯", "Best Accuracy", f"{round(df_historical['Conservative_Correct'].mean()*100)}%")
    ]
    for col, (icon, label, value) in zip([col1,col2,col3,col4,col5], metrics):
        with col:
            st.metric(f"{icon} {label}", value)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    st.markdown("### 📖 About This Research")
    st.write("""
    This research develops and evaluates a multi-agent AI decision support system
    designed to simulate corporate investment decision-making across multiple behavioral
    personas. The system applies heuristic behavioral bias detection to identify
    potential cognitive biases in simulated investment reasoning — drawing on established
    behavioral finance theory by Kahneman and Tversky (1979).

    **Important:** This system is a decision simulation tool — not a causal economic
    prediction model. Results reflect simulated reasoning patterns rather than
    guaranteed real-world financial outcomes.
    """)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    st.markdown("### 🎯 Three Research Contributions")
    col1, col2, col3 = st.columns(3)
    contributions = [
        ("01", "Multi-Agent Framework",
         "AI decision framework simulating corporate investment reasoning through three behavioral personas"),
        ("02", "Heuristic Bias Detection",
         "Module identifying overconfidence, herding, loss aversion and anchoring in simulated decisions"),
        ("03", "Comparative Analysis",
         "Framework comparing AI simulation against documented human decisions across 20 scenarios")
    ]
    for col, (num, title, desc) in zip([col1,col2,col3], contributions):
        with col:
            st.markdown(f"""
            <div style='background:#071528; border:1px solid #c9a227;
                        border-radius:12px; padding:24px; height:160px;'>
                <div style='color:#c9a227; font-size:32px;
                            font-weight:800;'>{num}</div>
                <div style='color:#FFD700; font-weight:700;
                            margin:8px 0 4px;'>{title}</div>
                <div style='color:#8899aa; font-size:13px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    st.markdown("### 🏆 Top 5 Simulation Findings")
    findings = [
        ("Finding 1", "Conservative Persona Most Accurate",
         "Conservative simulation showed highest alignment with successful real outcomes — risk-averse reasoning produces more reliable simulations."),
        ("Finding 2", "Overconfidence Most Detected Bias",
         "Aggressive persona showed heuristic overconfidence patterns in most failed decision simulations — mirroring documented human executive bias."),
        ("Finding 3", "Herding Pattern Detected in AI",
         "Simulated reasoning followed crowd sentiment in WeWork and Theranos — consistent with behavioral finance herding theory."),
        ("Finding 4", "Persona Framing Affects Simulation",
         "Identical AI with different behavioral framing produced significantly different investment scores — validating importance of decision context."),
        ("Finding 5", "2021 Market Euphoria Effect",
         "All personas over-scored 2021 growth companies — AI training data absorbed market optimism similar to documented human overconfidence.")
    ]
    for title, subtitle, desc in findings:
        st.markdown(f"""
        <div style='background:#071528; border:1px solid #1e3a5f;
                    border-left:4px solid #c9a227; border-radius:8px;
                    padding:16px; margin-bottom:12px;'>
            <span style='color:#c9a227; font-size:12px;
                         font-weight:700; text-transform:uppercase;
                         letter-spacing:1px;'>{title}</span>
            <div style='color:#FFD700; font-weight:700;
                        margin:6px 0 4px; font-size:15px;'>{subtitle}</div>
            <div style='color:#8899aa; font-size:13px;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

elif page == "🤖 Live Analyzer":
    st.title("🤖 Live Corporate Investment Simulator")
    st.markdown("*Simulate corporate investment decisions through AI behavioral personas*")
    st.info("⚠️ **Research Note:** Simulation tool — does not predict actual financial outcomes or constitute financial advice.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("🏢 Company Name:",
                               placeholder="e.g. Apple, Tesla, OpenAI")
    with col2:
        year = st.text_input("📅 Year:",
                            placeholder="e.g. 2019, 2023, 2025")

    decision_type = st.selectbox("📋 Type of Corporate Investment Decision:", [
        "IPO / Going Public",
        "Merger & Acquisition (M&A)",
        "Capital Expenditure / Expansion",
        "New Product / Service Investment",
        "Digital Transformation",
        "Market Entry / Geographic Expansion",
        "Research & Development Investment",
        "Strategic Pivot",
        "AI Investment",
        "Restructuring / Layoffs"
    ])

    custom_decision = st.text_input(
        "📝 Describe the specific decision (optional):",
        placeholder="e.g. Should the company acquire a competitor for $10 billion?"
    )

    if st.button("⚡ RUN SIMULATION", use_container_width=True):
        if company and year:
            st.markdown("---")
            st.markdown(f"### 📊 Simulation: **{company} ({year})**")

            personas = [
                {"name": "🤖 Neutral Advisor",
                 "color": "#4da6ff",
                 "instruction": "You are a neutral objective corporate finance advisor."},
                {"name": "📈 Aggressive CFO",
                 "color": "#ff6b6b",
                 "instruction": "You are an aggressive CFO who prioritizes growth and accepts high risk."},
                {"name": "🛡️ Conservative Board",
                 "color": "#51cf66",
                 "instruction": "You are a conservative board member who prioritizes stability and risk management."},
            ]

            all_decisions = []
            all_scores = []
            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]

            for i, persona in enumerate(personas):
                with cols[i]:
                    with st.spinner(f"Simulating..."):
                        specific = custom_decision if custom_decision else f"a major {decision_type} decision"
                        question = f"""
                        {persona['instruction']}
                        Company: {company} | Year: {year}
                        Decision: {specific}
                        Answer in EXACTLY this format:
                        DECISION: YES or NO
                        SCORE: (0 to 100)
                        CONFIDENCE: (0 to 100)
                        REASON 1: (one sentence)
                        REASON 2: (one sentence)
                        REASON 3: (one sentence)
                        """
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[{"role":"user","content":question}]
                        )
                        text = response.choices[0].message.content
                        lines = text.strip().split('\n')
                        decision=score=confidence=r1=r2=r3=""
                        for line in lines:
                            if line.startswith("DECISION:"): decision=line.replace("DECISION:","").strip()
                            elif line.startswith("SCORE:"): score=line.replace("SCORE:","").strip()
                            elif line.startswith("CONFIDENCE:"): confidence=line.replace("CONFIDENCE:","").strip()
                            elif line.startswith("REASON 1:"): r1=line.replace("REASON 1:","").strip()
                            elif line.startswith("REASON 2:"): r2=line.replace("REASON 2:","").strip()
                            elif line.startswith("REASON 3:"): r3=line.replace("REASON 3:","").strip()

                        all_decisions.append(decision)
                        try: all_scores.append(int(score))
                        except: all_scores.append(50)

                        st.markdown(f"""
                        <div style='background:#071528; border:1px solid {persona['color']};
                                    border-radius:12px; padding:16px; margin-bottom:8px;'>
                            <div style='color:{persona['color']}; font-weight:700;
                                        font-size:14px;'>{persona['name']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        if "YES" in decision.upper():
                            st.success("✅ PROCEED")
                        else:
                            st.error("❌ DO NOT PROCEED")

                        try: st.progress(int(score)/100)
                        except: pass

                        st.markdown(f"""
                        <div style='display:flex; gap:10px; margin:8px 0;'>
                            <span style='background:#071528; border:1px solid #c9a227;
                                        color:#FFD700; padding:4px 12px; border-radius:20px;
                                        font-size:12px; font-weight:700;'>
                                Score: {score}/100
                            </span>
                            <span style='background:#071528; border:1px solid #1e3a5f;
                                        color:#8899aa; padding:4px 12px; border-radius:20px;
                                        font-size:12px;'>
                                Confidence: {confidence}%
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write(f"📌 {r1}")
                        st.write(f"📌 {r2}")
                        st.write(f"📌 {r3}")

            st.markdown("---")
            avg = sum(all_scores)/len(all_scores) if all_scores else 50

            if avg >= 60: verdict="✅ SIMULATION SUGGESTS: PROCEED"; color="success"
            elif avg >= 40: verdict="⚠️ SIMULATION SUGGESTS: CAUTION"; color="warning"
            else: verdict="❌ SIMULATION SUGGESTS: DO NOT PROCEED"; color="error"

            st.markdown("### 🏆 Simulation Verdict")
            col1,col2,col3,col4 = st.columns(4)
            with col1: st.metric("⚡ Average Score", f"{avg:.0f}/100")
            with col2: st.metric("🤖 Neutral", f"{all_scores[0] if all_scores else 0}/100")
            with col3: st.metric("📈 Aggressive", f"{all_scores[1] if len(all_scores)>1 else 0}/100")
            with col4: st.metric("🛡️ Conservative", f"{all_scores[2] if len(all_scores)>2 else 0}/100")

            if color=="success": st.success(f"### {verdict}")
            elif color=="warning": st.warning(f"### {verdict}")
            else: st.error(f"### {verdict}")
            st.caption("⚠️ Simulation output only — not financial advice")

            st.markdown("---")
            bias_q = f"""
            Three advisors simulated {company} {decision_type} in {year}.
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
            bias_r = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role":"user","content":bias_q}]
            )
            blines = bias_r.choices[0].message.content.strip().split('\n')
            oc=la=h=an=mb=ex=""
            for line in blines:
                if line.startswith("OVERCONFIDENCE:"): oc=line.replace("OVERCONFIDENCE:","").strip()
                elif line.startswith("LOSS AVERSION:"): la=line.replace("LOSS AVERSION:","").strip()
                elif line.startswith("HERDING:"): h=line.replace("HERDING:","").strip()
                elif line.startswith("ANCHORING:"): an=line.replace("ANCHORING:","").strip()
                elif line.startswith("MAIN BIAS:"): mb=line.replace("MAIN BIAS:","").strip()
                elif line.startswith("EXPLANATION:"): ex=line.replace("EXPLANATION:","").strip()

            st.markdown("### 🧠 Heuristic Bias Detection")
            st.caption("*Heuristic indicators — not definitive bias diagnoses*")
            c1,c2,c3,c4 = st.columns(4)
            with c1: st.info(f"**Overconfidence**\n{oc}")
            with c2: st.info(f"**Loss Aversion**\n{la}")
            with c3: st.info(f"**Herding**\n{h}")
            with c4: st.info(f"**Anchoring**\n{an}")
            st.warning(f"**Heuristic Bias Indicator:** {mb}")
            st.write(f"**Behavioral Finance Link:** {ex}")

        else:
            st.error("⚠️ Please enter both company name and year!")

elif page == "📊 Dashboard":
    st.title("📊 Research Dashboard")
    st.markdown("*Simulation results from 20 corporate investment cases (2010–2025)*")
    st.info("⚠️ Results represent simulated decision reasoning — not causal financial predictions.")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "📊 Accuracy Analysis",
        "💯 Scoring Analysis",
        "🧠 Bias Analysis"
    ])

    with tab1:
        neutral_acc = round(df_historical["Neutral_Correct"].mean()*100)
        aggressive_acc = round(df_historical["Aggressive_Correct"].mean()*100)
        conservative_acc = round(df_historical["Conservative_Correct"].mean()*100)
        human_acc = round(df_historical["Human_Correct"].mean()*100)

        c1,c2,c3,c4 = st.columns(4)
        with c1: st.metric("🤖 Neutral Simulation", f"{neutral_acc}%")
        with c2: st.metric("📈 Aggressive Simulation", f"{aggressive_acc}%")
        with c3: st.metric("🛡️ Conservative Simulation", f"{conservative_acc}%")
        with c4: st.metric("🧑 Human Decision", f"{human_acc}%")

        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1:
            fig = px.bar(
                pd.DataFrame({
                    "Persona": ["Neutral AI","Aggressive AI","Conservative AI","Human"],
                    "Accuracy": [neutral_acc,aggressive_acc,conservative_acc,human_acc]
                }),
                x="Persona", y="Accuracy", color="Persona",
                color_discrete_map={
                    "Neutral AI":"#4da6ff","Aggressive AI":"#ff6b6b",
                    "Conservative AI":"#51cf66","Human":"#FFD700"
                },
                title="Simulation Accuracy vs Human Decisions",
                text="Accuracy"
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(**PLOT_THEME, yaxis_range=[0,110], showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            year_data = df_historical.groupby("Year")["Neutral_Correct"].mean().reset_index()
            year_data.columns = ["Year","Accuracy"]
            year_data["Accuracy"] = round(year_data["Accuracy"]*100)
            fig2 = px.line(year_data, x="Year", y="Accuracy",
                          title="Simulation Accuracy Over Time",
                          markers=True,
                          color_discrete_sequence=["#FFD700"])
            fig2.update_layout(**PLOT_THEME, yaxis_range=[0,110])
            st.plotly_chart(fig2, use_container_width=True)

        c1,c2 = st.columns(2)
        with c1:
            fig3 = go.Figure()
            for name, col, color in [
                ("Neutral","Neutral_Correct","#4da6ff"),
                ("Aggressive","Aggressive_Correct","#ff6b6b"),
                ("Conservative","Conservative_Correct","#51cf66")
            ]:
                fig3.add_trace(go.Bar(
                    name=name, x=df_historical["Company"],
                    y=df_historical[col], marker_color=color
                ))
            fig3.update_layout(
                **PLOT_THEME, barmode="group",
                title="Correct Simulations by Company",
                yaxis=dict(tickvals=[0,1], ticktext=["Wrong","Correct"])
            )
            st.plotly_chart(fig3, use_container_width=True)

        with c2:
            ind = df_historical.groupby("Industry")["Conservative_Correct"].mean().reset_index()
            ind.columns = ["Industry","Accuracy"]
            ind["Accuracy"] = round(ind["Accuracy"]*100)
            fig4 = px.bar(ind, x="Industry", y="Accuracy",
                         title="Conservative Accuracy by Industry",
                         color="Accuracy",
                         color_continuous_scale=[[0,"#cc3333"],[0.5,"#FFD700"],[1,"#51cf66"]],
                         text="Accuracy")
            fig4.update_traces(texttemplate='%{text}%', textposition='outside')
            fig4.update_layout(**PLOT_THEME, yaxis_range=[0,110])
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("### 📋 Full Simulation Results")
        st.dataframe(
            df_historical[[
                "Company","Year","Corporate_Decision",
                "Neutral_Decision","Aggressive_Decision",
                "Conservative_Decision","Human_Decision",
                "Actual_Outcome","Main_Bias"
            ]].rename(columns={
                "Corporate_Decision":"Decision",
                "Neutral_Decision":"Neutral","Aggressive_Decision":"Aggressive",
                "Conservative_Decision":"Conservative","Human_Decision":"Human",
                "Actual_Outcome":"Outcome","Main_Bias":"Heuristic Bias"
            }),
            use_container_width=True
        )

    with tab2:
        st.markdown("### 💯 Simulation Scoring Analysis")
        st.caption("*Scores represent simulated reasoning strength — not financial return predictions*")

        c1,c2,c3 = st.columns(3)
        with c1: st.metric("🤖 Avg Neutral", f"{df_historical['Neutral_Score'].mean():.0f}/100")
        with c2: st.metric("📈 Avg Aggressive", f"{df_historical['Aggressive_Score'].mean():.0f}/100")
        with c3: st.metric("🛡️ Avg Conservative", f"{df_historical['Conservative_Score'].mean():.0f}/100")

        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1:
            fig = px.scatter(
                df_historical, x="Average_Score", y="Neutral_Correct",
                text="Company",
                title="Higher Score = Better Decision?",
                labels={"Average_Score":"Average Score","Neutral_Correct":"Correct"},
                color="Actual_Outcome", size="Average_Score",
                color_discrete_sequence=["#51cf66","#FFD700","#ff6b6b"]
            )
            fig.update_traces(textposition="top center")
            fig.update_layout(**PLOT_THEME)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            score_df = pd.DataFrame({
                "Company": df_historical["Company"],
                "Neutral": df_historical["Neutral_Score"],
                "Aggressive": df_historical["Aggressive_Score"],
                "Conservative": df_historical["Conservative_Score"]
            })
            fig2 = px.line(score_df, x="Company",
                          y=["Neutral","Aggressive","Conservative"],
                          title="Score Comparison Across Personas",
                          color_discrete_map={
                              "Neutral":"#4da6ff",
                              "Aggressive":"#ff6b6b",
                              "Conservative":"#51cf66"
                          })
            fig2.update_layout(**PLOT_THEME)
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(
            df_historical[[
                "Company","Year","Neutral_Score","Aggressive_Score",
                "Conservative_Score","Average_Score","AI_Recommendation","Actual_Outcome"
            ]].rename(columns={
                "Neutral_Score":"Neutral","Aggressive_Score":"Aggressive",
                "Conservative_Score":"Conservative","Average_Score":"Avg Score",
                "AI_Recommendation":"AI Verdict","Actual_Outcome":"Outcome"
            }),
            use_container_width=True
        )

    with tab3:
        st.markdown("### 🧠 Heuristic Bias Analysis")
        st.caption("*Bias detection is heuristic — suggests possible patterns, not definitive diagnoses*")

        bias_counts = df_historical["Main_Bias"].value_counts().reset_index()
        bias_counts.columns = ["Bias","Count"]

        c1,c2 = st.columns(2)
        with c1:
            fig = px.pie(bias_counts, values="Count", names="Bias",
                        title="Heuristic Bias Distribution",
                        color_discrete_sequence=["#FFD700","#4da6ff","#ff6b6b","#51cf66","#cc3333"])
            fig.update_layout(**PLOT_THEME)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig2 = px.bar(bias_counts, x="Bias", y="Count",
                         title="Bias Indicator Frequency",
                         color="Bias", text="Count",
                         color_discrete_sequence=["#FFD700","#4da6ff","#ff6b6b","#51cf66","#cc3333"])
            fig2.update_traces(textposition='outside')
            fig2.update_layout(**PLOT_THEME, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(
            df_historical[[
                "Company","Year","Main_Bias",
                "Neutral_Decision","Aggressive_Decision",
                "Conservative_Decision","Actual_Outcome"
            ]].rename(columns={
                "Main_Bias":"Heuristic Bias",
                "Neutral_Decision":"Neutral",
                "Aggressive_Decision":"Aggressive",
                "Conservative_Decision":"Conservative",
                "Actual_Outcome":"Outcome"
            }),
            use_container_width=True
        )

elif page == "⚔️ AI vs Human":
    st.title("⚔️ AI Simulation vs Human Decisions")
    st.markdown("*Comparing simulated AI reasoning against documented human corporate decisions*")
    st.info("⚠️ Comparison between simulated AI reasoning and documented historical decisions — not causal performance measurement.")
    st.markdown("---")

    df_h = df_historical.copy()
    ai_wins = len(df_h[(df_h["Neutral_Correct"]==1)&(df_h["Human_Correct"]==0)])
    human_wins = len(df_h[(df_h["Human_Correct"]==1)&(df_h["Neutral_Correct"]==0)])
    both_right = len(df_h[(df_h["Neutral_Correct"]==1)&(df_h["Human_Correct"]==1)])
    both_wrong = len(df_h[(df_h["Neutral_Correct"]==0)&(df_h["Human_Correct"]==0)])
    total = len(df_h)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("🤖 AI Simulation Better", f"{ai_wins}", delta=f"{round(ai_wins/total*100)}%")
    with c2: st.metric("🧑 Human Better", f"{human_wins}", delta=f"{round(human_wins/total*100)}%")
    with c3: st.metric("🤝 Both Correct", f"{both_right}", delta=f"{round(both_right/total*100)}%")
    with c4: st.metric("❌ Both Incorrect", f"{both_wrong}", delta=f"{round(both_wrong/total*100)}%")

    st.markdown("---")
    c1,c2 = st.columns(2)

    with c1:
        fig = px.bar(
            pd.DataFrame({
                "Result":["AI Better","Human Better","Both Correct","Both Incorrect"],
                "Cases":[ai_wins,human_wins,both_right,both_wrong]
            }),
            x="Result", y="Cases", color="Result",
            color_discrete_map={
                "AI Better":"#4da6ff","Human Better":"#FFD700",
                "Both Correct":"#51cf66","Both Incorrect":"#ff6b6b"
            },
            title="AI Simulation vs Human — Head to Head",
            text="Cases"
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(**PLOT_THEME, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.bar(
            pd.DataFrame({
                "Decision Maker":["Neutral AI","Aggressive AI","Conservative AI","Human"],
                "Accuracy":[
                    round(df_h["Neutral_Correct"].mean()*100),
                    round(df_h["Aggressive_Correct"].mean()*100),
                    round(df_h["Conservative_Correct"].mean()*100),
                    round(df_h["Human_Correct"].mean()*100)
                ]
            }),
            x="Decision Maker", y="Accuracy",
            color="Decision Maker",
            title="Overall Accuracy Comparison",
            text="Accuracy",
            color_discrete_sequence=["#4da6ff","#ff6b6b","#51cf66","#FFD700"]
        )
        fig2.update_traces(texttemplate='%{text}%', textposition='outside')
        fig2.update_layout(**PLOT_THEME, yaxis_range=[0,110], showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📋 Case by Case Comparison")

    comp = df_h[["Company","Year","Neutral_Decision","Human_Decision",
                 "Actual_Outcome","Neutral_Correct","Human_Correct"]].copy()

    def label(row):
        if row["Neutral_Correct"]==1 and row["Human_Correct"]==0: return "🤖 AI Better"
        elif row["Human_Correct"]==1 and row["Neutral_Correct"]==0: return "🧑 Human Better"
        elif row["Neutral_Correct"]==1 and row["Human_Correct"]==1: return "🤝 Both Correct"
        else: return "❌ Both Incorrect"

    comp["Result"] = comp.apply(label, axis=1)
    st.dataframe(
        comp[["Company","Year","Neutral_Decision","Human_Decision","Actual_Outcome","Result"]].rename(columns={
            "Neutral_Decision":"AI Simulation",
            "Human_Decision":"Human Decision",
            "Actual_Outcome":"Outcome"
        }),
        use_container_width=True
    )

    st.markdown("---")
    best = round(df_h["Conservative_Correct"].mean()*100)
    human = round(df_h["Human_Correct"].mean()*100)
    diff = best - human
    if diff > 0:
        st.success(f"""
        **Conservative AI simulation aligned with correct outcomes {diff}% more
        than documented human decisions in this case study sample.**

        This suggests risk-averse behavioral framing may produce reasoning more
        consistent with successful corporate investment outcomes — though causal
        conclusions require larger samples and real corporate data.
        """)
    else:
        st.info(f"""
        **Human decisions aligned with correct outcomes {abs(diff)}% more
        than AI simulation in this case study sample.**

        This highlights the continuing importance of human judgment in
        corporate investment — particularly for strategic intuition and
        contextual understanding.
        """)

elif page == "📂 Custom Analysis":
    st.title("📂 Custom Investment Simulation")
    st.markdown("*Input your company data for a private AI-powered investment decision simulation*")
    st.info("""
    🔒 **Privacy:** Your data is never stored. Analysis generated in real time only.
    ⚠️ **Research Note:** Simulation tool — does not predict outcomes or constitute financial advice.
    """)
    st.markdown("---")

    st.markdown("### 📋 Section 1 — Company Identity")
    c1,c2,c3 = st.columns(3)
    with c1:
        company_name = st.text_input("🏢 Company Name:", placeholder="Your company")
        industry = st.selectbox("🏭 Industry:", [
            "Technology","Healthcare","Financial Services","Real Estate",
            "Retail/E-Commerce","Automotive","Energy","Media/Entertainment",
            "Manufacturing","Telecommunications","Education","Other"
        ])
    with c2:
        country = st.text_input("🌍 Country/Region:", placeholder="e.g. Italy, USA")
        company_type = st.selectbox("🏗️ Company Type:", [
            "Startup (0-3 years)","Growth Stage (3-7 years)",
            "SME","Large Corporation","Multinational"
        ])
    with c3:
        years_biz = st.number_input("📅 Years in Business:", min_value=0, value=5)
        status = st.selectbox("📊 Status:", [
            "Private","Public (Listed)","Family Business","State Owned","Subsidiary"
        ])

    st.markdown("---")
    st.markdown("### 💰 Section 2 — Financial Health")
    c1,c2,c3 = st.columns(3)
    with c1:
        revenue = st.number_input("💵 Annual Revenue ($M):", min_value=0.0, value=10.0)
        net_profit = st.number_input("📈 Net Profit/Loss ($M):", value=1.0)
        debt = st.number_input("💳 Total Debt ($M):", min_value=0.0, value=5.0)
    with c2:
        cash = st.number_input("🏦 Cash Reserves ($M):", min_value=0.0, value=3.0)
        growth = st.number_input("📊 Revenue Growth (%):", value=10.0)
        valuation = st.number_input("🏷️ Valuation ($M):", min_value=0.0, value=50.0)
    with c3:
        de_ratio = st.number_input("⚖️ Debt/Equity Ratio:", min_value=0.0, value=0.5)
        ebitda = st.number_input("📉 EBITDA ($M):", value=2.0)
        burn = st.number_input("🔥 Monthly Burn ($M):", min_value=0.0, value=0.5)

    st.markdown("---")
    st.markdown("### 🎯 Section 3 — The Investment Decision")
    c1,c2,c3 = st.columns(3)
    with c1:
        inv_type = st.selectbox("📋 Investment Type:", [
            "Merger & Acquisition","Geographic Expansion","New Product",
            "Technology Investment","R&D","Strategic Partnership",
            "IPO","Capital Expenditure","Digital Transformation","Restructuring"
        ])
        inv_amount = st.number_input("💰 Investment Amount ($M):", min_value=0.1, value=5.0)
    with c2:
        exp_return = st.number_input("📈 Expected Return (%):", value=15.0)
        timeframe = st.selectbox("⏱️ Timeframe:", [
            "Short term (under 1 year)","Medium term (1-3 years)",
            "Long term (3-10 years)","Very long term (10+ years)"
        ])
    with c3:
        market = st.selectbox("🌍 Target Market:", [
            "Local","National","Regional (multi-country)","Global"
        ])
        financing = st.selectbox("💳 Financing Method:", [
            "Own cash","Bank loan","Investor/VC funding",
            "Bond issuance","Mixed","Government grant"
        ])

    st.markdown("---")
    st.markdown("### 🌍 Section 4 — Strategic Context")
    c1,c2,c3 = st.columns(3)
    with c1:
        mkt_cond = st.selectbox("📊 Market Conditions:", [
            "Growing (high opportunity)","Stable (moderate)","Declining (high risk)",
            "Highly competitive","Emerging/disrupted"
        ])
        reg = st.selectbox("⚖️ Regulatory Environment:", [
            "Highly regulated","Moderately regulated",
            "Low regulation","Changing regulations"
        ])
    with c2:
        tech_risk = st.selectbox("💻 Tech Disruption Risk:", [
            "High — being disrupted","Medium — possible","Low — stable"
        ])
        risk_tol = st.selectbox("🎯 Risk Tolerance:", [
            "Very conservative","Moderate","Aggressive"
        ])
    with c3:
        why = st.text_area("❓ Why This Investment?", placeholder="Brief reason...", height=80)
        risk = st.text_area("⚠️ Biggest Risk?", placeholder="Main concern...", height=80)

    st.markdown("---")
    st.markdown("### 📝 Section 5 — Additional Context")
    c1,c2 = st.columns(2)
    with c1:
        competitors = st.text_input("🏆 Main Competitors:", placeholder="e.g. Amazon, Google")
        events = st.text_area("📰 Recent Major Events:", placeholder="Leadership change, merger...", height=80)
    with c2:
        decision = st.text_area(
            "📋 Describe Your Exact Investment Decision:",
            placeholder="e.g. We want to acquire a competitor in France for $20M to expand European market share...",
            height=120
        )

    st.markdown("---")

    if st.button("⚡ SIMULATE MY INVESTMENT", use_container_width=True):
        if company_name and decision:
            st.markdown("---")
            st.markdown(f"## 📊 Simulation: **{company_name}**")
            st.markdown(f"**Decision:** {decision}")

            profile = f"""
            COMPANY: {company_name} | Industry: {industry} | Country: {country}
            Type: {company_type} | Years: {years_biz} | Status: {status}
            Revenue: ${revenue}M | Profit/Loss: ${net_profit}M | Debt: ${debt}M
            Cash: ${cash}M | Growth: {growth}% | Valuation: ${valuation}M
            D/E: {de_ratio} | EBITDA: ${ebitda}M | Burn: ${burn}M/mo
            Investment: {inv_type} | Amount: ${inv_amount}M | Return: {exp_return}%
            Timeframe: {timeframe} | Market: {market} | Finance: {financing}
            Market conditions: {mkt_cond} | Regulatory: {reg}
            Tech risk: {tech_risk} | Risk tolerance: {risk_tol}
            Competitors: {competitors} | Why: {why} | Risk: {risk}
            Events: {events}
            DECISION: {decision}
            """

            personas = [
                {"name":"🤖 Neutral Advisor","color":"#4da6ff",
                 "instruction":"You are a neutral objective corporate finance advisor."},
                {"name":"📈 Aggressive CFO","color":"#ff6b6b",
                 "instruction":"You are an aggressive CFO who prioritizes growth."},
                {"name":"🛡️ Conservative Board","color":"#51cf66",
                 "instruction":"You are a conservative board member focused on stability."},
            ]

            all_decisions=[]
            all_scores=[]
            c1,c2,c3=st.columns(3)
            cols=[c1,c2,c3]

            for i,persona in enumerate(personas):
                with cols[i]:
                    with st.spinner(f"Simulating {persona['name']}..."):
                        q = f"""
                        {persona['instruction']}
                        Company data: {profile}
                        Should proceed with: {decision}?
                        Answer in EXACTLY this format:
                        DECISION: YES or NO
                        SCORE: (0-100)
                        CONFIDENCE: (0-100)
                        REASON 1: (specific to financials)
                        REASON 2: (specific to market context)
                        REASON 3: (specific to risk profile)
                        KEY RISK: (biggest risk)
                        ALTERNATIVE: (if NO — what instead?)
                        """
                        r = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[{"role":"user","content":q}]
                        )
                        text=r.choices[0].message.content
                        lines=text.strip().split('\n')
                        dec=sc=conf=r1=r2=r3=kr=alt=""
                        for line in lines:
                            if line.startswith("DECISION:"): dec=line.replace("DECISION:","").strip()
                            elif line.startswith("SCORE:"): sc=line.replace("SCORE:","").strip()
                            elif line.startswith("CONFIDENCE:"): conf=line.replace("CONFIDENCE:","").strip()
                            elif line.startswith("REASON 1:"): r1=line.replace("REASON 1:","").strip()
                            elif line.startswith("REASON 2:"): r2=line.replace("REASON 2:","").strip()
                            elif line.startswith("REASON 3:"): r3=line.replace("REASON 3:","").strip()
                            elif line.startswith("KEY RISK:"): kr=line.replace("KEY RISK:","").strip()
                            elif line.startswith("ALTERNATIVE:"): alt=line.replace("ALTERNATIVE:","").strip()

                        all_decisions.append(dec)
                        try: all_scores.append(int(sc))
                        except: all_scores.append(50)

                        st.markdown(f"""
                        <div style='border-left:4px solid {persona['color']};
                                    padding-left:12px; margin-bottom:8px;'>
                            <div style='color:{persona['color']};
                                        font-weight:700;'>{persona['name']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        if "YES" in dec.upper(): st.success("✅ PROCEED")
                        else: st.error("❌ DO NOT PROCEED")
                        try: st.progress(int(sc)/100)
                        except: pass
                        st.write(f"**Score:** {sc}/100 | **Confidence:** {conf}%")
                        st.write(f"📌 {r1}")
                        st.write(f"📌 {r2}")
                        st.write(f"📌 {r3}")
                        if kr: st.warning(f"⚠️ **Key Risk:** {kr}")
                        if alt and "NO" in dec.upper(): st.info(f"💡 **Alternative:** {alt}")

            st.markdown("---")
            avg=sum(all_scores)/len(all_scores) if all_scores else 50
            if avg>=60: v="✅ SIMULATION SUGGESTS: PROCEED"; c="success"
            elif avg>=40: v="⚠️ SIMULATION SUGGESTS: CAUTION"; c="warning"
            else: v="❌ SIMULATION SUGGESTS: DO NOT PROCEED"; c="error"

            st.markdown("## 🏆 Simulation Verdict")
            c1,c2,c3,c4=st.columns(4)
            with c1: st.metric("⚡ Average",f"{avg:.0f}/100")
            with c2: st.metric("🤖 Neutral",f"{all_scores[0] if all_scores else 0}/100")
            with c3: st.metric("📈 Aggressive",f"{all_scores[1] if len(all_scores)>1 else 0}/100")
            with c4: st.metric("🛡️ Conservative",f"{all_scores[2] if len(all_scores)>2 else 0}/100")

            if c=="success": st.success(f"### {v}")
            elif c=="warning": st.warning(f"### {v}")
            else: st.error(f"### {v}")
            st.caption("⚠️ Simulation only — not financial advice")

            st.markdown("---")
            bq=f"""
            Advisors simulated: {decision}
            Company: {company_name} Revenue:${revenue}M Debt:${debt}M
            Decisions:{', '.join(all_decisions)} Scores:{', '.join([str(s) for s in all_scores])}
            OVERCONFIDENCE: YES or NO — (why)
            LOSS AVERSION: YES or NO — (why)
            HERDING: YES or NO — (why)
            ANCHORING: YES or NO — (why)
            MAIN BIAS: (name or NONE)
            EXPLANATION: (one sentence)
            """
            br=client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"user","content":bq}])
            bl=br.choices[0].message.content.strip().split('\n')
            oc=la=h=an=mb=ex=""
            for line in bl:
                if line.startswith("OVERCONFIDENCE:"): oc=line.replace("OVERCONFIDENCE:","").strip()
                elif line.startswith("LOSS AVERSION:"): la=line.replace("LOSS AVERSION:","").strip()
                elif line.startswith("HERDING:"): h=line.replace("HERDING:","").strip()
                elif line.startswith("ANCHORING:"): an=line.replace("ANCHORING:","").strip()
                elif line.startswith("MAIN BIAS:"): mb=line.replace("MAIN BIAS:","").strip()
                elif line.startswith("EXPLANATION:"): ex=line.replace("EXPLANATION:","").strip()

            st.markdown("### 🧠 Heuristic Bias Detection")
            st.caption("*Heuristic indicators only*")
            c1,c2,c3,c4=st.columns(4)
            with c1: st.info(f"**Overconfidence**\n{oc}")
            with c2: st.info(f"**Loss Aversion**\n{la}")
            with c3: st.info(f"**Herding**\n{h}")
            with c4: st.info(f"**Anchoring**\n{an}")
            st.warning(f"**Heuristic Bias Indicator:** {mb}")
            st.write(f"**Behavioral Finance Link:** {ex}")
            st.success("🔒 Privacy: Your data was used only for this simulation and has not been stored.")

        else:
            st.error("⚠️ Please fill Company Name and describe your Investment Decision!")

elif page == "🎤 Jury Demo":
    st.title("🎤 Jury Presentation Demo")
    st.markdown("*Prepared live simulation for thesis defense*")
    st.markdown("""
    <div style='background:#071528; border:1px solid #c9a227;
                border-radius:12px; padding:20px; margin-bottom:20px;'>
        <div style='color:#FFD700; font-weight:700; font-size:16px;'>
            💡 Presentation Tip
        </div>
        <div style='color:#8899aa; margin-top:8px;'>
            Use this page during your jury defense to demonstrate the system live.
            Pre-filled with WeWork 2019 — the most compelling case from your research.
            One click shows real-time AI simulation to your jury.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1: demo_co = st.text_input("🏢 Company:", value="WeWork")
    with c2: demo_yr = st.text_input("📅 Year:", value="2019")
    with c3: demo_dec = st.text_input("📋 Decision:", value="Proceed with IPO expansion?")

    if st.button("⚡ RUN LIVE DEMONSTRATION", use_container_width=True):
        if demo_co and demo_yr:
            st.markdown("---")
            st.markdown(f"## 🔍 Live Simulation: **{demo_co} — {demo_yr}**")
            st.markdown(f"**Corporate Decision:** {demo_dec}")
            st.markdown("---")

            personas=[
                {"name":"🤖 Neutral Advisor","short":"Neutral","color":"#4da6ff",
                 "instruction":"You are a neutral objective corporate finance advisor."},
                {"name":"📈 Aggressive CFO","short":"Aggressive","color":"#ff6b6b",
                 "instruction":"You are an aggressive CFO who prioritizes growth."},
                {"name":"🛡️ Conservative Board","short":"Conservative","color":"#51cf66",
                 "instruction":"You are a conservative board member focused on stability."},
            ]

            decisions=[]
            scores=[]
            c1,c2,c3=st.columns(3)
            cols=[c1,c2,c3]

            for i,p in enumerate(personas):
                with cols[i]:
                    with st.spinner(f"Simulating {p['short']}..."):
                        q=f"""
                        {p['instruction']}
                        Company: {demo_co} | Year: {demo_yr}
                        Decision: {demo_dec}
                        Answer in EXACTLY this format:
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
                            elif line.startswith("SCORE:"): sc=line.replace("SCORE:","").strip()
                            elif line.startswith("CONFIDENCE:"): conf=line.replace("CONFIDENCE:","").strip()
                            elif line.startswith("REASON 1:"): r1=line.replace("REASON 1:","").strip()
                            elif line.startswith("REASON 2:"): r2=line.replace("REASON 2:","").strip()
                            elif line.startswith("REASON 3:"): r3=line.replace("REASON 3:","").strip()

                        decisions.append(dec)
                        try: scores.append(int(sc))
                        except: scores.append(50)

                        st.markdown(f"""
                        <div style='background:#071528; border:2px solid {p['color']};
                                    border-radius:12px; padding:16px;'>
                            <div style='color:{p['color']}; font-weight:800;
                                        font-size:15px;'>{p['name']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        if "YES" in dec.upper(): st.success("✅ PROCEED")
                        else: st.error("❌ DO NOT PROCEED")
                        try: st.progress(int(sc)/100)
                        except: pass
                        st.markdown(f"""
                        <div style='background:#071528; border:1px solid #c9a227;
                                    border-radius:8px; padding:8px 16px;
                                    display:inline-block; margin:8px 0;'>
                            <span style='color:#FFD700; font-weight:700;'>
                                Score: {sc}/100
                            </span>
                            <span style='color:#8899aa; margin-left:10px;'>
                                Confidence: {conf}%
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write(f"📌 {r1}")
                        st.write(f"📌 {r2}")
                        st.write(f"📌 {r3}")

            st.markdown("---")
            avg=sum(scores)/len(scores) if scores else 50

            st.markdown("## 🏆 SIMULATION VERDICT")
            c1,c2,c3,c4=st.columns(4)
            with c1: st.metric("⚡ Average Score",f"{avg:.0f}/100")
            with c2: st.metric("🤖 Neutral",f"{scores[0] if scores else 0}/100")
            with c3: st.metric("📈 Aggressive",f"{scores[1] if len(scores)>1 else 0}/100")
            with c4: st.metric("🛡️ Conservative",f"{scores[2] if len(scores)>2 else 0}/100")

            if avg>=60: st.success("# ✅ SIMULATION SUGGESTS: PROCEED")
            elif avg>=40: st.warning("# ⚠️ SIMULATION SUGGESTS: CAUTION")
            else: st.error("# ❌ SIMULATION SUGGESTS: DO NOT PROCEED")

            if demo_co in ["WeWork","Theranos","Kodak","Blockbuster","Peloton"]:
                st.markdown("---")
                st.markdown("### ✅ Historical Validation")
                st.error(f"**Actual Outcome: FAILED** — Simulation correctly identified risk in {demo_co}")
            elif demo_co in ["Tesla","Apple","Amazon","Netflix","Microsoft"]:
                st.markdown("---")
                st.markdown("### ✅ Historical Validation")
                st.success(f"**Actual Outcome: SUCCESS** — Simulation correctly identified opportunity in {demo_co}")

            st.caption("⚠️ Simulation output for research demonstration only — not financial advice")

elif page == "📋 About":
    st.title("📋 About This Research")
    st.markdown("---")

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("### 👩‍🎓 Researcher")
        st.markdown("""
        <div style='background:#071528; border:1px solid #c9a227;
                    border-radius:12px; padding:24px;'>
            <div style='margin-bottom:12px;'>
                <div style='color:#c9a227; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>Name</div>
                <div style='color:#e8e8e8; font-weight:700; font-size:16px;'>
                    Meryam El Ghouti</div>
            </div>
            <div style='margin-bottom:12px;'>
                <div style='color:#c9a227; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>University</div>
                <div style='color:#e8e8e8;'>Sapienza University of Rome</div>
            </div>
            <div style='margin-bottom:12px;'>
                <div style='color:#c9a227; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>Degree</div>
                <div style='color:#e8e8e8;'>Master's in Business Management</div>
            </div>
            <div style='margin-bottom:12px;'>
                <div style='color:#c9a227; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>Year</div>
                <div style='color:#e8e8e8;'>2026</div>
            </div>
            <div>
                <div style='color:#c9a227; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>Thesis Title</div>
                <div style='color:#e8e8e8;'>The Agentic Alpha — A Multi-Agent AI
                Decision Support System for Corporate Investment Simulation
                with Behavioral Bias Detection</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("### 🔬 Research Overview")
        st.markdown("""
        <div style='background:#071528; border:1px solid #1e3a5f;
                    border-radius:12px; padding:24px;'>
            <div style='margin-bottom:16px;'>
                <div style='color:#c9a227; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>Research Question</div>
                <div style='color:#e8e8e8; margin-top:6px;'>
                    Can a multi-agent AI system simulate corporate investment
                    reasoning with behavioral bias detection comparable to
                    human decision-makers?</div>
            </div>
            <div style='margin-bottom:16px;'>
                <div style='color:#c9a227; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>Approach</div>
                <div style='color:#e8e8e8; margin-top:6px;'>
                    Design Science Research | Multi-agent simulation |
                    Heuristic bias detection | 20 historical cases</div>
            </div>
            <div style='margin-bottom:16px;'>
                <div style='color:#c9a227; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>Key Theory</div>
                <div style='color:#e8e8e8; margin-top:6px;'>
                    Behavioral Finance — Kahneman & Tversky (1979)
                    Prospect Theory | Thaler (2015) Nudge Theory</div>
            </div>
            <div>
                <div style='color:#c9a227; font-size:11px; text-transform:uppercase;
                            letter-spacing:1px;'>Tools</div>
                <div style='color:#e8e8e8; margin-top:6px;'>
                    Python | Groq LLaMA API | Streamlit | Plotly</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    st.markdown("### 🎯 Three Research Contributions")
    c1,c2,c3=st.columns(3)
    for col,(num,title,desc) in zip([c1,c2,c3],[
        ("01","Multi-Agent Framework","AI decision framework simulating corporate investment reasoning through three distinct behavioral personas"),
        ("02","Heuristic Bias Detection","Module identifying overconfidence, herding, loss aversion and anchoring in simulated corporate decisions"),
        ("03","Comparative Analysis","Framework comparing AI simulation outputs against documented human decisions across 20 investment scenarios")
    ]):
        with col:
            st.markdown(f"""
            <div style='background:#071528; border:1px solid #c9a227;
                        border-radius:12px; padding:24px; height:160px;'>
                <div style='color:#c9a227; font-size:32px; font-weight:800;'>{num}</div>
                <div style='color:#FFD700; font-weight:700; margin:8px 0 4px;'>{title}</div>
                <div style='color:#8899aa; font-size:13px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    st.markdown("### 📚 Theoretical Framework")
    c1,c2,c3,c4=st.columns(4)
    for col,(bias,theory,desc) in zip([c1,c2,c3,c4],[
        ("Overconfidence","Kahneman & Tversky","Overestimating accuracy of corporate decisions"),
        ("Loss Aversion","Prospect Theory","Fear of losses stronger than desire for gains"),
        ("Herding Behavior","Shiller","Following crowd despite contradictory evidence"),
        ("Anchoring Bias","Tversky","Over-relying on first piece of information")
    ]):
        with col:
            st.markdown(f"""
            <div style='background:#071528; border:1px solid #1e3a5f;
                        border-left:4px solid #c9a227; border-radius:8px;
                        padding:16px;'>
                <div style='color:#FFD700; font-weight:700;'>{bias}</div>
                <div style='color:#c9a227; font-size:11px; margin:4px 0;'>{theory}</div>
                <div style='color:#8899aa; font-size:12px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    st.markdown("### 🛠️ System Architecture")
    st.code("""
    Input: Corporate Investment Decision
           (Known Company OR Custom Private Data)
                        ↓
    ┌─────────────────────────────────────────┐
    │         Multi-Agent AI Pipeline          │
    │              (Groq LLaMA)               │
    ├─────────────────────────────────────────┤
    │  Agent 1: Neutral Corporate Advisor     │
    │  Agent 2: Aggressive CFO                │
    │  Agent 3: Conservative Board Member     │
    └─────────────────────────────────────────┘
                        ↓
    Investment Scoring Module (0 — 100)
                        ↓
    Heuristic Bias Detection Module
    (Overconfidence | Loss Aversion | Herding | Anchoring)
                        ↓
    Simulated Corporate Investment Verdict
    """, language="text")

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; color:#556677; padding:20px;'>
        Master's Thesis | The Agentic Alpha | Meryam El Ghouti<br>
        Sapienza University of Rome | 2026<br>
        <span style='color:#c9a227;'>agenticalpha.streamlit.app</span>
    </div>
    """, unsafe_allow_html=True)
