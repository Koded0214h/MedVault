import React, { useState } from 'react';
import { FaSearch, FaMapMarkerAlt, FaHospital, FaFlask, FaMedkit, FaArrowRight, FaCheck, FaTimes, FaMap, FaClock, FaPhone } from 'react-icons/fa';

const MedicalResources = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedResource, setSelectedResource] = useState('all');

  const quickSearches = [
    { label: 'Insulin', icon: FaMedkit, color: 'bg-blue-100 text-blue-800' },
    { label: 'O- Blood', icon: FaMedkit, color: 'bg-red-100 text-red-800' },
    { label: 'Malaria Test', icon: FaFlask, color: 'bg-green-100 text-green-800' },
    { label: 'Antibiotics', icon: FaMedkit, color: 'bg-purple-100 text-purple-800' }
  ];

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">🗺️ What's In Stock? Real-Time Resource Tracker</h1>
        <p className="text-gray-600">Find critical medications, blood types, and medical supplies instantly. Powered by AI predictions.</p>

        {/* Search Bar */}
        <div className="relative mb-6 mt-4">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FaSearch className="text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Search for Insulin, O- Blood, Malaria Test, or any medical resource..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
          />
        </div>

        {/* Quick Search Buttons */}
        <div className="flex flex-wrap gap-2 mb-6">
          {quickSearches.map((item) => (
            <button
              key={item.label}
              onClick={() => setSearchQuery(item.label)}
              className={`flex items-center px-4 py-2 rounded-full text-sm font-medium ${item.color} hover:opacity-80 transition-opacity`}
            >
              <item.icon className="mr-2" />
              {item.label}
            </button>
          ))}
        </div>

        {/* Filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          {/* Resource Type */}
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">Resource Type</h3>
            <div className="space-y-2">
              {['Medicines', 'Lab Tests', 'Hospitals', 'Pharmacies'].map((type) => (
                <label key={type} className="flex items-center">
                  <input type="checkbox" className="rounded text-blue-600 mr-2" />
                  <span className="text-gray-600">{type}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Availability */}
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">Availability</h3>
            <div className="space-y-2">
              <label className="flex items-center">
                <input type="radio" name="availability" className="text-blue-600 mr-2" defaultChecked />
                <span className="text-gray-600">All</span>
              </label>
              <label className="flex items-center">
                <input type="radio" name="availability" className="text-blue-600 mr-2" />
                <span className="text-gray-600">Open Now</span>
              </label>
            </div>
          </div>

          {/* Distance */}
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">Distance</h3>
            <label className="flex items-center">
              <input type="radio" name="distance" className="text-blue-600 mr-2" defaultChecked />
              <span className="text-gray-600">Within 10 km</span>
            </label>
          </div>
        </div>

        <div className="border-t border-gray-200 my-6"></div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Sidebar - Locations */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="font-semibold text-blue-800 mb-2">FILTER</h3>
            <div className="space-y-1 text-sm text-blue-700">
              {['Gare oralation', 'Acemar Island', 'Golden Gate Bridge', "SHEERMAN'S WINNING", 'PACIFIC NEIGHTS', 'CHINA TOWN', 'UNION SOURCE'].map((location) => (
                <div key={location} className="py-1">{location}</div>
              ))}
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">San Francisco</h3>
            <div className="space-y-1 text-sm text-gray-600">
              {['BORROW', 'OUTER SUNSET', 'RUNSET DISTRICT', 'Lake Merced Park', 'El Man San Francisco'].map((location) => (
                <div key={location} className="py-1 flex justify-between items-center">
                  <span>{location}</span>
                  <span className={`text-xs px-2 py-1 rounded ${location.includes('Available') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {location.includes('Available') ? 'Available' : 'Unavailable'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">MISSION DISTRICT</h3>
            <div className="space-y-1 text-sm text-gray-600">
              {['Twin Peaks', 'Red Valley', 'HIGHLY HEIGHT', 'John McLan Park', 'Candestick Point State Recreation Area', 'San Bruno Mountain State'].map((location) => (
                <div key={location} className="py-1">{location}</div>
              ))}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-2">
          {/* Map Placeholder */}
          <div className="bg-gray-100 border-2 border-dashed border-gray-300 rounded-lg p-8 mb-6 text-center">
            <FaMap className="text-4xl text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-600 mb-2">Interactive Map View</h3>
            <p className="text-gray-500">Real-time resource locations will be displayed here. Map integration coming soon.</p>
          </div>

          {/* AI Prediction Alert */}
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-6">
            <div className="flex items-center mb-2">
              <FaClock className="text-orange-500 mr-2" />
              <span className="text-orange-700 font-semibold">AI Prediction Alert</span>
            </div>
            <p className="text-orange-700">
              Insulin shortage predicted in your district within 7 days. Confidence: 89%. Stock up now or find alternatives.
            </p>
          </div>

          {/* Search Result Info */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <p className="text-green-700 font-medium">
              ✅ Nearest available {searchQuery || 'O- Blood'} found 2.1km away at City Central Pharmacy.
            </p>
            <p className="text-green-600 text-sm mt-1">
              Last updated: 2 minutes ago • Real-time tracking active
            </p>
          </div>

          {/* Search Results */}
          <div className="space-y-4">
            {/* City Central Pharmacy */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-bold text-lg text-gray-800 flex items-center">
                    <FaMedkit className="text-blue-500 mr-2" />
                    City Central Pharmacy
                  </h3>
                  <p className="text-gray-600 text-sm">123 Health St. • 1.5km away • Open until 8PM</p>
                  <div className="flex items-center mt-1">
                    <FaPhone className="text-gray-400 mr-1 text-xs" />
                    <span className="text-gray-500 text-xs">+1 (555) 123-4567</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center text-green-600 text-sm mb-1">
                    <FaCheck className="mr-1" />
                    In Stock (12 units)
                  </div>
                  <div className="text-xs text-gray-500">Updated 5 min ago</div>
                </div>
              </div>
              <div className="flex space-x-2">
                <button className="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
                  <FaMapMarkerAlt className="mr-2" />
                  Navigate
                </button>
                <button className="flex items-center border border-blue-600 text-blue-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-50 transition-colors">
                  Reserve Now
                </button>
                <button className="flex items-center border border-gray-300 text-gray-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
                  Call
                </button>
              </div>
            </div>

            {/* Oak Valley Hospital */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-bold text-lg text-gray-800 flex items-center">
                    <FaHospital className="text-red-500 mr-2" />
                    Oak Valley Hospital
                  </h3>
                  <p className="text-gray-600 text-sm">456 Wellness Ave. • 2.8km away • Emergency Dept Open 24/7</p>
                  <div className="flex items-center mt-1">
                    <FaPhone className="text-gray-400 mr-1 text-xs" />
                    <span className="text-gray-500 text-xs">+1 (555) 987-6543</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center text-yellow-600 text-sm mb-1">
                    <FaClock className="mr-1" />
                    Limited Stock (3 units)
                  </div>
                  <div className="text-xs text-gray-500">Updated 12 min ago</div>
                </div>
              </div>
              <div className="flex space-x-2">
                <button className="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
                  <FaMapMarkerAlt className="mr-2" />
                  Navigate
                </button>
                <button className="flex items-center border border-blue-600 text-blue-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-50 transition-colors">
                  Details
                </button>
                <button className="flex items-center border border-gray-300 text-gray-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
                  Call
                </button>
              </div>
            </div>

            {/* Downtown Diagnostics Lab */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-bold text-lg text-gray-800 flex items-center">
                    <FaFlask className="text-green-500 mr-2" />
                    Downtown Diagnostics Lab
                  </h3>
                  <p className="text-gray-600 text-sm">789 Cure Blvd. • 4.1km away • Open until 6PM</p>
                  <div className="flex items-center mt-1">
                    <FaPhone className="text-gray-400 mr-1 text-xs" />
                    <span className="text-gray-500 text-xs">+1 (555) 456-7890</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center text-red-600 text-sm mb-1">
                    <FaTimes className="mr-1" />
                    Out of Stock
                  </div>
                  <div className="text-xs text-gray-500">Updated 1 hour ago</div>
                </div>
              </div>
              <div className="flex space-x-2">
                <button className="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
                  <FaMapMarkerAlt className="mr-2" />
                  Navigate
                </button>
                <button className="flex items-center border border-gray-300 text-gray-400 px-4 py-2 rounded-lg text-sm font-medium cursor-not-allowed">
                  Unavailable
                </button>
                <button className="flex items-center border border-gray-300 text-gray-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
                  Call
                </button>
              </div>
            </div>
          </div>

          {/* MCP Insights */}
          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-blue-800 mb-2">🧠 MCP AI Insights</h4>
            <div className="text-blue-700 text-sm space-y-1">
              <p>• Demand for {searchQuery || 'this resource'} is trending upward in your area</p>
              <p>• Alternative locations checked: 15 pharmacies, 8 hospitals, 5 labs</p>
              <p>• Next restock expected at City Central Pharmacy: Tomorrow 9AM</p>
            </div>
          </div>

          {/* Feedback */}
          <div className="mt-6 text-center text-gray-500 text-sm">
            <p>Share feedback or alert us if stock info seems outdated. Help us improve real-time accuracy!</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MedicalResources;