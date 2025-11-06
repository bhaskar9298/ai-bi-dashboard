# 🎨 Frontend Testing Guide

## ✅ Your Frontend is Ready!

The existing frontend will work with your v2.0 backend for **basic queries**. The new v2.0 features (flow visualization, discrepancy management) will require UI updates, but you can test responses now!

---

## 🚀 Quick Start

### Step 1: Start Backend
```bash
# Terminal 1
cd backend
python app.py
```

**Wait for**:
```
✅ MongoDB connected: X collections available
✅ API is ready to accept requests
📍 Access at: http://localhost:8000
```

### Step 2: Start Frontend
```bash
# Terminal 2 (new terminal)
cd frontend
npm start
```

**Wait for**:
```
Compiled successfully!
You can now view ai-bi-dashboard-frontend in the browser.
Local: http://localhost:3000
```

### Step 3: Open Browser
Navigate to: **http://localhost:3000**

---

## 🧪 What You Can Test

### ✅ Works Out of the Box

1. **Health Check** - Backend status
2. **Data Upload** - Simple JSON files
3. **Natural Language Queries** - Basic questions
4. **Visualizations** - Charts for simple data
5. **Data Source Info** - Collection status

### 🟡 Partially Works (Backend supports, UI needs update)

1. **Multi-Collection Queries** - Backend works, but UI doesn't show collection selector
2. **Flow Data Upload** - Backend endpoint exists, but no UI button
3. **Discrepancy View** - Data available via API, but no dedicated UI
4. **Resolution Tracking** - Backend ready, but no UI workflow

### ❌ Needs UI Development

1. **Flow Visualization** - Complete flow diagram
2. **Discrepancy Management** - Interactive discrepancy resolution
3. **Ticket System** - Workflow management UI
4. **Collection Selector** - Dropdown to choose collection

---

## 📝 Testing Scenarios

### Scenario 1: Test with Simple Data (Legacy Mode)

1. **Upload sample data**
   - Click "Upload JSON" button
   - Select `sample_reconciliation_data.json`
   - Wait for success message

2. **Query the data**
   - Enter: "show all reconciled transactions"
   - Click "Generate Chart"
   - See visualization

3. **Try different queries**
   - "show total amount by status"
   - "show transactions by type"
   - "count records by category"

### Scenario 2: Test Backend API Directly

If frontend has issues, test backend directly:

```bash
# Upload data
curl -X POST http://localhost:8000/upload-json \
  -F "file=@sample_reconciliation_data.json" \
  -F "drop_existing=true"

# Query with visualization
curl -X POST http://localhost:8000/generate_chart \
  -H "Content-Type: application/json" \
  -d '{"prompt": "show all reconciled records"}'

# Response will include:
# - pipeline (MongoDB query)
# - data (results)
# - plotly_figure (chart configuration)
```

### Scenario 3: Test New v2.0 Endpoints (API Only)

These work in backend but don't have UI yet:

```bash
# Get all collections
curl http://localhost:8000/collections

# Get reconciliation flow
curl http://localhost:8000/reconciliation-flow

# Get high severity discrepancies
curl http://localhost:8000/discrepancies?severity=high

# Get matching rules
curl http://localhost:8000/matching-rules
```

---

## 🐛 Troubleshooting

### Frontend won't start
```bash
cd frontend
npm install  # Install dependencies
npm start
```

### Backend connection error
Check `.env` file in frontend:
```
REACT_APP_API_URL=http://localhost:8000
```

Ensure backend is running on port 8000.

### CORS errors
Backend already configured with CORS. If issues persist:
1. Check browser console for exact error
2. Verify backend is running
3. Check firewall settings

### No data showing
1. Upload data first using UI or API
2. Check backend has data: `curl http://localhost:8000/collections`
3. Try refreshing the page

---

## 🎯 What to Expect

### ✅ Will Work
- **Data upload interface** - Upload simple JSON
- **Query input box** - Enter natural language questions
- **Chart display** - See visualizations
- **Error messages** - If something fails
- **Loading states** - While processing

