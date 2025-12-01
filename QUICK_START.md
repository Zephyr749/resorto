# 🚀 Resorto - Quick Start Guide

## One-Command Startup

```bash
./start.sh
```

That's it! Both backend and frontend will start automatically.

## Access the Application

Once started, open your browser:

**Frontend (Main App):**  
🌐 http://localhost:3000

**Backend API:**  
🔌 http://localhost:8000

**API Documentation:**  
📚 http://localhost:8000/docs

## What You Can Do NOW

### 1. Register a New Account
- Go to http://localhost:3000/register
- Fill in your details
- Click Register
- You'll be automatically logged in!

### 2. Login
- Go to http://localhost:3000/login
- Enter your email and password
- Click Login

### 3. Manage Your Profile
- After login, click your name in the header
- Select "Profile"
- View/edit your information
- Change your password

### 4. Logout
- Click your name in header
- Select "Logout"

## Stop the Application

```bash
./stop.sh
```

Or just press `Ctrl+C` in the terminal where you ran `./start.sh`

## Development Mode

If you want to see live logs:

```bash
./dev.sh
```

This shows real-time output from both backend and frontend.

## Troubleshooting

### Port Already in Use?

**Stop all services:**
```bash
./stop.sh
```

**Or manually:**
```bash
# Kill backend
lsof -ti:8000 | xargs kill -9

# Kill frontend
lsof -ti:3000 | xargs kill -9
```

### Dependencies Not Installed?

**Backend:**
```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cd ..
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### Need to Configure?

Edit backend configuration:
```bash
cd backend
nano .env
```

Required settings:
- MONGODB_URI - Your MongoDB connection string
- JWT_SECRET - Secret key for JWT tokens
- RAZORPAY_KEY_ID - Razorpay key (optional for now)
- RAZORPAY_KEY_SECRET - Razorpay secret (optional for now)

## Project Structure

```
Resorto/
├── start.sh          ← Start everything
├── stop.sh           ← Stop everything
├── dev.sh            ← Development mode
│
├── backend/          ← FastAPI backend
│   ├── .venv/       ← Python virtual env
│   ├── main.py      ← API entry point
│   └── modules/     ← Code modules
│
└── frontend/         ← React frontend
    ├── src/         ← Source code
    └── package.json ← Dependencies
```

## Available Features

### ✅ Working Now:
- User Registration
- User Login
- Profile Management
- Edit Profile (Name)
- Change Password
- Logout
- Protected Routes
- Role-Based Access

### 🔄 Coming Soon:
- Browse Spots/Rooms
- Create Bookings
- Make Payments
- View Booking History
- Admin Dashboard
- Spot Management
- Booking Management

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- MongoDB (Database)
- JWT (Authentication)
- Razorpay (Payments)

**Frontend:**
- React 18 (UI library)
- TypeScript (Type safety)
- Vite (Build tool)
- Ant Design (UI components)
- React Router (Routing)

## Ports

| Service | Port | URL |
|---------|------|-----|
| **Frontend** | 3000 | http://localhost:3000 |
| **Backend** | 8000 | http://localhost:8000 |
| **API Docs** | 8000 | http://localhost:8000/docs |

## Need Help?

Check these files:
- `README.md` - Full documentation
- `README_SCRIPTS.md` - Script usage details
- `PROJECT_COMPLETE.md` - Project status
- `FRONTEND_AUTH_COMPLETE.md` - Frontend features

## Quick Commands Reference

```bash
# Start everything
./start.sh

# Stop everything
./stop.sh

# Development mode (with logs)
./dev.sh

# Run backend tests
cd backend && ./test.sh

# Build frontend
cd frontend && npm run build

# Run backend only
cd backend && ./run.sh

# Run frontend only
cd frontend && npm run dev
```

---

**That's it! You're ready to go!** 🎉

Just run `./start.sh` and open http://localhost:3000
