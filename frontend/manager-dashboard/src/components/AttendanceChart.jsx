import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { day: "Mon", present: 95 },
  { day: "Tue", present: 98 },
  { day: "Wed", present: 92 },
  { day: "Thu", present: 100 },
  { day: "Fri", present: 102 },
];

export default function AttendanceChart() {
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="present" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
