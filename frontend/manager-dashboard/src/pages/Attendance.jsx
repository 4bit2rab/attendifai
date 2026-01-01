import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { getAttendance } from "../api/attendanceApi";
import { motion, AnimatePresence } from "framer-motion";

export default function Attendance() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [date, setDate] = useState(() => new Date().toISOString().slice(0, 10));

  useEffect(() => {
    fetchAttendance();
  }, [date]);

  const fetchAttendance = async () => {
    setLoading(true);
    try {
      const data = await getAttendance(date);
      setRecords(data);
    } catch (error) {
      console.error("Failed to load attendance:", error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const totalMinutes = Math.floor(seconds / 60);
    const hrs = Math.floor(totalMinutes / 60);
    const mins = totalMinutes % 60;
    return `${hrs}h ${mins}m`;
  };

  const chartData = records.map((r) => ({
    ...r,
    productive_time: Math.floor(r.productive_time / 60),
    idle_time: Math.floor(r.idle_time / 60),
    over_time: Math.floor(r.over_time / 60),
  }));

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4 text-blue-600">Daily Attendance</h2>

      {/* Date Picker */}
      <div className="mb-6 flex items-center gap-2">
        <label className="font-medium">Select Date:</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="border p-2 rounded hover:border-blue-400 transition"
        />
      </div>

      {/* Table */}
      {loading ? (
        <p>Loading attendance...</p>
      ) : (
        <table className="w-full bg-white shadow rounded mb-8">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3 text-left">Employee</th>
              <th className="p-3 text-left">Date</th>
              <th className="p-3 text-left">Productive</th>
              <th className="p-3 text-left">Idle</th>
              <th className="p-3 text-left">Overtime</th>
            </tr>
          </thead>
          <tbody>
            <AnimatePresence>
              {records.length === 0 ? (
                <motion.tr
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <td colSpan="5" className="p-3 text-center">
                    No records found
                  </td>
                </motion.tr>
              ) : (
                records.map((row, index) => (
                  <motion.tr
                    key={index}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    whileHover={{ scale: 1.02, backgroundColor: "#f0f9ff" }}
                    className="border-t transition"
                  >
                    <td className="p-3">{row.employee_name}</td>
                    <td className="p-3">{row.log_date}</td>
                    <td className="p-3">{formatTime(row.productive_time)}</td>
                    <td className="p-3">{formatTime(row.idle_time)}</td>
                    <td className="p-3">{formatTime(row.over_time)}</td>
                  </motion.tr>
                ))
              )}
            </AnimatePresence>
          </tbody>
        </table>
      )}

      {/* Chart */}
      {records.length > 0 && (
        <div className="h-96 bg-white shadow rounded p-4">
          <h3 className="text-lg font-semibold mb-4">Time Distribution (minutes)</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <XAxis dataKey="employee_name" />
              <YAxis label={{ value: "Minutes", angle: -90, position: "insideLeft" }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="productive_time" fill="#4ade80" name="Productive" />
              <Bar dataKey="idle_time" fill="#facc15" name="Idle" />
              <Bar dataKey="over_time" fill="#f87171" name="Overtime" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
