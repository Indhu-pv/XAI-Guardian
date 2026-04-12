# Utility functions for the engines

def safe_divide(numerator, denominator):
    return numerator / denominator if denominator != 0 else 0
