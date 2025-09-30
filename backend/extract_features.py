# pip install librosa soundfile numpy pandas
from __future__ import annotations
import math, io
import numpy as np
import librosa
import pandas as pd

def norm(x, lo, hi):
    x = float(np.clip(x, lo, hi))
    return (x - lo) / (hi - lo + 1e-9)

def estimate_mode_from_chroma(chroma: np.ndarray) -> int:
    """
    Crude major/minor mode via template matching on averaged chroma.
    Returns 1 for major, 0 for minor.
    """
    prof = chroma.mean(axis=1)  # 12-vector
    prof = prof / (prof.sum() + 1e-9)

    # Major/minor triad templates (C-based), then rotate for best match
    major = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], dtype=float)
    minor = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], dtype=float)

    def best_corr(template):
        # circularly rotate to best fit any key
        cors = [np.corrcoef(prof, np.roll(template, k))[0,1] for k in range(12)]
        return np.nanmax(cors)

    return int(best_corr(major) >= best_corr(minor))

def estimate_key_from_chroma(chroma: np.ndarray) -> int:
    """Return pitch class (0=C ... 11=B) with max mean chroma energy."""
    prof = chroma.mean(axis=1)
    return int(np.argmax(prof))

def extract_heuristic_features_from_audio(
    file_bytes: bytes,
    explicit: int = 0,
    track_genre: str = "unknown",
    sr: int = 22050,
):
    # Load mono
    y, sr = librosa.load(io.BytesIO(file_bytes), sr=sr, mono=True)
    duration_sec = librosa.get_duration(y=y, sr=sr)
    duration_ms = int(round(duration_sec * 1000))

    # Tempo & beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(tempo)
    if len(beat_frames) > 1:
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        sigma_b = float(np.std(np.diff(beat_times)))
        beat_reg = math.exp(-sigma_b / 0.20)  # S in formula
    else:
        sigma_b, beat_reg = 0.0, 0.0

    # Onset env (for beat strength / liveness)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_mean = float(np.mean(onset_env))

    # Loudness (RMS dB)
    rms_frame = librosa.feature.rms(y=y).squeeze()
    rms_mean = float(np.mean(rms_frame))
    rms_var  = float(np.var(rms_frame))
    loud_db = 20 * math.log10(rms_mean + 1e-9)

    # Spectral features
    centroid = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())
    rolloff  = float(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85).mean())
    flatness = float(librosa.feature.spectral_flatness(y=y).mean())
    nyquist = sr / 2.0
    C_bar = centroid / (nyquist + 1e-9)
    R_bar = rolloff  / (nyquist + 1e-9)

    # HPSS: harmonic ratio
    y_h, y_p = librosa.effects.hpss(y)
    harm_ratio = float(np.mean(np.abs(y_h)) / (np.mean(np.abs(y)) + 1e-9))

    # ZCR & MFCC variance (speechiness)
    zcr = float(librosa.feature.zero_crossing_rate(y).mean())
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_var = float(np.var(mfcc))

    # Chroma for key/mode
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    key_idx = estimate_key_from_chroma(chroma)
    mode = estimate_mode_from_chroma(chroma)  # 1 major, 0 minor

    # ----- Map to 0..1 via formulas above -----

    # Danceability
    T = math.exp(-((tempo - 120.0)**2) / (2*(20.0**2)))
    Lp = norm(loud_db, -40.0, -5.0)
    danceability = float(np.clip(0.5*T + 0.4*beat_reg + 0.1*Lp, 0.0, 1.0))

    # Valence
    brightness = float(np.clip(C_bar, 0.0, 1.0))
    openness   = float(np.clip(R_bar, 0.0, 1.0))
    valence = float(np.clip(0.4*brightness + 0.3*openness + 0.3*(1.0 if mode==1 else 0.0), 0.0, 1.0))

    # Acousticness
    SFp = norm(flatness, 0.02, 0.6)
    acousticness = float(np.clip(0.6*harm_ratio + 0.4*(1.0 - SFp), 0.0, 1.0))

    # Speechiness
    Zp = norm(zcr, 0.02, 0.20)
    Mp = norm(mfcc_var, 50.0, 2000.0)
    speechiness = float(np.clip(0.6*Zp + 0.4*(1.0 - Mp), 0.0, 1.0))

    # Instrumentalness (inverse of speechiness)
    instrumentalness = float(np.clip(1.0 - speechiness, 0.0, 1.0))

    # Liveness
    Op = norm(onset_mean, 0.0, 5.0)
    RMSv = norm(rms_var, 0.0, 0.01)
    liveness = float(np.clip(0.5*Op + 0.5*RMSv, 0.0, 1.0))

    # Time signature (heuristic default)
    time_signature = 4

    return {
        "duration_ms": duration_ms,
        "explicit": int(explicit),
        "danceability": danceability,
        "key": int(key_idx),                # 0=C ... 11=B
        "loudness": loud_db,                # dBFS (negative)
        "mode": int(mode),                  # 1=major, 0=minor
        "speechiness": speechiness,
        "acousticness": acousticness,
        "instrumentalness": instrumentalness,
        "liveness": liveness,
        "valence": valence,
        "tempo": float(tempo),
        "time_signature": time_signature,
        "track_genre": str(track_genre),
    }
