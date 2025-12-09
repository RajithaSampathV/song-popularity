"use client";
import { useState } from "react";
import ModernAudioUploader from "./components/ModernAudioUploader";
import ModernGaugeChart from "./components/ModernGaugeChart";
import { TrendingUp, Zap, Sparkles } from "lucide-react";

export default function Home() {
  const [result, setResult] = useState<any>(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" />
      </div>

      <div className="relative max-w-5xl mx-auto p-6 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-purple-500/20 px-4 py-2 rounded-full mb-4">
            <Zap className="w-4 h-4 text-yellow-400" />
            <span className="text-sm font-medium">AI-Powered Prediction</span>
          </div>
          
          <h1 className="text-5xl sm:text-6xl font-bold mb-4 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
            Music Popularity Predictor
          </h1>
          
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Upload your track and let our AI analyze its potential to become the next hit
          </p>
        </div>

        {/* Uploader Card */}
        <div className="bg-gray-800/30 backdrop-blur-xl rounded-3xl p-8 border border-gray-700/50 shadow-2xl mb-8">
          <ModernAudioUploader onResult={setResult} />
        </div>

        {/* Results Card */}
        {result && (
          <div className="bg-gray-800/30 backdrop-blur-xl rounded-3xl p-8 border border-gray-700/50 shadow-2xl animate-fadeIn">
            <div className="flex items-center gap-3 mb-6">
              <TrendingUp className="w-8 h-8 text-purple-400" />
              <h2 className="text-3xl font-bold">Prediction Results</h2>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {/* Gauge */}
              <div className="flex items-center justify-center">
                <ModernGaugeChart value={result.popularity_rounded} />
              </div>

              {/* Insights */}
              <div className="flex flex-col justify-center space-y-4">
                <div className="bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-2xl p-6 border border-purple-500/30">
                  <div className="flex items-start gap-3">
                    <Sparkles className="w-6 h-6 text-purple-400 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-lg mb-2">AI Insight</h3>
                      <p className="text-gray-300 leading-relaxed">{result.insight}</p>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-700/30 rounded-xl p-4 text-center">
                    <div className="text-3xl font-bold text-purple-400">
                      {result.popularity_rounded}
                    </div>
                    <div className="text-sm text-gray-400 mt-1">Score</div>
                  </div>
                  <div className="bg-gray-700/30 rounded-xl p-4 text-center">
                    <div className="text-3xl font-bold text-blue-400">
                      {result.popularity_rounded >= 75 ? 'High' : result.popularity_rounded >= 50 ? 'Medium' : 'Low'}
                    </div>
                    <div className="text-sm text-gray-400 mt-1">Potential</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.6s ease-out;
        }
      `}</style>
    </div>
  );
}