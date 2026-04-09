def human_evaluate(candidate, explain_like_human=True):
    """
    Simulates a human recruiter's evaluation approach.
    Values a balance of technical and soft skills.
    """
    
    human_score = (candidate["coding_score"] * 0.4) + (candidate["communication"] * 0.4) + (candidate["experience"] * 2)
    threshold = 70
    
    selected = human_score >= threshold
    
    if explain_like_human:
        if selected:
            explanation = f"I really liked {candidate['name']}. They might not be the absolute perfect coder on paper, but their communication is great ({candidate['communication']}/100) and they'd be a great cultural fit."
        else:
            explanation = f"Unfortunately, {candidate['name']} doesn't quite meet our bar right now. They're technically solid but might struggle with team collaboration given standard communication scores."
    else:
        if selected:
            explanation = f"SELECTED: Technical_weight=0.4, Comm_weight=0.4, Score={int(human_score)} > Threshold={threshold}."
        else:
            explanation = f"REJECTED: Technical_weight=0.4, Comm_weight=0.4, Score={int(human_score)} < Threshold={threshold}."

    return {
        "decision": "Selected" if selected else "Rejected",
        "explanation": explanation,
        "score": int(human_score)
    }
