// src/pages/Dashboard.jsx
import { useEffect, useState } from "react";
import { Users, UserCheck, UserX, Clock, TrendingUp } from "lucide-react";
import { getEmployees } from "../api/employeesApi";
import { getPredictedProductivity } from "../api/productivityApi";
import { getEmployeeRanking } from "../api/rankingApi";
import { getDefaultDateRange } from "../utils/dateUtils";
import ProductivityDonutChart from "../components/ProductivityDonutChart";
import { getWeeklySummary } from "../api/weeklysummaryApi";

/* -----------------------------
   Main Dashboard
------------------------------ */
export default function Dashboard() {
  const [totalEmployees, setTotalEmployees] = useState(0);
  const [presentToday, setPresentToday] = useState(0);
  const [absentToday, setAbsentToday] = useState(0);
  const [lateCheckins, setLateCheckins] = useState(0);

  const [predictions, setPredictions] = useState([]);
  const [topEmployees, setTopEmployees] = useState([]);
  const [weeklyProductivity, setWeeklyProductivity] = useState(null);



  /* -----------------------------
     Load Employees
  ------------------------------ */
  useEffect(() => {
    const loadEmployees = async () => {
      try {
        const employees = await getEmployees();
        setTotalEmployees(employees.length);

        let present = 0;
        let absent = 0;
        let late = 0;

        employees.forEach((emp) => {
          if (emp.status === "present") present++;
          if (emp.status === "absent") absent++;
          if (emp.isLate) late++;
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

  /* -----------------------------
     Load Productivity Predictions
  ------------------------------ */
  useEffect(() => {
    const loadPredictions = async () => {
      try {
        const data = await getPredictedProductivity();
        setPredictions(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error("Prediction API error:", err);
        setPredictions([]);
      }
    };

    loadPredictions();
  }, []);

   /* -----------------------------
     Load Employee Rankings
  ------------------------------ */

  useEffect(() => {
    const loadRankings = async () => {
      try {
        const { start_date, end_date } = getDefaultDateRange();
        const data = await getEmployeeRanking(start_date, end_date);
        setTopEmployees(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error("Ranking API error:", err);
        setTopEmployees([]);
      }
    };

    loadRankings();
  }, []);

  /* -----------------------------
     Load Weekly Productivity
  ------------------------------ */
  useEffect(() => {
  const loadWeeklyProductivity = async () => {
    try {
      const data = await getWeeklySummary();
      setWeeklyProductivity(data);
    } catch (err) {
      console.error("Weekly productivity error:", err);
      setWeeklyProductivity(null);
    }
  };

  loadWeeklyProductivity();
}, []);


  /* -----------------------------
     Helpers
  ------------------------------ */
  const getConfidenceStyle = (confidence) => {
    switch (confidence) {
      case "High":
        return "bg-green-100 text-green-700";
      case "Medium":
        return "bg-yellow-100 text-yellow-700";
      default:
        return "bg-red-100 text-red-700";
    }
  };

  const getBarColor = (value) => {
    if (value >= 32) return "bg-green-500"; // 80%+
    if (value >= 20) return "bg-yellow-500";
    return "bg-red-500";
  };

  /* -----------------------------
     Stats
  ------------------------------ */
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
        <h1 className="text-2xl font-bold mb-4 text-blue-600">
          Manager Dashboard
        </h1>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div
            key={index}
            className={`${stat.bg} rounded-xl shadow-sm p-5 flex justify-between`}
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
          <h2 className="font-semibold mb-4">Weekly Attendance</h2>
          <ProductivityDonutChart
            data={weeklyProductivity}
          />
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="font-semibold mb-4">
            🏆 Top 5 Employees
          </h2>

          {topEmployees.length === 0 ? (
            <p className="text-sm text-gray-500">
              No ranking data available.
            </p>
          ) : (
            <div className="space-y-4">
              {topEmployees.map((emp) => (
                <div
                  key={emp.employee_id}
                  className="border rounded-lg p-4"
                >
                  <div className="flex justify-between items-center mb-2">
                    <div>
                      <p className="font-medium text-gray-800">
                        #{emp.rank} {emp.employee_name}
                      </p>
                      <p className="text-xs text-gray-500">
                        Performance: {emp.performance}
                      </p>
                    </div>

                    <span className="text-sm font-semibold text-indigo-600">
                      {emp.productivity_score.toFixed(1)}%
                    </span>
                  </div>

                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-indigo-600 h-3 rounded-full"
                      style={{ width: `${emp.productivity_score}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* 🔮 Productivity Prediction Section */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="text-indigo-600" />
          <h2 className="text-lg font-semibold">
            Next Week Productivity Prediction
          </h2>
        </div>

        {predictions.length === 0 ? (
          <p className="text-sm text-gray-500">
            No prediction data available.
          </p>
        ) : (
          <div className="space-y-5">
            {predictions.map((emp) => {
              const percentage = Math.min(
                (emp.predicted_next_week_productive_hours / 40) * 100,
                100
              );

              return (
                <div
                  key={emp.employee_id}
                  className="border rounded-lg p-4"
                >
                  <div className="flex justify-between items-center mb-2">
                    <p className="font-medium text-gray-800">
                      {emp.employee_name}
                    </p>

                    <span
                      className={`text-xs px-2 py-1 rounded-full ${getConfidenceStyle(
                        emp.confidence
                      )}`}
                    >
                      {emp.confidence}
                    </span>
                  </div>

                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`${getBarColor(
                        emp.predicted_next_week_productive_hours
                      )} h-3 rounded-full`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>

                  <p className="text-xs text-gray-600 mt-1">
                    Predicted Hours:{" "}
                    <strong>
                      {emp.predicted_next_week_productive_hours.toFixed(1)}hrs
                    </strong>
                  </p>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
