import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');

        :root {
            --bg: #08111f;
            --bg-soft: #0d1a2b;
            --surface: rgba(16, 29, 46, 0.9);
            --surface-2: rgba(12, 25, 40, 0.9);
            --stroke: rgba(255, 255, 255, 0.08);
            --text-primary: #edf3ff;
            --text-secondary: #b9c8dd;
            --accent-blue: #2f80ff;
            --accent-teal: #00b8a9;
            --success: #2cc07f;
            --warning: #f2c04d;
            --danger: #ff5d73;
        }

        .stApp {
            background:
                radial-gradient(900px 500px at 10% -10%, rgba(47, 128, 255, 0.20), transparent 60%),
                radial-gradient(700px 400px at 95% -5%, rgba(0, 184, 169, 0.18), transparent 60%),
                linear-gradient(180deg, #060d18 0%, var(--bg) 60%, #060c16 100%);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        h1, h2, h3, h4 {
            color: var(--text-primary);
            font-family: 'Manrope', sans-serif;
            letter-spacing: -0.02em;
        }

        p, label, .stMarkdown, .stCaption {
            color: var(--text-secondary);
        }

        .hero {
            text-align: center;
            margin: 0 auto 1.4rem;
            padding: 2.1rem 1.2rem;
            border-radius: 20px;
            border: 1px solid var(--stroke);
            background: linear-gradient(145deg, rgba(47, 128, 255, 0.14), rgba(0, 184, 169, 0.08));
            backdrop-filter: blur(8px);
            box-shadow: 0 20px 45px rgba(2, 8, 18, 0.45);
            animation: fadeInUp 0.7s ease-out;
        }

        .hero-title {
            margin: 0;
            font-size: clamp(1.7rem, 4vw, 2.8rem);
            font-weight: 800;
            line-height: 1.2;
            color: var(--text-primary);
        }

        .gradient-text {
            background: linear-gradient(90deg, #66b3ff 0%, #33e4d4 45%, #5adf8d 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            color: transparent;
        }

        .hero-subtitle {
            margin-top: 0.6rem;
            font-size: 1rem;
            color: #d8e3f8;
        }

        .hero-tagline {
            margin-top: 0.4rem;
            font-size: 0.92rem;
            color: #9bb1cf;
        }

        .metric-card {
            border: 1px solid var(--stroke);
            border-radius: 16px;
            padding: 0.95rem 1rem;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01));
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.3);
            min-height: 114px;
            transition: transform 0.25s ease, border-color 0.25s ease;
            animation: fadeInUp 0.8s ease-out;
        }

        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(47, 128, 255, 0.5);
        }

        .metric-label {
            font-size: 0.84rem;
            color: #9bb1cf;
            margin-bottom: 0.55rem;
        }

        .metric-value {
            color: #f5f9ff;
            font-size: 1.48rem;
            font-weight: 800;
            line-height: 1.2;
        }

        .metric-note {
            margin-top: 0.3rem;
            font-size: 0.8rem;
            color: #8ea4c5;
        }

        .ui-card {
            border: 1px solid var(--stroke);
            border-radius: 16px;
            background: linear-gradient(180deg, var(--surface), var(--surface-2));
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.34);
            padding: 1.05rem 1.15rem;
            margin-bottom: 1rem;
            animation: fadeInUp 0.6s ease-out;
        }

        .card-heading {
            margin: 0 0 0.35rem;
            color: #eaf2ff;
            font-size: 1.02rem;
            font-weight: 700;
        }

        .card-desc {
            margin: 0 0 0.75rem;
            font-size: 0.86rem;
            color: #9bb1cf;
        }

        [data-testid="stTabs"] [role="tablist"] {
            gap: 0.55rem;
            border: none;
            padding: 0.25rem;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 999px;
            width: fit-content;
            margin: 0 auto 1.3rem;
        }

        [data-testid="stTabs"] [role="tab"] {
            border: 1px solid transparent;
            border-radius: 999px;
            padding: 0.45rem 1rem;
            background: rgba(255, 255, 255, 0.03);
            color: #c8d8ef;
            transition: all 0.25s ease;
        }

        [data-testid="stTabs"] [role="tab"]:hover {
            background: rgba(47, 128, 255, 0.16);
            color: #f3f8ff;
        }

        [data-testid="stTabs"] [aria-selected="true"] {
            background: linear-gradient(90deg, rgba(47, 128, 255, 0.28), rgba(0, 184, 169, 0.2));
            border-color: rgba(83, 149, 255, 0.5);
            color: #f5f9ff;
        }

        [data-testid="stTabs"] [data-testid="stVerticalBlock"] {
            animation: fadeInUp 0.45s ease-out;
        }

        .stButton > button {
            border-radius: 12px;
            border: 1px solid rgba(85, 150, 255, 0.5);
            color: #f6f9ff;
            font-weight: 700;
            background: linear-gradient(100deg, #2f80ff 0%, #1f9ed8 55%, #00b8a9 100%);
            box-shadow: 0 10px 24px rgba(23, 84, 170, 0.35);
            transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.22s ease;
            width: 100%;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            filter: brightness(1.06);
            box-shadow: 0 15px 28px rgba(20, 92, 185, 0.4);
        }

        .status-APPROVED {
            color: var(--success);
            font-weight: 700;
        }

        .status-UNDERREVIEW {
            color: var(--warning);
            font-weight: 700;
        }

        .status-DENIED {
            color: var(--danger);
            font-weight: 700;
        }

        .footer {
            margin-top: 1.4rem;
            text-align: center;
            color: #8ea4c5;
            font-size: 0.85rem;
            border-top: 1px solid var(--stroke);
            padding-top: 0.9rem;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    """, unsafe_allow_html=True)
