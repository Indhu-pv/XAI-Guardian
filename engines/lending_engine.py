import random

def score_applicant(applicant_dict, add_jitter=False):
    """
    Given a dict representing an applicant, return the score.
    If add_jitter is True, simulates system instability for XAI re-eval.
    """
    score = 0
    income = applicant_dict.get('income', 0)
    job_history = applicant_dict.get('job_history', 0)
    collateral_pct = applicant_dict.get('collateral_pct', 0)
    credit_history = applicant_dict.get('credit_history', 'Clean')
    gender = applicant_dict.get('gender', 'Male')
    location = applicant_dict.get('location', 'Urban')
    age = applicant_dict.get('age', 30)

    # INCOME
    if income >= 1000000:
        score += 30
    elif income >= 500000:
        score += 20
    elif income >= 250000:
        score += 10
    
    # JOB STABILITY
    if job_history >= 5:
        score += 25
    elif job_history >= 3:
        score += 15
    elif job_history >= 1:
        score += 8
    else:
        score += 2
        
    # COLLATERAL
    if collateral_pct >= 0.6:
        score += 25
    elif collateral_pct >= 0.4:
        score += 15
    elif collateral_pct >= 0.2:
        score += 8
        
    # CREDIT HISTORY
    if credit_history == 'Clean':
        score += 20
    elif credit_history == '1 Default':
        score += 10
    elif credit_history == '2-3 Defaults':
        score += 5
    else:  # Recent defaults
        score -= 15
        
    # DEMOGRAPHIC BONUS
    if gender == 'Female':
        score += 2
    if location == 'Rural':
        score += 2
    if 25 <= age <= 45:
        score += 1
        
    if add_jitter:
        # Introduced minimal arbitrary noise for system consistency audit testing
        jitter = random.choice([0, 0, 0, -2, 2, -5, 5])
        score += jitter

    return min(100, max(0, score))


def generate_explanation(applicant_dict, score, status, trust_score=None):
    """
    Generate an explanation payload based on score components.
    """
    helped = []
    hurt = []
    
    income = applicant_dict.get('income', 0)
    if income >= 500000:
        helped.append(f"Strong annual income (₹{income:,.0f})")
    elif income < 250000:
        hurt.append(f"Low annual income (₹{income:,.0f}) can be improved")
        
    job_h = applicant_dict.get('job_history', 0)
    if job_h >= 3:
        helped.append(f"Stable job history ({job_h} years)")
    else:
        hurt.append(f"Limited job history ({job_h} years) - Ideally need 2+ years")
        
    collat = applicant_dict.get('collateral_pct', 0)
    if collat >= 0.4:
        helped.append(f"Good collateral ({int(collat*100)}% of loan)")
    else:
        hurt.append(f"Limited collateral ({int(collat*100)}%) - Need 40%+ ideally")
        
    credit = applicant_dict.get('credit_history', 'Clean')
    if credit == 'Clean':
        helped.append("Clean credit history")
    else:
        hurt.append(f"Credit History concerns: {credit}")
        
    if not hurt and status != 'APPROVED':
        hurt.append("Overall risk profile slightly elevated based on aggregated factors")
        
    explanation = {
        "score": score,
        "status": status,
        "helped": helped,
        "hurt": hurt,
        "trust_score": trust_score if trust_score else 85,
        "recommendation": "APPROVE - Safe Decision" if status == "APPROVED" else ("REVIEW" if status == "UNDER REVIEW" else "DENY")
    }
    return explanation
