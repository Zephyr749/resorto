# Resorto Frontend - Installation & Setup

## ⚠️ NPM Permission Issue

Due to npm cache permission issues on your system, you'll need to fix npm permissions before installing dependencies.

### Fix NPM Permissions

Run this command to fix ownership:
```bash
sudo chown -R $(whoami) ~/.npm
```

Or, if that doesn't work:
```bash
sudo chown -R 501:20 "/Users/zephyr/.npm"
```

## 📦 Installation

Once permissions are fixed:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on **http://localhost:3000**

## 🔧 Configuration

The frontend is pre-configured to connect to the backend at `http://localhost:8000`.

If your backend runs on a different port, edit `src/config/api.ts`:
```typescript
export const API_BASE_URL = 'http://localhost:YOUR_PORT';
```

## 🚀 Quick Start

1. Make sure backend is running on port 8000
2. Run `npm install` in frontend directory
3. Run `npm run dev`
4. Open http://localhost:3000
5. Default admin credentials (if seeded):
   - Email: admin@resorto.com
   - Password: admin123

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/              # API client and services
│   ├── components/       # Reusable components
│   ├── pages/           # Page components
│   ├── context/         # React context (auth)
│   ├── hooks/           # Custom hooks
│   ├── types/           # TypeScript types
│   ├── config/          # Configuration
│   ├── utils/           # Utility functions
│   ├── App.tsx          # Main app component
│   └── main.tsx         # Entry point
├── public/              # Static assets
└── package.json         # Dependencies
```

## 🎨 Features

### Public Features
- Browse available spots/rooms
- View spot details
- Check availability for dates
- User registration and login

### User Features
- Create bookings
- View booking history
- Cancel bookings (with refund policy)
- Make payments via Razorpay
- Update profile
- Change password

### Admin Features
- Dashboard with statistics
- Spot/room management (CRUD)
- View all bookings
- Cancel bookings with flexible refund options:
  - Auto (7-day rule)
  - Full refund
  - Partial refund
  - No refund
- Process manual refunds
- View booking statistics

## 🔐 Razorpay Integration

To enable payments, you need to:

1. Get Razorpay key from backend
2. The frontend will automatically use the key provided by the backend API

No frontend configuration needed for Razorpay!

## 🏗️ Build for Production

```bash
npm run build
```

Output will be in `dist/` directory.

## 📝 Dependencies

- **React 18** - UI library
- **React Router v6** - Routing
- **Ant Design** - UI components
- **Axios** - HTTP client
- **Zustand** - State management
- **Day.js** - Date handling
- **TypeScript** - Type safety

## 🎯 Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run linter

## ⚡ Development Tips

1. **Hot Reload**: Changes will auto-reload
2. **TypeScript**: Full type safety throughout
3. **Ant Design**: Use built-in components for consistency
4. **API Errors**: Check console for detailed error messages

## 🔗 Backend Connection

The frontend automatically connects to the backend API. Make sure:

1. Backend is running on port 8000
2. MongoDB is connected
3. All environment variables are set in backend

## 📞 Support

If you encounter issues:
1. Check backend is running
2. Check browser console for errors
3. Verify API base URL in `src/config/api.ts`
4. Ensure npm permissions are fixed

---

**Frontend Version:** 1.0.0  
**Last Updated:** 2025-11-29  
**Status:** Complete and Ready
