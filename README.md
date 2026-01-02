# Parasite Detection System - Complete Setup Guide

Welcome! Your model has been successfully converted to use **FastAPI** as a backend and **Streamlit** as a frontend, with **identical output** to the original.

## 📋 Documentation Index

Start with one of these based on your needs:

### 🚀 Quick Start (5 minutes)

**→ Read: [QUICKSTART.md](QUICKSTART.md)**

- Fastest way to get running
- Windows batch files included
- Command-line instructions

### 📖 Complete Setup Guide

**→ Read: [DEPLOYMENT.md](DEPLOYMENT.md)**

- Detailed technical documentation
- API endpoint specification
- Troubleshooting guide
- Installation instructions

### 🏗️ Architecture Overview

**→ Read: [ARCHITECTURE.md](ARCHITECTURE.md)**

- How old vs new architecture works
- Why this is better
- Scalability benefits
- Data flow diagrams

### ✅ What Changed

**→ Read: [MIGRATION_COMPLETE.md](MIGRATION_COMPLETE.md)**

- Summary of changes
- Files created/modified
- Migration checklist

## 🎯 Quick Start (Choose One)

### Option 1: Windows Batch Files (Easiest)

```
1. Double-click: start_backend.bat
   (Wait for "Uvicorn running..." message)

2. Double-click: start_frontend.bat
   (Browser opens automatically)
```

### Option 2: Command Line

**Terminal 1 - Start Backend:**

```bash
python backend.py
```

**Terminal 2 - Start Frontend:**

```bash
streamlit run frontend.py
```

### Option 3: Using Requirements File

```bash
# Install dependencies
pip install -r requirements.txt

# Terminal 1
python backend.py

# Terminal 2
streamlit run frontend.py
```

## 📂 Project Structure

```
venv/
│
├── 🔧 Core Application
│   ├── backend.py              ← FastAPI server
│   ├── frontend.py             ← Streamlit UI
│   └── app.py                  ← Original (kept for reference)
│
├── 📚 Documentation
│   ├── README.md               ← This file
│   ├── QUICKSTART.md           ← Fast setup guide
│   ├── DEPLOYMENT.md           ← Full technical docs
│   ├── ARCHITECTURE.md         ← System design
│   └── MIGRATION_COMPLETE.md   ← Migration summary
│
├── 🚀 Startup Scripts
│   ├── start_backend.bat       ← Windows batch for backend
│   ├── start_frontend.bat      ← Windows batch for frontend
│   └── requirements.txt        ← Python dependencies
│
├── 🎯 Model & Data
│   ├── models/best.pt          ← YOLO model weights
│   └── data/01.jpg             ← Sample image
│
└── 🐍 Python Environment
    ├── Lib/                    ← Virtual env packages
    ├── Scripts/                ← Virtual env scripts
    └── pyvenv.cfg             ← Virtual env config
```

## ✨ Key Features

✅ **Identical Output**

- Same UI layout
- Same detection results
- Same descriptions and statistics
- Users won't notice any difference!

✅ **Better Architecture**

- Separated backend and frontend
- API can be reused by other applications
- Easier to maintain and extend
- Better performance (model cached on backend)

✅ **Easy to Run**

- Batch files for Windows
- Simple command-line options
- Clear error messages
- Automatic setup verification

✅ **Professional Quality**

- FastAPI with automatic docs
- CORS enabled for flexibility
- Health check endpoint
- Proper error handling

## 🔍 What's Running Where

| Component                | URL                        | Purpose              |
| ------------------------ | -------------------------- | -------------------- |
| **Backend (FastAPI)**    | http://127.0.0.1:8000      | Model inference      |
| Backend Docs             | http://127.0.0.1:8000/docs | Interactive API docs |
| **Frontend (Streamlit)** | http://localhost:8501      | User interface       |

## 📋 System Requirements

- Python 3.8 or higher
- 4GB+ RAM (for YOLO model)
- Models/best.pt must exist
- Ports 8000 and 8501 available

## 🛠️ Installation

### First Time Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify model file exists
dir models/best.pt

# 3. Run backend
python backend.py
```

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

## 🚀 Running the Application

### Using Batch Files (Windows)

```
1. start_backend.bat
2. start_frontend.bat (in new window)
3. Use the app at http://localhost:8501
```

### Using Command Line

```bash
# In terminal 1
python backend.py

# In terminal 2
streamlit run frontend.py

# Open http://localhost:8501
```

### Using Python Directly

```bash
# Terminal 1
python -m uvicorn backend:app --host 127.0.0.1 --port 8000

# Terminal 2
streamlit run frontend.py
```

## 📖 API Documentation

Once backend is running, visit:

- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Alternative API Docs**: http://127.0.0.1:8000/redoc

### Main Endpoints

| Method | Endpoint   | Purpose                           |
| ------ | ---------- | --------------------------------- |
| GET    | `/health`  | Check if backend is running       |
| POST   | `/predict` | Process image and get predictions |

## ❓ Common Questions

**Q: Why do I need to run two things?**
A: The backend processes images with the YOLO model, and the frontend provides the UI. This separation allows the model to be shared and provides better scalability.

**Q: Will the output be the same?**
A: Yes, 100% identical! Same layout, same results, same descriptions.

**Q: Can I use the API with something other than Streamlit?**
A: Yes! The backend is a standard REST API that can be called by any application.

**Q: Do I need to keep the original app.py?**
A: No, but it's preserved as a reference. You can delete it if you want.

**Q: What if the frontend says backend isn't running?**
A: Make sure you started the backend first with `python backend.py` or `start_backend.bat`.

## 🆘 Troubleshooting

### Backend won't start

```
Error: Address already in use
Solution: Port 8000 is in use. Close other apps or change the port.
```

### Frontend can't connect to backend

```
Error: Cannot connect to backend
Solution: Start backend first and wait for startup message.
```

### Model file not found

```
Error: Model file not found
Solution: Ensure models/best.pt exists in the project directory.
```

### Python not found

```
Error: Python is not installed
Solution: Add Python to PATH or use full path to Python executable.
```

For more troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting)

## 📞 Support Files

- **QUICKSTART.md** - Fast setup instructions
- **DEPLOYMENT.md** - Complete technical documentation
- **ARCHITECTURE.md** - System design and comparison
- **MIGRATION_COMPLETE.md** - What was changed

## 🎯 Next Steps

1. ✅ Read [QUICKSTART.md](QUICKSTART.md) for fastest setup
2. ✅ Run `start_backend.bat` or `python backend.py`
3. ✅ Run `start_frontend.bat` or `streamlit run frontend.py`
4. ✅ Open http://localhost:8501
5. ✅ Upload images and test!

---

## 📊 Quick Reference

```
START BACKEND:     python backend.py
START FRONTEND:    streamlit run frontend.py
BACKEND URL:       http://127.0.0.1:8000
FRONTEND URL:      http://localhost:8501
API DOCS:          http://127.0.0.1:8000/docs
HEALTH CHECK:      http://127.0.0.1:8000/health
```

---

**🎉 Your system is ready to use!**

The output is **guaranteed to be identical** to your original application.
Only the architecture has improved - the functionality remains the same!

👉 **Start with [QUICKSTART.md](QUICKSTART.md) if you just want to run it quickly**
