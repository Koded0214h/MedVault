import React from 'react';
import Header from '../components/Header';
import Dashboard from '../components/Dashboard';

const DashboardPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Dashboard />
    </div>
  );
};

export default DashboardPage;
