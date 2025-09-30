# frontend/streamlit_app.py
import streamlit as st
import requests
import os
import plotly.graph_objects as go

st.set_page_config(
    page_title="🎵 Music Popularity Predictor",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Sidebar info ---
st.sidebar.title("🎵 About")
st.sidebar.info(
    """
    Upload your MP3 song and select the genre.
    Our AI model predicts the song's popularity score (0-100).
    """
)

st.title("🎵 Music Popularity Predictor")
st.subheader("Predict your song's popularity score")

# --- Upload MP3 ---
uploaded_file = st.file_uploader(
    "Upload your song (MP3 format only)", 
    type=["mp3"],
    help="Supported formats: .mp3"
)

# --- Select genre ---
genre = st.selectbox(
    "Select genre", 
    ["pop", "rock", "hip-hop", "electronic", "j-pop", "classical", "acoustic"]
)

API_URL = "http://127.0.0.1:8000/predict_file"

if uploaded_file:
    # Display audio player
    st.audio(uploaded_file, format="audio/mp3")

    # Predict button
    if st.button("Predict Popularity"):
        progress_bar = st.progress(0, text="Uploading file...")
        status_text = st.empty()

        tmp_file_path = "temp_upload.mp3"
        with open(tmp_file_path, "wb") as f:
            f.write(uploaded_file.read())
        progress_bar.progress(30, text="File uploaded")

        try:
            with open(tmp_file_path, "rb") as f:
                files = {"file": (os.path.basename(tmp_file_path), f, "audio/mpeg")}
                data = {"genre": genre}
                status_text.text("Sending request to backend...")
                r = requests.post(API_URL, files=files, data=data)
            progress_bar.progress(70, text="Processing...")

            if r.status_code == 200:
                result = r.json()
                popularity = result.get("popularity_rounded", 0)
                progress_bar.progress(100, text="Done!")

                # --- Display metric card ---
                st.metric(label="🎵 Predicted Popularity", value=f"{popularity}/100")

                # --- Interactive Plotly gauge chart ---
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=popularity,
                    title={'text': "Popularity Score"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "#4CAF50"},
                           'steps': [
                               {'range': [0, 50], 'color': "#FF6347"},
                               {'range': [50, 75], 'color': "#FFD700"},
                               {'range': [75, 100], 'color': "#4CAF50"}]}
                ))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.error(f"Prediction failed: {r.status_code} - {r.text}")

        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
