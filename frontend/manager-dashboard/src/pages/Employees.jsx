import { useEffect, useState } from "react";
import { X } from "lucide-react";
import { getEmployees } from "../api/employeesApi";
import { getShifts } from "../api/shiftsApi";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [shifts, setShifts] = useState([]);
  const [error, setError] = useState("");

  // Assign shift
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [selectedShift, setSelectedShift] = useState("");

  // Global activity threshold
  const [showThresholdModal, setShowThresholdModal] = useState(false);
  const [idleMinutes, setIdleMinutes] = useState(10);

  // ------------------------
  // Load data
  // ------------------------
  useEffect(() => {
    loadEmployees();
    loadShifts();
    loadGlobalThreshold();
  }, []);

  const getAuthToken = () => sessionStorage.getItem("access_token");

  const loadEmployees = async () => {
    try {
      const data = await getEmployees();
      setEmployees(Array.isArray(data) ? data : []);
    } catch {
      setError("Failed to load employees");
    }
  };

  const loadShifts = async () => {
    try {
      const data = await getShifts();
      setShifts(Array.isArray(data) ? data : []);
    } catch {
      console.error("Failed to load shifts");
    }
  };

  const loadGlobalThreshold = async () => {
    try {
      const token = getAuthToken();
      if (!token) throw new Error("Authorization token missing");

      const res = await axios.get(`${API_BASE_URL}/activity-threshold`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setIdleMinutes(res.data.idle_time_out);
    } catch {
      console.warn("Using default idle timeout");
    }
  };

  // ------------------------
  // Assign shift
  // ------------------------
  const assignShift = async () => {
    if (!selectedEmployee || !selectedShift) return;

    try {
      const token = getAuthToken();
      if (!token) throw new Error("Authorization token missing");

      await axios.put(
        `${API_BASE_URL}/assign-shift/${selectedEmployee.employee_id}`,
        null,
        { params: { shift_code: selectedShift }, headers: { Authorization: `Bearer ${token}` } }
      );

      await loadEmployees();
      setSelectedEmployee(null);
      setSelectedShift("");
    } catch {
      alert("Failed to assign shift");
    }
  };

  // ------------------------
  // Save idle threshold
  // ------------------------
  const saveGlobalThreshold = async () => {
    try {
      const token = getAuthToken();
      if (!token) throw new Error("Authorization token missing");

      await axios.post(
        `${API_BASE_URL}/activity-threshold`,
        { idle_time_out: Number(idleMinutes) },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setShowThresholdModal(false);
      alert("Idle timeout updated successfully");
    } catch {
      alert("Failed to save idle timeout");
    }
  };

  const formatTime = (time) => time?.slice(0, 5);

  return (
    <div className="p-6 relative">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-blue-600">Employees</h2>

        <button
          onClick={() => setShowThresholdModal(true)}
          className="bg-gray-800 text-white px-4 py-2 rounded"
        >
          Activity Threshold ⚙️
        </button>
      </div>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      {/* Employees Table */}
      <div className="bg-white shadow rounded-lg overflow-x-auto">
        <table className="w-full">
          <thead className="bg-blue-50">
            <tr>
              <th className="p-3 text-left">Name</th>
              <th className="p-3 text-left">Email</th>
              <th className="p-3 text-left">Phone</th>
              <th className="p-3 text-left">Shift</th>
              <th className="p-3 text-left">Action</th>
            </tr>
          </thead>

          <tbody>
            {employees.length === 0 ? (
              <tr>
                <td colSpan="5" className="p-4 text-center text-gray-500">
                  No employees found
                </td>
              </tr>
            ) : (
              employees.map((emp) => (
                <tr key={emp.employee_id} className="border-t">
                  <td className="p-3">{emp.employee_name}</td>
                  <td className="p-3">{emp.employee_email}</td>
                  <td className="p-3">{emp.employee_phone}</td>
                  <td className="p-3">{emp.shift_code || "-"}</td>
                  <td className="p-3">
                    <button
                      onClick={() => {
                        setSelectedEmployee(emp);
                        setSelectedShift(emp.shift_code || "");
                      }}
                      className="bg-blue-600 text-white px-3 py-1 rounded"
                    >
                      Assign Shift
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Assign Shift Modal */}
      {selectedEmployee && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white w-full max-w-md rounded-lg p-6 relative">
            <button
              onClick={() => setSelectedEmployee(null)}
              className="absolute top-3 right-3 text-gray-500"
            >
              <X />
            </button>

            <h3 className="text-lg font-semibold mb-3">
              Assign Shift – {selectedEmployee.employee_name}
            </h3>

            <select
              value={selectedShift}
              onChange={(e) => setSelectedShift(e.target.value)}
              className="w-full border p-2 rounded mb-4"
            >
              <option value="">Select shift</option>
              {shifts.map((shift) => (
                <option key={shift.shift_code} value={shift.shift_code}>
                  {shift.shift_code} ({formatTime(shift.shift_start)} -{" "}
                  {formatTime(shift.shift_end)})
                </option>
              ))}
            </select>

            <button
              onClick={assignShift}
              className="w-full bg-blue-600 text-white py-2 rounded"
            >
              Assign Shift
            </button>
          </div>
        </div>
      )}

      {/* Global Idle Threshold Modal */}
      {showThresholdModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white w-full max-w-md rounded-lg p-6 relative">
            <button
              onClick={() => setShowThresholdModal(false)}
              className="absolute top-3 right-3 text-gray-500"
            >
              <X />
            </button>

            <h3 className="text-lg font-semibold mb-4">
              Global Activity Threshold
            </h3>

            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium">
                  Idle Timeout (minutes)
                </label>
                <input
                  type="number"
                  min="1"
                  value={idleMinutes}
                  onChange={(e) => setIdleMinutes(e.target.value)}
                  className="w-full border p-2 rounded"
                />
              </div>
            </div>

            <button
              onClick={saveGlobalThreshold}
              className="w-full mt-5 bg-blue-600 text-white py-2 rounded"
            >
              Save Settings
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
