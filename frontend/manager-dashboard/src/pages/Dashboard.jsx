import AttendanceChart from "../components/AttendanceChart";
import RecentActivity from "../components/RecentActivity";
import { Users, UserCheck, UserX, Clock } from "lucide-react";

export default function Dashboard() {
  const stats = [
    {
      title: "Total Employees",
      value: 128,
      icon: <Users className="h-6 w-6 text-white" />,
      bg: "bg-blue-600",
    },
    {
      title: "Present Today",
      value: 102,
      icon: <UserCheck className="h-6 w-6 text-white" />,
      bg: "bg-green-600",
    },
    {
      title: "Absent Today",
      value: 18,
      icon: <UserX className="h-6 w-6 text-white" />,
      bg: "bg-red-600",
    },
    {
      title: "Late Check-ins",
      value: 8,
      icon: <Clock className="h-6 w-6 text-white" />,
      bg: "bg-yellow-500",
    },
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Dashboard Header */}
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <p className="text-sm text-gray-500">
          Overview of attendance and productivity.
        </p>
      </div>

      {/* Stats Boxes */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div
            key={index}
            className={`${stat.bg} rounded-xl shadow-sm p-5 flex items-center justify-between`}
          >
            <div>
              <p className="text-sm text-white">{stat.title}</p>
              <p className="text-2xl font-bold text-white">{stat.value}</p>
            </div>
            <div className="h-12 w-12 flex items-center justify-center rounded-lg bg-white/20">
              {stat.icon}
            </div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Weekly Attendance
          </h2>
          <AttendanceChart />
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Recent Activity
          </h2>
          <RecentActivity />
        </div>
      </div>
    </div>
  );
}
