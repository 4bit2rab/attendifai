import { Link, useLocation } from "react-router-dom";
import { HomeIcon, CalendarCheckIcon, ClockIcon, UsersIcon } from "lucide-react";

export default function Sidebar() {
  const location = useLocation();
  const links = [
    { name: "Dashboard", path: "/dashboard", icon: "🏠  " },
    { name: "Attendance", path: "/attendance", icon: "📅  " },
    { name: "Shifts", path: "/shifts", icon: "⏰  " },
    { name: "Employees", path: "/employees", icon: "👥  " },
  ];
  // const links = [
  //   { name: "Dashboard", path: "/dashboard", icon: <HomeIcon className="w-5 h-5 mr-2" /> },
  //   { name: "Attendance", path: "/attendance", icon: <CalendarCheckIcon className="w-5 h-5 mr-2" /> },
  //   { name: "Shifts", path: "/shifts", icon: <ClockIcon className="w-5 h-5 mr-2" /> },
  //   { name: "Employees", path: "/employees", icon: <UsersIcon className="w-5 h-5 mr-2" /> },
  // ];

  return (
    <div className="w-64 bg-white shadow h-full p-6 flex flex-col">
      <h2 className="text-2xl font-bold mb-8 text-blue-600">Attendifai</h2>

      <nav className="flex-1 space-y-2">
        {links.map((link) => {
          const isActive = location.pathname === link.path;
          return (
            <Link
              key={link.name}
              to={link.path}
              className={`flex items-center p-3 rounded-lg transition-colors duration-200
                ${isActive ? "bg-blue-100 text-blue-700 font-semibold" : "text-gray-700 hover:bg-blue-50 hover:text-blue-600"}
              `}
            >
              {link.icon}
              {link.name}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto pt-4 border-t border-gray-200">
        <button className="w-full p-3 text-gray-700 rounded-lg hover:bg-red-100 hover:text-red-600 transition-colors duration-200">
          Logout
        </button>
      </div>
    </div>
  );
}
