import pandas as pd

def calculate_group_approval(df, group_col, group_val):
    group = df[df[group_col] == group_val]
    if len(group) == 0: return 0, 0
    approved = len(group[group['status'] == 'APPROVED'])
    return approved / len(group), len(group)

def run_batch_bias_analysis(df):
    """
    Takes the full batch of applicants and calculates overall fairness metrics.
    """
    total = len(df)
    total_approved = len(df[df['status'] == 'APPROVED'])
    overall_rate = total_approved / total if total > 0 else 0
    
    # Demographics
    men_rate, men_count = calculate_group_approval(df, 'gender', 'Male')
    women_rate, women_count = calculate_group_approval(df, 'gender', 'Female')
    urban_rate, urban_count = calculate_group_approval(df, 'location', 'Urban')
    rural_rate, rural_count = calculate_group_approval(df, 'location', 'Rural')
    
    # Intersectional
    rural_women = df[(df['location'] == 'Rural') & (df['gender'] == 'Female')]
    rural_women_rate = len(rural_women[rural_women['status'] == 'APPROVED']) / len(rural_women) if len(rural_women) > 0 else 0
    
    # Age groups
    y_group = df[df['age'] < 30]
    m_group = df[(df['age'] >= 30) & (df['age'] <= 50)]
    o_group = df[df['age'] > 50]
    
    y_rate = len(y_group[y_group['status'] == 'APPROVED'])/len(y_group) if len(y_group)>0 else 0
    m_rate = len(m_group[m_group['status'] == 'APPROVED'])/len(m_group) if len(m_group)>0 else 0
    o_rate = len(o_group[o_group['status'] == 'APPROVED'])/len(o_group) if len(o_group)>0 else 0
    
    # Alerts
    alerts = []
    
    gender_gap = abs(men_rate - women_rate)
    if gender_gap > 0.05:
        alerts.append({
            "level": "WARNING",
            "message": f"Gender gap of {gender_gap*100:.1f}% (women {women_rate*100:.1f}%, men {men_rate*100:.1f}%)",
            "action": "Monitor next 50 applications. Consider reweighting collateral vs income factors."
        })
        
    location_gap = abs(urban_rate - rural_rate)
    if location_gap > 0.10:
        alerts.append({
            "level": "CRITICAL",
            "message": f"Rural applicants approved at {rural_rate*100:.1f}% vs urban {urban_rate*100:.1f}% ({location_gap*100:.1f}% gap)",
            "action": "Review rural scoring rules. Consider +2 point bonus for rural applicants."
        })
        
    if overall_rate > 0 and (overall_rate - rural_women_rate) > 0.15:
         alerts.append({
            "level": "CRITICAL",
            "message": f"Women in rural areas approved {rural_women_rate*100:.1f}% only",
            "action": "Urgent manual review of last 20 denials. Consider intersectional fairness audit."
        })
         
    return {
        "overall_rate": overall_rate,
        "gender_rates": {"Male": men_rate, "Female": women_rate},
        "location_rates": {"Urban": urban_rate, "Rural": rural_rate},
        "age_rates": {"<30": y_rate, "30-50": m_rate, ">50": o_rate},
        "alerts": alerts,
        "raw_counts": {
            "Male": men_count, "Female": women_count, 
            "Urban": urban_count, "Rural": rural_count
        }
    }
