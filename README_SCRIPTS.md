# 🚀 Resorto - Quick Start Scripts

## Available Scripts

### 1. Start Everything (Background Mode)
```bash
./start.sh
```

**What it does:**
- Starts backend API on port 8000
- Starts frontend dev server on port 5173
- Runs both in background
- Creates log files (backend.log, frontend.log)
- Shows URLs to access
- Press Ctrl+C to stop both

**Output:**
```
🚀 Starting Resorto...
📦 Starting Backend API...
📦 Starting Frontend Dev Server...

✅ Resorto is running!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Backend API:      http://localhost:8000
API Docs:         http://localhost:8000/docs
Frontend:         http://localhost:3000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Logs:
   Backend:  tail -f backend.log
   Frontend: tail -f frontend.log

Press Ctrl+C to stop both servers
```

### 2. Development Mode (Live Logs)
```bash
./dev.sh
```

**What it does:**
- Starts both backend and frontend
- Shows live output from both services
- Hot reload enabled
- Press Ctrl+C to stop both

**Best for:** Active development when you want to see logs

### 3. Stop Everything
```bash
./stop.sh
```

**What it does:**
- Stops backend (uvicorn process)
- Stops frontend (vite process)
- Cleans up log files
- Safe to run anytime

**Output:**
```
🛑 Stopping Resorto...
✅ Backend stopped (PID: 12345)
✅ Frontend stopped (PID: 12346)
🗑️  Cleaned backend.log
🗑️  Cleaned frontend.log

✅ Resorto stopped successfully
```

## 📋 Prerequisites

Before running scripts, ensure:

1. **Backend Virtual Environment:**
   ```bash
   cd backend
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

2. **Backend Environment Variables:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your MongoDB URI and Razorpay keys
   ```

3. **Frontend Dependencies:**
   ```bash
   cd frontend
   npm install
   ```

## 🎯 Quick Start Workflow

**First time setup:**
```bash
# 1. Setup backend
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
cd ..

# 2. Setup frontend
cd frontend
npm install
cd ..

# 3. Start everything
./start.sh
```

**Daily development:**
```bash
# Start in background
./start.sh

# Or start with live logs
./dev.sh

# When done
./stop.sh
```

## 📝 Viewing Logs

**If using start.sh (background mode):**
```bash
# Watch backend logs
tail -f backend.log

# Watch frontend logs
tail -f frontend.log

# Watch both in separate terminals
# Terminal 1:
tail -f backend.log

# Terminal 2:
tail -f frontend.log
```

**If using dev.sh:**
Logs are shown directly in the terminal

## 🔧 Troubleshooting

### "Backend virtual environment not found"
```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### "Frontend dependencies not installed"
```bash
cd frontend
npm install
```

### Port already in use
```bash
# Stop any running processes
./stop.sh

# Or manually find and kill
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

### Can't execute script
```bash
chmod +x start.sh stop.sh dev.sh
```

## 🌐 Access Points

Once started, access:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## ⚡ Pro Tips

1. **Use dev.sh during active development** - See logs immediately
2. **Use start.sh when running in background** - Clean terminal
3. **Always use stop.sh before restarting** - Prevents port conflicts
4. **Check logs if something fails** - `tail -f backend.log` or `tail -f frontend.log`

## 🎨 Script Features

✅ **Automatic checks** - Verifies dependencies before starting  
✅ **Color output** - Easy to read status messages  
✅ **Clean shutdown** - Ctrl+C stops both services gracefully  
✅ **Log management** - Separate logs for backend and frontend  
✅ **Error handling** - Clear error messages if something is missing  
✅ **Process management** - Properly tracks and kills processes  

## 📊 What Each Script Does

| Script | Background | Live Logs | Auto-cleanup |
|--------|-----------|-----------|--------------|
| `start.sh` | ✅ Yes | ❌ No (use tail) | ✅ Yes |
| `dev.sh` | ❌ No | ✅ Yes | ✅ Yes |
| `stop.sh` | - | - | ✅ Yes |

## 🎯 Recommended Usage

**For Development:**
```bash
./dev.sh  # See everything happening
```

**For Testing:**
```bash
./start.sh  # Run in background, test in browser
```

**To Stop:**
```bash
./stop.sh  # Or just Ctrl+C if using dev.sh
```

---

**That's it! You can now start Resorto with a single command!** 🚀
