// import { useEffect, useState } from "react";
// import { getMonthlyReport } from "../api/reportApi";
// import { motion, AnimatePresence } from "framer-motion";

// // Helper to format seconds → "xh ym"
// const formatTime = (seconds) => {
//   const totalMinutes = Math.floor(seconds / 60);
//   const hrs = Math.floor(totalMinutes / 60);
//   const mins = totalMinutes % 60;
//   return `${hrs}h ${mins}m`;
// };

// // Get total days in a month
// const getDaysInMonth = (year, month) => {
//   return new Date(year, month, 0).getDate();
// };

// // Get day of week for a date string (0=Sun, 6=Sat)
// const getDayOfWeek = (dateStr) => {
//   return new Date(dateStr).getDay();
// };

// export default function Report() {
//   const today = new Date();
//   const [selectedYear, setSelectedYear] = useState(today.getFullYear());
//   const [selectedMonth, setSelectedMonth] = useState(today.getMonth() + 1);
//   const [reportData, setReportData] = useState([]);
//   const [loading, setLoading] = useState(true);

//   const fetchReport = async () => {
//     setLoading(true);
//     try {
//       const data = await getMonthlyReport(selectedYear, selectedMonth);
//       setReportData(data);
//     } catch (err) {
//       console.error(err);
//       setReportData([]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     fetchReport();
//   }, [selectedYear, selectedMonth]);

//   const totalDays = getDaysInMonth(selectedYear, selectedMonth);

//   // Organize data by employee
//   const employees = [...new Set(reportData.map((r) => r.employee_name))];
//   const employeeMap = {};
//   employees.forEach((emp) => {
//     employeeMap[emp] = {};
//   });

//   reportData.forEach((record) => {
//     employeeMap[record.employee_name][record.log_date] = record;
//   });

//   return (
//     <div className="p-6 space-y-6">
//       <h2 className="text-2xl font-bold text-blue-600">Monthly Report</h2>

//       {/* Year & Month selector */}
//       <div className="flex gap-4 items-center">
//         <label>Year:</label>
//         <input
//           type="number"
//           min="2000"
//           max="2100"
//           value={selectedYear}
//           onChange={(e) => setSelectedYear(parseInt(e.target.value))}
//           className="border p-1 rounded"
//         />
//         <label>Month:</label>
//         <input
//           type="number"
//           min="1"
//           max="12"
//           value={selectedMonth}
//           onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
//           className="border p-1 rounded"
//         />
//         <button
//           onClick={fetchReport}
//           className="bg-blue-600 text-white px-3 py-1 rounded"
//         >
//           Load
//         </button>
//       </div>

//       {loading ? (
//         <p className="text-gray-500 mt-4">Loading report...</p>
//       ) : (
//         <div className="overflow-x-auto">
//           <table className="border-collapse border border-gray-200 min-w-max">
//             <thead>
//               <tr>
//                 <th className="border p-2 bg-gray-100">Employee</th>
//                 {Array.from({ length: totalDays }, (_, i) => {
//                   const date = new Date(selectedYear, selectedMonth - 1, i + 1);
//                   const dayOfWeek = date.getDay();
//                   return (
//                     <th
//                       key={i}
//                       className={`border p-2 text-sm ${
//                         dayOfWeek === 0
//                           ? "bg-red-100" // Sunday
//                           : dayOfWeek === 6
//                           ? "bg-yellow-100" // Saturday
//                           : "bg-gray-50"
//                       }`}
//                       title={date.toDateString()}
//                     >
//                       {i + 1}
//                     </th>
//                   );
//                 })}
//               </tr>
//             </thead>
//             <tbody>
//               <AnimatePresence>
//                 {employees.map((emp, idx) => (
//                   <motion.tr
//                     key={emp}
//                     initial={{ opacity: 0, y: -10 }}
//                     animate={{ opacity: 1, y: 0 }}
//                     exit={{ opacity: 0, y: 10 }}
//                     className="hover:bg-blue-50 transition"
//                   >
//                     <td className="border p-2 font-medium bg-gray-100">{emp}</td>
//                     {Array.from({ length: totalDays }, (_, i) => {
//                       const dateStr = `${selectedYear}-${String(
//                         selectedMonth
//                       ).padStart(2, "0")}-${String(i + 1).padStart(2, "0")}`;
//                       const record = employeeMap[emp][dateStr];

