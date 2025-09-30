# backend/app.py
import os
import tempfile
from typing import List, Optional

import joblib
import numpy as np
import pandas as pd
import librosa

from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from extract_features import extract_heuristic_features_from_audio
from normalize_output import normalize_song_features

# --- Genre list
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


# ------------------------- Config / Artifacts -------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "random_forest.joblib")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "models", "scaler.joblib")
GENRE_ENCODER_PATH = os.path.join(os.path.dirname(__file__), "models", "track_genre_encoder.joblib")


# the full raw feature order you trained on (after label-encoding track_genre)
FEATURE_ORDER = [
    "duration_ms", "explicit", "danceability", "key", "loudness", "mode",
    "speechiness", "acousticness", "instrumentalness", "liveness", "valence",
    "tempo", "time_signature", "track_genre"
]

# ------------------------- Load artifacts once ------------------------
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model not found: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

# scaler & label encoder are required to match training preprocessing
if not os.path.exists(SCALER_PATH):
    raise RuntimeError(f"Scaler not found: {SCALER_PATH}")
scaler = joblib.load(SCALER_PATH)

if not os.path.exists(GENRE_ENCODER_PATH):
    raise RuntimeError(f"Track-genre encoder not found: {GENRE_ENCODER_PATH}")
genre_encoder = joblib.load(GENRE_ENCODER_PATH)
_known_genres = set(genre_encoder.classes_)
# choose a safe fallback for unseen genres
_fallback_genre = "other" if "other" in _known_genres else list(genre_encoder.classes_)[0]
_genre_to_id = {cls: i for i, cls in enumerate(genre_encoder.classes_)}


# ------------------------- FastAPI app & schema -----------------------
class PredictResponse(BaseModel):
    popularity: float
    popularity_rounded: int

app = FastAPI(title="Song Popularity Predictor (File Upload)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def convert_to_wav(input_path: str, output_path: str) -> None:
    """
    Convert any audio file to WAV format using librosa.
    
    Args:
        input_path: Path to the input audio file
        output_path: Path where the WAV file will be saved
    """
    try:
        # Load audio with librosa (automatically resamples to 22050 Hz by default)
        y, sr = librosa.load(input_path, sr=22050)  # Standard sample rate
        
        # Save as WAV file
        import soundfile as sf
        sf.write(output_path, y, sr, subtype='PCM_16')
        
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {str(e)}")

# ------------------------- Endpoint ----------------------------------
@app.post("/predict_file", response_model=PredictResponse)
async def predict_file(
    file: UploadFile,
    track_genre: str = Form(...),
):
    # Validate genre
    if track_genre not in GENRES:
        raise HTTPException(status_code=400, detail=f"Unknown genre: {track_genre}")
    
    # Validate file type
    allowed_extensions = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg', '.wma'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
        )

    # Save uploaded file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as input_tmp_file:
        input_tmp_file.write(await file.read())
        input_tmp_path = input_tmp_file.name

    # Create temp file for WAV conversion
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as wav_tmp_file:
        wav_tmp_path = wav_tmp_file.name

    try:
        # Convert to WAV if not already WAV
        if file_extension != '.wav':
            convert_to_wav(input_tmp_path, wav_tmp_path)
            audio_file_path = wav_tmp_path
        else:
            audio_file_path = input_tmp_path

        # Read the WAV file and extract features
        with open(audio_file_path, "rb") as f:
            feats = extract_heuristic_features_from_audio(
                f.read(),
                track_genre=str(track_genre),
            )

        # Normalize + encode using your saved artifacts
        norm = normalize_song_features(feats)

        # Build model input as a 2D array/DataFrame in training order
        X = pd.DataFrame([norm], columns=FEATURE_ORDER)

        # Predict
        pred = model.predict(X)
        popularity = float(pred[0])
        popularity = max(0.0, min(100.0, popularity))  # clip to [0,100]

        return PredictResponse(
            popularity=popularity,
            popularity_rounded=int(round(popularity))
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
    finally:
        # Clean up temporary files
        try:
            os.remove(input_tmp_path)
        except Exception:
            pass
        try:
            if os.path.exists(wav_tmp_path):
                os.remove(wav_tmp_path)
        except Exception:
            pass