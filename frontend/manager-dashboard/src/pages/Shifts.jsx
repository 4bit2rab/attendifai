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
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-6 text-blue-600">Shifts</h2>

      {/* Add Shift Form */}
      <div className="mb-6 p-4 border rounded shadow bg-white">
        <h3 className="font-semibold mb-3 flex items-center gap-2">
          <PlusCircle className="w-5 h-5 text-green-500" />
          Add New Shift
        </h3>
        <form onSubmit={handleFormSubmit} className="flex flex-col md:flex-row gap-2">
          <input
            type="text"
            placeholder="Shift Code"
            value={formData.shift_code}
            onChange={(e) => setFormData({ ...formData, shift_code: e.target.value })}
            className="border p-2 rounded flex-1"
            required
          />
          <input
            type="time"
            value={formData.shift_start}
            onChange={(e) => setFormData({ ...formData, shift_start: e.target.value })}
            min="00:00"
            max="23:59"
            className="border p-2 rounded w-full md:w-40"
            required
          />
          <input
            type="time"
            value={formData.shift_end}
            onChange={(e) => setFormData({ ...formData, shift_end: e.target.value })}
            min="00:00"
            max="23:59"
            className="border p-2 rounded w-full md:w-40"
            required
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded flex items-center justify-center gap-1 hover:bg-blue-600 transition"
          >
            Add
          </button>
        </form>
      </div>

      {/* Shifts Table */}
      {loading ? (
        <p>Loading shifts...</p>
      ) : (
        <table className="w-full bg-white shadow rounded overflow-hidden">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3 text-left">Shift Code</th>
              <th className="p-3 text-left">Start Time</th>
              <th className="p-3 text-left">End Time</th>
              <th className="p-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {shifts.length === 0 ? (
              <tr>
                <td colSpan="4" className="p-3 text-center">
                  No shifts found
                </td>
              </tr>
            ) : (
              shifts.map((shift, idx) => (
                <tr
                  key={shift.shift_code}
                  className={`border-t transition-colors duration-300 ${
                    idx % 2 === 0 ? "bg-gray-50" : "bg-white"
                  }`}
                >
                  {editingShift === shift.shift_code ? (
                    <>
                      <td className="p-2">
                        <input
                          type="text"
                          value={editData.shift_code}
                          onChange={(e) => setEditData({ ...editData, shift_code: e.target.value })}
                          className="border p-1 rounded w-full"
                        />
                      </td>
                      <td className="p-2">
                        <input
                          type="time"
                          value={editData.shift_start}
                          onChange={(e) => setEditData({ ...editData, shift_start: e.target.value })}
                          min="00:00"
                          max="23:59"
                          className="border p-1 rounded w-full"
                        />
                      </td>
                      <td className="p-2">
                        <input
                          type="time"
                          value={editData.shift_end}
                          onChange={(e) => setEditData({ ...editData, shift_end: e.target.value })}
                          min="00:00"
                          max="23:59"
                          className="border p-1 rounded w-full"
                        />
                      </td>
                      <td className="p-2 flex gap-2">
                        <button
                          onClick={handleSaveClick}
                          className="bg-green-500 text-white p-2 rounded hover:bg-green-600 transition"
                        >
                          <CheckCircle className="w-4 h-4 inline" /> Save
                        </button>
                        <button
                          onClick={handleCancelClick}
                          className="bg-gray-400 text-white p-2 rounded hover:bg-gray-500 transition"
                        >
                          <XCircle className="w-4 h-4 inline" /> Cancel
                        </button>
                      </td>
                    </>
                  ) : (
                    <>
                      <td className="p-3 font-medium">{shift.shift_code}</td>
                      <td className="p-3">{shift.shift_start}</td>
                      <td className="p-3">{shift.shift_end}</td>
                      <td className="p-3 flex gap-2">
                        <button
                          onClick={() => handleEditClick(shift)}
                          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition flex items-center gap-1"
                        >
                          <Edit2 className="w-4 h-4" /> Edit
                        </button>
                        <button
                          onClick={() => handleDeleteClick(shift.shift_code)}
                          className="bg-red-500 text-white p-2 rounded hover:bg-red-600 transition flex items-center gap-1"
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
  );
}

