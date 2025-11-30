"use client";
import dynamic from "next/dynamic";
import React from "react";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

interface Props {
  value: number;
}

const GaugeChart: React.FC<Props> = ({ value }) => (
  <Plot
    data={[
      {
        type: "indicator",
        mode: "gauge+number",
        value,
        title: { text: "Popularity Score" },
        gauge: {
          axis: { range: [0, 100] },
          bar: { color: "#4CAF50" },
          steps: [
            { range: [0, 50], color: "#FF6347" },
            { range: [50, 75], color: "#FFD700" },
            { range: [75, 100], color: "#4CAF50" },
          ],
        },
      },
    ]}
    layout={{ width: 400, height: 400 }}
  />
);

export default GaugeChart;
