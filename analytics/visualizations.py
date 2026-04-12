import plotly.express as px


def _apply_dark_chart_style(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10, 22, 36, 0.35)",
        font=dict(color="#dce8ff"),
        title_font=dict(color="#eef4ff", size=18),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.09)")
    return fig

def plot_approval_by_group(df, group_col, title):
    group_data = df.groupby(group_col)['status'].apply(lambda x: (x == 'APPROVED').mean() * 100).reset_index()
    group_data.columns = [group_col, 'Approval %']
    
    fig = px.bar(
        group_data,
        x=group_col,
        y='Approval %',
        text='Approval %',
        title=title,
        color_discrete_sequence=["#2f80ff"],
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(yaxis_range=[0, 100])
    return _apply_dark_chart_style(fig)

def plot_score_distribution(df):
    fig = px.histogram(df, x="score", color="status",
                       color_discrete_map={
                           "APPROVED": "#2cc07f",
                           "UNDER REVIEW": "#f2c04d",
                           "DENIED": "#ff5d73"
                       },
                       title="Score Distribution", nbins=20)
    
    # Add approval threshold line
    fig.add_vline(x=70, line_dash="dash", line_color="#9bb1cf", annotation_text="Approval Threshold (70)")
    return _apply_dark_chart_style(fig)

def plot_intersectional_heatmap(df):
    heatmap_data = df.pivot_table(index='gender', columns='location', values='status', 
                                  aggfunc=lambda x: (x == 'APPROVED').mean() * 100)
    
    fig = px.imshow(heatmap_data, text_auto=".1f", color_continuous_scale=['#ff5d73', '#f2c04d', '#2cc07f'], 
                    title="Approval % by Gender and Location", labels={"color": "Approval %"})
    return _apply_dark_chart_style(fig)
