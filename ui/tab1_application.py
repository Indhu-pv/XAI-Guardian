import streamlit as st
import pandas as pd
from engines.lending_engine import score_applicant, generate_explanation
from engines.xai_guardian import full_audit

def show_tab1():
    st.markdown("<h2 style='margin-bottom: 0.15rem;'>Applicant Loan Application</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 1rem;'>Single applicant enters details and gets instant decision intelligence.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(
            """
            <div class="ui-card">
                <h4 class="card-heading">👤 Personal Info</h4>
                <p class="card-desc">Identity and demographic profile for contextual fairness analysis.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        name = st.text_input("Full Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.slider("Age", 18, 80, 30)
        location = st.selectbox("Location Type", ["Urban", "Rural"])

        st.markdown(
            """
            <div class="ui-card">
                <h4 class="card-heading">💼 Financial Info</h4>
                <p class="card-desc">Income strength and job stability used by the lending policy engine.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        income = st.number_input("Annual Income (₹)", min_value=0, value=300000, step=50000)
        job_history = st.slider("Years of Employment", 0, 20, 3)

    with col2:
        st.markdown(
            """
            <div class="ui-card">
                <h4 class="card-heading">🏦 Loan Details</h4>
                <p class="card-desc">Requested amount, collateral cover, and prior credit behavior.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        loan_amount = st.number_input("Loan Amount Requested (₹)", min_value=10000, value=100000, step=10000)
        collateral_val = st.number_input("Collateral Value (₹)", min_value=0, value=50000, step=10000)
        credit_history = st.selectbox("Credit History", ["Clean", "1 Default", "2-3 Defaults", "Recent Defaults"])

        st.markdown(
            """
            <div class="ui-card">
                <h4 class="card-heading">🔍 Decision Context</h4>
                <p class="card-desc">The model blends scoring logic with explainability and fairness audits before final recommendation.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    applicant = {
        'name': name,
        'gender': gender,
        'age': age,
        'location': location,
        'income': income,
        'job_history': job_history,
        'collateral_pct': collateral_val / loan_amount if loan_amount > 0 else 0,
        'credit_history': credit_history
    }
    
    # Needs a session global DF to check against for bias
    df = st.session_state.get('df')

    b1, b2, b3 = st.columns([1, 1.4, 1])
    with b2:
        submit = st.button("Check Loan Eligibility", type="primary")

    if submit:
        score = score_applicant(applicant)
        if score >= 70:
            status = 'APPROVED'
        elif score >= 50:
            status = 'UNDER REVIEW'
        else:
            status = 'DENIED'
            
        applicant['score'] = score
        applicant['status'] = status
        
        audit = full_audit(applicant, df)
        explanation = generate_explanation(applicant, score, status, audit['trust']['score'])
        
        # UI DISPLAY
        st.divider()
        st.markdown(
            f"""
            <div class="ui-card">
                <h3 class="card-heading">Loan Decision: <span class='status-{status.replace(' ', '')}'>{status}</span></h3>
                <p class="card-desc">Applicant score <strong>{score}/100</strong> with explainability and trust confidence.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if status == 'APPROVED':
            st.success(f"Decision Confidence: {audit['trust']['score']}% (XAI Guardian)")
        elif status == 'UNDER REVIEW':
            st.warning(f"Decision Confidence: {audit['trust']['score']}% (XAI Guardian)")
        else:
            st.error(f"Decision Confidence: {audit['trust']['score']}% (XAI Guardian)")
            
        col_help, col_hurt = st.columns(2)
        with col_help:
            st.markdown(
                """
                <div class="ui-card">
                    <h4 class="card-heading">✅ Factors That Helped</h4>
                    <p class="card-desc">Positive signals that increased approval confidence.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for h in explanation['helped']:
                st.markdown(f"✓ {h}")
        with col_hurt:
            st.markdown(
                """
                <div class="ui-card">
                    <h4 class="card-heading">⚠️ Areas For Improvement</h4>
                    <p class="card-desc">Signals that lowered score or triggered review pressure.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for h in explanation['hurt']:
                st.markdown(f"⚠ {h}")
                
        st.divider()
        st.markdown(
            """
            <div class="ui-card">
                <h4 class="card-heading">🛡️ XAI Guardian Audit</h4>
                <p class="card-desc">Consistency, human-alignment, demographic fairness, and trust score checks.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        status_color = lambda s: "🟢 PASS" if s == "PASS" else ("🟡 WARNING" if s == "WARNING" else "🔴 FAIL/ALERT")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Re-evaluation", status_color(audit['re_evaluation'].get('status', 'PASS')))
        if audit['re_evaluation'].get('status') != 'PASS':
            c1.caption(audit['re_evaluation'].get('alert', 'Error'))
            
        c2.metric("Human Sim", status_color(audit['human_simulation'].get('status', 'PASS')))
        if audit['human_simulation'].get('status') != 'PASS':
            c2.caption(audit['human_simulation'].get('alert', 'Error'))
            
        c3.metric("Bias Check", status_color(audit['bias_detection'].get('status', 'PASS')))
        if audit['bias_detection'].get('status') != 'PASS':
            for k in ['gender_bias', 'location_bias']:
                if audit['bias_detection'].get(k):
                    c3.caption(audit['bias_detection'][k]['alert'])
            
        c4.metric("Trust Score", f"{audit['trust']['score']}%", audit['trust']['recommendation'])
