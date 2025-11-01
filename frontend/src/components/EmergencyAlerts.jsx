import React, { useState } from 'react';
import { FaExclamationTriangle, FaInfoCircle, FaExclamationCircle, FaMapMarkerAlt, FaArrowRight, FaBroadcastTower, FaUserMd, FaClock, FaCheckCircle } from 'react-icons/fa';

const EmergencyAlerts = () => {
  const [selectedRegion, setSelectedRegion] = useState('all');
  const [selectedProfile, setSelectedProfile] = useState('all');

  const alerts = [
    {
      severity: 'critical',
      title: 'Cholera outbreak in Region B',
      description: 'An active cholera outbreak has been confirmed. Residents are advised to boil drinking water and maintain strict hygiene.',
      time: 'Updated 5 mins ago',
      icon: FaExclamationTriangle,
      color: 'red',
      region: 'Region B',
      profile: 'general',
      deliveryStatus: 'Broadcasting to 15,000 users'
    },
    {
      severity: 'warning',
      title: 'High Pollen Count Advisory',
      description: 'Air quality index has reached unhealthy levels for sensitive groups. Limit outdoor activities.',
      time: 'Updated 2 hours ago',
      icon: FaExclamationCircle,
      color: 'orange',
      region: 'Region A',
      profile: 'respiratory',
      deliveryStatus: 'Delivered to 8,500 users'
    },
    {
      severity: 'info',
      title: 'Free Flu Shot Clinic Opening',
      description: 'A new temporary clinic is offering free influenza vaccinations at the community center from 9 AM to 5 PM.',
      time: 'Updated yesterday',
      icon: FaInfoCircle,
      color: 'blue',
      region: 'Region C',
      profile: 'general',
      deliveryStatus: 'Delivered to 12,200 users'
    }
  ];

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 border-red-300 text-red-800';
      case 'warning': return 'bg-orange-100 border-orange-300 text-orange-800';
      case 'info': return 'bg-blue-100 border-blue-300 text-blue-800';
      default: return 'bg-gray-100 border-gray-300 text-gray-800';
    }
  };

  const getIconColor = (severity) => {
    switch (severity) {
      case 'critical': return 'text-red-500';
      case 'warning': return 'text-orange-500';
      case 'info': return 'text-blue-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">📢 Hyper-Local Emergency Alerts</h1>
        <p className="text-gray-600">AI-powered "Break Glass" emergency communication system for critical health situations.</p>
      </div>

      {/* Geographic Targeting & Profile Filters */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6 p-4 bg-gray-50 rounded-lg">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
            <FaMapMarkerAlt className="mr-2 text-blue-500" />
            Geographic Targeting (District Level)
          </label>
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Regions</option>
            <option value="region-a">Region A (Downtown)</option>
            <option value="region-b">Region B (Suburban)</option>
            <option value="region-c">Region C (Rural)</option>
            <option value="district-1">District 1 (High Risk)</option>
            <option value="district-2">District 2 (Medium Risk)</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
            <FaUserMd className="mr-2 text-green-500" />
            Medical Profile Targeting
          </label>
          <select
            value={selectedProfile}
            onChange={(e) => setSelectedProfile(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-green-500"
          >
            <option value="all">All Profiles</option>
            <option value="diabetes">Diabetes Patients</option>
            <option value="respiratory">Respiratory Conditions</option>
            <option value="cardiac">Cardiac Patients</option>
            <option value="pregnant">Pregnant Women</option>
            <option value="elderly">Elderly (65+)</option>
            <option value="children">Children (0-12)</option>
          </select>
        </div>
      </div>

      {/* Emergency Broadcast Panel */}
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center">
            <FaBroadcastTower className="text-red-500 mr-2" />
            <span className="font-semibold text-red-800">Emergency Broadcast System</span>
          </div>
          <button className="bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">
            🚨 Break Glass - Broadcast Now
          </button>
        </div>
        <p className="text-red-700 text-sm">
          Send immediate alerts to targeted medical profiles in selected geographic areas. Use only for critical situations.
        </p>
      </div>

      <div className="border-t border-gray-200 my-6"></div>

      {/* Alerts with Real-time Delivery Status */}
      <div className="space-y-4 mb-8">
        {alerts.map((alert, index) => (
          <div key={index} className={`border-l-4 ${getSeverityColor(alert.severity)} rounded-r-lg p-4 hover:shadow-md transition-shadow`}>
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center">
                <alert.icon className={`mr-2 ${getIconColor(alert.severity)}`} />
                <span className="font-semibold capitalize">{alert.severity}</span>
                <span className="ml-2 text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded">
                  {alert.region}
                </span>
              </div>
              <div className="text-right">
                <span className="text-sm text-gray-500 block">{alert.time}</span>
                <div className="flex items-center text-xs text-gray-500 mt-1">
                  <FaCheckCircle className="text-green-500 mr-1" />
                  {alert.deliveryStatus}
                </div>
              </div>
            </div>
            <h3 className="font-bold text-lg text-gray-800 mb-2">{alert.title}</h3>
            <p className="text-gray-600 mb-3">{alert.description}</p>
            <div className="flex items-center justify-between">
              <button className="flex items-center text-blue-600 hover:text-blue-800 font-medium">
                <FaMapMarkerAlt className="mr-2" />
                Find Nearest Help Center
                <FaArrowRight className="ml-2" />
              </button>
              <div className="flex items-center text-xs text-gray-500">
                <FaClock className="mr-1" />
                Real-time tracking active
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* MCP Integration Status */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-bold text-lg text-blue-800 mb-4 flex items-center">
          <FaBroadcastTower className="mr-2" />
          MCP Integration Status
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">15,000</div>
            <div className="text-sm text-blue-700">Users Targeted</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">98.7%</div>
            <div className="text-sm text-green-700">Delivery Rate</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">2.1min</div>
            <div className="text-sm text-orange-700">Avg Response Time</div>
          </div>
        </div>
        <div className="space-y-3 text-blue-700">
          <div className="flex items-start">
            <div className="bg-blue-100 rounded-full p-1 mr-3 mt-1">
              <FaExclamationTriangle className="text-blue-600 text-sm" />
            </div>
            <span><strong>1 Critical Alert</strong> active in Region B. Cholera outbreak confirmed.</span>
          </div>
          <div className="flex items-start">
            <div className="bg-blue-100 rounded-full p-1 mr-3 mt-1">
              <FaMapMarkerAlt className="text-blue-600 text-sm" />
            </div>
            <span><strong>Nearest clinic finder:</strong> Integrated with MCP for real-time capacity updates.</span>
          </div>
          <div className="flex items-start">
            <div className="bg-blue-100 rounded-full p-1 mr-3 mt-1">
              <FaInfoCircle className="text-blue-600 text-sm" />
            </div>
            <span><strong>AI Recommendation:</strong> Target diabetes patients in high-risk districts for insulin alerts.</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmergencyAlerts;