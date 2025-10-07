import streamlit as st

st.set_page_config(page_title="About | Music Popularity Predictor", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: #fff;
        font-family: 'Inter', sans-serif;
    }

    .about-container {
        max-width: 1000px;
        margin: 2.5rem auto;
        background: linear-gradient(145deg, #161a23 0%, #11141a 100%);
        padding: 3.5rem;
        border-radius: 20px;
        border: 1px solid #1f2530;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        animation: fadeIn 0.8s ease-in-out;
    }

    h1 {
        color: #38bdf8;
        text-align: center;
        font-size: 2.6rem;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
        font-weight: 700;
    }

    h3 {
        color: #f87171;
        margin-top: 2rem;
        font-size: 1.4rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    p, li {
        font-size: 1.05rem;
        line-height: 1.8;
        color: #e5e7eb;
        margin-top: 0.4rem;
    }

    ul {
        margin-left: 1.2rem;
        margin-top: 0.6rem;
    }

    .highlight {
        color: #22c55e;
        font-weight: 600;
    }

    .section {
        margin-top: 2rem;
        padding: 1.5rem 2rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid #1f2530;
        transition: background 0.3s ease;
    }

    .section:hover {
        background: rgba(255, 255, 255, 0.05);
    }
    .st-emotion-cache-467cry a{
            color:white;
            text-decoration:none;}
    .cta {
        background: linear-gradient(90deg, #10b981, #3b82f6);
        color: white;
        border-radius: 12px;
        padding: 1rem 2.5rem;
        text-align: center;
        display: inline-block;
        margin-top: 2.5rem;
        font-weight: 600;
        font-size: 1.05rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-decoration: none;
    }

    .cta:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
    }

    .emoji {
        font-size: 1.4rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Main Content ---
st.markdown("<h1>About Music Popularity Predictor</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="section">
    <h3><span class="emoji">🧠</span> What We Do</h3>
    <p>Our system analyzes multiple audio characteristics — tempo, energy, spectral balance, 
    and danceability — to compute a <span class="highlight">popularity score (0–100)</span> using 
    machine learning models trained on real-world streaming and chart data.</p>
</div>

<div class="section">
    <h3><span class="emoji">🎯</span> Our Mission</h3>
    <p>We bridge creativity and data science — empowering artists to make informed, confident 
    decisions before publishing their music to global audiences.</p>
</div>

<div class="section">
    <h3><span class="emoji">⚙️</span> Built With</h3>
    <ul>
        <li>FastAPI + Streamlit</li>
        <li>Librosa + Scikit-Learn</li>
        <li>Google Cloud Run Hosting</li>
        <li>Plotly Interactive Visualizations</li>
    </ul>
</div>

<div class="section">
    <h3><span class="emoji">🌍</span> Why It Matters</h3>
    <p>Predicting popularity helps producers and labels allocate resources effectively — 
    focusing on songs with the highest potential, optimizing marketing strategies, and 
    understanding the pulse of their target audience.</p>
</div>

<div style="text-align:center;">
    <a href="/Contact" target="_blank" class="cta">Contact Our Team</a>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
