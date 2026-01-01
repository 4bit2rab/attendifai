import { NavLink } from "react-router-dom";
import {
  HomeIcon,
  CalendarCheckIcon,
  ClockIcon,
  UsersIcon,
  BarChartIcon,
  LogOutIcon,
} from "lucide-react";

export default function Sidebar() {
  const links = [
    { name: "Dashboard", path: "/dashboard", icon: HomeIcon },
    { name: "Attendance", path: "/attendance", icon: CalendarCheckIcon },
    { name: "Shifts", path: "/shifts", icon: ClockIcon },
    { name: "Employees", path: "/employees", icon: UsersIcon },
    { name: "Monthly Report", path: "/reports/monthly", icon: BarChartIcon },
  ];

  return (
    <aside className="w-64 bg-gradient-to-b from-blue-700 to-blue-800 text-white flex flex-col shadow-xl">
      {/* Logo */}
      <div className="px-6 py-6 text-2xl font-extrabold tracking-wide">
        AttendifAI
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 space-y-2">
        {links.map(({ name, path, icon: Icon }) => (
          <NavLink
            key={name}
            to={path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200
              ${
                isActive
                  ? "bg-white/20 shadow text-white font-semibold"
                  : "text-blue-100 hover:bg-white/10"
              }`
            }
          >
            <Icon className="w-5 h-5" />
            {name}
          </NavLink>
        ))}
      </nav>

      {/* Logout */}
      <div className="p-4 border-t border-blue-600">
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-blue-100 hover:bg-red-600 hover:text-white transition">
          <LogOutIcon className="w-5 h-5" />
          Logout
        </button>
      </div>
    </aside>
  );
}
