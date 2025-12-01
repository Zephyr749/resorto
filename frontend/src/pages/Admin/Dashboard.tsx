import { useEffect, useState } from 'react';
import { message, Spin } from 'antd';
import { adminApi } from '../../api/admin';
import { BookingStats } from '../../types';

const AdminDashboard = () => {
  const [stats, setStats] = useState<BookingStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await adminApi.getStats();
      setStats(data);
    } catch (error: any) {
      message.error('Failed to load statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div className="py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-stone-900 mb-8">Admin Dashboard</h1>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="glass-card p-6">
            <div className="text-4xl mb-2">📊</div>
            <h3 className="text-sm font-semibold text-stone-600 mb-1">Total Bookings</h3>
            <p className="text-3xl font-bold text-stone-900">{stats?.totalBookings || 0}</p>
          </div>

          <div className="glass-card p-6">
            <div className="text-4xl mb-2">✅</div>
            <h3 className="text-sm font-semibold text-stone-600 mb-1">Confirmed</h3>
            <p className="text-3xl font-bold text-emerald-600">{stats?.confirmedBookings || 0}</p>
          </div>

          <div className="glass-card p-6">
            <div className="text-4xl mb-2">⏳</div>
            <h3 className="text-sm font-semibold text-stone-600 mb-1">Pending</h3>
            <p className="text-3xl font-bold text-amber-600">{stats?.pendingBookings || 0}</p>
          </div>

          <div className="glass-card p-6">
            <div className="text-4xl mb-2">❌</div>
            <h3 className="text-sm font-semibold text-stone-600 mb-1">Cancelled</h3>
            <p className="text-3xl font-bold text-red-600">{stats?.cancelledBookings || 0}</p>
          </div>

          <div className="glass-card p-6">
            <div className="text-4xl mb-2">💰</div>
            <h3 className="text-sm font-semibold text-stone-600 mb-1">Total Revenue</h3>
            <p className="text-3xl font-bold text-emerald-600">₹{stats?.totalRevenue || 0}</p>
          </div>

          <div className="glass-card p-6">
            <div className="text-4xl mb-2">📅</div>
            <h3 className="text-sm font-semibold text-stone-600 mb-1">Today's Bookings</h3>
            <p className="text-3xl font-bold text-stone-900">{stats?.todayBookings || 0}</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="glass-card p-6">
          <h2 className="text-xl font-bold text-stone-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <a
              href="/admin/spots"
              className="px-6 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-semibold rounded-lg hover:from-emerald-500 hover:to-teal-500 transition-all shadow-md text-center"
            >
              Manage Spots
            </a>
            <a
              href="/admin/bookings"
              className="px-6 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-500 hover:to-indigo-500 transition-all shadow-md text-center"
            >
              Manage Bookings
            </a>
            <a
              href="/spots"
              className="px-6 py-4 bg-stone-100 text-stone-700 font-semibold rounded-lg hover:bg-stone-200 transition-colors text-center"
            >
              View Public Site
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
