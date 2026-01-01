// src/pages/Employees.jsx
import { useState, useEffect } from "react";
import {
  getEmployees
} from "../api/employeesApi";
import {
  getShifts,
  assignShiftToEmployee
} from "../api/shiftsApi";

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([]);
  const [shifts, setShifts] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState("");
  const [selectedShift, setSelectedShift] = useState("");
  const [editData, setEditData] = useState(null);

  useEffect(() => {
    fetchEmployees();
    fetchShifts();
  }, []);

  const fetchEmployees = async () => {
    const data = await getEmployees();
    setEmployees(data);
  };

  const fetchShifts = async () => {
    const data = await getShifts();
    setShifts(data);
  };

  const openAssignModal = () => {
    setSelectedEmployee("");
    setSelectedShift("");
    setEditData(null);
    setIsModalOpen(true);
  };

  const handleEdit = (employee) => {
    setSelectedEmployee(employee.id);
    setSelectedShift(employee.shift_code || "");
    setEditData(employee);
    setIsModalOpen(true);
  };

  const handleSave = async () => {
    if (!selectedEmployee || !selectedShift) {
      alert("Select both employee and shift!");
      return;
    }
    const result = await assignShiftToEmployee(selectedEmployee, selectedShift);
    if (result) {
      alert("Shift assigned successfully!");
      setIsModalOpen(false);
      setSelectedEmployee("");
      setSelectedShift("");
      setEditData(null);
      fetchEmployees(); // refresh table
    }
  };

  return (
    <div className="p-6">
      {/* Top-right Assign Shift button */}
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Employees</h1>
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          onClick={openAssignModal}
        >
          Assign Shift
        </button>
      </div>

      {/* Employee Table */}
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">Employee</th>
            <th className="border p-2">Shift</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((emp) => (
            <tr key={emp.id}>
              <td className="border p-2">{emp.name}</td>
              <td className="border p-2">{emp.shift_name || "-"}</td>
              <td className="border p-2">
                <button
                  className="bg-yellow-400 px-2 py-1 rounded"
                  onClick={() => handleEdit(emp)}
                >
                  Edit
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 w-96 relative">
            <h2 className="text-xl font-semibold mb-4">
              {editData ? "Edit Shift" : "Assign Shift"}
            </h2>

            <label className="block mb-2">Employee</label>
            <select
              className="w-full border p-2 rounded mb-4"
              value={selectedEmployee}
              onChange={(e) => setSelectedEmployee(e.target.value)}
            >
              <option value="">Select Employee</option>
              {employees.map((emp) => (
                <option key={emp.id} value={emp.id}>
                  {emp.name}
                </option>
              ))}
            </select>

            <label className="block mb-2">Shift</label>
            <select
              className="w-full border p-2 rounded mb-4"
              value={selectedShift}
              onChange={(e) => setSelectedShift(e.target.value)}
            >
              <option value="">Select Shift</option>
              {shifts.map((shift) => (
                <option key={shift.shift_code} value={shift.shift_code}>
                  {shift.shift_name} ({shift.start_time} - {shift.end_time})
                </option>
              ))}
            </select>

            <div className="flex justify-end gap-2">
              <button
                className="px-4 py-2 rounded bg-gray-300 hover:bg-gray-400"
                onClick={() => setIsModalOpen(false)}
              >
                Cancel
              </button>
              <button
                className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
                onClick={handleSave}
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
