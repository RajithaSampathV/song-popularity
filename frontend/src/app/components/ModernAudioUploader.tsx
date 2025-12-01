"use client";
import React, { useState, useRef, useEffect } from "react";
import { Upload, Music, Sparkles, Play, Pause, Volume2 } from "lucide-react";

// Custom Audio Player Component
const CustomAudioPlayer: React.FC<{ file: File }> = ({ file }) => {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [audioUrl, setAudioUrl] = useState<string>("");

  // Create object URL for audio file
  useEffect(() => {
    if (!file) return;

    const url = URL.createObjectURL(file);
    setAudioUrl(url);

    return () => {
      URL.revokeObjectURL(url);
      setAudioUrl("");
      setIsPlaying(false);
      setCurrentTime(0);
      setDuration(0);
    };
  }, [file]);

  // Setup event listeners
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => setCurrentTime(audio.currentTime);
    const updateDuration = () => setDuration(audio.duration);
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener("timeupdate", updateTime);
    audio.addEventListener("loadedmetadata", updateDuration);
    audio.addEventListener("ended", handleEnded);

    return () => {
      audio.removeEventListener("timeupdate", updateTime);
      audio.removeEventListener("loadedmetadata", updateDuration);
      audio.removeEventListener("ended", handleEnded);
    };
  }, [audioUrl]);

  const togglePlay = async () => {
    const audio = audioRef.current;
    if (!audio) return;

    try {
      if (isPlaying) {
        audio.pause();
        setIsPlaying(false);
      } else {
        await audio.play();
        setIsPlaying(true);
      }
    } catch (error) {
      console.error("Error playing audio:", error);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = parseFloat(e.target.value);
    setCurrentTime(newTime);
    if (audioRef.current) audioRef.current.currentTime = newTime;
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    if (audioRef.current) audioRef.current.volume = newVolume;
  };

  const formatTime = (time: number) => {
    if (isNaN(time)) return "0:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, "0")}`;
  };

  return (
    <div className="bg-linear-to-br from-purple-900/40 to-blue-900/40 rounded-xl p-6 backdrop-blur-sm border border-purple-500/30">
      {audioUrl && <audio ref={audioRef} src={audioUrl} />}

      <div className="flex items-center gap-4">
        {/* Play/Pause Button */}
        <button
          onClick={togglePlay}
          className="w-12 h-12 rounded-full bg-linear-to-r from-purple-600 to-blue-600 flex items-center justify-center hover:scale-110 transition-transform shadow-lg shadow-purple-500/50"
        >
          {isPlaying ? (
            <Pause className="w-5 h-5 text-white" fill="white" />
          ) : (
            <Play className="w-5 h-5 text-white ml-1" fill="white" />
          )}
        </button>

        {/* Progress Bar */}
        <div className="flex-1">
          <input
            type="range"
            min={0}
            max={duration || 0}
            value={currentTime}
            onChange={handleSeek}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
            style={{
              background: `linear-gradient(to right, #a855f7 0%, #3b82f6 ${
                duration ? (currentTime / duration) * 100 : 0
              }%, #374151 ${duration ? (currentTime / duration) * 100 : 0}%, #374151 100%)`,
            }}
          />
          <div className="flex justify-between text-xs text-gray-400 mt-1">
            <span>{formatTime(currentTime)}</span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>

        {/* Volume Control */}
        <div className="flex items-center gap-2">
          <Volume2 className="w-5 h-5 text-gray-400" />
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={volume}
            onChange={handleVolumeChange}
            className="w-20 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
            style={{
              background: `linear-gradient(to right, #a855f7 0%, #3b82f6 ${
                volume * 100
              }%, #374151 ${volume * 100}%, #374151 100%)`,
            }}
          />
        </div>
      </div>

      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 16px;
          height: 16px;
          background: white;
          border-radius: 50%;
          cursor: pointer;
          box-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
        }
        .slider::-moz-range-thumb {
          width: 16px;
          height: 16px;
          background: white;
          border-radius: 50%;
          cursor: pointer;
          border: none;
          box-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
        }
      `}</style>
    </div>
  );
};

// Modern Audio Uploader
interface Props {
  onResult: (data: any) => void;
}

const ModernAudioUploader: React.FC<Props> = ({ onResult }) => {
  const [file, setFile] = useState<File | null>(null);
  const [genre, setGenre] = useState<string>("pop");
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const genres = [
    { value: "pop", emoji: "🎤", label: "Pop" },
    { value: "rock", emoji: "🎸", label: "Rock" },
    { value: "hip-hop", emoji: "🎧", label: "Hip-Hop" },
    { value: "electronic", emoji: "🎹", label: "Electronic" },
    { value: "j-pop", emoji: "🎌", label: "J-Pop" },
    { value: "classical", emoji: "🎻", label: "Classical" },
    { value: "acoustic", emoji: "🪕", label: "Acoustic" },
  ];

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "audio/mpeg") {
      setFile(droppedFile);
    }
  };

  const handleSubmit = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("track_genre", genre);

    try {
      setLoading(true);
      const res = await fetch(
        "https://song-predictor-800986629929.asia-south1.run.app/predict_file",
        {
          method: "POST",
          body: formData,
        }
      );
      const data = await res.json();
      onResult(data);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Drag & Drop Zone */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-12 transition-all cursor-pointer
          ${isDragging ? "border-purple-500 bg-purple-500/10 scale-105" : "border-gray-600 hover:border-purple-400"}
          ${file ? "bg-linear-to-br from-purple-500/20 to-blue-500/20" : "bg-gray-800/50"}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="audio/mpeg"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="hidden"
        />

        <div className="flex flex-col items-center gap-4">
          {file ? (
            <>
              <Music className="w-16 h-16 text-purple-400 animate-pulse" />
              <div className="text-center">
                <p className="text-xl font-semibold text-white">{file.name}</p>
                <p className="text-sm text-gray-400 mt-1">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </>
          ) : (
            <>
              <Upload className="w-16 h-16 text-gray-400" />
              <div className="text-center">
                <p className="text-xl font-semibold text-white">Drop your MP3 here</p>
                <p className="text-sm text-gray-400 mt-1">or click to browse</p>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Genre Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-3">
          Select Genre
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {genres.map((g) => (
            <button
              key={g.value}
              onClick={() => setGenre(g.value)}
              className={`p-4 rounded-xl border-2 transition-all transform hover:scale-105
                ${genre === g.value
                  ? "border-purple-500 bg-purple-500/20 shadow-lg shadow-purple-500/50"
                  : "border-gray-600 bg-gray-800/50 hover:border-purple-400"
                }`}
            >
              <div className="text-3xl mb-1">{g.emoji}</div>
              <div className="text-sm font-medium text-white">{g.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Custom Audio Player */}
      {file && <CustomAudioPlayer file={file} />}

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={!file || loading}
        className="w-full bg-linear-to-r from-purple-600 to-blue-600 text-white py-4 rounded-xl
          font-semibold text-lg transition-all transform hover:scale-105 hover:shadow-2xl
          hover:shadow-purple-500/50 disabled:opacity-50 disabled:cursor-not-allowed
          disabled:transform-none flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            Analyzing...
          </>
        ) : (
          <>
            <Sparkles className="w-5 h-5" />
            Predict Popularity
          </>
        )}
      </button>
    </div>
  );
};

export default ModernAudioUploader;
