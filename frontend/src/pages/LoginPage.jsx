import React, { useState } from 'react';
import { FaUserMd, FaShieldAlt, FaEye, FaEyeSlash, FaRobot } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Handle login logic here
    try {
      const response = await api.post('/auth/login/', { username: email, password });
      localStorage.setItem('access-token', response.data.access);
      localStorage.setItem('refresh-token', response.data.refresh);
      navigate('/dashboard');
    } catch (error) {
      setError('Invalid credentials. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-green-500 rounded-full mb-4">
            <FaUserMd className="text-white text-2xl" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome to MedVault</h1>
          <p className="text-gray-600">Unified Health Records. Real-Time Resource Access. Health Equity Delivered.</p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="your.email@example.com"
                required
              />
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                  placeholder="Enter your password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-sm text-gray-600">Remember me</span>
              </label>
              <Link
                to="/forgot-password"
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                Forgot password?
              </Link>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-500 to-green-500 text-white py-3 px-4 rounded-lg font-semibold hover:from-blue-600 hover:to-green-600 transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              Log In
            </button>
          </form>

          {error && (
            <div className = "mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded mt-4">
              {error}
            </div>
          )}

          {/* Divider */}
          <div className="mt-8 mb-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Don't have an account?</span>
              </div>
            </div>
          </div>

          {/* Sign Up Link */}
          <Link
            to="/signup"
            className="w-full block text-center bg-gray-50 text-gray-700 py-3 px-4 rounded-lg font-semibold hover:bg-gray-100 transition-colors border border-gray-200"
          >
            Create Account
          </Link>
        </div>

        {/* Security Notice */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center text-sm text-gray-500">
            <FaShieldAlt className="mr-2 text-green-500" />
            Your data is protected with end-to-end encryption
          </div>
        </div>

        {/* AI Assistant */}
        <div className="fixed bottom-6 right-6">
          <button
            onClick={() => setShowHelp(!showHelp)}
            className="bg-gradient-to-r from-blue-500 to-green-500 text-white p-4 rounded-full shadow-lg hover:from-blue-600 hover:to-green-600 transition-all duration-200 transform hover:scale-110"
          >
            <FaRobot className="text-xl" />
          </button>

          {showHelp && (
            <div className="absolute bottom-20 right-0 bg-white rounded-lg shadow-xl p-4 max-w-xs border border-gray-200">
              <div className="flex items-center mb-2">
                <FaRobot className="text-blue-500 mr-2" />
                <span className="font-semibold text-gray-800">AI Assistant</span>
              </div>
              <p className="text-sm text-gray-600 mb-3">
                Need help signing in? I can guide you through the process or help with common issues.
              </p>
              <button className="text-sm bg-blue-50 text-blue-600 px-3 py-1 rounded hover:bg-blue-100 transition-colors">
                Get Help
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
