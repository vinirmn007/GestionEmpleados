import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import { ThemeProvider } from './ThemeContext';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import EmployeeCreate from './pages/EmployeeCreate';
import PayrollList from './pages/PayrollList';
import PayrollCreate from './pages/PayrollCreate';
import PayrollDetail from './pages/PayrollDetail';
import Attendance from './pages/Attendance';
import Schedule from './pages/Schedule';
import Leaves from './pages/Leaves';
import Settings from './pages/Settings';

// Wrapper for pages that require the sidebar layout
const LayoutRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return <Layout>{children}</Layout>;
};

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route path="/" element={<LayoutRoute><Dashboard /></LayoutRoute>} />
          <Route path="/employees" element={<LayoutRoute><Dashboard /></LayoutRoute>} />
          <Route path="/employees/new" element={<LayoutRoute><EmployeeCreate /></LayoutRoute>} />
          
          <Route path="/payroll" element={<LayoutRoute><PayrollList /></LayoutRoute>} />
          <Route path="/payroll/create" element={<LayoutRoute><PayrollCreate /></LayoutRoute>} />
          <Route path="/payroll/detail" element={<LayoutRoute><PayrollDetail /></LayoutRoute>} />
          
          <Route path="/attendance" element={<LayoutRoute><Attendance /></LayoutRoute>} />
          <Route path="/schedule" element={<LayoutRoute><Schedule /></LayoutRoute>} />
          <Route path="/leaves" element={<LayoutRoute><Leaves /></LayoutRoute>} />
          <Route path="/reports" element={<LayoutRoute><div className="p-10 text-center text-slate-500">Reportes (Coming Soon)</div></LayoutRoute>} />
          <Route path="/settings" element={<LayoutRoute><Settings /></LayoutRoute>} />
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;