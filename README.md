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
4. Open the localhost link generated in the terminal to view the dashboard!
