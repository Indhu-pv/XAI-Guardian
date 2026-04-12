import streamlit as st
import pandas as pd
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

if __name__ == "__main__":
    main()
