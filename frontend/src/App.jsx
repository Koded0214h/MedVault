import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MedicalResourcesPage from './pages/MedicalResourcesPage';
import DashboardPage from './pages/DashboardPage';
import EmergencyAlertsPage from './pages/EmergencyAlertsPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import OTPVerificationPage from './pages/OTPVerificationPage';
import StoreBrowserPage from './pages/StoreBrowserPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/verify-otp" element={<OTPVerificationPage />} />
          <Route path="/medical-resources" element={<MedicalResourcesPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/emergency-alerts" element={<EmergencyAlertsPage />} />
          <Route path="/store" element={<StoreBrowserPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;