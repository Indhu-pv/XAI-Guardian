import streamlit as st
import pandas as pd
from engines.lending_engine import generate_explanation
from engines.xai_guardian import full_audit

def show_tab3():
    st.markdown("<h2 style='margin-bottom: 0.15rem;'>Lender Manual Review & Audit Interface</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 1rem;'>Flag suspicious decisions, apply overrides, and maintain audit-ready transparency.</p>", unsafe_allow_html=True)
    
    df = st.session_state.get('df')
    if df is None:
        return
        
    st.markdown(
        """
        <div class="ui-card">
            <h4 class="card-heading">🔎 Filter & Search</h4>
            <p class="card-desc">Narrow by outcome and applicant id before manual review.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    status_filter = c1.selectbox("Decision Filter", ["All", "APPROVED", "DENIED", "UNDER REVIEW"])
    search_id = c2.text_input("Search ID")
    
    # Process filters
    view_df = df.copy()
    if status_filter != "All":
        view_df = view_df[view_df['status'] == status_filter]
    if search_id:
        view_df = view_df[view_df['id'].str.contains(search_id)]
        
    st.markdown(
        """
        <div class="ui-card">
            <h4 class="card-heading">📋 Review Queue</h4>
            <p class="card-desc">Current slice of applications matching your filters.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(view_df[['id', 'name', 'gender', 'location', 'score', 'status']], use_container_width=True)
    
    st.divider()
    st.markdown(
        """
        <div class="ui-card">
            <h4 class="card-heading">🧾 Detailed Decision Audit</h4>
            <p class="card-desc">Inspect explainability signals and fairness diagnostics for a selected applicant.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_id = st.selectbox("Select Applicant ID to Audit", view_df['id'].tolist())
    
    if selected_id:
        applicant = df[df['id'] == selected_id].iloc[0].to_dict()
        audit = full_audit(applicant, df)
        
        st.markdown(
            f"""
            <div class="ui-card">
                <h4 class="card-heading">Applicant: {applicant['name']} (ID: {applicant['id']})</h4>
                <p class="card-desc">Reviewing original decision logic and override context.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        status_color = 'green' if applicant['status'] == 'APPROVED' else ('orange' if applicant['status'] == 'UNDER REVIEW' else 'red')
        st.markdown(f"**ORIGINAL DECISION:** :{status_color}[{applicant['status']}]")
        st.markdown(f"**Score:** {applicant['score']}/100 | **Trust Score:** {audit['trust']['score']}% ({audit['trust']['recommendation']})")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 class='card-heading'>📊 Scoring Breakdown</h4>", unsafe_allow_html=True)
            st.write(f"- **Income (₹{applicant['income']}):** Base logic applied")
            st.write(f"- **Job History ({applicant['job_history']} years):** Base logic applied")
            st.write(f"- **Collateral ({(applicant['collateral_pct']*100):.0f}%):** Base logic applied")
            st.write(f"- **Demographics:** {applicant['gender']}, {applicant['location']}")
            
        with col2:
            st.markdown("<h4 class='card-heading'>🛡️ XAI Guardian Audit</h4>", unsafe_allow_html=True)
            st.write(f"- **Re-evaluation:** {audit['re_evaluation'].get('status')}")
            st.write(f"- **Human Simulation:** {audit['human_simulation'].get('status')}")
            bias_stat = audit['bias_detection'].get('status')
            st.write(f"- **Bias Detection:** {bias_stat}")
            if bias_stat != 'PASS':
                 st.caption("Investigate similar profile approval rates.")
                 
        st.divider()
        st.markdown(
            """
            <div class="ui-card">
                <h4 class="card-heading">✍️ Lender Action</h4>
                <p class="card-desc">Apply a justified manual override and capture notes for the audit trail.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        override = st.selectbox("Manual Override", ["No Override", "APPROVE", "DENY", "REQUEST MORE INFO"])
        if override != "No Override":
            reason = st.selectbox("Reason for Override", ["Better local knowledge", "Customer history", "Bias correction", "Other"])
            notes = st.text_area("Additional Notes")
            if st.button("CONFIRM OVERRIDE"):
                st.success(f"Successfully overridden decision to {override} by Lender due to: {reason}.")
