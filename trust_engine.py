def calculate_trust(ai_res, reeval_res, bias_res):
    """
    Calculates the timeline of AI trust based on subsequent checks.
    Starts at 95 (base AI trust).
    """
    
    timeline_events = []
    scores = []
    current_trust = 95
    
    timeline_events.append("Initial Evaluation")
    scores.append(current_trust)
    
    # Stage 2: Re-evaluation Check
    if reeval_res["inconsistency_detected"]:
        current_trust -= 20
        timeline_events.append("Self-Doubt Check (Failed)")
    else:
        timeline_events.append("Self-Doubt Check (Passed)")
    scores.append(current_trust)
    
    if bias_res["is_biased"]:
        current_trust -= (bias_res["bias_score"] // 2)
        timeline_events.append("Bias Check (Failed)")
    else:
        timeline_events.append("Bias Check (Passed)")
    scores.append(current_trust)
        
    # Stage 4: Confidence Factor
    confidence_penalty = (100 - ai_res["confidence"]) // 4
    current_trust -= confidence_penalty
    timeline_events.append("Final Calibrated Trust")
    scores.append(max(current_trust, 0)) # Ensure doesn't go below 0
    
    return {
        "final_score": scores[-1],
        "timeline_events": timeline_events,
        "timeline_scores": scores
    }
