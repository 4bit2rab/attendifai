import { useEffect, useState } from "react";

export default function Employees() {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    // TEMP data (replace with API later)
    setEmployees([
      { id: 1, name: "John Doe", role: "Developer" },
      { id: 2, name: "Jane Smith", role: "Designer" },
      { id: 3, name: "Alex Johnson", role: "Tester" },
    ]);
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Employees</h2>

      <table className="w-full bg-white shadow rounded">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-3 text-left">Name</th>
            <th className="p-3 text-left">Role</th>
          </tr>
        </thead>

        <tbody>
          {employees.map((emp) => (
            <tr key={emp.id} className="border-t">
              <td className="p-3">{emp.name}</td>
              <td className="p-3">{emp.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
