import { useEffect, useState } from "react";
import { getShifts, addShift, updateShift, deleteShift } from "../api/shiftsApi";
import { Edit2, Trash2, PlusCircle, XCircle, CheckCircle } from "lucide-react";

export default function Shifts() {
  const [shifts, setShifts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Add Shift form state
  const [formData, setFormData] = useState({
    shift_code: "",
    shift_start: "",
    shift_end: "",
  });

  // Edit Shift state
  const [editingShift, setEditingShift] = useState(null);
  const [editData, setEditData] = useState({ shift_code: "", shift_start: "", shift_end: "" });

  // Fetch all shifts
  const fetchShifts = async () => {
    setLoading(true);
    const data = await getShifts();
    setShifts(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchShifts();
  }, []);

  // Add shift
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    const added = await addShift(formData);
    if (added) {
      setFormData({ shift_code: "", shift_start: "", shift_end: "" });
      fetchShifts();
    }
  };

  // Edit shift
  const handleEditClick = (shift) => {
    setEditingShift(shift.shift_code);
    setEditData({ ...shift });
  };

  const handleSaveClick = async () => {
    const updated = await updateShift(editingShift, editData);
    if (updated) {
      setEditingShift(null);
      fetchShifts();
    }
  };

  const handleCancelClick = () => setEditingShift(null);

  // Delete shift
  const handleDeleteClick = async (shift_code) => {
    const confirmed = window.confirm("Are you sure you want to delete this shift?");
    if (!confirmed) return;

    const deleted = await deleteShift(shift_code);
    if (deleted) fetchShifts();
  };

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold text-blue-600">Shifts</h2>

      {/* Add Shift Form */}
      <div className="bg-white rounded-xl shadow p-4">
        <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
          <PlusCircle className="w-5 h-5 text-green-500" /> Add New Shift
        </h3>
        <form
          onSubmit={handleFormSubmit}
          className="flex flex-col md:flex-row gap-3 items-center"
        >
          <input
            type="text"
            placeholder="Shift Code"
            value={formData.shift_code}
            onChange={(e) => setFormData({ ...formData, shift_code: e.target.value })}
            className="border rounded-lg p-2 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
          <input
            type="time"
            value={formData.shift_start}
            onChange={(e) => setFormData({ ...formData, shift_start: e.target.value })}
            min="00:00"
            max="23:59"
            className="border rounded-lg p-2 w-full md:w-40 focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
          <input
            type="time"
            value={formData.shift_end}
            onChange={(e) => setFormData({ ...formData, shift_end: e.target.value })}
            min="00:00"
            max="23:59"
            className="border rounded-lg p-2 w-full md:w-40 focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded flex items-center gap-1 transition hover:scale-105"
          >
            <PlusCircle className="w-4 h-4" /> Add
          </button>
        </form>
      </div>

      {/* Shifts Table */}
      <div className="bg-white rounded-xl shadow overflow-x-auto">
        {loading ? (
          <p className="p-4 text-gray-500">Loading shifts...</p>
        ) : (
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Shift Code</th>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Start Time</th>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">End Time</th>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Actions</th>
              </tr>
            </thead>
            <tbody>
              {shifts.length === 0 ? (
                <tr>
                  <td colSpan="4" className="p-4 text-center text-gray-500">
                    No shifts found
                  </td>
                </tr>
              ) : (
                shifts.map((shift, idx) => (
                  <tr
                    key={shift.shift_code}
                    className={`border-t hover:bg-blue-50 transition-colors duration-200 ${
                      idx % 2 === 0 ? "bg-gray-50" : "bg-white"
                    }`}
                  >
                    {editingShift === shift.shift_code ? (
                      <>
                        <td className="p-2">
                          <input
                            type="text"
                            value={editData.shift_code}
                            onChange={(e) =>
                              setEditData({ ...editData, shift_code: e.target.value })
                            }
                            className="border rounded-lg p-1 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
                          />
                        </td>
                        <td className="p-2">
                          <input
                            type="time"
                            value={editData.shift_start}
                            onChange={(e) =>
                              setEditData({ ...editData, shift_start: e.target.value })
                            }
                            className="border rounded-lg p-1 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
                          />
                        </td>
                        <td className="p-2">
                          <input
                            type="time"
                            value={editData.shift_end}
                            onChange={(e) =>
                              setEditData({ ...editData, shift_end: e.target.value })
                            }
                            className="border rounded-lg p-1 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
                          />
                        </td>
                        <td className="p-2 flex gap-2">
                          <button
                            onClick={handleSaveClick}
                            className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded flex items-center gap-1 transition hover:scale-105"
                          >
                            <CheckCircle className="w-4 h-4" /> Save
                          </button>
                          <button
                            onClick={handleCancelClick}
                            className="bg-gray-400 hover:bg-gray-500 text-white px-3 py-1 rounded flex items-center gap-1 transition hover:scale-105"
                          >
                            <XCircle className="w-4 h-4" /> Cancel
                          </button>
                        </td>
                      </>
                    ) : (
                      <>
                        <td className="p-3 font-medium">{shift.shift_code}</td>
                        <td className="p-3">
                          <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded-full text-sm">
                            {shift.shift_start}
                          </span>
                        </td>
                        <td className="p-3">
                          <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded-full text-sm">
                            {shift.shift_end}
                          </span>
                        </td>
                        <td className="p-3 flex gap-2">
                          <button
                            onClick={() => handleEditClick(shift)}
                            className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded flex items-center gap-1 transition hover:scale-105"
                          >
                            <Edit2 className="w-4 h-4" /> Edit
                          </button>
                          <button
                            onClick={() => handleDeleteClick(shift.shift_code)}
                            className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded flex items-center gap-1 transition hover:scale-105"
                          >
                            <Trash2 className="w-4 h-4" /> Delete
                          </button>
                        </td>
                      </>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
