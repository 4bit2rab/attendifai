import { useEffect, useState } from "react";
import { UserPlus, X } from "lucide-react";
import { createEmployee, getEmployees } from "../api/employeesApi";

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [formData, setFormData] = useState({
    employee_name: "",
    employee_email: "",
    employee_phone: "",
    shift_code: "",
  });

  // ✅ Load employees on mount
  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      const data = await getEmployees();
      setEmployees(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError("Failed to load employees");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const result = await createEmployee(formData);

    if (!result) {
      setError("Failed to create employee");
      setLoading(false);
      return;
    }

    await loadEmployees();
    setShowForm(false);
    setLoading(false);
  };

  return (
    <div className="p-6 relative">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-blue-600">Employees</h2>

        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2"
        >
          <UserPlus size={18} />
          Add Employee
        </button>
      </div>

      {/* Error */}
      {error && (
        <p className="mb-4 text-red-600 font-medium">{error}</p>
      )}

      {/* Table */}
      <div className="bg-white shadow rounded-lg overflow-x-auto">
        <table className="w-full">
          <thead className="bg-blue-50">
            <tr>
              <th className="p-3 text-left">Name</th>
              <th className="p-3 text-left">Email</th>
              <th className="p-3 text-left">Phone</th>
              <th className="p-3 text-left">Shift</th>
            </tr>
          </thead>

          <tbody>
            {employees.length === 0 ? (
              <tr>
                <td colSpan="4" className="p-4 text-center text-gray-500">
                  No employees found
                </td>
              </tr>
            ) : (
              employees.map((emp) => (
                <tr key={emp.id ?? emp.employee_email} className="border-t">
                  <td className="p-3">{emp.employee_name}</td>
                  <td className="p-3">{emp.employee_email}</td>
                  <td className="p-3">{emp.employee_phone}</td>
                  <td className="p-3">{emp.shift_code}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white w-full max-w-md rounded-lg p-6 relative">
            <button
              onClick={() => setShowForm(false)}
              className="absolute top-3 right-3 text-gray-500"
            >
              <X />
            </button>

            <h3 className="text-lg font-semibold mb-4">
              Add Employee
            </h3>

            <form onSubmit={handleSubmit} className="space-y-3">
              <input
                placeholder="Name"
                className="w-full border p-2 rounded"
                value={formData.employee_name}
                onChange={(e) =>
                  setFormData({ ...formData, employee_name: e.target.value })
                }
                required
              />

              <input
                type="email"
                placeholder="Email"
                className="w-full border p-2 rounded"
                value={formData.employee_email}
                onChange={(e) =>
                  setFormData({ ...formData, employee_email: e.target.value })
                }
                required
              />

              <input
                placeholder="Phone"
                className="w-full border p-2 rounded"
                value={formData.employee_phone}
                onChange={(e) =>
                  setFormData({ ...formData, employee_phone: e.target.value })
                }
                required
              />

              <input
                placeholder="Shift Code"
                className="w-full border p-2 rounded"
                value={formData.shift_code}
                onChange={(e) =>
                  setFormData({ ...formData, shift_code: e.target.value })
                }
                required
              />

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-2 rounded"
              >
                {loading ? "Saving..." : "Save"}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
