import React from 'react';
import Header from '../components/Header';
import EmergencyAlerts from '../components/EmergencyAlerts';

const EmergencyAlertsPage = () => {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <EmergencyAlerts />
    </div>
  );
};

export default EmergencyAlertsPage;
