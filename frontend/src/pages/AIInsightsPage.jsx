import React, { useState, useEffect } from 'react';
import { FaRobot, FaCalendarAlt, FaExclamationTriangle, FaMapMarkerAlt, FaChartLine, FaClock, FaArrowUp, FaArrowDown } from 'react-icons/fa';
import Header from '../components/Header';

const AIInsightsPage = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('7d');
  const [assistantMessage, setAssistantMessage] = useState('');

  const periods = [
    { value: '7d', label: 'Last 7 Days' },
    { value: '30d', label: 'Last 30 Days' },
    { value: '90d', label: 'Last 90 Days' }
  ];

  const shortagePredictions = [
    {
      category: 'Vaccines',
      severity: 'critical',
      predictedShortage: '14 days',
      affectedRegions: 8,
      confidence: 92,
      trend: 'increasing'
    },
    {
      category: 'Blood Types',
      severity: 'warning',
      predictedShortage: '21 days',
      affectedRegions: 5,
      confidence: 87,
      trend: 'stable'
    },
    {
      category: 'Medications',
      severity: 'info',
      predictedShortage: '30 days',
      affectedRegions: 12,
      confidence: 78,
      trend: 'decreasing'
    }
  ];

  const regions = [
    { name: 'District A', risk: 'high', cases: 45 },
    { name: 'District B', risk: 'medium', cases: 23 },
    { name: 'District C', risk: 'low', cases: 12 },
    { name: 'District D', risk: 'high', cases: 67 },
    { name: 'District E', risk: 'medium', cases: 34 },
    { name: 'District F', risk: 'low', cases: 8 }
  ];

  const timelineData = [
    { date: '2024-01-01', supply: 85, demand: 78 },
    { date: '2024-01-08', supply: 82, demand: 85 },
    { date: '2024-01-15', supply: 78, demand: 92 },
    { date: '2024-01-22', supply: 75, demand: 98 },
    { date: '2024-01-29', supply: 72, demand: 105 }
  ];

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'text-red-500 bg-red-50 border-red-200';
      case 'warning': return 'text-orange-500 bg-orange-50 border-orange-200';
      case 'info': return 'text-blue-500 bg-blue-50 border-blue-200';
      default: return 'text-gray-500 bg-gray-50 border-gray-200';
    }
  };

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'high': return 'bg-red-400';
      case 'medium': return 'bg-orange-400';
      case 'low': return 'bg-green-400';
      default: return 'bg-gray-400';
    }
  };

  const CircularProgress = ({ percentage, size = 80 }) => {
    const radius = (size - 10) / 2;
    const circumference = radius * 2 * Math.PI;
    const strokeDasharray = circumference;
    const strokeDashoffset = circumference - (percentage / 100) * circumference;

    return (
      <div className="relative inline-flex items-center justify-center">
        <svg width={size} height={size} className="transform -rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#e5e7eb"
            strokeWidth="8"
            fill="transparent"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#3b82f6"
            strokeWidth="8"
            fill="transparent"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-lg font-semibold text-gray-700">{percentage}%</span>
        </div>
      </div>
    );
  };

  useEffect(() => {
    const messages = [
      "Consider reordering malaria kits in District B - predicted shortage in 14 days.",
      "Blood type O- availability dropping in 3 regions. Suggest contacting suppliers.",
      "Vaccine supply stable, but demand increasing in urban areas."
    ];
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    setAssistantMessage(randomMessage);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-emerald-50">
      <Header />

      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">AI Insights Center</h1>
              <p className="text-gray-600">Predictive Health Intelligence Dashboard</p>
            </div>

            <div className="flex items-center gap-3">
              <FaCalendarAlt className="text-gray-400" />
              <select
                value={selectedPeriod}
                onChange={(e) => setSelectedPeriod(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
              >
                {periods.map((period) => (
                  <option key={period.value} value={period.value}>{period.label}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-3 space-y-8">
            {/* Shortage Predictions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                <FaExclamationTriangle className="mr-3 text-orange-500" />
                Shortage Predictions by Category
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {shortagePredictions.map((prediction, index) => (
                  <div
                    key={prediction.category}
                    className={`border rounded-lg p-4 animate-fade-in ${getSeverityColor(prediction.severity)}`}
                    style={{ animationDelay: `${index * 200}ms` }}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold text-gray-800">{prediction.category}</h3>
                      <div className="flex items-center">
                        {prediction.trend === 'increasing' && <FaArrowUp className="text-red-500 mr-1" />}
                        {prediction.trend === 'decreasing' && <FaArrowDown className="text-green-500 mr-1" />}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <p className="text-sm text-gray-600">
                        Shortage in: <span className="font-medium">{prediction.predictedShortage}</span>
                      </p>
                      <p className="text-sm text-gray-600">
                        Affected regions: <span className="font-medium">{prediction.affectedRegions}</span>
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Confidence:</span>
                        <CircularProgress percentage={prediction.confidence} size={60} />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Regional Heat Map */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                <FaMapMarkerAlt className="mr-3 text-blue-500" />
                Regional Risk Heat Map
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {regions.map((region, index) => (
                  <div
                    key={region.name}
                    className="bg-gray-50 rounded-lg p-4 animate-fade-in hover:shadow-md transition-shadow"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-gray-800">{region.name}</span>
                      <div className={`w-3 h-3 rounded-full ${getRiskColor(region.risk)}`}></div>
                    </div>
                    <p className="text-sm text-gray-600">{region.cases} cases reported</p>
                    <div className="mt-2 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${getRiskColor(region.risk)} transition-all duration-1000`}
                        style={{ width: `${Math.min(region.cases * 2, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Supply/Demand Timeline */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                <FaChartLine className="mr-3 text-emerald-500" />
                Supply vs Demand Timeline
              </h2>
              <div className="space-y-4">
                {timelineData.map((data, index) => (
                  <div
                    key={data.date}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg animate-fade-in"
                    style={{ animationDelay: `${index * 150}ms` }}
                  >
                    <div className="flex items-center">
                      <FaClock className="text-gray-400 mr-3" />
                      <span className="text-sm font-medium text-gray-700">{data.date}</span>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-center">
                        <p className="text-xs text-gray-500">Supply</p>
                        <p className="text-sm font-semibold text-emerald-600">{data.supply}%</p>
                      </div>
                      <div className="text-center">
                        <p className="text-xs text-gray-500">Demand</p>
                        <p className="text-sm font-semibold text-blue-600">{data.demand}%</p>
                      </div>
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-emerald-500 h-2 rounded-full transition-all duration-1000"
                          style={{ width: `${data.supply}%` }}
                        ></div>
                      </div>
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full transition-all duration-1000"
                          style={{ width: `${data.demand}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* AI Assistant Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-24">
              <div className="bg-gradient-to-br from-blue-50 to-emerald-50 rounded-xl border border-blue-200 p-6 shadow-lg">
                <div className="flex items-center mb-4">
                  <div className="bg-blue-500 rounded-full p-2 mr-3 animate-pulse">
                    <FaRobot className="text-white text-lg" />
                  </div>
                  <h3 className="font-semibold text-gray-800">AI Assistant</h3>
                </div>

                <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200 mb-4">
                  <p className="text-sm text-gray-700 leading-relaxed">{assistantMessage}</p>
                </div>

                <div className="space-y-3">
                  <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors shadow-sm">
                    Take Action
                  </button>
                  <button className="w-full border border-gray-300 text-gray-700 py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
                    View Details
                  </button>
                </div>

                <div className="mt-6 pt-4 border-t border-gray-200">
                  <p className="text-xs text-gray-500 text-center">
                    Powered by MedVault MCP
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIInsightsPage;