//                       if (!record) {
//                         return (
//                           <td
//                             key={i}
//                             className="border p-1 bg-gray-50"
//                             title="No data"
//                           ></td>
//                         );
//                       }

//                       const totalShift = record.productive_time + record.idle_time;
//                       const productivePercent = totalShift
//                         ? (record.productive_time / totalShift) * 100
//                         : 0;
//                       const idlePercent = totalShift
//                         ? (record.idle_time / totalShift) * 100
//                         : 0;

//                       return (
//                         <td key={i} className="border p-1">
//                           <div
//                             className="w-full h-6 relative rounded"
//                             title={`Productive: ${formatTime(
//                               record.productive_time
//                             )}, Idle: ${formatTime(
//                               record.idle_time
//                             )}, Overtime: ${formatTime(record.over_time)}`}
//                           >
//                             <div
//                               className="absolute left-0 top-0 h-full bg-green-500 rounded-l"
//                               style={{ width: `${productivePercent}%` }}
//                             />
//                             <div
//                               className="absolute left-0 top-0 h-full bg-orange-400"
//                               style={{ width: `${idlePercent}%`, marginLeft: `${productivePercent}%` }}
//                             />
//                           </div>
//                         </td>
//                       );
//                     })}
//                   </motion.tr>
//                 ))}
//               </AnimatePresence>
//             </tbody>
//           </table>
//         </div>
//       )}

//       {/* Legend */}
//       <div className="flex gap-4 mt-4">
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-green-500 rounded"></div>
//           <span>Productive</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-orange-400 rounded"></div>
//           <span>Idle</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-red-100 rounded"></div>
//           <span>Saturday</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-yellow-100 rounded"></div>
//           <span>Sunday</span>
//         </div>
//       </div>
//     </div>
//   );
// }


// import { useEffect, useState } from "react";
// import { getMonthlyReport } from "../api/reportApi";
// import { motion, AnimatePresence } from "framer-motion";

// // Helper to format seconds → "xh ym"
// const formatTime = (seconds) => {
//   const totalMinutes = Math.floor(seconds / 60);
//   const hrs = Math.floor(totalMinutes / 60);
//   const mins = totalMinutes % 60;
//   return `${hrs}h ${mins}m`;
// };

// // Get total days in a month
// const getDaysInMonth = (year, month) => {
//   return new Date(year, month, 0).getDate();
// };

// export default function Report() {
//   const today = new Date();
//   const [selectedYear, setSelectedYear] = useState(today.getFullYear());
//   const [selectedMonth, setSelectedMonth] = useState(today.getMonth() + 1);
//   const [reportData, setReportData] = useState([]);
//   const [loading, setLoading] = useState(true);

//   const fetchReport = async () => {
//     setLoading(true);
//     try {
//       const data = await getMonthlyReport(selectedYear, selectedMonth);
//       setReportData(data);
//     } catch (err) {
//       console.error(err);
//       setReportData([]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     fetchReport();
//   }, [selectedYear, selectedMonth]);

//   const totalDays = getDaysInMonth(selectedYear, selectedMonth);

//   // Organize data by employee
//   const employees = [...new Set(reportData.map((r) => r.employee_name))];
//   const employeeMap = {};
//   employees.forEach((emp) => {
//     employeeMap[emp] = {};
//   });
//   reportData.forEach((record) => {
//     employeeMap[record.employee_name][record.log_date] = record;
//   });

//   return (
//     <div className="p-6 space-y-6">
//       <h2 className="text-2xl font-bold text-blue-600">Monthly Report</h2>

//       {/* Year & Month selector */}
//       <div className="flex gap-4 items-center mb-4">
//         <label>Year:</label>
//         <input
//           type="number"
//           min="2000"
//           max="2100"
//           value={selectedYear}
//           onChange={(e) => setSelectedYear(parseInt(e.target.value))}
//           className="border p-1 rounded"
//         />
//         <label>Month:</label>
//         <input
//           type="number"
//           min="1"
//           max="12"
//           value={selectedMonth}
//           onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
//           className="border p-1 rounded"
//         />
//         <button
//           onClick={fetchReport}
//           className="bg-blue-600 text-white px-3 py-1 rounded"
//         >
//           Load
//         </button>
//       </div>

