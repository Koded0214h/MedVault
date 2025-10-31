import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MedicalResourcesPage from './pages/MedicalResourcesPage';
import DashboardPage from './pages/DashboardPage';
import PatientDashboardPage from './pages/PatientDashboardPage';
import EmergencyAlertsPage from './pages/EmergencyAlertsPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import OTPVerificationPage from './pages/OTPVerificationPage';
import StoreBrowserPage from './pages/StoreBrowserPage';
import AIInsightsPage from './pages/AIInsightsPage';
import { AuthProvider } from './contexts/AuthContext';
import AuthContext from './contexts/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/verify-otp" element={<OTPVerificationPage />} />
            {/* Protected routes */}
            <Route path="/medical-resources" element={<ProtectedRoute><MedicalResourcesPage /></ProtectedRoute>} />
            <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
            <Route path="/patient-dashboard" element={<ProtectedRoute><PatientDashboardPage /></ProtectedRoute>} />
            <Route path="/emergency-alerts" element={<ProtectedRoute><EmergencyAlertsPage /></ProtectedRoute>} />
            <Route path="/store" element={<ProtectedRoute><StoreBrowserPage /></ProtectedRoute>} />
            <Route path="/ai-insights" element={<ProtectedRoute><AIInsightsPage /></ProtectedRoute>} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

const ProtectedRoute = ({children}) => {
  const { isAuthenticated } = React.useContext(AuthContext);
  return isAuthenticated ? children: <Navigate to="/login" />;
}
export default App;
