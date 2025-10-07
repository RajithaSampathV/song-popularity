import streamlit as st

st.set_page_config(page_title="Payment | Music Popularity Predictor", layout="centered")

if "selected_plan" not in st.session_state:
    st.warning("⚠️ Please select a plan first from the Pricing page.")
    st.stop()

plan = st.session_state["selected_plan"]

# --- Payment UI ---
st.markdown(f"""
    <style>
        body {{
            background-color: #0e1117;
            color: #fff;
        }}
        .pay-card {{
            background: #161a23;
            border: 1px solid #262a35;
            border-radius: 20px;
            padding: 2.5rem;
            text-align: center;
            width: 400px;
            margin: 3rem auto;
        }}
        .btn-pay {{
            background: linear-gradient(90deg, #10b981, #3b82f6);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 2rem;
            font-weight: 600;
            cursor: pointer;
        }}
    </style>
    <div class='pay-card'>
        <h2>💳 Payment for {plan} Plan</h2>
        <p>Complete your purchase securely to unlock premium features.</p>
    </div>
""", unsafe_allow_html=True)

# --- Fake Payment Form ---
name = st.text_input("Full Name")
email = st.text_input("Email")
card_number = st.text_input("Card Number", type="password")
expiry = st.text_input("Expiry Date (MM/YY)")
cvv = st.text_input("CVV", type="password")

if st.button("Confirm Payment"):
    if not name or not email or not card_number:
        st.error("Please fill in all required fields.")
    else:
        st.success(f"✅ Payment successful! You are now subscribed to the **{plan} Plan**.")
        st.session_state.pop("selected_plan")
