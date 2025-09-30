# frontend/streamlit_app.py
import streamlit as st
import requests
import os

st.title("🎵 Music Popularity Predictor (Upload MP3)")

uploaded_file = st.file_uploader("Upload your song (MP3)", type=["mp3"])
genre = st.selectbox(
    "Select genre (required)", 
    ["pop", "rock", "hip-hop", "electronic", "j-pop", "classical", "acoustic"]
)

API_URL = "http://127.0.0.1:8000/predict_file"

if uploaded_file is not None and st.button("Predict Popularity"):
    with open(os.path.join("temp_upload.mp3"), "wb") as f:
        f.write(uploaded_file.read())
        tmp_file_path = f.name

    try:
        with open(tmp_file_path, "rb") as f:
            files = {"file": (os.path.basename(tmp_file_path), f, "audio/mpeg")}
            data = {"genre": genre}
            r = requests.post(API_URL, files=files, data=data)

        if r.status_code == 200:
            result = r.json()
            popularity = result.get("popularity_rounded", 0)
            st.metric(label="Predicted Popularity", value=f"{popularity}/100")

            import matplotlib.pyplot as plt
            plt.figure(figsize=(4,3))
            plt.bar(["Popularity"], [popularity], color="green")
            plt.ylim(0,100)
            st.pyplot(plt)
        else:
            st.error(f"Prediction failed: {r.status_code} - {r.text}")

    finally:
        os.remove(tmp_file_path)
