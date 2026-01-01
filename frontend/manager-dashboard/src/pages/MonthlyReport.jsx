import { useState } from "react";
import { FileText } from "lucide-react";
import { getMonthlyEmployeeReport } from "../api/reportApi";

export default function MonthlyReport() {
  const [month, setMonth] = useState("2025-01");
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState([]);

  const managerId = "MANAGER_001"; // 🔴 Replace with real logged-in manager ID

  const handleGenerateReport = async () => {
    setLoading(true);

    // Convert month to start & end date
    const startDate = `${month}-01`;
    const endDate = `${month}-31`;

    const data = await getMonthlyEmployeeReport(
      managerId,
      startDate,
      endDate
    );

    setReportData(data);
    setLoading(false);
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-blue-600">
            Monthly Employee Report
          </h1>
          <p className="text-sm text-gray-500">
            Total, productive, idle & overtime hours
          </p>
        </div>

        <div className="flex gap-3">
          <input
            type="month"
            value={month}
            onChange={(e) => setMonth(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          />

          <button
            onClick={handleGenerateReport}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
          >
            <FileText size={18} />
            Generate
          </button>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <p className="text-center text-gray-500">
          Generating report...
        </p>
      )}

      {/* Table */}
      {!loading && reportData.length > 0 && (
        <div className="overflow-x-auto bg-white rounded-xl shadow-sm">
          <table className="min-w-full text-sm">
            <thead className="bg-blue-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left font-semibold">
                  Employee
                </th>
                <th className="px-6 py-3 text-center font-semibold">
                  Total Hours
                </th>
                <th className="px-6 py-3 text-center font-semibold">
                  Productive
                </th>
                <th className="px-6 py-3 text-center font-semibold">
                  Idle
                </th>
                <th className="px-6 py-3 text-center font-semibold">
                  Overtime
                </th>
              </tr>
            </thead>

            <tbody className="divide-y">
              {reportData.map((emp, index) => (
                <tr
                  key={index}
                  className="hover:bg-blue-50 transition"
                >
                  <td className="px-6 py-4 font-medium">
                    {emp.employee_name}
                  </td>

                  <td className="px-6 py-4 text-center">
                    {emp.total_hours} hrs
                  </td>

                  <td className="px-6 py-4 text-center text-green-600 font-medium">
                    {emp.productive_hours} hrs
                  </td>

                  <td className="px-6 py-4 text-center text-yellow-600 font-medium">
                    {emp.idle_hours} hrs
                  </td>

                  <td className="px-6 py-4 text-center">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        emp.overtime_hours > 10
                          ? "bg-red-100 text-red-700"
                          : "bg-green-100 text-green-700"
                      }`}
                    >
                      {emp.overtime_hours} hrs
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {!loading && reportData.length === 0 && (
        <p className="text-center text-gray-500">
          No data found for selected month
        </p>
      )}
    </div>
  );
}
