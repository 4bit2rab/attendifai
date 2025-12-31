import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-64 bg-white shadow h-full p-4">
      <h2 className="text-xl font-bold mb-6">Manager</h2>

      <nav className="space-y-3">
        <Link to="/dashboard" className="block hover:text-blue-600">
          Dashboard
        </Link>
        <Link to="/attendance" className="block hover:text-blue-600">
          Attendance
        </Link>
        <Link to="/shifts" className="block hover:text-blue-600">
          Shifts
        </Link>
        <Link to="/employees" className="block hover:text-blue-600">
            Employees
        </Link>
      </nav>
    </div>
  );
}