//       {loading ? (
//         <p className="text-gray-500">Loading report...</p>
//       ) : (
//         <div className="overflow-x-auto border rounded-lg">
//           <table className="border-collapse border border-gray-200 min-w-max">
//             <thead>
//               <tr>
//                 <th className="border p-2 bg-gray-100 sticky left-0 z-10">Employee</th>
//                 {Array.from({ length: totalDays }, (_, i) => {
//                   const date = new Date(selectedYear, selectedMonth - 1, i + 1);
//                   const dayOfWeek = date.getDay();
//                   return (
//                     <th
//                       key={i}
//                       className={`border p-2 text-sm ${
//                         dayOfWeek === 0
//                           ? "bg-red-100"
//                           : dayOfWeek === 6
//                           ? "bg-yellow-100"
//                           : "bg-gray-50"
//                       } w-16`}
//                       title={date.toDateString()}
//                     >
//                       {i + 1}
//                     </th>
//                   );
//                 })}
//               </tr>
//             </thead>
//             <tbody>
//               <AnimatePresence>
//                 {employees.map((emp) => (
//                   <motion.tr
//                     key={emp}
//                     initial={{ opacity: 0, y: -10 }}
//                     animate={{ opacity: 1, y: 0 }}
//                     exit={{ opacity: 0, y: 10 }}
//                     className="hover:bg-blue-50 transition"
//                   >
//                     <td className="border p-2 font-medium bg-gray-100 sticky left-0 z-10">
//                       {emp}
//                     </td>
//                     {Array.from({ length: totalDays }, (_, i) => {
//                       const dateStr = `${selectedYear}-${String(
//                         selectedMonth
//                       ).padStart(2, "0")}-${String(i + 1).padStart(2, "0")}`;
//                       const record = employeeMap[emp][dateStr];

//                       if (!record) {
//                         return (
//                           <td
//                             key={i}
//                             className="border p-1 bg-gray-50"
//                             title="No data"
//                           ></td>
//                         );
//                       }

//                       const totalShift = record.productive_time + record.idle_time + record.over_time;
//                       const productivePercent = totalShift
//                         ? (record.productive_time / totalShift) * 100
//                         : 0;
//                       const idlePercent = totalShift
//                         ? (record.idle_time / totalShift) * 100
//                         : 0;
//                       const overtimePercent = totalShift
//                         ? (record.over_time / totalShift) * 100
//                         : 0;

//                       return (
//                         <td key={i} className="border p-1">
//                           <div
//                             className="w-full h-10 relative rounded"
//                             title={`Productive: ${formatTime(
//                               record.productive_time
//                             )}, Idle: ${formatTime(
//                               record.idle_time
//                             )}, Overtime: ${formatTime(record.over_time)}`}
//                           >
//                             {/* Productive */}
//                             <div
//                               className="absolute left-0 top-0 h-full bg-green-500 rounded-l"
//                               style={{ width: `${productivePercent}%` }}
//                             />
//                             {/* Idle */}
//                             <div
//                               className="absolute left-0 top-0 h-full bg-orange-400"
//                               style={{
//                                 width: `${idlePercent}%`,
//                                 marginLeft: `${productivePercent}%`,
//                               }}
//                             />
//                             {/* Overtime */}
//                             <div
//                               className="absolute left-0 top-0 h-full bg-red-500 rounded-r"
//                               style={{
//                                 width: `${overtimePercent}%`,
//                                 marginLeft: `${productivePercent + idlePercent}%`,
//                               }}
//                             />
//                           </div>
//                         </td>
//                       );
//                     })}
//                   </motion.tr>
//                 ))}
//               </AnimatePresence>
//             </tbody>
//           </table>
//         </div>
//       )}

//       {/* Legend */}
//       <div className="flex gap-4 mt-4">
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-green-500 rounded"></div>
//           <span>Productive</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-orange-400 rounded"></div>
//           <span>Idle</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-red-500 rounded"></div>
//           <span>Overtime</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-red-100 rounded"></div>
//           <span>Saturday</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-yellow-100 rounded"></div>
//           <span>Sunday</span>
//         </div>
//       </div>
//     </div>
//   );
// }

// import { useEffect, useState } from "react";
// import { getMonthlyReport } from "../api/reportApi";
// import { motion, AnimatePresence } from "framer-motion";

// // Helper to format seconds → "xh ym"
// const formatTime = (seconds) => {
//   const totalMinutes = Math.floor(seconds / 60);
//   const hrs = Math.floor(totalMinutes / 60);
//   const mins = totalMinutes % 60;
//   return `${hrs}h ${mins}m`;
// };

