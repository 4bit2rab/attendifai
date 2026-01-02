import { useEffect, useState } from "react";
import { getMonthlyReport, getMonthlySalary } from "../api/reportApi"; // import salary API
import { motion, AnimatePresence } from "framer-motion";
import * as XLSX from "xlsx";

/* ---------- Helpers ---------- */
const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return `${h}h ${m}m`;
};

const getDaysInMonth = (year, month) =>
  new Date(year, month, 0).getDate();

/* ---------- Component ---------- */
export default function Report() {
  const today = new Date();

  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);
  const [data, setData] = useState([]);
  const [salaries, setSalaries] = useState({}); // { employee_name: total_salary }
  const [loading, setLoading] = useState(false);

  const loadReport = async () => {
    setLoading(true);
    try {
      // Fetch both daily report and monthly salary
      const [dailyReport, salaryReport] = await Promise.all([
        getMonthlyReport(year, month),
        getMonthlySalary(year, month),
      ]);

      setData(dailyReport);

      const salaryMap = {};
      salaryReport.forEach((s) => {
        salaryMap[s.employee_name] = s.total_salary;
      });
      setSalaries(salaryMap);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReport();
  }, []);

  const days = getDaysInMonth(year, month);

  /* ---------- Normalize data ---------- */
  const employees = [...new Set(data.map((d) => d.employee_name))];
  const map = {};
  employees.forEach((e) => (map[e] = {}));
  data.forEach((r) => {
    map[r.employee_name][r.log_date] = r;
  });

  /* ---------- Excel Export (updated with salary) ---------- */
  const downloadExcel = () => {
    const workbook = XLSX.utils.book_new();

    const topHeader = ["Employee"];
    const subHeader = [""];

    for (let d = 1; d <= days; d++) {
      const dateObj = new Date(year, month - 1, d);
      const monthName = dateObj.toLocaleString("default", { month: "short" });
      const weekday = dateObj.toLocaleString("default", { weekday: "short" });

      topHeader.push(`${monthName} ${d} - ${weekday}`, "", "");
      subHeader.push("Productive", "Idle", "Overtime");
    }

    // Add salary column header
    topHeader.push("Total Salary");
    subHeader.push("");

    const rows = employees.map((emp) => {
      const row = [emp];
      for (let d = 1; d <= days; d++) {
        const dateStr = `${year}-${String(month).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
        const r = map[emp][dateStr];

        row.push(
          r ? (r.productive_time / 3600).toFixed(2) : 0,
          r ? (r.idle_time / 3600).toFixed(2) : 0,
          r ? (r.over_time / 3600).toFixed(2) : 0
        );
      }
      // Push salary
      row.push(salaries[emp]?.toFixed(2) || 0);
      return row;
    });

    const ws = XLSX.utils.aoa_to_sheet([topHeader, subHeader, ...rows]);

    let colIndex = 1;
    for (let d = 1; d <= days; d++) {
      ws["!merges"] = ws["!merges"] || [];
      ws["!merges"].push({
        s: { r: 0, c: colIndex },
        e: { r: 0, c: colIndex + 2 },
      });
      colIndex += 3;
    }

    XLSX.utils.book_append_sheet(workbook, ws, "Monthly Report");
    XLSX.writeFile(
      workbook,
      `Monthly_Report_${year}_${String(month).padStart(2, "0")}.xlsx`
    );
  };

  return (
    <div className="p-6 space-y-6 overflow-x-hidden">
      <h2 className="text-2xl font-bold text-blue-600">Monthly Report</h2>

      {/* Controls */}
      <div className="flex gap-4 items-center flex-wrap">
        <label>Year</label>
        <input
          type="number"
          value={year}
          onChange={(e) => setYear(+e.target.value)}
          className="border p-1 rounded w-24"
        />
        <label>Month</label>
        <input
          type="number"
          value={month}
          onChange={(e) => setMonth(+e.target.value)}
          className="border p-1 rounded w-20"
        />
        <button
          onClick={loadReport}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-1 rounded disabled:opacity-50"
        >
          {loading ? "Loading..." : "Load"}
        </button>
        <button
          onClick={downloadExcel}
          disabled={!data.length}
          className="bg-green-600 text-white px-4 py-1 rounded disabled:opacity-50"
        >
          Download Excel
        </button>
      </div>

      {/* GRID */}
      {loading ? (
        <p className="text-gray-500">Loading report...</p>
      ) : (
        <div
          className="border rounded-lg overflow-hidden"
          style={{ height: "420px", display: "grid", gridTemplateColumns: "220px 1fr" }}
        >
          {/* Employee column */}
          <div className="bg-gray-100 overflow-y-auto">
            <table className="border-collapse w-full">
              <thead>
                <tr>
                  <th className="sticky top-0 bg-gray-200 border p-2">Employee</th>
                </tr>
              </thead>
              <tbody>
                {employees.map((e) => (
                  <tr key={e}>
                    <td className="border p-2 font-medium">{e}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Dates grid */}
          <div className="overflow-x-scroll overflow-y-auto">
            <table
              className="border-collapse"
              style={{ width: `${days * 80 + 120}px` }} // +120 for salary column
            >
              <thead>
                <tr>
                  {Array.from({ length: days }, (_, i) => {
                    const d = new Date(year, month - 1, i + 1);
                    const day = d.getDay();
                    return (
                      <th
                        key={i}
                        className={`sticky top-0 border p-2 text-sm ${
                          day === 0 ? "bg-red-100" : day === 6 ? "bg-yellow-100" : "bg-gray-50"
                        }`}
                      >
                        {i + 1}
                      </th>
                    );
                  })}
                  <th className="sticky top-0 border p-2 text-sm bg-gray-200">Salary</th>
                </tr>
              </thead>
              <tbody>
                <AnimatePresence>
                  {employees.map((emp) => (
                    <motion.tr key={emp}>
                      {Array.from({ length: days }, (_, i) => {
                        const date = `${year}-${String(month).padStart(2, "0")}-${String(i + 1).padStart(2, "0")}`;
                        const r = map[emp][date];

                        if (!r) return <td key={i} className="border h-10" />;

                        const total = r.productive_time + r.idle_time + r.over_time;
                        const prod = (r.productive_time / total) * 100;
                        const idle = (r.idle_time / total) * 100;
                        const over = (r.over_time / total) * 100;

                        return (
                          <td key={i} className="border h-10 relative group">
                            <div className="flex items-center justify-center h-full">
                              <div className="flex w-full h-6 bg-gray-200 rounded overflow-hidden">
                                <div className="bg-green-500" style={{ width: `${prod}%` }} />
                                <div className="bg-orange-400" style={{ width: `${idle}%` }} />
                                <div className="bg-red-500" style={{ width: `${over}%` }} />
                              </div>
                            </div>

                            {/* Tooltip */}
                            <div className="absolute z-30 hidden group-hover:block bg-black text-white text-xs rounded p-2 
                                          left-full ml-2 top-1/2 -translate-y-1/2 whitespace-nowrap shadow-lg">
                              <div>Productive: {formatTime(r.productive_time)}</div>
                              <div>Idle: {formatTime(r.idle_time)}</div>
                              <div>Overtime: {formatTime(r.over_time)}</div>
                            </div>
                          </td>
                        );
                      })}
                      {/* Salary column */}
                      <td className="border h-10 text-center font-medium bg-gray-100">
                        {salaries[emp]?.toFixed(2) || 0}
                      </td>
                    </motion.tr>
                  ))}
                </AnimatePresence>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Legend */}
      <div className="flex gap-6 flex-wrap">
        <span className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-500 rounded" /> Productive
        </span>
        <span className="flex items-center gap-2">
          <div className="w-4 h-4 bg-orange-400 rounded" /> Idle
        </span>
        <span className="flex items-center gap-2">
          <div className="w-4 h-4 bg-red-500 rounded" /> Overtime
        </span>
        <span className="flex items-center gap-2">
          <div className="w-4 h-4 bg-yellow-100 rounded" /> Saturday
        </span>
        <span className="flex items-center gap-2">
          <div className="w-4 h-4 bg-red-100 rounded" /> Sunday
        </span>
        <span className="flex items-center gap-2">
          <div className="w-4 h-4 bg-gray-200 rounded" /> Month-to-Date Salary
        </span>
      </div>
    </div>
  );
}
