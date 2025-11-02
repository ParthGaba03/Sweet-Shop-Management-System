import React, { useState } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { getApiUrl } from '../../config';
import '../Auth/Auth.css';

const ForgotPassword: React.FC = () => {
  const [searchParams] = useSearchParams();
  const urlToken = searchParams.get('token');
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [resetToken, setResetToken] = useState<string>(urlToken || ''); // Store token in state
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<'request' | 'reset'>(urlToken ? 'reset' : 'request');

  const handleRequestReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const response = await axios.post(getApiUrl('/api/auth/forgot-password'), { email });
      
      // If token is returned (email exists in database), automatically show reset form
      if (response.data.reset_token) {
        // Store token in state
        setResetToken(response.data.reset_token);
        // Immediately switch to reset password form
        setStep('reset');
        setSuccess('Please enter your new password below.');
      } else {
        // Email not found, show generic message
        setSuccess(response.data.message);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send reset link. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (newPassword.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    if (!resetToken) {
      setError('Reset token is missing. Please request a new password reset.');
      return;
    }

    setLoading(true);

    try {
      await axios.post(getApiUrl('/api/auth/reset-password'), {
        token: resetToken,
        new_password: newPassword,
      });
      setSuccess('Password reset successful! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to reset password. Token may be invalid or expired.');
    } finally {
      setLoading(false);
    }
  };

  if (step === 'reset') {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <h2>Reset Your Password</h2>
          <form onSubmit={handleResetPassword}>
            <div className="form-group">
              <label htmlFor="newPassword">New Password</label>
              <input
                type="password"
                id="newPassword"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                minLength={8}
                autoComplete="new-password"
              />
              <small style={{ color: '#666', fontSize: '0.85em' }}>Minimum 8 characters</small>
            </div>
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm New Password</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                minLength={8}
                autoComplete="new-password"
              />
            </div>
            {error && <div className="error">{error}</div>}
            {success && <div className="success">{success}</div>}
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>
          <p className="auth-link">
            Remember your password? <Link to="/login">Login here</Link>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Forgot Password</h2>
        <p style={{ color: '#666', marginBottom: '20px' }}>
          Enter your email address and we'll send you instructions to reset your password.
        </p>
        <form onSubmit={handleRequestReset}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
              placeholder="your.email@example.com"
            />
          </div>
          {error && <div className="error">{error}</div>}
          {success && <div className="success" style={{ whiteSpace: 'pre-line' }}>{success}</div>}
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Sending...' : 'Send Reset Link'}
          </button>
        </form>
        <p className="auth-link">
          Remember your password? <Link to="/login">Login here</Link>
        </p>
        <p className="auth-link">
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;