// // Get total days in a month
// const getDaysInMonth = (year, month) => {
//   return new Date(year, month, 0).getDate();
// };

// export default function Report() {
//   const today = new Date();
//   const [selectedYear, setSelectedYear] = useState(today.getFullYear());
//   const [selectedMonth, setSelectedMonth] = useState(today.getMonth() + 1);
//   const [reportData, setReportData] = useState([]);
//   const [loading, setLoading] = useState(true);

//   const fetchReport = async () => {
//     setLoading(true);
//     try {
//       const data = await getMonthlyReport(selectedYear, selectedMonth);
//       setReportData(data);
//     } catch (err) {
//       console.error(err);
//       setReportData([]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     fetchReport();
//   }, [selectedYear, selectedMonth]);

//   const totalDays = getDaysInMonth(selectedYear, selectedMonth);

//   // Organize data by employee
//   const employees = [...new Set(reportData.map((r) => r.employee_name))];
//   const employeeMap = {};
//   employees.forEach((emp) => {
//     employeeMap[emp] = {};
//   });
//   reportData.forEach((record) => {
//     employeeMap[record.employee_name][record.log_date] = record;
//   });

//   return (
//     <div className="p-6 space-y-6">
//       <h2 className="text-2xl font-bold text-blue-600">Monthly Report</h2>

//       {/* Year & Month selector */}
//       <div className="flex gap-4 items-center mb-4">
//         <label>Year:</label>
//         <input
//           type="number"
//           min="2000"
//           max="2100"
//           value={selectedYear}
//           onChange={(e) => setSelectedYear(parseInt(e.target.value))}
//           className="border p-1 rounded"
//         />
//         <label>Month:</label>
//         <input
//           type="number"
//           min="1"
//           max="12"
//           value={selectedMonth}
//           onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
//           className="border p-1 rounded"
//         />
//         <button
//           onClick={fetchReport}
//           className="bg-blue-600 text-white px-3 py-1 rounded"
//         >
//           Load
//         </button>
//       </div>

//       {loading ? (
//         <p className="text-gray-500">Loading report...</p>
//       ) : (
//         <div className="flex border rounded-lg overflow-hidden">
//           {/* Fixed employee names */}
//           <div className="flex-shrink-0 bg-gray-100">
//             <table className="border-collapse border border-gray-200 min-w-max">
//               <thead>
//                 <tr>
//                   <th className="border p-2 bg-gray-100 sticky top-0 z-10">
//                     Employee
//                   </th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {employees.map((emp) => (
//                   <tr key={emp} className="hover:bg-blue-50 transition">
//                     <td className="border p-2 font-medium">{emp}</td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           </div>

//           {/* Scrollable dates */}
//           <div className="overflow-x-auto">
//             <table className="border-collapse border border-gray-200 min-w-max">
//               <thead>
//                 <tr>
//                   {Array.from({ length: totalDays }, (_, i) => {
//                     const date = new Date(selectedYear, selectedMonth - 1, i + 1);
//                     const dayOfWeek = date.getDay();
//                     return (
//                       <th
//                         key={i}
//                         className={`border p-2 text-sm ${
//                           dayOfWeek === 0
//                             ? "bg-red-100"
//                             : dayOfWeek === 6
//                             ? "bg-yellow-100"
//                             : "bg-gray-50"
//                         } w-16 sticky top-0 z-5`}
//                         title={date.toDateString()}
//                       >
//                         {i + 1}
//                       </th>
//                     );
//                   })}
//                 </tr>
//               </thead>
//               <tbody>
//                 <AnimatePresence>
//                   {employees.map((emp, empIdx) => (
//                     <motion.tr
//                       key={emp}
//                       initial={{ opacity: 0, y: -10 }}
//                       animate={{ opacity: 1, y: 0 }}
//                       exit={{ opacity: 0, y: 10 }}
//                     >
//                       {Array.from({ length: totalDays }, (_, i) => {
//                         const dateStr = `${selectedYear}-${String(
//                           selectedMonth
//                         ).padStart(2, "0")}-${String(i + 1).padStart(2, "0")}`;
//                         const record = employeeMap[emp][dateStr];

//                         if (!record) {
//                           return (
//                             <td
//                               key={i}
//                               className="border p-1 bg-gray-50 w-16 h-10"
//                               title="No data"
//                             ></td>
//                           );
//                         }

