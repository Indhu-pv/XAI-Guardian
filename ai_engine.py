def evaluate_candidate(candidate, high_comp_mode=False):
    """
    Strict, rule-based AI engine heavily weighting technical features.
    """
    # AI focuses mostly on coding score and experience
    coding_weight = 0.65
    exp_weight = 2.5  # Each year of experience = 2.5 points
    
    # Calculate base score out of 100
    score = (candidate["coding_score"] * coding_weight) + (candidate["experience"] * exp_weight)
    
    # High competition mode makes the AI stricter
    threshold = 85 if high_comp_mode else 75
    if high_comp_mode:
        score -= 5  # general penalty under stress
        
    score = min(max(int(score), 0), 100)
    
    selected = score >= threshold
    confidence = min(100, 50 + abs(score - threshold) * 1.5)
    
    reasons = []
    if selected:
        reasons.append(f"Strong technical coding score ({candidate['coding_score']}/100)")
        if candidate['experience'] > 5:
            reasons.append(f"Solid tenure of {candidate['experience']} years.")
    else:
        if candidate['coding_score'] < 80:
            reasons.append(f"Coding score ({candidate['coding_score']}/100) below competitive threshold.")
        if candidate['experience'] < 4:
            reasons.append(f"Experience ({candidate['experience']} years) insufficient for senior track.")
            
    return {
        "decision": "Selected" if selected else "Rejected",
        "score": score,
        "confidence": int(confidence),
        "reasons": reasons
    }
