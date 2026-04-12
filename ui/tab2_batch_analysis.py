import streamlit as st
import pandas as pd
from analytics.bias_analytics import run_batch_bias_analysis
from analytics.visualizations import plot_approval_by_group, plot_score_distribution, plot_intersectional_heatmap
from analytics.report_generator import generate_csv_report

def show_tab2():
    st.markdown("<h2 style='margin-bottom: 0.15rem;'>Batch Analysis & Bias Audit Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 1rem;'>Analyze your lending portfolio for fairness, drift, and approval consistency.</p>", unsafe_allow_html=True)
    
    df = st.session_state.get('df')
    if df is None:
        st.warning("No data loaded. Please check app configuration.")
        return
        
    metrics = run_batch_bias_analysis(df)
    
    st.markdown(
        """
        <div class="ui-card">
            <h4 class="card-heading">📌 Summary Metrics</h4>
            <p class="card-desc">Portfolio-level decisions split by approval outcome.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    total = len(df)
    approved = len(df[df['status'] == 'APPROVED'])
    review = len(df[df['status'] == 'UNDER REVIEW'])
    denied = len(df[df['status'] == 'DENIED'])
    
    c1.metric("Total Applications", total)
    c2.metric("Approved", f"{approved} ({(approved/total)*100:.1f}%)")
    c3.metric("Under Review", f"{review} ({(review/total)*100:.1f}%)")
    c4.metric("Denied", f"{denied} ({(denied/total)*100:.1f}%)")
    
    st.divider()

    st.markdown(
        """
        <div class="ui-card">
            <h4 class="card-heading">🚨 Action Items & Bias Alerts</h4>
            <p class="card-desc">High-priority fairness patterns and recommended remediation actions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not metrics.get('alerts'):
        st.success("No critical bias patterns detected in current dataset.")
    else:
        for alert in metrics['alerts']:
            if alert['level'] == 'CRITICAL':
                st.error(f"🔴 **CRITICAL:** {alert['message']}\n\n-> **Action:** {alert['action']}")
            else:
                st.warning(f"⚠ **WARNING:** {alert['message']}\n\n-> **Action:** {alert['action']}")
                
    st.divider()

    st.markdown(
        """
        <div class="ui-card">
            <h4 class="card-heading">📉 Approval Distribution Charts</h4>
            <p class="card-desc">Visual drill-down of fairness outcomes across demographics and score bands.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("<div class='ui-card'><h4 class='card-heading'>Gender Approval Profile</h4><p class='card-desc'>Approved rate by gender group.</p></div>", unsafe_allow_html=True)
        fig_gender = plot_approval_by_group(df, 'gender', "Approval Rate by Gender")
        st.plotly_chart(fig_gender, use_container_width=True)
        
    with colB:
        st.markdown("<div class='ui-card'><h4 class='card-heading'>Location Approval Profile</h4><p class='card-desc'>Urban and rural approval distribution.</p></div>", unsafe_allow_html=True)
        fig_loc = plot_approval_by_group(df, 'location', "Approval Rate by Location")
        st.plotly_chart(fig_loc, use_container_width=True)
        
    colC, colD = st.columns(2)
    with colC:
        st.markdown("<div class='ui-card'><h4 class='card-heading'>Score Distribution</h4><p class='card-desc'>Outcome clustering around approval thresholds.</p></div>", unsafe_allow_html=True)
        fig_score = plot_score_distribution(df)
        st.plotly_chart(fig_score, use_container_width=True)
        
    with colD:
        st.markdown("<div class='ui-card'><h4 class='card-heading'>Intersectional Heatmap</h4><p class='card-desc'>Approval percentage by gender and location.</p></div>", unsafe_allow_html=True)
        fig_heat = plot_intersectional_heatmap(df)
        st.plotly_chart(fig_heat, use_container_width=True)
        
    # Export Options
    st.divider()
    st.markdown(
        """
        <div class="ui-card">
            <h4 class="card-heading">⬇️ Export Options</h4>
            <p class="card-desc">Download a CSV audit artifact for reporting and review workflows.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    csv_data = generate_csv_report(df)
    st.download_button("Download CSV Report", csv_data, "batch_audit_report.csv", "text/csv")
