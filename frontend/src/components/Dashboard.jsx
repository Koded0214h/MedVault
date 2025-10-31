import React, {useState, useEffect } from 'react';
import { FaExclamationTriangle, FaBox, FaClipboardList, FaPlus, FaCheckCircle, FaBrain, FaChartLine, FaTruck, FaBell } from 'react-icons/fa';
import api from '../services/api';

const Dashboard = () => {
  const [inventoryData, setInventoryData] = useState([]);
  const [inventorySummary, setInventorySummary] = useState({});
  const [loading, setLoading] = useState(true);
  const [alerts, setAlerts] = useState([]);
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const inventoryResponse = await api.get('/inventory/items/');
        const inventoryData = inventoryResponse.data;

        const summary = {
          totalItems: inventoryData.length,
          lowStock: inventoryData.filter(item => item.quantity < item.min_threshold).length,
          totalValue: inventoryData.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0)
        };

        setInventoryData(inventoryData);
        setInventorySummary(summary);

        const predictionsResponse = await api.get('/mcp/predictions/');
        setPredictions(predictionsResponse.data.slice(0, 5));

        const alertsResponse = await api.get('/notifications/alerts/');
        setAlerts(alertsResponse.data.slice(0, 3));

      } catch (error) {
         console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }
  
  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">🧠 AI-Powered Dashboard</h1>
        <p className="text-gray-600">Real-time insights and MCP predictions for proactive healthcare management.</p>
      </div>

      {/* MCP Prediction Alerts */}
      <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-6">
        <div className="flex items-center mb-2">
          <FaBrain className="text-orange-500 mr-3" />
          <span className="text-orange-700 font-semibold">MCP Shortage Predictions</span>
        </div>
        <div className="space-y-2 text-orange-700">
          <p><strong>Insulin:</strong> 89% confidence shortage in 7 days - Order recommended</p>
          <p><strong>Malaria Test Kits:</strong> 76% confidence shortage in 14 days - Monitor closely</p>
          <p><strong>O- Blood:</strong> Supply stable, but demand increasing 15%</p>
        </div>
      </div>

      {/* Alert Banner */}
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <div className="flex items-center">
          <FaExclamationTriangle className="text-red-500 mr-3" />
          <span className="text-red-700 font-semibold">{inventorySummary.lowStock || 0} Items Below Threshold</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* MCP Prediction Insights */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <FaChartLine className="text-blue-500 mr-2" />
              MCP Prediction Insights
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-blue-800 mb-2">Demand Trends</h3>
                <div className="space-y-2 text-sm text-blue-700">
                  <p>Insulin: ↑ 23% this week</p>
                  <p>Malaria Tests: ↑ 15% this month</p>
                  <p>Antibiotics: ↗️ 8% trending up</p>
                </div>
              </div>
              <div className="p-4 bg-green-50 rounded-lg">
                <h3 className="font-semibold text-green-800 mb-2">Supply Alerts</h3>
                <div className="space-y-2 text-sm text-green-700">
                  <p>✅ O- Blood: Well stocked</p>
                  <p>⚠️ Insulin: Monitor closely</p>
                  <p>🚨 Malaria Kits: Order soon</p>
                </div>
              </div>
            </div>
          </div>

          {/* Inventory Summary */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Inventory Summary: Top 5 Items</h2>
            <div className="space-y-3">
              {[
                { name: 'Ibuprofen', level: 80, prediction: 'Stable' },
                { name: 'Atorvastatin', level: 65, prediction: 'Declining' },
                { name: 'Metformin', level: 50, prediction: 'Critical' },
                { name: 'Lisinopril', level: 35, prediction: 'Order Now' },
                { name: 'Amlodipine', level: 20, prediction: 'Shortage Risk' }
              ].map((item, index) => (
                <div key={item.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <span className="text-gray-700 font-medium">{item.name}</span>
                    <div className="text-xs text-gray-500 mt-1">{item.prediction}</div>
                  </div>
                  <div className="w-24 bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${item.level < 30 ? 'bg-red-500' : item.level < 60 ? 'bg-yellow-500' : 'bg-green-500'}`}
                      style={{ width: `${item.level}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Patient Orders */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Patient Orders</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 text-gray-600 font-semibold">ORDER ID</th>
                    <th className="text-left py-3 text-gray-600 font-semibold">PATIENT</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 text-blue-600 font-medium">#MV-84321</td>
                    <td className="py-3 text-gray-700">John Doe</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Total Inventory */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
            <div className="flex items-center justify-center mb-3">
              <FaBox className="text-blue-500 text-2xl mr-2" />
              <h3 className="text-lg font-semibold text-gray-700">Total Inventory Items</h3>
            </div>
            <div className="text-4xl font-bold text-gray-800">{inventorySummary.totalItems || 0}</div>
          </div>

          {/* Automated Order Recommendations */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <FaTruck className="text-green-500 mr-2" />
              MCP Order Recommendations
            </h3>
            <div className="space-y-3">
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-red-800">Insulin</span>
                  <span className="text-xs text-red-600">89% confidence</span>
                </div>
                <p className="text-sm text-red-700">Order 200 units - Shortage in 7 days</p>
                <button className="mt-2 w-full bg-red-600 text-white text-sm py-1 px-3 rounded hover:bg-red-700 transition-colors">
                  Order Now
                </button>
              </div>
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-yellow-800">Malaria Test Kits</span>
                  <span className="text-xs text-yellow-600">76% confidence</span>
                </div>
                <p className="text-sm text-yellow-700">Order 150 kits - Shortage in 14 days</p>
                <button className="mt-2 w-full bg-yellow-600 text-white text-sm py-1 px-3 rounded hover:bg-yellow-700 transition-colors">
                  Add to Cart
                </button>
              </div>
            </div>
          </div>

          {/* Quick Stock Update */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Stock Update</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Item Name / SKU</label>
                <input
                  type="text"
                  placeholder="e.g. ibuprofen 200mg"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
                <input
                  type="number"
                  placeholder="e.g. 50"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <button className="w-full flex items-center justify-center bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors">
                <FaPlus className="mr-2" />
                Add Stock
              </button>
            </div>
          </div>

          {/* View All Orders */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">View All Orders</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-2 text-gray-600 font-semibold">QTY</th>
                    <th className="text-left py-2 text-gray-600 font-semibold">STATUS</th>
                    <th className="text-left py-2 text-gray-600 font-semibold">ACTIONS</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="py-2 text-gray-700">1</td>
                    <td className="py-2">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        Pending
                      </span>
                    </td>
                    <td className="py-2">
                      <button className="flex items-center text-blue-600 hover:text-blue-800 text-sm font-medium">
                        <FaCheckCircle className="mr-1" />
                        Fulfill
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;