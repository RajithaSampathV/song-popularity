"use client";
import React, { useState, useRef } from 'react';
import { Upload, Music, Sparkles } from 'lucide-react';

interface Props {
  onResult: (data: any) => void;
}

const ModernAudioUploader: React.FC<Props> = ({ onResult }) => {
  const [file, setFile] = useState<File | null>(null);
  const [genre, setGenre] = useState<string>('pop');
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const genres = [
    { value: 'pop', emoji: '🎤', label: 'Pop' },
    { value: 'rock', emoji: '🎸', label: 'Rock' },
    { value: 'hip-hop', emoji: '🎧', label: 'Hip-Hop' },
    { value: 'electronic', emoji: '🎹', label: 'Electronic' },
    { value: 'j-pop', emoji: '🎌', label: 'J-Pop' },
    { value: 'classical', emoji: '🎻', label: 'Classical' },
    { value: 'acoustic', emoji: '🪕', label: 'Acoustic' }
  ];

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === 'audio/mpeg') {
      setFile(droppedFile);
    }
  };

  const handleSubmit = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('track_genre', genre);

    try {
      setLoading(true);
      const res = await fetch(
        'https://song-predictor-800986629929.asia-south1.run.app/predict_file',
        {
          method: 'POST',
          body: formData
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
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-12 transition-all cursor-pointer
          ${isDragging ? 'border-purple-500 bg-purple-500/10 scale-105' : 'border-gray-600 hover:border-purple-400'}
          ${file ? 'bg-linear-to-br from-purple-500/20 to-blue-500/20' : 'bg-gray-800/50'}`}
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
                  ? 'border-purple-500 bg-purple-500/20 shadow-lg shadow-purple-500/50'
                  : 'border-gray-600 bg-gray-800/50 hover:border-purple-400'
                }`}
            >
              <div className="text-3xl mb-1">{g.emoji}</div>
              <div className="text-sm font-medium text-white">{g.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Audio Player */}
      {file && (
        <div className="bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm">
          <audio controls src={URL.createObjectURL(file)} className="w-full" />
        </div>
      )}

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