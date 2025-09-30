# backend/app.py
import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# --- Genre list (exact ordering from your LabelEncoder) ---
GENRES = [
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

# --- Feature order required by the model (must match training) ---
FEATURE_ORDER = [
    "duration_ms",
    "explicit",
    "danceability",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "time_signature",
    "track_genre"
]

# Pydantic model for incoming prediction request
class PredictRequest(BaseModel):
    duration_ms: int = Field(..., example=210000)
    explicit: int = Field(..., ge=0, le=1, example=0)  # 0 or 1
    danceability: float = Field(..., ge=0.0, le=1.0, example=0.7)
    key: int = Field(..., ge=0, le=11, example=0)
    loudness: float = Field(..., example=-6.5)
    mode: int = Field(..., ge=0, le=1, example=1)
    speechiness: float = Field(..., ge=0.0, le=1.0, example=0.05)
    acousticness: float = Field(..., ge=0.0, le=1.0, example=0.01)
    instrumentalness: float = Field(..., ge=0.0, le=1.0, example=0.0)
    liveness: float = Field(..., ge=0.0, le=1.0, example=0.12)
    valence: float = Field(..., ge=0.0, le=1.0, example=0.6)
    tempo: float = Field(..., example=120.0)
    time_signature: int = Field(..., ge=1, le=7, example=4)
    track_genre: str = Field(..., example="pop")

class PredictResponse(BaseModel):
    popularity: float
    popularity_rounded: int

app = FastAPI(title="Song Popularity (Random Forest)")

# allow Streamlit (running on a dev port) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, set this to the correct origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model on startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "random_forest.joblib")
model = None

@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model file not found at: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    # optionally inspect model
    print("Random Forest model loaded from:", MODEL_PATH)

def genre_to_label(genre_name: str) -> int:
    """Convert genre string to label index based on training LabelEncoder order."""
    try:
        return GENRES.index(genre_name)
    except ValueError:
        # unknown genre -> raise an error
        raise HTTPException(status_code=400, detail=f"Unknown genre: '{genre_name}'. Available genres: {len(GENRES)}")

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Build feature vector in the exact order used for training
    try:
        genre_label = genre_to_label(payload.track_genre)
    except HTTPException:
        raise

    feature_vector = [
        payload.duration_ms,
        payload.explicit,
        payload.danceability,
        payload.key,
        payload.loudness,
        payload.mode,
        payload.speechiness,
        payload.acousticness,
        payload.instrumentalness,
        payload.liveness,
        payload.valence,
        payload.tempo,
        payload.time_signature,
        genre_label
    ]

    X = np.array(feature_vector, dtype=float).reshape(1, -1)

    # Predict
    try:
        pred = model.predict(X)  # scikit-learn regression -> returns array
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction error: {e}")

    popularity = float(pred[0])
    # clip and round for safe display
    popularity_clipped = max(0.0, min(100.0, popularity))
    popularity_rounded = int(round(popularity_clipped))

    return PredictResponse(popularity=popularity_clipped, popularity_rounded=popularity_rounded)

@app.get("/genres", response_model=List[str])
def get_genres():
    """Return the list of available genres (useful for frontend)"""
    return GENRES

@app.get("/health")
def health():
    return {"status": "ok"}
