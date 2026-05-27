import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Attendance from "./pages/Attendance";
import Shifts from "./pages/Shifts";
import Employees from "./pages/Employees";
import DashboardLayout from "./layout/DashboardLayout";
import Report from "./pages/Report";
import OvertimeApproval from "./pages/OvertimeApproval.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected / Dashboard Routes */}
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/attendance" element={<Attendance />} />
          <Route path="/shifts" element={<Shifts />} />
          <Route path="/employees" element={<Employees />} />
          <Route path="/report" element={<Report />} />
          <Route path="/overtime-approval" element={<OvertimeApproval />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
