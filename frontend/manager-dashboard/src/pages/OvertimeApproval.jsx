import { useEffect, useState } from "react";
import { getOvertime, approveOvertime } from "../api/overtimeApi";

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

      alert("Overtime approved successfully");
      fetchOvertime();
    } catch (error) {
      console.error(error);
      alert("Approval failed");
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Overtime Approval</h2>

      <div style={styles.tableWrapper}>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Employee</th>
              <th style={styles.th}>Date</th>
              <th style={styles.th}>Overtime (hrs)</th>
              <th style={styles.th}>Action</th>
            </tr>
          </thead>

          <tbody>
            {records.map((row) => (
              <tr key={`${row.employee_id}-${row.log_date}`}>
                <td style={styles.td}>{row.employee_name}</td>
                <td style={styles.td}>{row.log_date}</td>

                <td style={styles.td}>
                  <div style={styles.overtimeBox}>
                    {(row.over_time / 3600).toFixed(2)} hrs
                  </div>
                </td>

                <td style={styles.td}>
                  <select
                    style={styles.select}
                    defaultValue=""
                    onChange={(e) =>
                      handleApprovalChange(
                        row.employee_id,
                        row.log_date,
                        e.target.value
                      )
                    }
                  >
                    <option value="" disabled>
                      Select
                    </option>
                    <option value="approved">Approve</option>
                    <option value="rejected">Reject</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <button style={styles.button} onClick={submitApprovals}>
        Submit Approvals
      </button>
    </div>
  );
}

/* ================= STYLES ================= */

const styles = {
  container: {
    padding: "20px",
  },

  heading: {
    marginBottom: "16px",
  },

  tableWrapper: {
    overflowX: "auto",
    borderRadius: "8px",
    border: "1px solid #ddd",
  },

  table: {
    width: "100%",
    borderCollapse: "collapse",
  },

  th: {
    background: "#f5f5f5",
    padding: "10px",
    textAlign: "left",
    borderBottom: "1px solid #ddd",
  },

  td: {
    padding: "10px",
    borderBottom: "1px solid #eee",
  },

  overtimeBox: {
    background: "#ffe5e5",
    color: "#b30000",
    padding: "4px 10px",
    borderRadius: "6px",
    fontWeight: "600",
    display: "inline-block",
  },

  select: {
    padding: "6px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    cursor: "pointer",
  },

  button: {
    marginTop: "16px",
    padding: "10px 18px",
    backgroundColor: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
};
