import joblib
import numpy as np
import pandas as pd

# --- artifacts you saved during training ---
SCALER_PATH = "models/scaler.joblib"
GENRE_ENCODER_PATH = "models/track_genre_encoder.joblib"

# must match training
SCALE_COLS = [
    "duration_ms", "danceability", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
]

def normalize_song_features(raw_features: dict) -> dict:
    # Load artifacts
    scaler = joblib.load(SCALER_PATH)
    le = joblib.load(GENRE_ENCODER_PATH)

    # Build a single-row DataFrame
    df = pd.DataFrame([raw_features]).copy()

    # --- Label encode track_genre using the exact same encoder as training ---
    # If an unseen genre appears, map to a safe default (first known class or 'other' if it exists).
    try:
        df["track_genre"] = le.transform(df["track_genre"])
    except ValueError:
        # unseen label; fall back
        classes = list(le.classes_)
        fallback = "other" if "other" in classes else classes[0]
        mapping = {c: i for i, c in enumerate(classes)}
        df["track_genre"] = df["track_genre"].map(lambda g: mapping.get(g, mapping[fallback])).astype(int)

    # Ensure correct dtypes for numeric fields (esp. if they came as strings)
    for c in SCALE_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # --- Normalize only the columns you scaled during training ---
    df[SCALE_COLS] = scaler.transform(df[SCALE_COLS])

    # Return as a plain dict
    return df.iloc[0].to_dict()

