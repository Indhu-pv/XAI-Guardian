import numpy as np
from engines.lending_engine import score_applicant

def re_evaluate_decision(applicant):
    """
    Rescore applicant independently with synthetic jitter to check consistency.
    """
    original_score = score_applicant(applicant, add_jitter=False)
    re_eval_score = score_applicant(applicant, add_jitter=True)
    
    consistency = 1 - abs(original_score - re_eval_score) / 100
    
    if consistency < 0.95:
        return {
            "alert": "INCONSISTENT SCORING",
            "severity": "HIGH",
            "original": original_score,
            "re_eval": re_eval_score,
            "consistency_pct": round(consistency * 100),
            "status": "FAIL"
        }
    return {
        "alert": None,
        "consistency_pct": round(consistency * 100),
        "status": "PASS"
    }

def simulate_human_decision(applicant):
    """
    Mimic how a human loan officer would decide.
    """
    income = applicant.get('income', 0)
    job_history = applicant.get('job_history', 0)
    collateral = applicant.get('collateral_pct', 0)
    
    human_approve = False
    if income > 600000 and job_history >= 2:
        human_approve = True
    elif income > 400000 and collateral >= 0.4:
        human_approve = True
    elif income > 250000 and collateral >= 0.6:
        human_approve = True
        
    ai_approve = score_applicant(applicant) >= 70
    
    alignment = 1 if human_approve == ai_approve else 0
    
    if alignment == 0:
        return {
            "alert": "AI-HUMAN DIVERGENCE",
            "severity": "MEDIUM",
            "human_says": "APPROVE" if human_approve else "DENY",
            "ai_says": "APPROVE" if ai_approve else "DENY",
            "recommendation": "Manual review advised",
            "status": "FAIL"
        }
    return {
        "alert": None,
        "alignment_pct": 100,
        "status": "PASS"
    }

def detect_demographic_bias(applicant, all_applicants_df=None, threshold=0.05):
    """
    Find applicants with SAME SCORE but DIFFERENT OUTCOMES by demographics.
    Check: Does gender/location affect approval despite similar score?
    """
    if all_applicants_df is None or len(all_applicants_df) == 0:
        # Default pass if no global context
        return {
            "gender_bias": None,
            "location_bias": None,
            "status": "PASS",
            "bias_score": 100
        }
        
    myscore = applicant.get('score', score_applicant(applicant))
    mygender = applicant.get('gender')
    mylocation = applicant.get('location')
    mystatus = applicant.get('status')
    
    # Relax exact score matching to a small window
    # In a real scenario, this would use model metrics or similarity
    similar_applicants = all_applicants_df[
        (all_applicants_df['score'].between(myscore - 5, myscore + 5))
    ]
    
    bias_score = 100
    findings = {"gender_bias": None, "location_bias": None, "intersectional_bias": None, "status": "PASS"}
    
    # Location
    opp_location = 'Urban' if mylocation == 'Rural' else 'Rural'
    similar_opp_loc = similar_applicants[similar_applicants['location'] == opp_location]
    if len(similar_opp_loc) >= 5: # Need enough for a statistical guess
        opp_loc_appr = (similar_opp_loc['status'] == 'APPROVED').mean()
        my_group = similar_applicants[similar_applicants['location'] == mylocation]
        my_loc_appr = (my_group['status'] == 'APPROVED').mean() if len(my_group)>0 else 0
        
        if mylocation == 'Rural' and (opp_loc_appr - my_loc_appr) > threshold:
            findings["location_bias"] = {
                "alert": "LOCATION BIAS DETECTED",
                "severity": "CRITICAL",
                "explanation": f"Similar score: Urban approved {opp_loc_appr*100:.0f}%, Rural approved {my_loc_appr*100:.0f}%"
            }
            bias_score -= 20
            findings["status"] = "WARNING"
            
    # Gender
    opp_gender = 'Male' if mygender == 'Female' else 'Female'
    similar_opp_gen = similar_applicants[similar_applicants['gender'] == opp_gender]
    if len(similar_opp_gen) >= 5:
        opp_gen_appr = (similar_opp_gen['status'] == 'APPROVED').mean()
        my_group = similar_applicants[similar_applicants['gender'] == mygender]
        my_gen_appr = (my_group['status'] == 'APPROVED').mean() if len(my_group)>0 else 0
        
        if mygender == 'Female' and (opp_gen_appr - my_gen_appr) > threshold:
            findings["gender_bias"] = {
                "alert": "GENDER BIAS DETECTED",
                "severity": "MEDIUM",
                "explanation": f"Similar score: Male approved {opp_gen_appr*100:.0f}%, Female approved {my_gen_appr*100:.0f}%"
            }
            bias_score -= 15
            findings["status"] = "WARNING"
            
    findings["bias_score"] = bias_score
    return findings


def calculate_trust_score(re_eval, human_sim, bias_res):
    """
    Combine factors into a trustworthiness metric.
    Trust = (Consistency * 0.4) + (Human Alignment * 0.4) + (Fairness * 0.2)
    """
    consistency_val = re_eval.get("consistency_pct", 100)
    human_align_val = 100 if human_sim.get("alignment_pct") else 0
    fairness_val = bias_res.get("bias_score", 100)
    
    trust = (consistency_val * 0.4) + (human_align_val * 0.4) + (fairness_val * 0.2)
    trust_pct = round(trust)
    
    if trust_pct >= 85:
        recommendation = "APPROVE - Highly Trustworthy Decision"
        color = "green"
    elif trust_pct >= 70:
        recommendation = "REVIEW - Moderate Confidence"
        color = "yellow"
    else:
        recommendation = "ESCALATE - Low Confidence, Manual Review Required"
        color = "red"
        
    return {
        "score": trust_pct,
        "recommendation": recommendation,
        "color": color
    }
    
def full_audit(applicant, all_applicants_df=None):
    re_eval = re_evaluate_decision(applicant)
    human = simulate_human_decision(applicant)
    bias = detect_demographic_bias(applicant, all_applicants_df)
    trust = calculate_trust_score(re_eval, human, bias)
    
    return {
        "re_evaluation": re_eval,
        "human_simulation": human,
        "bias_detection": bias,
        "trust": trust
    }
