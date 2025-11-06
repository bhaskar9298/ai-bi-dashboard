# 🔥 QUICK FIX GUIDE

## The Problem
```
❌ OrchestrationAgent.process_query() takes 2 positional arguments but 3 were given
```

## The Solution (3 Steps)

### 1️⃣ Run the One-Click Fix
```cmd
cd C:\Users\Lenovo\Desktop\ai-bi-dashboard\backend
python one_click_fix.py
```

This automatically:
- ✅ Kills running Python processes
- ✅ Deletes all Python cache files
- ✅ Verifies the code fix is in place
- ✅ Runs diagnostic tests
- ✅ Optionally starts your server

### 2️⃣ Start Your Server (if not auto-started)
```cmd
python app.py
```

### 3️⃣ Test It Works
```cmd
curl -X POST http://localhost:8000/generate_chart ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Show analysis of american express reconciliation\"}"
```

---

## ⚡ Even Faster (One Command)

Just run this and press 'y' when asked:
```cmd
python one_click_fix.py
```

---

## 🎯 What Gets Fixed

**Before (broken):**
```python
orchestration_agent.process_query(request.prompt, collection=request.collection)
```

**After (working):**
```python
orchestration_agent.process_query(
    query=request.prompt,
    collection=request.collection
)
```

---

## ✅ Success Indicators

You'll know it worked when:

1. **No errors in the curl response**
2. **You see this in server logs:**
   ```
   🚀 Processing Query: 'Show analysis of american express reconciliation'
   📋 Step 1: Fetching collection schema...
   ✅ Schema fetched
   ```
3. **Response includes data and chart_config**

---

## 🆘 If Still Broken

Run this command sequence:
```cmd
taskkill /F /IM python.exe
timeout /t 3
python one_click_fix.py
```

Or check the full guide: `URGENT_FIX_README.md`

---

## 📋 Script Reference

| Script | Purpose |
|--------|---------|
| `one_click_fix.py` | ⭐ Run this first - does everything |
| `force_clean_restart.py` | Cleans cache only |
| `diagnostic_check.py` | Shows method signature |
| `test_fix.py` | Tests if fix works |
| `complete_fix.bat` | Windows batch version |

---

**The golden rule:** Always run `one_click_fix.py` after code changes! 🚀
