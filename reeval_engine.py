from ai_engine import evaluate_candidate

def reevaluate(candidate, initial_result, high_comp_mode=False):
    """
    Self-Doubt Logic: the AI slightly perturbs its internal thresholds or looks at secondary features
    to see if its initial decision might be brittle.
    """
    
    # Simulate the AI questioning itself by introducing a slight boost to communication 
    # to see if it flips a marginal rejection.
    perturbed_candidate = candidate.copy()
    
    # "What if communication compensates for a slightly lower coding score?"
    if candidate["communication"] > 85:
        perturbed_candidate["coding_score"] += 5
        
    # Run through the strict AI again with perturbed data
    second_pass_result = evaluate_candidate(perturbed_candidate, high_comp_mode)
    
    # Determine inconsistency
    inconsistency_detected = initial_result["decision"] != second_pass_result["decision"]
    
    reasons = []
    if inconsistency_detected:
        reasons.append("⚠️ SECOND PASS FLIP: High communication score compensated for marginal technical gap.")
    else:
        reasons.append("Decision remained consistent upon re-evaluation.")
        
    return {
        "decision": second_pass_result["decision"],
        "score": second_pass_result["score"],
        "confidence": second_pass_result["confidence"],
        "inconsistency_detected": inconsistency_detected,
        "reasons": reasons
    }