### 🟡 May Look Different
- Collection info might show new collections
- Some responses might have extra data
- New endpoints won't be in UI (use API directly)

### ❌ Won't Work Yet
- Collection dropdown selector
- Flow visualization diagram
- Discrepancy management interface
- Ticket workflow screens
- Resolution document upload

---

## 📊 Expected Frontend Layout

```
┌─────────────────────────────────────────────┐
│  AI-Powered BI Dashboard                    │
├─────────────────────────────────────────────┤
│                                             │
│  📤 Data Source: [Upload JSON] [Status]    │
│                                             │
│  ❓ Query: [____________________] [Submit]  │
│                                             │
│  📊 Visualization:                          │
│  ┌───────────────────────────────────────┐ │
│  │                                       │ │
│  │     [Interactive Chart/Graph]        │ │
│  │                                       │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  📋 Data Preview:                           │
│  [Table showing query results]              │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🔧 Quick Frontend Fixes (If Needed)

If you want to add collection selector quickly:

### Option 1: Add Collection Input (Quick Hack)
In your query component, add:
```javascript
const [collection, setCollection] = useState('');

// In the form
<input 
  value={collection}
  onChange={(e) => setCollection(e.target.value)}
  placeholder="Collection name (optional)"
/>

// When submitting query
const response = await axios.post('/generate_chart', {
  prompt: query,
  collection: collection || null
});
```

### Option 2: Use API Directly with Postman/Insomnia
Download Postman and test all endpoints:
- Easier for testing
- Better visibility of responses
- Can save requests

---

## 📱 Testing with Browser DevTools

1. **Open DevTools** (F12)
2. **Network Tab** - See all API requests
3. **Console Tab** - Check for errors
4. **Look for**:
   - Request URL (should be http://localhost:8000/...)
   - Response Status (should be 200)
   - Response Data (JSON with your results)

---

## ✅ Success Indicators

### Backend is Working If:
- ✅ Health endpoint returns 200
- ✅ Collections endpoint shows data
- ✅ Query returns plotly_figure
- ✅ No 500 errors in responses

### Frontend is Working If:
- ✅ Page loads without errors
- ✅ Upload button is visible
- ✅ Query box is interactive
- ✅ Charts render properly
- ✅ Network requests show in DevTools

---

## 🎓 Pro Tips

1. **Test Simple Queries First**
   - "show all data"
   - "count records"
   - Start basic, then get complex

2. **Use Sample Data**
   - `sample_reconciliation_data.json` is perfect for testing
   - Small, clean, easy to verify

3. **Check Backend Logs**
   - Watch terminal for errors
   - See actual queries being generated

4. **Use Browser DevTools**
   - Inspect network requests
   - Check response payloads
   - Debug JavaScript errors

5. **Keep Both Terminals Visible**
   - Backend terminal: See processing
   - Frontend terminal: See compilation

---

## 📞 Need Help?

### If Frontend Issues:
1. Check browser console for errors
2. Verify backend is running
3. Test backend directly with curl
4. Check CORS settings

### If Backend Issues:
1. Check MongoDB is running
2. Verify .env configuration
3. Look at backend terminal logs
4. Test health endpoint

### If Query Issues:
1. Test with simple queries first
2. Check if data exists in database
3. Try curl command directly
4. Verify query syntax

---

## 🎯 Summary

**You CAN use the frontend NOW for:**
✅ Testing backend responses
✅ Uploading simple JSON data
✅ Running natural language queries
✅ Viewing visualizations
✅ Checking data status

**You CANNOT use frontend for:**
❌ Flow visualization (no UI yet)
❌ Discrepancy management (no UI yet)
❌ Resolution workflow (no UI yet)
❌ Multi-collection selector (no UI yet)

**But ALL of these work via API!** Use curl or Postman for now.

---

## 🚀 Start Testing!

```bash
# Terminal 1
cd backend
python app.py

# Terminal 2
cd frontend
npm start

# Browser
http://localhost:3000
```

**Your system is ready for testing! 🎉**
