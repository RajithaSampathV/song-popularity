"use client";
import React, { useState } from "react";
import axios from "axios";

interface Props {
  onResult: (data: any) => void;
}

const AudioUploader: React.FC<Props> = ({ onResult }) => {
  const [file, setFile] = useState<File | null>(null);
  const [genre, setGenre] = useState<string>("pop");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) return alert("Please upload a file");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("track_genre", genre);

    try {
      setLoading(true);
      const res = await axios.post(
        "https://song-predictor-800986629929.asia-south1.run.app/predict_file",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      onResult(res.data);
    } catch (err: any) {
      alert(err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <input
        type="file"
        accept="audio/mp3"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="border p-2 rounded"
      />

      <select
        value={genre}
        onChange={(e) => setGenre(e.target.value)}
        className="border p-2 rounded"
      >
        {["pop", "rock", "hip-hop", "electronic", "j-pop", "classical", "acoustic"].map(
          (g) => (
            <option key={g} value={g}>
              {g}
            </option>
          )
        )}
      </select>

      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white p-2 rounded disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "Predicting..." : "Predict Popularity"}
      </button>

      {file && <audio controls src={URL.createObjectURL(file)} className="mt-2" />}
    </div>
  );
};

export default AudioUploader;
