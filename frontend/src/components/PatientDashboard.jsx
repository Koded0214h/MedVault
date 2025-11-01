import React from 'react';
import { FaUserMd, FaCalendarAlt, FaPrescriptionBottle, FaBell, FaBrain, FaChartBar, FaHeartbeat, FaStethoscope } from 'react-icons/fa';

const PatientDashboard = () => {

  
  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">👤 Patient Dashboard</h1>
        <p className="text-gray-600">Your personalized health overview and AI-powered insights.</p>
      </div>

      {/* Health Summary */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
          <FaHeartbeat className="text-red-500 mr-2" />
          Health Summary
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <FaStethoscope className="text-blue-500 text-2xl mx-auto mb-2" />
            <div className="text-2xl font-bold text-blue-800">Normal</div>
            <div className="text-sm text-blue-600">Blood Pressure</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <FaHeartbeat className="text-green-500 text-2xl mx-auto mb-2" />
            <div className="text-2xl font-bold text-green-800">72 bpm</div>
            <div className="text-sm text-green-600">Heart Rate</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <FaChartBar className="text-purple-500 text-2xl mx-auto mb-2" />
            <div className="text-2xl font-bold text-purple-800">98%</div>
            <div className="text-sm text-purple-600">Oxygen Saturation</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Upcoming Appointments */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <FaCalendarAlt className="text-blue-500 mr-2" />
              Upcoming Appointments
            </h2>
            <div className="space-y-3">
              <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-blue-800">Dr. Sarah Johnson</h3>
                    <p className="text-blue-600 text-sm">Cardiology Consultation</p>
                    <p className="text-blue-700 text-sm mt-1">Tomorrow, 10:00 AM</p>
                  </div>
                  <button className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                    Join Call
                  </button>
                </div>
              </div>
              <div className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-green-800">Dr. Michael Chen</h3>
                    <p className="text-green-600 text-sm">Follow-up Check</p>
                    <p className="text-green-700 text-sm mt-1">Friday, 2:30 PM</p>
                  </div>
                  <button className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">
                    Reschedule
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Current Prescriptions */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <FaPrescriptionBottle className="text-purple-500 mr-2" />
              Current Prescriptions
            </h2>
            <div className="space-y-3">
              {[
                { name: 'Lisinopril', dosage: '10mg', frequency: 'Once daily', remaining: 15, total: 30 },
                { name: 'Metformin', dosage: '500mg', frequency: 'Twice daily', remaining: 8, total: 60 },
                { name: 'Atorvastatin', dosage: '20mg', frequency: 'Once daily', remaining: 22, total: 30 }
              ].map((med, index) => (
                <div key={med.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <span className="text-gray-700 font-medium">{med.name} {med.dosage}</span>
                    <div className="text-xs text-gray-500 mt-1">{med.frequency}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-600">{med.remaining}/{med.total} remaining</div>
                    <div className="w-16 bg-gray-200 rounded-full h-2 mt-1">
                      <div
                        className={`h-2 rounded-full ${med.remaining < 10 ? 'bg-red-500' : med.remaining < 20 ? 'bg-yellow-500' : 'bg-green-500'}`}
                        style={{ width: `${(med.remaining / med.total) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Patient Demand Data */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <FaBrain className="text-indigo-500 mr-2" />
              Patient Demand Data Insights
            </h2>
            <p className="text-gray-600 text-sm mb-4">Aggregate, anonymized medication/treatment history from MedVault's EHRs</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-indigo-50 rounded-lg">
                <h3 className="font-semibold text-indigo-800 mb-2">Common Treatments</h3>
                <div className="space-y-2 text-sm text-indigo-700">
                  <p>Hypertension: 45% of similar patients</p>
                  <p>Diabetes: 32% of similar patients</p>
                  <p>Cardiovascular: 28% of similar patients</p>
                </div>
              </div>
              <div className="p-4 bg-teal-50 rounded-lg">
                <h3 className="font-semibold text-teal-800 mb-2">Medication Trends</h3>
                <div className="space-y-2 text-sm text-teal-700">
                  <p>ACE Inhibitors: ↑ 15% usage</p>
                  <p>Statins: ↗️ 8% trending up</p>
                  <p>Metformin: Stable demand</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Emergency Alerts */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <FaBell className="text-red-500 mr-2" />
              Emergency Alerts
            </h2>
            <div className="space-y-3">
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-red-800">Recall Alert</span>
                  <span className="text-xs text-red-600">High Priority</span>
                </div>
                <p className="text-sm text-red-700">Blood pressure medication batch recall. Contact your doctor immediately.</p>
              </div>
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-yellow-800">Appointment Reminder</span>
                  <span className="text-xs text-yellow-600">Tomorrow</span>
                </div>
                <p className="text-sm text-yellow-700">Cardiology consultation at 10:00 AM. Don't forget your medical records.</p>
              </div>
            </div>
          </div>

          {/* AI Health Insights */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <FaBrain className="text-blue-500 mr-2" />
              AI Health Insights
            </h2>
            <div className="space-y-3">
              <div className="p-3 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-blue-800 text-sm mb-1">Risk Assessment</h3>
                <p className="text-sm text-blue-700">Low risk for cardiovascular events based on current metrics.</p>
              </div>
              <div className="p-3 bg-green-50 rounded-lg">
                <h3 className="font-semibold text-green-800 text-sm mb-1">Medication Adherence</h3>
                <p className="text-sm text-green-700">Excellent adherence to prescribed medications this month.</p>
              </div>
              <div className="p-3 bg-purple-50 rounded-lg">
                <h3 className="font-semibold text-purple-800 text-sm mb-1">Lifestyle Recommendations</h3>
                <p className="text-sm text-purple-700">Consider increasing daily physical activity by 20 minutes.</p>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <button className="w-full flex items-center justify-center bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors">
                <FaUserMd className="mr-2" />
                Schedule Appointment
              </button>
              <button className="w-full flex items-center justify-center bg-green-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-700 transition-colors">
                <FaPrescriptionBottle className="mr-2" />
                Refill Prescription
              </button>
              <button className="w-full flex items-center justify-center bg-purple-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-purple-700 transition-colors">
                <FaBell className="mr-2" />
                Emergency Contact
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard;
