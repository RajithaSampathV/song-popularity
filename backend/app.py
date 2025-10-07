# backend/app.py

import os
import tempfile
from typing import Optional

import pandas as pd
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from extract_features import extract_heuristic_features_from_audio
from normalize_output import normalize_song_features
# ------------------------- FastAPI app -------------------------
app = FastAPI(title="Song Popularity Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------- ML Artifacts -------------------------
MODEL = None
SCALER = None
GENRE_ENCODER = None

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "random_forest.joblib")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "models", "scaler.joblib")
GENRE_ENCODER_PATH = os.path.join(os.path.dirname(__file__), "models", "track_genre_encoder.joblib")

FEATURE_ORDER = [
    "duration_ms", "explicit", "danceability", "key", "loudness", "mode",
    "speechiness", "acousticness", "instrumentalness", "liveness", "valence",
    "tempo", "time_signature", "track_genre"
]

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

# ------------------------- Schemas -------------------------
class PredictResponse(BaseModel):
    popularity: float
    popularity_rounded: int

# ------------------------- Helper Functions -------------------------
def lazy_load_models():
    """Load ML artifacts only on first request."""
    global MODEL, SCALER, GENRE_ENCODER
    if MODEL is None:
        import joblib
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Model not found: {MODEL_PATH}")
        if not os.path.exists(SCALER_PATH):
            raise RuntimeError(f"Scaler not found: {SCALER_PATH}")
        if not os.path.exists(GENRE_ENCODER_PATH):
            raise RuntimeError(f"Genre encoder not found: {GENRE_ENCODER_PATH}")

        MODEL = joblib.load(MODEL_PATH)
        SCALER = joblib.load(SCALER_PATH)
        GENRE_ENCODER = joblib.load(GENRE_ENCODER_PATH)

def convert_to_wav(input_path: str, output_path: str) -> None:
    """Convert any audio file to WAV using librosa."""
    import librosa
    import soundfile as sf
    y, sr = librosa.load(input_path, sr=22050)
    sf.write(output_path, y, sr, subtype='PCM_16')


# ------------------------- Endpoints -------------------------
@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/predict_file", response_model=PredictResponse)
async def predict_file(file: UploadFile, track_genre: str = Form(...)):
    lazy_load_models()

    # Validate genre
    if track_genre not in GENRES:
        raise HTTPException(status_code=400, detail=f"Unknown genre: {track_genre}")

    # Validate file extension
    allowed_extensions = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg', '.wma'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_input:
        tmp_input.write(await file.read())
        input_path = tmp_input.name

    # Convert to WAV if needed
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        wav_path = tmp_wav.name

    try:
        audio_path = wav_path if ext != ".wav" else input_path
        if ext != ".wav":
            convert_to_wav(input_path, wav_path)

        with open(audio_path, "rb") as f:
            feats = extract_heuristic_features_from_audio(f.read(), track_genre=track_genre)

        norm_feats = normalize_song_features(feats)
        X = pd.DataFrame([norm_feats], columns=FEATURE_ORDER)

        pred = MODEL.predict(X)
        popularity = float(pred[0])
        popularity = max(0.0, min(100.0, popularity))

        return PredictResponse(
            popularity=popularity,
            popularity_rounded=int(round(popularity))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
    finally:
        # Cleanup temporary files
        try: os.remove(input_path)
        except: pass
        try: os.remove(wav_path)
        except: pass

# ------------------------- Run server (Cloud Run) -------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
