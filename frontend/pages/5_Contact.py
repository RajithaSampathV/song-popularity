import streamlit as st

st.set_page_config(page_title="Contact | Music Popularity Predictor", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: #fff;
        font-family: 'Inter', sans-serif;
    }

    .contact-container {
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

    .contact-form {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        margin-top: 1.5rem;
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .form-label {
        font-weight: 600;
        color: #e5e7eb;
        font-size: 1rem;
    }

    .form-input, .form-textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #e5e7eb;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .form-input:focus, .form-textarea:focus {
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    .form-textarea {
        min-height: 120px;
        resize: vertical;
    }

    .submit-btn {
        background: linear-gradient(90deg, #10b981, #3b82f6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.05rem;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-top: 1rem;
    }

    .submit-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
    }

    .contact-info {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }

    .info-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #1f2530;
        text-align: center;
        transition: all 0.3s ease;
        height: 200px;
    }

    .info-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-5px);
    }

    .info-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    .info-title {
        font-weight: 600;
        color: #38bdf8;
        margin-bottom: 0.5rem;
    }

    .info-detail {
        color: #e5e7eb;
        font-size: 0.95rem;
    }

    .social-links {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 2rem;
    }

    .social-link {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.75rem;
        border-radius: 10px;
        text-decoration: none;
        color: #e5e7eb;
        transition: all 0.3s ease;
        border: 1px solid #374151;
    }

    .social-link:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: #3b82f6;
        transform: translateY(-2px);
    }

    .emoji {
        font-size: 1.4rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .success-message {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid #22c55e;
        color: #22c55e;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        text-align: center;
    }
    .st-emotion-cache-467cry a{
            color:white;
            text-decoration:none;
    }
</style>
""", unsafe_allow_html=True)

# --- Main Content ---
# Header
st.markdown("<h1>Contact Us</h1>", unsafe_allow_html=True)

# Contact Form Section
st.markdown('<h3><span class="emoji">📧</span> Send Us a Message</h3>', unsafe_allow_html=True)
st.markdown('<p>Have questions about our music popularity predictor? We\'d love to hear from you. Send us a message and we\'ll respond as soon as possible.</p>', unsafe_allow_html=True)

# Contact Form using Streamlit components
with st.form("contact_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input(
            "Full Name *",
            placeholder="Enter your full name",
            help="Please enter your full name"
        )
    
    with col2:
        email = st.text_input(
            "Email Address *",
            placeholder="Enter your email",
            help="We'll never share your email with anyone else"
        )
    
    subject = st.text_input(
        "Subject *",
        placeholder="What is this regarding?",
        help="Brief description of your inquiry"
    )
    
    message = st.text_area(
        "Message *",
        placeholder="Tell us about your inquiry...",
        height=120,
        help="Please provide detailed information about your question or concern"
    )
    
    submitted = st.form_submit_button(
        "Send Message",
        type="primary",
        use_container_width=True
    )
    
    if submitted:
        if name and email and subject and message:
            st.success("🎉 Thank you! Your message has been sent successfully. We'll get back to you within 24 hours.")
        else:
            st.error("⚠️ Please fill in all required fields.")

st.markdown('</div>', unsafe_allow_html=True)

# Contact Information Section
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<h3><span class="emoji">📍</span> Get In Touch</h3>', unsafe_allow_html=True)
st.markdown('<p>Prefer other ways to reach us? Here are our contact details:</p>', unsafe_allow_html=True)

# Contact Info Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">📧</div>
        <div class="info-title">Email Us</div>
        <div class="info-detail">support@songpopularity.com</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">📞</div>
        <div class="info-title">Call Us</div>
        <div class="info-detail">+94 71 955 24 84</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🏢</div>
        <div class="info-title">Visit Us</div>
        <div class="info-detail">123 Kaduwela road<br>Malabe</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🕒</div>
        <div class="info-title">Business Hours</div>
        <div class="info-detail">Mon - Fri: 9AM - 6PM<br>Weekends: Closed</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Social Media Section
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<h3><span class="emoji">🌐</span> Follow Us</h3>', unsafe_allow_html=True)
st.markdown('<p>Stay connected with us on social media for updates and news:</p>', unsafe_allow_html=True)

# Social Media Links
social_cols = st.columns(5)
social_platforms = [
    ("📘", "Facebook", "https://facebook.com"),
    ("🐦", "Twitter", "https://twitter.com"),
    ("💼", "LinkedIn", "https://linkedin.com"),
    ("🐙", "GitHub", "https://github.com"),
    ("📷", "Instagram", "https://instagram.com")
]

for i, (icon, platform, url) in enumerate(social_platforms):
    with social_cols[i]:
        st.markdown(f"""
        <a href="{url}" target="_blank" class="social-link">
            {icon} {platform}
        </a>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# FAQ Section
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<h3><span class="emoji">❓</span> Frequently Asked Questions</h3>', unsafe_allow_html=True)

# FAQ Items
faq_data = [
    {
        "question": "How accurate is the popularity prediction?",
        "answer": "Our model achieves approximately 85% accuracy based on historical data and continuous testing."
    },
    {
        "question": "What audio formats do you support?",
        "answer": "We currently support MP3, WAV, and FLAC formats up to 50MB in size."
    },
    {
        "question": "Is my data secure?",
        "answer": "Yes, we take data privacy seriously. All uploaded files are processed securely and deleted after analysis."
    },
    {
        "question": "Do you offer API access?",
        "answer": "Yes, we provide API access for enterprise clients. Contact us for pricing and documentation."
    }
]

for faq in faq_data:
    with st.expander(f"**{faq['question']}**"):
        st.write(faq['answer'])

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)