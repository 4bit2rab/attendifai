// import { useEffect, useState } from "react";
// import { getAttendance } from "../api/attendanceApi";

// export default function Attendance() {
//   const [records, setRecords] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [date, setDate] = useState("2025-12-31");

//   useEffect(() => {
//     fetchAttendance();
//   }, [date]);

//   const fetchAttendance = async () => {
//     try {
//       setLoading(true);
//       const data = await getAttendance(date);
//       setRecords(data);
//     } catch (error) {
//       console.error("Failed to load attendance:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const formatTime = (minutes) => {
//     const hrs = Math.floor(minutes / 60);
//     const mins = minutes % 60;
//     return `${hrs}h ${mins}m`;
//   };

//   return (
//     <div>
//       <h2 className="text-xl font-bold mb-4">Daily Attendance</h2>

//       {/* Date Picker */}
//       <div className="mb-4">
//         <label className="mr-2 font-medium">Select Date:</label>
//         <input
//           type="date"
//           value={date}
//           onChange={(e) => setDate(e.target.value)}
//           className="border p-2 rounded"
//         />
//       </div>

//       {loading ? (
//         <p>Loading attendance...</p>
//       ) : (
//         <table className="w-full bg-white shadow rounded">
//           <thead className="bg-gray-100">
//             <tr>
//               <th className="p-3 text-left">Employee</th>
//               <th className="p-3 text-left">Date</th>
//               <th className="p-3 text-left">Productive</th>
//               <th className="p-3 text-left">Idle</th>
//               <th className="p-3 text-left">Overtime</th>
//             </tr>
//           </thead>

//           <tbody>
//             {records.map((row, index) => (
//               <tr key={index} className="border-t">
//                 <td className="p-3">{row.employee_name}</td>
//                 <td className="p-3">{row.log_date}</td>
//                 <td className="p-3">{formatTime(row.productive_time)}</td>
//                 <td className="p-3">{formatTime(row.idle_time)}</td>
//                 <td className="p-3">{formatTime(row.over_time)}</td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       )}
//     </div>
//   );
// }

import { useEffect, useState } from "react";
import { getAttendance } from "../api/attendanceApi";

export default function Attendance() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [date, setDate] = useState("2025-12-31"); // default date

  useEffect(() => {
    fetchAttendance();
  }, [date]);

  const fetchAttendance = async () => {
    try {
      setLoading(true);
      const data = await getAttendance(date);
      console.log("Fetched records:", data); // debug
      setRecords(data);
    } catch (error) {
      console.error("Failed to load attendance:", error);
    } finally {
      setLoading(false);
    }
  };
  const formatTime = (seconds) => {
    const totalMinutes = Math.floor(seconds / 60);
    const hrs = Math.floor(totalMinutes / 60);
    const mins = totalMinutes % 60;
    return `${hrs}h ${mins}m`;
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Daily Attendance</h2>

      {/* Date Picker */}
      <div className="mb-4">
        <label className="mr-2 font-medium">Select Date:</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="border p-2 rounded"
        />
      </div>

      {loading ? (
        <p>Loading attendance...</p>
      ) : (
        <table className="w-full bg-white shadow rounded">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3 text-left">Employee</th>
              <th className="p-3 text-left">Date</th>
              <th className="p-3 text-left">Productive</th>
              <th className="p-3 text-left">Idle</th>
              <th className="p-3 text-left">Overtime</th>
            </tr>
          </thead>

          <tbody>
            {records.length === 0 ? (
              <tr>
                <td colSpan="5" className="p-3 text-center">
                  No records found
                </td>
              </tr>
            ) : (
              records.map((row, index) => (
                <tr key={index} className="border-t">
                  <td className="p-3">{row.employee_name}</td>
                  <td className="p-3">{row.log_date}</td>
                  <td className="p-3">{formatTime(row.productive_time)}</td>
                  <td className="p-3">{formatTime(row.idle_time)}</td>
                  <td className="p-3">{formatTime(row.over_time)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
