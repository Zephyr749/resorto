import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { AuthProvider } from './context/AuthContext';

// Pages
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Profile from './pages/User/Profile';
import SpotList from './pages/Public/SpotList';
import SpotDetails from './pages/Public/SpotDetails';
import MyBookings from './pages/User/MyBookings';
import CreateBooking from './pages/User/CreateBooking';
import AdminDashboard from './pages/Admin/Dashboard';
import AdminSpots from './pages/Admin/SpotManagement';
import AdminBookings from './pages/Admin/BookingManagement';

// Components
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 6,
        },
      }}
    >
      <AuthProvider>
        <Router>
          <Routes>
            {/* Public Auth Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Layout Routes */}
            <Route element={<Layout />}>
              <Route path="/" element={<SpotList />} />
              <Route path="/spots" element={<SpotList />} />
              <Route path="/spots/:id" element={<SpotDetails />} />
              
              {/* User Protected Routes */}
              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <Profile />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/my-bookings"
                element={
                  <ProtectedRoute>
                    <MyBookings />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/book/:spotId"
                element={
                  <ProtectedRoute>
                    <CreateBooking />
                  </ProtectedRoute>
                }
              />
              
              {/* Admin Protected Routes */}
              <Route
                path="/admin/dashboard"
                element={
                  <ProtectedRoute adminOnly>
                    <AdminDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/spots"
                element={
                  <ProtectedRoute adminOnly>
                    <AdminSpots />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/bookings"
                element={
                  <ProtectedRoute adminOnly>
                    <AdminBookings />
                  </ProtectedRoute>
                }
              />
            </Route>
            
            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ConfigProvider>
  );
}

export default App;
