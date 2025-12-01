#!/bin/bash

# Resorto Frontend - Complete Setup Script
# This script creates all remaining frontend files

cd "$(dirname "$0")"

echo "🚀 Creating Resorto Frontend Files..."

# Create main App.tsx
cat > src/App.tsx << 'EOF'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { AuthProvider } from './context/AuthContext';

// Pages
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import SpotList from './pages/Public/SpotList';
import SpotDetails from './pages/Public/SpotDetails';
import MyBookings from './pages/User/MyBookings';
import CreateBooking from './pages/User/CreateBooking';
import Profile from './pages/User/Profile';
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
        },
      }}
    >
      <AuthProvider>
        <Router>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Layout Routes */}
            <Route element={<Layout />}>
              <Route path="/" element={<SpotList />} />
              <Route path="/spots" element={<SpotList />} />
              <Route path="/spots/:id" element={<SpotDetails />} />
              
              {/* User Protected Routes */}
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
              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <Profile />
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
EOF

# Create main.tsx
cat > src/main.tsx << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

# Create index.css
cat > src/index.css << 'EOF'
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#root {
  min-height: 100vh;
}
EOF

echo "✅ Core files created"
echo "📝 Run: npm run dev"
echo "🌐 Frontend will start on http://localhost:3000"
echo ""
echo "⚠️  Note: You need to manually create the page components in src/pages/"
echo "   See FRONTEND_IMPLEMENTATION.md for complete code"

EOF

chmod +x frontend/SETUP_COMPLETE.sh
