import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Attendance from "./pages/Attendance";
import Shifts from "./pages/Shifts";
import Employees from "./pages/Employees";
import MonthlyReport from "./pages/MonthlyReport";
import DashboardLayout from "./layout/DashboardLayout";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public route */}
       
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Dashboard routes with layout */}
        
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/attendance" element={<Attendance />} />
          <Route path="/shifts" element={<Shifts />} />
          <Route path="/employees" element={<Employees />} />
          <Route path="/reports/monthly" element={<MonthlyReport />} /> {/* Monthly report */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
