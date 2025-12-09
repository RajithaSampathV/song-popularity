"use client";
import React, { useState, useEffect } from 'react';

interface Props {
  value: number;
}

const ModernGaugeChart: React.FC<Props> = ({ value }) => {
  const [animatedValue, setAnimatedValue] = useState(0);

  useEffect(() => {
    let start = 0;
    const duration = 2000;
    const increment = value / (duration / 16);
    
    const timer = setInterval(() => {
      start += increment;
      if (start >= value) {
        setAnimatedValue(value);
        clearInterval(timer);
      } else {
        setAnimatedValue(Math.floor(start));
      }
    }, 16);

    return () => clearInterval(timer);
  }, [value]);

  const circumference = 2 * Math.PI * 120;
  const offset = circumference - (animatedValue / 100) * circumference;
  
  const getColor = (val: number) => {
    if (val >= 75) return '#10b981';
    if (val >= 50) return '#f59e0b';
    return '#ef4444';
  };

  const getRating = (val: number) => {
    if (val >= 90) return { text: 'Viral Hit! 🔥', color: 'text-green-400' };
    if (val >= 75) return { text: 'Chart Topper! ⭐', color: 'text-green-400' };
    if (val >= 60) return { text: 'Rising Star 🌟', color: 'text-yellow-400' };
    if (val >= 40) return { text: 'Growing Potential 📈', color: 'text-orange-400' };
    return { text: 'Needs Work 💪', color: 'text-red-400' };
  };

  const rating = getRating(animatedValue);

  return (
    <div className="flex flex-col items-center gap-6">
      <div className="relative">
        <svg width="300" height="300" className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx="150"
            cy="150"
            r="120"
            stroke="#374151"
            strokeWidth="20"
            fill="none"
          />
          
          {/* Animated progress circle */}
          <circle
            cx="150"
            cy="150"
            r="120"
            stroke={getColor(animatedValue)}
            strokeWidth="20"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-300"
            style={{
              filter: `drop-shadow(0 0 10px ${getColor(animatedValue)})`
            }}
          />
        </svg>
        
        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-6xl font-bold text-white mb-2">{animatedValue}</div>
          <div className="text-gray-400 text-sm">/ 100</div>
        </div>
      </div>

      <div className={`text-2xl font-bold ${rating.color}`}>
        {rating.text}
      </div>
    </div>
  );
};

export default ModernGaugeChart;