//                         const totalShift =
//                           record.productive_time +
//                           record.idle_time +
//                           record.over_time;
//                         const productivePercent = totalShift
//                           ? (record.productive_time / totalShift) * 100
//                           : 0;
//                         const idlePercent = totalShift
//                           ? (record.idle_time / totalShift) * 100
//                           : 0;
//                         const overtimePercent = totalShift
//                           ? (record.over_time / totalShift) * 100
//                           : 0;

//                         return (
//                           <td key={i} className="border p-1 w-16 h-10">
//                             <div
//                               className="w-full h-full relative rounded"
//                               title={`Productive: ${formatTime(
//                                 record.productive_time
//                               )}, Idle: ${formatTime(
//                                 record.idle_time
//                               )}, Overtime: ${formatTime(record.over_time)}`}
//                             >
//                               {/* Productive */}
//                               <div
//                                 className="absolute left-0 top-0 h-full bg-green-500 rounded-l"
//                                 style={{ width: `${productivePercent}%` }}
//                               />
//                               {/* Idle */}
//                               <div
//                                 className="absolute left-0 top-0 h-full bg-orange-400"
//                                 style={{
//                                   width: `${idlePercent}%`,
//                                   marginLeft: `${productivePercent}%`,
//                                 }}
//                               />
//                               {/* Overtime */}
//                               <div
//                                 className="absolute left-0 top-0 h-full bg-red-500 rounded-r"
//                                 style={{
//                                   width: `${overtimePercent}%`,
//                                   marginLeft: `${
//                                     productivePercent + idlePercent
//                                   }%`,
//                                 }}
//                               />
//                             </div>
//                           </td>
//                         );
//                       })}
//                     </motion.tr>
//                   ))}
//                 </AnimatePresence>
//               </tbody>
//             </table>
//           </div>
//         </div>
//       )}

//       {/* Legend */}
//       <div className="flex gap-4 mt-4 flex-wrap">
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-green-500 rounded"></div>
//           <span>Productive</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-orange-400 rounded"></div>
//           <span>Idle</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-red-500 rounded"></div>
//           <span>Overtime</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-red-100 rounded"></div>
//           <span>Saturday</span>
//         </div>
//         <div className="flex items-center gap-2">
//           <div className="w-6 h-6 bg-yellow-100 rounded"></div>
//           <span>Sunday</span>
//         </div>
//       </div>
//     </div>
//   );
// }



















import { useEffect, useState } from "react";
import { getMonthlyReport } from "../api/reportApi";
import { motion, AnimatePresence } from "framer-motion";

// Helper to format seconds → "xh ym"
const formatTime = (seconds) => {
  const totalMinutes = Math.floor(seconds / 60);
  const hrs = Math.floor(totalMinutes / 60);
  const mins = totalMinutes % 60;
  return `${hrs}h ${mins}m`;
};

// Get total days in a month
const getDaysInMonth = (year, month) => {
  return new Date(year, month, 0).getDate();
};

