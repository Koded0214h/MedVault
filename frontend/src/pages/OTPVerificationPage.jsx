import React, { useState, useEffect } from 'react';
import { FaUserMd, FaShieldAlt, FaRobot, FaArrowLeft } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const OTPVerificationPage = () => {
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes
  const [showHelp, setShowHelp] = useState(false);
  const [isResending, setIsResending] = useState(false);

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [timeLeft]);

  const handleOtpChange = (index, value) => {
    if (value.length > 1) return; // Only allow single digit

    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    // Auto-focus next input
    if (value && index < 5) {
      const nextInput = document.getElementById(`otp-${index + 1}`);
      if (nextInput) nextInput.focus();
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      const prevInput = document.getElementById(`otp-${index - 1}`);
      if (prevInput) prevInput.focus();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const otpCode = otp.join('');
    if (otpCode.length === 6) {
      console.log('OTP verification:', otpCode);
      // Handle OTP verification logic here
    }
  };

  const handleResendOTP = async () => {
    setIsResending(true);
    // Simulate API call
    setTimeout(() => {
      setTimeLeft(300);
      setIsResending(false);
    }, 2000);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const isOtpComplete = otp.every(digit => digit !== '');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-green-500 rounded-full mb-4">
            <FaShieldAlt className="text-white text-2xl" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Verify Your Account</h1>
          <p className="text-gray-600">We've sent a 6-digit code to your email address.</p>
        </div>

        {/* OTP Form */}
        <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* OTP Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4 text-center">
                Enter verification code
              </label>
              <div className="flex justify-center space-x-3">
                {otp.map((digit, index) => (
                  <input
                    key={index}
                    id={`otp-${index}`}
                    type="text"
                    value={digit}
                    onChange={(e) => handleOtpChange(index, e.target.value.replace(/\D/g, ''))}
                    onKeyDown={(e) => handleKeyDown(index, e)}
                    className="w-12 h-12 text-center text-xl font-semibold border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    maxLength="1"
                    required
                  />
                ))}
              </div>
            </div>

            {/* Verify Button */}
            <button
              type="submit"
              disabled={!isOtpComplete}
              className="w-full bg-gradient-to-r from-blue-500 to-green-500 text-white py-3 px-4 rounded-lg font-semibold hover:from-blue-600 hover:to-green-600 transition-all duration-200 transform hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {isOtpComplete ? 'Verify Account' : 'Enter Complete Code'}
            </button>
          </form>

          {/* Resend Timer */}
          <div className="mt-6 text-center">
            {timeLeft > 0 ? (
              <p className="text-sm text-gray-600">
                Resend code in{' '}
                <span className="font-semibold text-blue-600">{formatTime(timeLeft)}</span>
              </p>
            ) : (
              <button
                onClick={handleResendOTP}
                disabled={isResending}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isResending ? 'Sending...' : 'Resend verification code'}
              </button>
            )}
          </div>

          {/* Help Text */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-500">
              Didn't receive the code? Check your spam folder or{' '}
              <Link to="/contact-support" className="text-blue-600 hover:text-blue-800 underline">
                contact support
              </Link>
            </p>
          </div>

          {/* Back to Login */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <Link
              to="/login"
              className="flex items-center justify-center text-gray-600 hover:text-gray-800 transition-colors"
            >
              <FaArrowLeft className="mr-2" />
              Back to Login
            </Link>
          </div>
        </div>

        {/* Security Notice */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center text-sm text-gray-500">
            <FaShieldAlt className="mr-2 text-green-500" />
            Secure verification powered by MedVault
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
                Having trouble with verification? I can help you troubleshoot or guide you through alternative verification methods.
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

export default OTPVerificationPage;
