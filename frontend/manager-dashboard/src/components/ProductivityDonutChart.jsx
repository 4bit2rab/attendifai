import React from "react";

const ProductivityDonutChart = ({ data }) => {
  /* -----------------------------
     Convert API response → %
  ------------------------------ */
  const total =
    (data?.total_productive_hours || 0) +
    (data?.total_idle_hours || 0) +
    (data?.total_overtime_hours || 0);

  const chartData = total
    ? [
        {
          label: "Productive",
          value: Math.round(
            (data.total_productive_hours / total) * 100
          ),
          color: "#22C55E",
        },
        {
          label: "Idle",
          value: Math.round(
            (data.total_idle_hours / total) * 100
          ),
          color: "#F97316",
        },
        {
          label: "Overtime",
          value: Math.round(
            (data.total_overtime_hours / total) * 100
          ),
          color: "#6366F1",
        },
      ]
    : [
        { label: "Productive", value: 0, color: "#22C55E" },
        { label: "Idle", value: 0, color: "#F97316" },
        { label: "Overtime", value: 0, color: "#6366F1" },
      ];

  /* -----------------------------
     SVG Geometry
  ------------------------------ */
  const radius = 110;
  const strokeWidth = 25;
  const center = 130;
  const circumference = 2 * Math.PI * radius;

  /* -----------------------------
     Build donut slices immutably
  ------------------------------ */
  const circles = chartData.reduce(
    (acc, item) => {
      const dash = (item.value / 100) * circumference;

      acc.circles.push({
        ...item,
        dash,
        dashOffset: acc.offset,
      });

      acc.offset -= dash;
      return acc;
    },
    { offset: 0, circles: [] }
  ).circles;

  return (
    <div className="flex flex-col items-center bg-white p-6 rounded-xl shadow">
      <h2 className="text-lg font-semibold text-gray-700">
        Weekly Productivity
      </h2>
      <p className="text-sm text-gray-400 mb-4">Last 7 days</p>

      {/* Donut */}
      <svg width="280" height="280">
        <g transform={`rotate(-90 ${center} ${center})`}>
          {circles.map((item, index) => (
            <circle
              key={index}
              cx={center}
              cy={center}
              r={radius}
              fill="transparent"
              stroke={item.color}
              strokeWidth={strokeWidth}
              strokeDasharray={`${item.dash} ${circumference}`}
              strokeDashoffset={item.dashOffset}
              strokeLinecap="round"
            />
          ))}
        </g>

        {/* Center text */}
        <text
          x={center}
          y={center - 5}
          textAnchor="middle"
          className="fill-gray-500 text-sm"
        >
          Productive
        </text>
        <text
          x={center}
          y={center + 22}
          textAnchor="middle"
          className="fill-green-600 text-2xl font-bold"
        >
          {chartData[0].value}%
        </text>
      </svg>

      {/* Legend */}
      <div className="flex gap-6 mt-4">
        {chartData.map((item) => (
          <div key={item.label} className="flex items-center gap-2">
            <span
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: item.color }}
            />
            <span className="text-sm text-gray-600">
              {item.label} ({item.value}%)
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductivityDonutChart;
