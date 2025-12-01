import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { LoginCredentials } from '../../types';
import { message } from 'antd';

const Login = () => {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<LoginCredentials>({ email: '', password: '' });
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.email || !formData.password) {
      message.error('Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      await login(formData);
      navigate('/');
    } catch (error) {
      // Error handled by context
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        {/* Logo & Header */}
        <div className="text-center">
          <div className="flex justify-center mb-4">
            <div className="text-7xl">🏖️</div>
          </div>
          <h1 className="text-4xl font-bold text-emerald-900 mb-2">
            Resorto
          </h1>
          <h2 className="text-2xl font-semibold text-stone-800 mb-2">
            Welcome back
          </h2>
          <p className="text-stone-600">
            Sign in to continue to your resort bookings
          </p>
        </div>

        {/* Form Card */}
        <div className="glass-card p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-stone-900 mb-2">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="input-field"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-semibold text-stone-900 mb-2">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="input-field"
                placeholder="Enter your password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          <div className="mt-6 text-center text-sm">
            <span className="text-stone-600">Don't have an account? </span>
            <Link 
              to="/register" 
              className="font-semibold text-emerald-600 hover:text-emerald-500 transition-colors"
            >
              Create one
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
