import { useEffect, useState } from "react";
import { getOvertime } from "../api/overtimeApi";
import { motion, AnimatePresence } from "framer-motion";

export default function OvertimeApproval() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [date, setDate] = useState(() => new Date().toISOString().slice(0, 10));
  const [approvals, setApprovals] = useState({}); // { employeeId_date: "approved"/"rejected"/null }

  useEffect(() => {
    fetchOvertime();
  }, [date]);

  const fetchOvertime = async () => {
    setLoading(true);
    try {
      const data = await getOvertime(date);
      setRecords(data);

      const initialApprovals = {};
      data.forEach((r) => {
        initialApprovals[`${r.employee_id}_${r.log_date}`] = null;
      });
      setApprovals(initialApprovals);
    } catch (error) {
      console.error("Failed to load overtime:", error);
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

  const handleApprovalChange = (key, value) => {
    setApprovals((prev) => ({ ...prev, [key]: value }));
  };

  const submitApprovals = () => {
    console.log("Submitted Approvals:", approvals);
    // TODO: Call API to save approvals
  };

  const rowColors = ["bg-white", "bg-blue-50"];

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold mb-4 text-blue-600">Overtime Approval</h2>

      {/* Date Picker */}
      <div className="mb-6 flex flex-col sm:flex-row items-start sm:items-center gap-3">
        <label className="font-medium">Select Date:</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="border p-2 rounded-lg hover:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
        />
      </div>

      {/* Overtime Table */}
      <div className="bg-white shadow rounded-xl overflow-hidden">
        {loading ? (
          <p className="p-4 text-gray-500">Loading overtime records...</p>
        ) : (
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Employee</th>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Date</th>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Overtime</th>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Approval</th>
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
                    <td colSpan="4" className="p-4 text-center text-gray-500">
                      No records found
                    </td>
                  </motion.tr>
                ) : (
                  records.map((row, index) => {
                    const key = `${row.employee_id}_${row.log_date}`;
                    return (
                      <motion.tr
                        key={key}
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        whileHover={{ scale: 1.02, backgroundColor: "#e0f2fe" }}
                        className={`border-t ${rowColors[index % rowColors.length]} transition-colors duration-200`}
                      >
                        <td className="p-3 font-medium">{row.employee_name}</td>
                        <td className="p-3">{row.log_date}</td>
                        <td className="p-3">
                          <span className="px-2 py-1 rounded-full bg-red-100 text-red-800">
                            {formatTime(row.over_time)}
                          </span>
                        </td>
                        <td className="p-3">
                          <select
                            value={approvals[key] || ""}
                            onChange={(e) => handleApprovalChange(key, e.target.value)}
                            className="border rounded p-1"
                          >
                            <option value="">-- Select --</option>
                            <option value="approved">Approved</option>
                            <option value="rejected">Rejected</option>
                          </select>
                        </td>
                      </motion.tr>
                    );
                  })
                )}
              </AnimatePresence>
            </tbody>
          </table>
        )}
      </div>

      {/* Submit Button */}
      <div className="flex justify-end mt-4">
        <button
          onClick={submitApprovals}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          Submit Approvals
        </button>
      </div>
    </div>
  );
}
