import streamlit as st
import pandas as pd
<<<<<<< HEAD
import os
from data.synthetic_applicants import generate_synthetic_applicants
from analytics.bias_analytics import run_batch_bias_analysis
from ui.styles import apply_custom_css
from ui.tab1_application import show_tab1
from ui.tab2_batch_analysis import show_tab2
from ui.tab3_lender_audit import show_tab3

# Must be the very first Streamlit command
st.set_page_config(page_title="XAI Guardian", page_icon="🏦", layout="wide")

def load_data():
    if 'df' not in st.session_state:
        if os.path.exists('seed_data.csv'):
            st.session_state.df = pd.read_csv('seed_data.csv')
        else:
            df = generate_synthetic_applicants(500)
            df.to_csv('seed_data.csv', index=False)
            st.session_state.df = df

def render_kpi_cards(df):
    metrics = run_batch_bias_analysis(df)
    overall_rate = metrics.get('overall_rate', 0) * 100

    male_rate = metrics.get('gender_rates', {}).get('Male', 0)
    female_rate = metrics.get('gender_rates', {}).get('Female', 0)
    urban_rate = metrics.get('location_rates', {}).get('Urban', 0)
    rural_rate = metrics.get('location_rates', {}).get('Rural', 0)

    gender_gap = abs(male_rate - female_rate) * 100
    location_gap = abs(urban_rate - rural_rate) * 100
    bias_score = max(0, 100 - (gender_gap * 1.2 + location_gap * 1.5))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class=\"metric-card\">
                <div class=\"metric-label\">📈 Overall Approval Rate</div>
                <div class=\"metric-value\">{overall_rate:.1f}%</div>
                <div class=\"metric-note\">Across all processed applications</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class=\"metric-card\">
                <div class=\"metric-label\">🧠 Bias Score</div>
                <div class=\"metric-value\">{bias_score:.0f}/100</div>
                <div class=\"metric-note\">Composite fairness confidence index</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class=\"metric-card\">
                <div class=\"metric-label\">⚖️ Gender Gap</div>
                <div class=\"metric-value\">{gender_gap:.1f}%</div>
                <div class=\"metric-note\">Approval delta between male and female</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class=\"metric-card\">
                <div class=\"metric-label\">🌍 Location Gap</div>
                <div class=\"metric-value\">{location_gap:.1f}%</div>
                <div class=\"metric-note\">Urban vs rural approval delta</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
            
