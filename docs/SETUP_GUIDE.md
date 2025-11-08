# 🚀 AgroSmart - Complete Setup Guide

This guide will walk you through setting up the AgroSmart application for local demonstration.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Node.js** (v18 or higher) - [Download here](https://nodejs.org/)
- [ ] **Python** (v3.9 or higher) - [Download here](https://www.python.org/)
- [ ] **Git** (optional but recommended)
- [ ] **Terminal/Command Line** access
- [ ] **Code Editor** (VS Code recommended)

### Verify Installations

```bash
# Check Node.js version
node --version
# Should show v18.x.x or higher

# Check npm version
npm --version
# Should show 9.x.x or higher

# Check Python version
python3 --version
# Should show 3.9.x or higher

# Check pip version
pip --version
# Should show pip for Python 3.9+
```

---

## 🎯 Step-by-Step Setup

### Step 1: Get the Project Files

#### Option A: Clone from GitHub
```bash
git clone https://github.com/arindxm/AgroSmart.git
cd AgroSmart
```

#### Option B: You Already Have It
```bash
cd /home/DevCrewX/Desktop/AgroSmart
```

---

### Step 2: Frontend Setup (5 minutes)

```bash
# 1. Install Node.js dependencies
npm install

# Wait for installation to complete...
# You should see "added XXX packages" message

# 2. Create environment file
cp .env.example .env

# 3. Verify installation
npm list --depth=0
# Should show all installed packages
```

**Expected output:**
```
✓ Dependencies installed successfully
✓ Created .env file
```

---

### Step 3: Backend Setup (Next Phase)

The backend will be created in the next steps. For now, just prepare the directory:

```bash
# Create backend directory
mkdir -p backend/api backend/models backend/schemas backend/utils

# Verify structure
ls -la backend/
```

---

### Step 4: Test Frontend (2 minutes)

```bash
# Start development server
npm run dev
```

**Expected output:**
```
  VITE v5.4.2  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Open your browser:**
- Navigate to: http://localhost:5173
- You should see the AgroSmart home page
- Currently uses mock data (we'll connect real backend next)

**Test Navigation:**
- ✓ Click "Start Predicting" button
- ✓ Navigate to Crop Prediction page
- ✓ Try entering some values
- ✓ Click "Predict Crop" (will show mock results)

**Stop the server:** Press `Ctrl+C` in terminal

---

## 🐍 Python Backend Setup (Next Steps)

### Step 1: Create Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows

# Your prompt should now show (venv)
```

### Step 2: Install Python Dependencies (After requirements.txt is created)

```bash
# Will be provided in next steps
pip install -r requirements.txt
```

---

## 🔧 Common Issues & Solutions

### Issue 1: "npm command not found"
**Solution:**
```bash
# Install Node.js from nodejs.org
# Or use nvm (Node Version Manager):
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### Issue 2: "Port 5173 already in use"
**Solution:**
```bash
# Option A: Kill the process
lsof -ti:5173 | xargs kill -9

# Option B: Use different port
npm run dev -- --port 3000
```

### Issue 3: "Python3 not found"
**Solution:**
```bash
# On Linux:
sudo apt update
sudo apt install python3 python3-pip python3-venv

# On Mac (with Homebrew):
brew install python3

# On Windows:
# Download from python.org and run installer
```

### Issue 4: "Permission denied" errors
**Solution:**
```bash
# On Linux/Mac, try without sudo first
# If needed, fix npm permissions:
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

### Issue 5: Slow npm install
**Solution:**
```bash
# Use faster mirror (if in India)
npm config set registry https://registry.npmmirror.com

# Or clear cache and retry
npm cache clean --force
npm install
```

---

## 📂 Project Structure Overview

After complete setup, your project should look like:

```
AgroSmart/
├── backend/              ← We'll create this next
│   ├── venv/            ← Python virtual environment
│   ├── main.py          ← FastAPI entry point
│   ├── requirements.txt  ← Python dependencies
│   └── ...
├── node_modules/         ← Created by npm install
├── src/                 ← React frontend (already done)
├── public/              ← Static assets
├── .env                 ← Your environment config
├── .env.example         ← Template for .env
├── package.json         ← Node dependencies
└── README.md           ← Main documentation
```

---

## ✅ Verification Checklist

After setup, verify everything works:

### Frontend Checklist
- [ ] `npm install` completed without errors
- [ ] `.env` file exists
- [ ] `npm run dev` starts server
- [ ] Browser opens http://localhost:5173
- [ ] Home page loads correctly
- [ ] Navigation works
- [ ] Can access all pages (Crop, Fertilizer, Yield, Dashboard, About)
- [ ] Dark mode toggle works
- [ ] Forms accept input (even if using mock data)

### Backend Checklist (After Setup)
- [ ] Virtual environment created
- [ ] Python dependencies installed
- [ ] `uvicorn main:app --reload` starts server
- [ ] http://localhost:8000/docs shows Swagger UI
- [ ] API endpoints respond
- [ ] Frontend can call backend

---

## 🎬 Next Steps

Now that frontend is set up, we'll:

1. ✅ **Create Backend Structure** - FastAPI application
2. ✅ **Implement API Endpoints** - Crop, Fertilizer, Yield APIs
3. ✅ **Add ML Models** - Prediction logic (rule-based or trained models)
4. ✅ **Connect Frontend to Backend** - Replace mock data with real API calls
5. ✅ **Test Everything** - End-to-end testing
6. ✅ **Polish & Demo** - Ready for demonstration

---

## 📚 Useful Commands Reference

### Frontend Commands
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run typecheck    # Check TypeScript types
```

### Backend Commands (After Setup)
```bash
uvicorn main:app --reload        # Start with auto-reload
uvicorn main:app --port 8000     # Specify port
python -m pytest                 # Run tests
pip freeze > requirements.txt    # Save dependencies
```

### Git Commands (Optional)
```bash
git status                    # Check changes
git add .                     # Stage all changes
git commit -m "message"       # Commit changes
git push                      # Push to remote
```

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the error message** - Read carefully
2. **Search the error** - Google/Stack Overflow
3. **Check this guide** - Troubleshooting section
4. **Verify prerequisites** - Versions and installations
5. **Start fresh** - Delete node_modules and reinstall

---

## 📝 Notes

- This is a **local demonstration** setup
- No cloud services or deployment needed
- Both frontend and backend run on localhost
- Database is optional (can use in-memory data)
- Perfect for learning and showcasing

---

**Ready to proceed with backend setup!** 🚀
