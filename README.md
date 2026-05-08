<<<<<<< HEAD
# XAI Guardian: Ethical AI for Microfinance Lending

This project combines a robust Microfinance Lending Engine with an Explainable AI (XAI) Guardian Audit Framework to ensure ethical, transparent, and fair microfinance lending decisions.

## Setup Instructions

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

## Application Structure

- **Tab 1: Application Form:** Interface for single applicant evaluations with an immediate decision and XAI Guardian Audit report.
- **Tab 2: Batch Analysis Dashboard:** Comprehensive visualizations for demographic parity, approval rates, and structural bias alerts across hundreds of simulated records.
- **Tab 3: Lender Audit & Manual Review:** Detail-oriented review dashboard enabling lenders to analyze AI decisions, XAI score confidence, and manually override system judgments with detailed documentation.

## Social Impact

Enables unbanked populations to access microfinance securely with transparent, auditable decision-making that combats intersectional biases.
=======
# XAI Guardian: AI That Questions Itself 🧠

A hackathon-level Explainable AI (XAI) Dashboard built with Streamlit, Python, and Plotly.

## Overview
This system simulates a high-stakes AI evaluating a candidate profile but introduces layers of "self-reflection":
- **AI Engine**: Strict standard rule-based evaluation.
- **Re-evaluation Engine (Self-Doubt)**: AI slightly perturbs inputs to see if the decision is brittle.
- **Human Engine**: AI attempts to compare its result with a human-like evaluation.
- **Bias Engine**: Actively checks for potential indirect penalties on protected classes.
- **Trust Engine**: Calculates a dynamic trust score over the whole pipeline.

## How to run:
1. Ensure you have Python 3.11+ installed.
2. Install the necessary libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

