# 🚨 URGENT FIX - Method Signature Error

## Error
```
OrchestrationAgent.process_query() takes 2 positional arguments but 3 were given
```

## Root Cause
Python is loading **cached bytecode** (.pyc files) from the old version of the code. Even though the source files are correct, the running server is using old compiled Python files.

## ✅ COMPLETE FIX (Follow These Steps)

### Option 1: Automated Fix (Recommended)

#### On Windows:
```cmd
cd C:\Users\Lenovo\Desktop\ai-bi-dashboard\backend

# Run the complete fix script
complete_fix.bat
```

This will:
1. Kill any running Python processes
2. Clean all cache files
3. Run diagnostics
4. Optionally start the server

### Option 2: Manual Fix (Step by Step)

#### Step 1: Stop the Server
Press `Ctrl+C` in the terminal where the server is running

Or kill all Python processes:
```cmd
# Windows
taskkill /F /IM python.exe

# Linux/Mac
pkill -9 python
```

#### Step 2: Clean All Cache Files
```cmd
cd C:\Users\Lenovo\Desktop\ai-bi-dashboard\backend
python force_clean_restart.py
```

This removes:
- All `__pycache__` directories
- All `.pyc` files

#### Step 3: Run Diagnostic Check
```cmd
python diagnostic_check.py
```

This will show you:
- The actual loaded method signature
- Whether bytecode is still being used
- If the fix is properly applied

#### Step 4: Run Test Script
```cmd
python test_fix.py
```

This tests both calling patterns to confirm the fix.

#### Step 5: Start the Server Fresh
```cmd
python app.py
```

**IMPORTANT**: Start from a **fresh terminal** if possible!

#### Step 6: Test the Endpoint
```cmd
curl -X POST http://localhost:8000/generate_chart ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Show analysis of american express reconciliation\"}"
```

## 🔍 Understanding the Fix

### What Changed in Code

**File: `backend/app.py` (Line ~531)**

**BEFORE (causes error):**
```python
result = orchestration_agent.process_query(request.prompt, collection=request.collection)
```

**AFTER (correct):**
```python
result = orchestration_agent.process_query(
    query=request.prompt,
    collection=request.collection
)
```

### Why This Matters

The method signature is:
```python
def process_query(self, query: str, collection: Optional[str] = None) -> Dict[str, Any]:
```

When you call it on an instance:
```python
orchestration_agent.process_query(...)
```

Python automatically passes:
1. `self` (the instance) - **automatic**
2. `query` - first parameter
3. `collection` - second parameter

By using explicit parameter names (`query=...`), we ensure Python knows exactly where each argument goes.

## 🚫 Why Just Editing Files Isn't Enough

Python compiles `.py` files to `.pyc` bytecode files for performance. These are stored in `__pycache__` directories. When you:

1. Edit `app.py`
2. Restart the server with `Ctrl+C` and `python app.py`

Python might **still load the old .pyc files** if:
- The modification time isn't updated correctly
- The files are cached in memory
- The process wasn't fully killed

That's why you MUST:
1. **Kill the process completely**
2. **Delete all cache files**
3. **Start fresh**

## 🧪 Verification Steps

After the fix, you should see:

### 1. Diagnostic Check Output
```
✅ Successfully imported orchestration_agent
📋 Method Signature:
   process_query(query: str, collection: Optional[str] = None)
```

### 2. Test Script Output
```
Test 2: Call with keyword arguments (NEW WAY - SHOULD WORK)
   ✅ Succeeded!
```

### 3. Server Startup
```
🚀 Reconciliation DataFlow Dashboard Agent (Multi-Collection)
✅ MongoDB connected: X collections available
✅ API is ready to accept requests
```

### 4. API Call Response
```json
{
  "success": true,
  "query": "Show analysis of american express reconciliation",
  "data": [...],
  "chart_config": {...},
  "plotly_figure": {...}
}
```

## ⚠️ If Still Not Working

### Check 1: Python Process
Make sure NO Python processes are running:
```cmd
# Windows
tasklist | findstr python.exe

# Linux/Mac
ps aux | grep python
```

If you see any, kill them:
```cmd
# Windows (use PID from tasklist)
taskkill /F /PID <pid>

# Linux/Mac
kill -9 <pid>
```

### Check 2: Verify File Contents
```cmd
# Check app.py has the fix
findstr /C:"query=request.prompt" app.py
```

Should output:
```
            query=request.prompt,
```

### Check 3: Check Import Path
Run:
```python
python diagnostic_check.py
```

Look for:
```
📁 Source File:
   C:\Users\Lenovo\Desktop\ai-bi-dashboard\backend\agents\orchestration_agent.py
```

If it shows a `.pyc` file path, cache wasn't properly cleared!

### Check 4: Virtual Environment
Make sure you're using the correct virtual environment:
```cmd
# Activate venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Verify
where python  # Windows
which python  # Linux/Mac
```

Should point to the venv Python, not system Python.

## 📝 Alternative: Nuclear Option

If nothing else works, delete EVERYTHING and start fresh:

```cmd
cd C:\Users\Lenovo\Desktop\ai-bi-dashboard\backend

# 1. Kill all Python
taskkill /F /IM python.exe

# 2. Delete all cache recursively
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

# 3. Delete virtual environment
rd /s /q .venv
rd /s /q venv

# 4. Recreate venv
python -m venv .venv
.venv\Scripts\activate

# 5. Reinstall dependencies
pip install -r requirements.txt

# 6. Start server
python app.py
```

## 📞 Debug Logging

If you want to see exactly what's being called, add this to `app.py` before the orchestration call:

```python
# Add this right before the process_query call
import inspect
sig = inspect.signature(orchestration_agent.process_query)
print(f"DEBUG: Method signature: {sig}")
print(f"DEBUG: Calling with query='{request.prompt}', collection='{request.collection}'")
```

This will show in the server logs what signature is being used.

## ✅ Success Checklist

- [ ] All Python processes killed
- [ ] All `__pycache__` deleted
- [ ] All `.pyc` files deleted
- [ ] Diagnostic check passes
- [ ] Test script passes
- [ ] Server starts without errors
- [ ] API call returns success
- [ ] No "takes 2 positional arguments but 3 were given" error

## 🎯 Quick Command Reference

```cmd
# Complete fix in one go (Windows)
cd C:\Users\Lenovo\Desktop\ai-bi-dashboard\backend
taskkill /F /IM python.exe
python force_clean_restart.py
python diagnostic_check.py
python app.py

# Test
curl -X POST http://localhost:8000/generate_chart -H "Content-Type: application/json" -d "{\"prompt\":\"test\"}"
```

---

**Last Updated**: 2025-11-06
**Status**: Fix applied, cache cleaning required
