// src/pages/Dashboard.jsx
import { useEffect, useState } from "react";
import { Users, UserCheck, UserX, Clock } from "lucide-react";
import { getEmployees } from "../api/employeesApi"; // import your API

// Placeholder components for now
function AttendanceChart() {
  return (
    <div className="h-48 flex items-center justify-center bg-gray-100 rounded-lg">
      <span className="text-gray-500">[Weekly Attendance Chart]</span>
    </div>
  );
}

function RecentActivity() {
  return (
    <div className="flex flex-col space-y-2">
      <div className="p-2 bg-gray-100 rounded">John Doe checked in</div>
      <div className="p-2 bg-gray-100 rounded">Jane Smith checked out</div>
      <div className="p-2 bg-gray-100 rounded">Mark Lee was absent</div>
    </div>
  );
}

export default function Dashboard() {
  const [totalEmployees, setTotalEmployees] = useState(0);
  const [presentToday, setPresentToday] = useState(0);
  const [absentToday, setAbsentToday] = useState(0);
  const [lateCheckins, setLateCheckins] = useState(0);

  useEffect(() => {
    const loadEmployees = async () => {
      try {
        const employees = await getEmployees(); // call your API
        setTotalEmployees(Array.isArray(employees) ? employees.length : 0);

        // Example: calculate stats dynamically
        let present = 0;
        let absent = 0;
        let late = 0;

        employees.forEach((emp) => {
          if (emp.status === "present") present += 1;
          else if (emp.status === "absent") absent += 1;

          if (emp.isLate) late += 1;
        });

        setPresentToday(present);
        setAbsentToday(absent);
        setLateCheckins(late);
      } catch (err) {
        console.error("Failed to load employees:", err);
      }
    };

    loadEmployees();
  }, []);

  const stats = [
    {
      title: "Total Employees",
      value: totalEmployees,
      icon: <Users className="h-6 w-6 text-white" />,
      bg: "bg-blue-600",
    },
    {
      title: "Present Today",
      value: presentToday,
      icon: <UserCheck className="h-6 w-6 text-white" />,
      bg: "bg-green-600",
    },
    {
      title: "Absent Today",
      value: absentToday,
      icon: <UserX className="h-6 w-6 text-white" />,
      bg: "bg-red-600",
    },
    {
      title: "Late Check-ins",
      value: lateCheckins,
      icon: <Clock className="h-6 w-6 text-white" />,
      bg: "bg-yellow-500",
    },
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <p className="text-sm text-gray-500">
          Overview of attendance and productivity.
        </p>
      </div>

      {/* Stats */}
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