def main():
    apply_custom_css()
    load_data()
    df = st.session_state.get('df')
    
    st.markdown(
        """
        <div class="hero">
            <h1 class="hero-title">🏦 XAI Guardian: <span class="gradient-text">Ethical AI</span> for Microfinance</h1>
            <p class="hero-subtitle">Ensuring fair, transparent, and explainable lending decisions with production-style decision intelligence.</p>
            <p class="hero-tagline">From loan scoring to bias audits, every decision is measurable, explainable, and accountable.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df is not None:
        render_kpi_cards(df)
        st.markdown("<div style='height: 0.7rem;'></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["👤 Applicant", "📊 Batch Analysis", "🛡️ Audit"])
    
    with tab1:
        show_tab1()
        
    with tab2:
        show_tab2()
        
    with tab3:
        show_tab3()

    st.markdown(
        "<div class='footer'>Built for Ethical AI in Finance | Hackathon Project</div>",
        unsafe_allow_html=True,
    )
=======
import plotly.express as px
import plotly.graph_objects as go
import time

from utils import get_sample_data, apply_custom_css
from ai_engine import evaluate_candidate
from reeval_engine import reevaluate
from human_engine import human_evaluate
from bias_engine import detect_bias
from trust_engine import calculate_trust

# Set Page Config
st.set_page_config(page_title="XAI Guardian", page_icon="🧠", layout="wide")

def main():
    apply_custom_css()
    
    # --------------- SIDEBAR ---------------
    st.sidebar.title("🧠 XAI Guardian")
    st.sidebar.caption("AI that explains, audits, and questions itself.")
    
    st.sidebar.divider()
    page = st.sidebar.radio("Navigation", ["Main Dashboard", "Decision Analysis", "Insights & Visualizations"])
    st.sidebar.divider()
    
<<<<<<< HEAD

=======
>>>>>>> 1dc8f4ebb23f7a93adb5b50ebdc0ac399edbbec6
    st.sidebar.subheader("Global Constraints")
    high_comp_mode = st.sidebar.toggle("🔥 High Competition Mode", value=False)
    explain_like_human = st.sidebar.toggle("🗣️ Explain Like Human", value=True)
    
  
    candidates = get_sample_data()
    candidate_names = [c["name"] for c in candidates]
    
    st.sidebar.divider()
    selected_name = st.sidebar.selectbox("Select Candidate to Evaluate", candidate_names)
    
    # Extract the selected candidate object
    candidate = next(c for c in candidates if c["name"] == selected_name)
    
    # Run pipeline
    ai_res = evaluate_candidate(candidate, high_comp_mode)
    reeval_res = reevaluate(candidate, ai_res, high_comp_mode)
    bias_res = detect_bias(candidate)
    trust_res = calculate_trust(ai_res, reeval_res, bias_res)
    human_res = human_evaluate(candidate, explain_like_human)
    
    # Simulate processing delay the first time a candidate is chosen
    if f"processed_{candidate['id']}" not in st.session_state:
        with st.spinner("Executing strict rules..."):
            time.sleep(0.5)
        st.session_state[f"processed_{candidate['id']}"] = True

    # --------------- PAGE 1: MAIN DASHBOARD ---------------
    if page == "Main Dashboard":
        st.title("Main Dashboard")
        
        col1, col2 = st.columns([1, 2])
        
        # Left Panel (Input)
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader("👤 Applicant Profile")
            st.write(f"**Name:** {candidate['name']}")
            st.write(f"**Age:** {candidate['age']}")
            st.write(f"**Gender:** {candidate['gender']}")
            st.write(f"**Experience:** {candidate['experience']} years")
            st.markdown("---")
            st.write("**Skills:**")
            st.progress(candidate['coding_score'] / 100.0, text=f"Coding ({candidate['coding_score']})")
            st.progress(candidate['communication'] / 100.0, text=f"Communication ({candidate['communication']})")
            st.markdown("</div>", unsafe_allow_html=True)

        # Right Panel (Output)
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader("🤖 Final AI Decision")
            if ai_res["decision"] == "Selected":
                st.markdown("<h1 style='color:#10b981;'>SELECTED</h1>", unsafe_allow_html=True)
            else:
                st.markdown("<h1 style='color:#ef4444;'>REJECTED</h1>", unsafe_allow_html=True)
                
            st.markdown(f"**Confidence:** {ai_res['confidence']}%")
            
            # Trust Timeline Score Progress
            trust_score = trust_res['final_score']
            trust_color = "green" if trust_score > 75 else "orange" if trust_score > 50 else "red"
            st.markdown(f"**System Trust Score:**")
            st.progress(trust_score / 100.0, text=f"{trust_score}%")
            
            st.markdown("---")
            st.write("**AI Reasoning:**")
            for r in ai_res["reasons"]:
                st.write(f"- {r}")
                
            st.markdown("</div>", unsafe_allow_html=True)

            if reeval_res["inconsistency_detected"]:
                st.markdown("<div class='alert-warning'><b>⚠️ Self-Doubt Triggered:</b> I might be wrong. My secondary sweep noted inconsistencies in the evaluation criteria. View 'Decision Analysis' for details.</div>", unsafe_allow_html=True)


    # --------------- PAGE 2: DECISION ANALYSIS ---------------
    elif page == "Decision Analysis":
        st.title("Decision Analysis")
        st.write("Comparing System AI execution vs Human reasoning layers.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader("AI System (1st Pass)")
            st.write(f"**Decision:** {ai_res['decision']}")
            st.write(f"**Raw Score:** {ai_res['score']}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader("Re-evaluation Engine")
            st.write(f"**Decision:** {reeval_res['decision']}")
            st.write(f"**Raw Score:** {reeval_res['score']}")
            
            if reeval_res['inconsistency_detected']:
                st.markdown("<div class='alert-danger'>⚠️ Decision inconsistency detected</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Human vs AI Explanation comparison")
        hcol, acol = st.columns(2)
        with hcol:
            st.info("**Human Baseline Simulation**")
            st.write(human_res["explanation"])
            
        with acol:
            st.info("**AI Direct Reasoning**")
            for r in ai_res["reasons"]:
                st.write(f"- {r}")
            for r in reeval_res["reasons"]:
                st.write(f"- {r}")


    # --------------- PAGE 3: INSIGHTS & VISUALIZATION ---------------
    elif page == "Insights & Visualizations":
        st.title("Insights & Visualizations")
        
        # 1. Trust Timeline Chart
        st.subheader("Trust Decay Timeline")
        df_trust = pd.DataFrame({
            "Event": trust_res["timeline_events"],
            "Trust Score": trust_res["timeline_scores"]
        })
        fig = px.line(df_trust, x="Event", y="Trust Score", markers=True, 
                      title="AI Trust Calculation over Audit stages", template="plotly_dark")
        fig.update_traces(line_color='#3b82f6', marker=dict(size=10, color="#fcd34d"))
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        # 2. Bias Engine
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader("⚠️ Bias Engine Alerts")
            if bias_res["is_biased"]:
                for w in bias_res["warnings"]:
                    st.markdown(f"<div class='alert-warning'>{w}</div>", unsafe_allow_html=True)
                st.write(f"**Computed Bias Penalty:** {bias_res['bias_score']}")
            else:
                st.markdown("<div class='alert-success'>✅ No severe bias patterns detected in primary features.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 3. Why Not? / Improvement
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader("💡 'Why Not?' Insights")
            if ai_res["decision"] == "Rejected":
                st.write("What the candidate could improve to get selected:")
                if candidate['coding_score'] < 80:
                    st.write("- **Coding Score:** Improve fundamental algorithmic logic.")
                if candidate['experience'] < 5:
                    st.write("- **Tenure:** Gain more years of production experience.")
                if high_comp_mode:
                    st.write("- **Note:** The current cycle is highly competitive. Standard scores are falling short.")
            else:
                st.write("Candidate was selected. No critical blocking improvements needed.")
                if candidate['communication'] < 75:
                    st.write("- *Minor suggestion:* Can improve cross-functional communication.")
            st.markdown("</div>", unsafe_allow_html=True)
            
>>>>>>> 3129cf3947e94ffbaffb1c0522fe49c78a5ce036

if __name__ == "__main__":
    main()
