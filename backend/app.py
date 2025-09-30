# backend/app.py
import os
import tempfile
from typing import List
from fastapi import FastAPI, UploadFile, Form, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import librosa
from fastapi.middleware.cors import CORSMiddleware

# --- Genre list (must match training LabelEncoder order) ---
GENRES = [
    "acoustic","afrobeat","alt-rock","alternative","ambient","anime","black-metal",
    "bluegrass","blues","brazil","breakbeat","british","cantopop","chicago-house","children",
    "chill","classical","club","comedy","country","dance","dancehall","death-metal","deep-house",
    "detroit-techno","disco","disney","drum-and-bass","dub","dubstep","edm","electro","electronic",
    "emo","folk","forro","french","funk","garage","german","gospel","goth","grindcore","groove",
    "grunge","guitar","happy","hard-rock","hardcore","hardstyle","heavy-metal","hip-hop","honky-tonk",
    "house","idm","indian","indie-pop","indie","industrial","iranian","j-dance","j-idol","j-pop",
    "j-rock","jazz","k-pop","kids","latin","latino","malay","mandopop","metal","metalcore",
    "minimal-techno","mpb","new-age","opera","pagode","party","piano","pop-film","pop",
    "power-pop","progressive-house","psych-rock","punk-rock","punk","r-n-b","reggae","reggaeton",
    "rock-n-roll","rock","rockabilly","romance","sad","salsa","samba","sertanejo","show-tunes",
    "singer-songwriter","ska","sleep","songwriter","soul","spanish","study","swedish","synth-pop",
    "tango","techno","trance","trip-hop","turkish","world-music"
]

# --- Pydantic response model ---
class PredictResponse(BaseModel):
    popularity: float
    popularity_rounded: int

# --- FastAPI app ---
app = FastAPI(title="Song Popularity Predictor (File Upload)")

# allow Streamlit frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Random Forest model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "random_forest.joblib")
model = joblib.load(MODEL_PATH)
print("Random Forest model loaded!")

# --- Helper: extract features from audio ---
def extract_features_from_audio(y, sr, genre):
    features = {
        "duration_ms": int(len(y)/sr*1000),
        "danceability": float(np.mean(librosa.feature.rms(y=y))),
        "loudness": float(np.mean(librosa.amplitude_to_db(np.abs(y)))),
        "tempo": float(librosa.beat.tempo(y=y, sr=sr)[0]),
        "speechiness": 0.05,
        "acousticness": 0.1,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.5,
        "explicit": 0,
        "key": 0,
        "mode": 1,
        "time_signature": 4,
        "track_genre": genre
    }
    return features

# --- API endpoint: upload MP3 and predict ---
@app.post("/predict_file", response_model=PredictResponse)
async def predict_file(file: UploadFile, genre: str = Form(...)):
    if genre not in GENRES:
        raise HTTPException(status_code=400, detail=f"Unknown genre: {genre}")

    # Save MP3 to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name

    try:
        # Load first 2 minutes of audio
        y, sr = librosa.load(tmp_file_path, mono=True, duration=120)

        # Extract features
        features = extract_features_from_audio(y, sr, genre)

        # Build feature vector in model order
        genre_label = GENRES.index(genre)
        feature_vector = [
            features["duration_ms"], features["explicit"], features["danceability"],
            features["key"], features["loudness"], features["mode"], features["speechiness"],
            features["acousticness"], features["instrumentalness"], features["liveness"],
            features["valence"], features["tempo"], features["time_signature"], genre_label
        ]
        X = np.array(feature_vector).reshape(1, -1)

        # Predict
        pred = model.predict(X)
        popularity = float(pred[0])
        popularity_clipped = max(0.0, min(100.0, popularity))

        return PredictResponse(popularity=popularity_clipped, popularity_rounded=int(round(popularity_clipped)))

    finally:
        os.remove(tmp_file_path)
