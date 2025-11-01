import React from 'react';
import Header from '../components/Header';
import PatientDashboard from '../components/PatientDashboard';

const PatientDashboardPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <PatientDashboard />
    </div>
  );
};

export default PatientDashboardPage;
