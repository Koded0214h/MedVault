import React from 'react';
import Header from '../components/Header';
import MedicalResources from '../components/MedicalResources';

const MedicalResourcesPage = () => {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <MedicalResources />
    </div>
  );
};

export default MedicalResourcesPage;
