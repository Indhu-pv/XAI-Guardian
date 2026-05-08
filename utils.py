import streamlit as st

def get_sample_data():
    return [
        {
            "id": "CAND-001",
            "name": "Alex Mercer",
            "experience": 8,
            "coding_score": 92,
            "communication": 65,
            "age": 31,
            "gender": "Male",
            "background": "Traditional CS degree, mostly backend."
        },
        {
            "id": "CAND-002",
            "name": "Sarah Jenkins",
            "experience": 3,
            "coding_score": 85,
            "communication": 95,
            "age": 27,
            "gender": "Female",
            "background": "Bootcamp grad, strong frontend and team leadership."
        },
        {
            "id": "CAND-003",
            "name": "Robert Chen",
            "experience": 20,
            "coding_score": 88,
            "communication": 80,
            "age": 55,
            "gender": "Male",
            "background": "Veteran dev, transitioning to modern stacks."
        },
        {
            "id": "CAND-004",
            "name": "Emily Davis",
            "experience": 1,
            "coding_score": 60,
            "communication": 90,
            "age": 23,
            "gender": "Female",
            "background": "Junior dev, great culture fit but needs technical mentoring."
        }
    ]

def apply_custom_css():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        .css-1d391kg {
            background-color: #1e293b;
        }
        .stButton>button {
            background-color: #3b82f6;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #2563eb;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }
        .metric-card {
            background-color: #1e293b;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #334155;
            margin-bottom: 1rem;
        }
        .alert-warning {
            background-color: #f59e0b1a;
            border-left: 4px solid #f59e0b;
            padding: 1rem;
            border-radius: 4px;
            color: #fcd34d;
        }
        .alert-danger {
            background-color: #ef44441a;
            border-left: 4px solid #ef4444;
            padding: 1rem;
            border-radius: 4px;
            color: #fca5a5;
        }
        .alert-success {
            background-color: #10b9811a;
            border-left: 4px solid #10b981;
            padding: 1rem;
            border-radius: 4px;
            color: #6ee7b7;
        }
        h1, h2, h3 {
            color: #ffffff;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)
