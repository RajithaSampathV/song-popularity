# frontend/streamlit_app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Song Popularity Predictor", layout="centered")

st.title("🎵 Song Popularity Predictor — Random Forest")
st.markdown("Enter song features below and get a predicted popularity score (0-100).")

# --- Fetch genres from backend (if backend not ready, fallback to a local list) ---
@st.cache_data(ttl=600)
def fetch_genres():
    try:
        r = requests.get(f"{API_URL}/genres", timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    # fallback hardcoded list (must match backend order)
    return [
      "acoustic", "afrobeat", "alt-rock", "alternative", "ambient",
      "anime", "black-metal", "bluegrass", "blues", "brazil",
      "breakbeat", "british", "cantopop", "chicago-house", "children",
      "chill", "classical", "club", "comedy", "country", "dance",
      "dancehall", "death-metal", "deep-house", "detroit-techno",
      "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm",
      "electro", "electronic", "emo", "folk", "forro", "french", "funk",
      "garage", "german", "gospel", "goth", "grindcore", "groove",
      "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle",
      "heavy-metal", "hip-hop", "honky-tonk", "house", "idm", "indian",
      "indie-pop", "indie", "industrial", "iranian", "j-dance", "j-idol",
      "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino",
      "malay", "mandopop", "metal", "metalcore", "minimal-techno", "mpb",
      "new-age", "opera", "pagode", "party", "piano", "pop-film", "pop",
      "power-pop", "progressive-house", "psych-rock", "punk-rock",
      "punk", "r-n-b", "reggae", "reggaeton", "rock-n-roll", "rock",
      "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo",
      "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter",
      "soul", "spanish", "study", "swedish", "synth-pop", "tango",
      "techno", "trance", "trip-hop", "turkish", "world-music"
    ]

genres = fetch_genres()

# Friendly key names mapping (0-11)
KEY_MAP = {
    0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F",
    6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"
}

with st.form("input_form"):
    st.subheader("Basic info")
    duration_ms = st.number_input("Duration (ms)", min_value=1000, max_value=1000_000, value=210000, step=1000)
    explicit = st.selectbox("Explicit?", options=[0, 1], index=0, format_func=lambda x: "Yes" if x==1 else "No")
    danceability = st.slider("Danceability (0.0 - 1.0)", 0.0, 1.0, 0.7, 0.01)
    key_display = st.selectbox("Musical key", options=list(KEY_MAP.keys()), format_func=lambda k: f"{k} — {KEY_MAP[k]}", index=0)
    loudness = st.number_input("Loudness (dB, usually negative)", value=-6.5, step=0.1, format="%.2f")
    mode = st.selectbox("Mode", options=[1, 0], index=0, format_func=lambda m: "Major (1)" if m==1 else "Minor (0)")

    st.subheader("Audio features")
    speechiness = st.slider("Speechiness (0.0 - 1.0)", 0.0, 1.0, 0.05, 0.01)
    acousticness = st.slider("Acousticness (0.0 - 1.0)", 0.0, 1.0, 0.01, 0.01)
    instrumentalness = st.slider("Instrumentalness (0.0 - 1.0)", 0.0, 1.0, 0.0, 0.01)
    liveness = st.slider("Liveness (0.0 - 1.0)", 0.0, 1.0, 0.12, 0.01)
    valence = st.slider("Valence (0.0 - 1.0)", 0.0, 1.0, 0.6, 0.01)
    tempo = st.number_input("Tempo (BPM)", min_value=20.0, max_value=300.0, value=120.0, step=0.5, format="%.1f")
    time_signature = st.selectbox("Time signature", options=[3,4,5,6], index=1)

    st.subheader("Metadata")
    track_genre = st.selectbox("Track genre", options=genres, index=genres.index("pop") if "pop" in genres else 0)

    submitted = st.form_submit_button("Predict popularity")

if submitted:
    payload = {
        "duration_ms": int(duration_ms),
        "explicit": int(explicit),
        "danceability": float(danceability),
        "key": int(key_display),
        "loudness": float(loudness),
        "mode": int(mode),
        "speechiness": float(speechiness),
        "acousticness": float(acousticness),
        "instrumentalness": float(instrumentalness),
        "liveness": float(liveness),
        "valence": float(valence),
        "tempo": float(tempo),
        "time_signature": int(time_signature),
        "track_genre": track_genre
    }

    try:
        with st.spinner("Calling prediction API..."):
            r = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        if r.status_code != 200:
            st.error(f"Prediction failed: {r.status_code} — {r.text}")
        else:
            data = r.json()
            popularity = data.get("popularity")
            popularity_rounded = data.get("popularity_rounded")
            st.metric(label="Predicted Popularity", value=f"{popularity_rounded}/100", delta=None)
            st.write(f"Exact prediction (float): {popularity:.3f}")
            # Optional: visualize as progress bar
            st.progress(int(popularity_rounded))
    except Exception as e:
        st.error(f"Error calling API: {e}")
