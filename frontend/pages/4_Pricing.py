import streamlit as st

st.set_page_config(page_title="Pricing Plans | Music Popularity Predictor", layout="wide")

# --- Custom CSS for industrial look ---
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #fff;
        }
        .pricing-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 2rem;
            margin-top: 3rem;
        }
        .card {
            background: #161a23;
            border: 1px solid #262a35;
            border-radius: 20px;
            padding: 2rem;
            width: 320px;
            height: 350px;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 5px 25px rgba(0, 255, 160, 0.2);
        }
        .plan-title {
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .plan-price {
            font-size: 1.4rem;
            color: #34d399;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .feature-list {
            text-align: left;
            margin: 1rem 0;
        }
        .feature-list li {
            margin: 0.5rem 0;
        }
        .btn {
            display: inline-block;
            background: linear-gradient(90deg, #10b981, #3b82f6);
            color: white;
            font-weight: 600;
            padding: 0.6rem 1.5rem;
            border-radius: 12px;
            text-decoration: none;
            transition: opacity 0.3s ease;
        }
        .btn:hover {
            opacity: 0.85;
        }
        .title {
            text-align: center;
            margin-top: 2rem;
        }
        .subtitle {
            text-align: center;
            color: #9ca3af;
        }
        .st-emotion-cache-wfksaw{
            align-items: center;}
    </style>
""", unsafe_allow_html=True)

# --- Page Header ---
st.markdown("<h1 class='title'>💎 Choose Your Plan</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Find the perfect plan for artists, producers, or record labels</p>", unsafe_allow_html=True)

# --- Pricing Plans ---
col1, col2, col3 = st.columns(3, gap="large")

plans = {
    "Free": {
        "price": "$0 / month",
        "emoji": "🎧",
        "features": [
            "3 predictions / day",
            "Limited genres",
            "Basic insights"
        ]
    },
    "Pro": {
        "price": "$4.99 / month",
        "emoji": "🚀",
        "features": [
            "100 predictions / month",
            "All genres access",
            "Advanced analytics",
            "Downloadable reports"
        ]
    },
    "Business": {
        "price": "$14.99 / month",
        "emoji": "🏢",
        "features": [
            "Unlimited predictions",
            "Custom model training",
            "Dedicated analytics dashboard",
            "24/7 premium support"
        ]
    }
}

# --- Render Cards ---
selected_plan = None

for i, (plan, details) in enumerate(plans.items()):
    with [col1, col2, col3][i]:
        st.markdown(f"""
            <div class="card">
                <div class="plan-title">{details['emoji']} {plan}</div>
                <div class="plan-price">{details['price']}</div>
                <ul class="feature-list">
                    {''.join(f"<li>✅ {f}</li>" for f in details['features'])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"Select {plan} Plan", key=plan):
            selected_plan = plan

# --- Redirect to Payment Page ---
if selected_plan:
    st.session_state["selected_plan"] = selected_plan
    st.switch_page("pages/payment.py")
