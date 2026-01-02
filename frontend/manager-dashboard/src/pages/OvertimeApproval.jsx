import { useEffect, useState } from "react";
import { getOvertime, approveOvertime } from "../api/overtimeApi";
import { Check, X } from "lucide-react";

export default function OvertimeApproval() {
  const [records, setRecords] = useState([]);
  const [approvals, setApprovals] = useState({});

  useEffect(() => {
    fetchOvertime();
  }, []);

  const fetchOvertime = async () => {
    try {
      const data = await getOvertime();
      setRecords(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleApprovalChange = (employeeId, logDate, status) => {
    const key = `${employeeId}_${logDate}`;
    setApprovals((prev) => ({
      ...prev,
      [key]: {
        employee_id: employeeId,
        log_date: logDate,
        status,
      },
    }));
  };

  const submitApprovals = async () => {
    if (!Object.keys(approvals).length) {
      alert("No approvals selected");
      return;
    }

    try {
      await approveOvertime({
        approvals: Object.values(approvals),
      });
      alert("Overtime processed successfully");
      setApprovals({});
      fetchOvertime();
    } catch (error) {
      console.error(error);
      alert("Approval failed");
    }
  };

  return (
    <div className="p-6 relative">
      {/* Header (same as Employees page) */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-blue-600">
          Overtime Approval
        </h2>

        <button
          onClick={submitApprovals}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold"
        >
          Submit
        </button>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow border overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Employee</th>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Date</th>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Overtime</th>
                <th className="p-3 text-left text-gray-700 uppercase text-sm">Action</th>
              </tr>
            </thead>
            <tbody>
            {records.map((row) => {
              const key = `${row.employee_id}_${row.log_date}`;
              const selected = approvals[key]?.status;

              return (
                <tr
                  key={key}
                  className="border-t hover:bg-gray-50 transition"
                >
                  <td className="px-4 py-3 font-medium">
                    {row.employee_name}
                  </td>

                  <td className="px-4 py-3 text-gray-600">
                    {row.log_date}
                  </td>

                  <td className="px-4 py-3">
                    <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-xs font-semibold">
                      {(row.over_time / 3600).toFixed(2)} hrs
                    </span>
                  </td>

                  <td className="px-4 py-3 text-center space-x-3">
                    {/* Approve */}
                    <button
                      onClick={() =>
                        handleApprovalChange(
                          row.employee_id,
                          row.log_date,
                          "approved"
                        )
                      }
                      className={`w-9 h-9 rounded-full inline-flex items-center justify-center transition
                        ${
                          selected === "approved"
                            ? "bg-green-600 text-white"
                            : "bg-green-100 text-green-700 hover:bg-green-200"
                        }
                        ${selected === "rejected" && "opacity-40"}
                      `}
                    >
                      <Check size={18} />
                    </button>

                    {/* Reject */}
                    <button
                      onClick={() =>
                        handleApprovalChange(
                          row.employee_id,
                          row.log_date,
                          "rejected"
                        )
                      }
                      className={`w-9 h-9 rounded-full inline-flex items-center justify-center transition
                        ${
                          selected === "rejected"
                            ? "bg-red-600 text-white"
                            : "bg-red-100 text-red-700 hover:bg-red-200"
                        }
                        ${selected === "approved" && "opacity-40"}
                      `}
                    >
                      <X size={18} />
                    </button>
                  </td>
                </tr>
              );
            })}

            {!records.length && (
              <tr>
                <td
                  colSpan="4"
                  className="text-center py-6 text-gray-500"
                >
                  No overtime records found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
