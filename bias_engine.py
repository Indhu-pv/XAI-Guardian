def detect_bias(candidate):
    """
    Checks if there are indirect bias indicators based on age or gender.
    Returns a bias score (0 = no bias, higher = more potential bias)
    and warnings.
    """
    warnings = []
    bias_score = 0
    
    # Example logic: Older candidates might be penalized by strict rule-engines 
    # if modern tech stacks aren't perfectly mapped in their base score.
    if candidate["age"] > 50:
        bias_score += 30
        warnings.append(f"⚠️ POTENTIAL AGE BIAS: AI models often under-index legacy experience. Candidate age ({candidate['age']}) flags a potential indirect penalty.")
        
    # Example logic: If gender is female and they have very high communication but slightly lower coding score,
    # the strict AI might reject them, reflecting a systemic bias where soft-skills are undervalued in technical screens.
    if candidate["gender"] == "Female" and candidate["communication"] > 85 and candidate["coding_score"] < 85:
        bias_score += 40
        warnings.append("⚠️ SYSTEMIC BIAS ALERT: System heavily penalizes coding score while undervaluing strong communication skills common in cross-functional female candidates.")
        
    return {
        "bias_score": bias_score,
        "warnings": warnings,
        "is_biased": bias_score > 0
    }
