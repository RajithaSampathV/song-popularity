"use client";
import { useState } from "react";
import AudioUploader from "./components/AudioUploader";
import GaugeChart from "./components/GaugeChart";

export default function Home() {
  const [result, setResult] = useState<any>(null);

  return (
    <main className="max-w-3xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-4">🎵 Music Popularity Predictor</h1>
      <p className="mb-6">
        Upload your MP3 song and select the genre. Our AI predicts the popularity score and provides insight.
      </p>

      <AudioUploader onResult={setResult} />

      {result && (
        <div className="mt-8 border p-4 rounded shadow-md">
          <h2 className="text-2xl font-semibold mb-2">
            🎵 Predicted Popularity: {result.popularity_rounded}/100
          </h2>
          <p className="mb-4">💡 AI Insight: {result.insight}</p>
          <GaugeChart value={result.popularity_rounded} />
        </div>
      )}
    </main>
  );
}
