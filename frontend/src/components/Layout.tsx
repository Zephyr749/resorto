import { Outlet, Link, useNavigate } from 'react-router-dom';
import { Dropdown } from 'antd';
import type { MenuProps } from 'antd';
import { useAuth } from '../context/AuthContext';

const Layout = () => {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      label: 'My Profile',
      onClick: () => navigate('/profile'),
    },
    {
      key: 'mybookings',
      label: 'My Bookings',
      onClick: () => navigate('/my-bookings'),
    },
    ...(isAdmin
      ? [
          { type: 'divider' as const },
          {
            key: 'admin',
            label: 'Admin Dashboard',
            onClick: () => navigate('/admin/dashboard'),
          },
          {
            key: 'admin-spots',
            label: 'Manage Spots',
            onClick: () => navigate('/admin/spots'),
          },
          {
            key: 'admin-bookings',
            label: 'Manage Bookings',
            onClick: () => navigate('/admin/bookings'),
          },
        ]
      : []),
    { type: 'divider' as const },
    {
      key: 'logout',
      label: 'Logout',
      onClick: handleLogout,
      danger: true,
    },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-stone-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
              <span className="text-3xl">🏖️</span>
              <span className="text-xl font-bold text-emerald-900">Resorto</span>
            </Link>

            {/* Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <Link to="/" className="text-stone-700 hover:text-emerald-600 font-medium transition-colors">
                Home
              </Link>
              <Link to="/spots" className="text-stone-700 hover:text-emerald-600 font-medium transition-colors">
                Browse Spots
              </Link>
            </nav>

            {/* User Menu */}
            <div className="flex items-center space-x-4">
              {user ? (
                <Dropdown menu={{ items: userMenuItems }} placement="bottomRight" trigger={['click']}>
                  <button className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-stone-100 hover:bg-stone-200 transition-colors">
                    <div className="w-8 h-8 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                      {user.firstName?.[0]}{user.lastName?.[0]}
                    </div>
                    <span className="text-stone-900 font-medium">{user.firstName}</span>
                    {isAdmin && (
                      <span className="text-xs text-emerald-600 font-semibold">Admin</span>
                    )}
                  </button>
                </Dropdown>
              ) : (
                <div className="flex items-center space-x-3">
                  <button
                    onClick={() => navigate('/login')}
                    className="px-4 py-2 text-stone-700 font-medium hover:text-emerald-600 transition-colors"
                  >
                    Sign In
                  </button>
                  <button
                    onClick={() => navigate('/register')}
                    className="px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-semibold rounded-lg hover:from-emerald-500 hover:to-teal-500 transition-all shadow-md"
                  >
                    Get Started
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-stone-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <span className="text-2xl">🏖️</span>
              <span className="text-lg font-bold text-emerald-900">Resorto</span>
            </div>
            <p className="text-stone-600 text-sm">
              Your Perfect Getaway © {new Date().getFullYear()}
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