export default function Report() {
  const today = new Date();
  const [selectedYear, setSelectedYear] = useState(today.getFullYear());
  const [selectedMonth, setSelectedMonth] = useState(today.getMonth() + 1);
  const [reportData, setReportData] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchReport = async () => {
    setLoading(true);
    try {
      const data = await getMonthlyReport(selectedYear, selectedMonth);
      setReportData(data);
    } catch (err) {
      console.error(err);
      setReportData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport();
  }, [selectedYear, selectedMonth]);

  const totalDays = getDaysInMonth(selectedYear, selectedMonth);

  // Organize data by employee
  const employees = [...new Set(reportData.map((r) => r.employee_name))];
  const employeeMap = {};
  employees.forEach((emp) => {
    employeeMap[emp] = {};
  });
  reportData.forEach((record) => {
    employeeMap[record.employee_name][record.log_date] = record;
  });

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold text-blue-600">Monthly Report</h2>

      {/* Year & Month selector */}
      <div className="flex gap-4 items-center mb-4">
        <label>Year:</label>
        <input
          type="number"
          min="2000"
          max="2100"
          value={selectedYear}
          onChange={(e) => setSelectedYear(parseInt(e.target.value))}
          className="border p-1 rounded"
        />
        <label>Month:</label>
        <input
          type="number"
          min="1"
          max="12"
          value={selectedMonth}
          onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
          className="border p-1 rounded"
        />
        <button
          onClick={fetchReport}
          className="bg-blue-600 text-white px-3 py-1 rounded"
        >
          Load
        </button>
      </div>

      {loading ? (
        <p className="text-gray-500">Loading report...</p>
      ) : (
        <div
          className="flex border rounded-lg overflow-hidden"
          style={{ height: "400px" }} // Fixed container height
        >
          {/* Fixed employee names column */}
          <div
            className="flex-shrink-0 bg-gray-100 overflow-y-auto"
            style={{ maxHeight: "400px" }}
          >
            <table className="border-collapse border border-gray-200 min-w-max">
              <thead>
                <tr>
                  <th className="border p-2 bg-gray-100 sticky top-0 z-10">
                    Employee
                  </th>
                </tr>
              </thead>
              <tbody>
                {employees.map((emp) => (
                  <tr key={emp} className="hover:bg-blue-50 transition">
                    <td className="border p-2 font-medium">{emp}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Scrollable dates */}
          <div
            className="overflow-x-auto overflow-y-auto"
            style={{ maxHeight: "400px" }}
          >
            <table className="border-collapse border border-gray-200 min-w-max">
              <thead>
                <tr>
                  {Array.from({ length: totalDays }, (_, i) => {
                    const date = new Date(selectedYear, selectedMonth - 1, i + 1);
                    const dayOfWeek = date.getDay();
                    return (
                      <th
                        key={i}
                        className={`border p-2 text-sm ${
                          dayOfWeek === 0
                            ? "bg-red-100"
                            : dayOfWeek === 6
                            ? "bg-yellow-100"
                            : "bg-gray-50"
                        } w-16 sticky top-0 z-5`}
                        title={date.toDateString()}
                      >
                        {i + 1}
                      </th>
                    );
                  })}
                </tr>
              </thead>
              <tbody>
                <AnimatePresence>
                  {employees.map((emp) => (
                    <motion.tr
                      key={emp}
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                    >
                      {Array.from({ length: totalDays }, (_, i) => {
                        const dateStr = `${selectedYear}-${String(
                          selectedMonth
                        ).padStart(2, "0")}-${String(i + 1).padStart(2, "0")}`;
                        const record = employeeMap[emp][dateStr];

                        if (!record) {
                          return (
                            <td
                              key={i}
                              className="border p-1 bg-gray-50 w-16 h-10"
                              title="No data"
                            ></td>
                          );
                        }

                        const totalShift =
                          record.productive_time +
                          record.idle_time +
                          record.over_time;
                        const productivePercent = totalShift
                          ? (record.productive_time / totalShift) * 100
                          : 0;
                        const idlePercent = totalShift
                          ? (record.idle_time / totalShift) * 100
                          : 0;
                        const overtimePercent = totalShift
                          ? (record.over_time / totalShift) * 100
                          : 0;

                        return (
                          <td key={i} className="border p-1 w-16 h-10">
                            <div
                              className="w-full h-full relative rounded"
                              title={`Productive: ${formatTime(
                                record.productive_time
                              )}, Idle: ${formatTime(
                                record.idle_time
                              )}, Overtime: ${formatTime(record.over_time)}`}
                            >
                              {/* Productive */}
                              <div
                                className="absolute left-0 top-0 h-full bg-green-500 rounded-l"
                                style={{ width: `${productivePercent}%` }}
                              />
                              {/* Idle */}
                              <div
                                className="absolute left-0 top-0 h-full bg-orange-400"
                                style={{
                                  width: `${idlePercent}%`,
                                  marginLeft: `${productivePercent}%`,
                                }}
                              />
                              {/* Overtime */}
                              <div
                                className="absolute left-0 top-0 h-full bg-red-500 rounded-r"
                                style={{
                                  width: `${overtimePercent}%`,
                                  marginLeft: `${
                                    productivePercent + idlePercent
                                  }%`,
                                }}
                              />
                            </div>
                          </td>
                        );
                      })}
                    </motion.tr>
                  ))}
                </AnimatePresence>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Legend */}
      <div className="flex gap-4 mt-4 flex-wrap">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-green-500 rounded"></div>
          <span>Productive</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-orange-400 rounded"></div>
          <span>Idle</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-red-500 rounded"></div>
          <span>Overtime</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-red-100 rounded"></div>
          <span>Saturday</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-yellow-100 rounded"></div>
          <span>Sunday</span>
        </div>
      </div>
    </div>
  );
}
