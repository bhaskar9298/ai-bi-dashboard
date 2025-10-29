# 🔧 Troubleshooting Guide

Common issues and their solutions for the AI BI Dashboard.

## 🚨 Backend Issues

### Issue: MongoDB Connection Failed

**Error Message:**
```
❌ MongoDB connection failed: ServerSelectionTimeoutError
```

**Solutions:**

1. **Check if MongoDB is running:**
   ```bash
   # On Windows
   net start MongoDB
   
   # On Mac/Linux
   sudo systemctl status mongod
   # or
   brew services list
   ```

2. **Verify connection string:**
   ```bash
   # Check .env file
   cat backend/.env | grep MONGODB_URI
   
   # Should be: mongodb://localhost:27017/
   ```

3. **Test MongoDB connection:**
   ```bash
   mongosh
   # or
   mongo
   ```

4. **Check firewall:**
   - Ensure port 27017 is not blocked
   - Disable firewall temporarily to test

---

### Issue: LLM API Key Not Working

**Error Message:**
```
ValueError: GOOGLE_API_KEY not found in environment
```

**Solutions:**

1. **Verify .env file exists:**
   ```bash
   ls backend/.env
   ```

2. **Check API key is set:**
   ```bash
   cat backend/.env | grep API_KEY
   ```

3. **Get a new API key:**
   - Gemini: https://makersuite.google.com/app/apikey
   - OpenAI: https://platform.openai.com/api-keys

4. **Update .env file:**
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   LLM_PROVIDER=gemini
   ```

5. **Restart the backend:**
   ```bash
   # Kill existing process
   pkill -f "python app.py"
   
   # Start again
   python app.py
   ```

---

### Issue: No Data in Database

**Error Message:**
```
✅ Query executed: 0 records returned
```

**Solutions:**

1. **Generate mock data:**
   ```bash
   cd backend
   python generate_mock_db.py
   ```

2. **Verify data was inserted:**
   ```bash
   mongosh
   use bi_dashboard
   db.sales.countDocuments()
   # Should return 1000
   ```

3. **Check collection name:**
   ```bash
   # In .env file
   MONGODB_COLLECTION=sales
   ```

---

### Issue: Query Agent Generates Invalid Pipeline

**Error Message:**
```
❌ Query execution failed: Invalid pipeline stage
```

**Solutions:**

1. **Check LLM temperature:**
   - In `query_agent.py`, verify temperature is set to 0.1
   
2. **Improve prompt:**
   - Add more examples to the prompt template
   - Be more specific in your natural language query

3. **Test with simpler queries:**
   ```python
   # Try these first:
   "show total sales by category"
   "count of products"
   ```

4. **Check LLM response:**
   - Enable debug mode in .env: `DEBUG=True`
   - Check terminal output for raw LLM responses

---

## 🎨 Frontend Issues

### Issue: Cannot Connect to Backend

**Error Message:**
```
Network Error / Failed to fetch
```

**Solutions:**

1. **Verify backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check CORS settings:**
   - In `backend/app.py`, verify frontend URL is in allowed origins

3. **Check API URL in frontend:**
   ```bash
   cat frontend/.env
   # Should be: REACT_APP_API_URL=http://localhost:8000
   ```

4. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

---

### Issue: Charts Not Displaying

**Error Message:**
```
No visualization available
```

**Solutions:**

1. **Check Plotly installation:**
   ```bash
   cd backend
   pip show plotly
   ```

2. **Verify data structure:**
   - Check browser console for errors
   - Inspect the API response in Network tab

3. **Try different chart types:**
   - Some data structures work better with specific charts

4. **Reinstall frontend dependencies:**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

---

### Issue: Build Errors

**Error Message:**
```
Module not found: Can't resolve 'react-plotly.js'
```

**Solutions:**

1. **Install missing dependencies:**
   ```bash
   cd frontend
   npm install react-plotly.js plotly.js
   ```

2. **Clear npm cache:**
   ```bash
   npm cache clean --force
   npm install
   ```

3. **Check Node version:**
   ```bash
   node --version
   # Should be 16.x or higher
   ```

---

## 🐛 Common Runtime Errors

### Issue: Port Already in Use

**Error Message:**
```
Error: Address already in use (Port 8000)
```

**Solutions:**

1. **Find and kill process:**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # Mac/Linux
   lsof -ti:8000 | xargs kill -9
   ```

2. **Use different port:**
   ```env
   # In backend/.env
   BACKEND_PORT=8001
   ```

---

### Issue: ModuleNotFoundError

**Error Message:**
```
ModuleNotFoundError: No module named 'langchain'
```

**Solutions:**

1. **Activate virtual environment:**
   ```bash
   # Windows
   backend\venv\Scripts\activate
   
   # Mac/Linux
   source backend/venv/bin/activate
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check Python version:**
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

---

### Issue: Slow Query Performance

**Symptoms:**
- Queries taking more than 10 seconds
- Timeout errors

**Solutions:**

1. **Create MongoDB indexes:**
   ```javascript
   mongosh
   use bi_dashboard
   db.sales.createIndex({ category: 1 })
   db.sales.createIndex({ region: 1 })
   db.sales.createIndex({ date: -1 })
   ```

2. **Reduce dataset size:**
   ```python
   # In generate_mock_db.py, change:
   generate_mock_sales_data(100)  # Instead of 1000
   ```

3. **Optimize aggregation pipeline:**
   - Add $match stages early
   - Use $project to limit fields
   - Add $limit for large results

---

## 🔍 Debugging Tips

### Enable Debug Mode

1. **Backend logging:**
   ```env
   # In backend/.env
   DEBUG=True
   ```

2. **Check terminal output:**
   - Backend prints detailed logs for each step
   - Look for 🤖, 📋, ⚡, 📊 emoji markers

3. **Frontend debugging:**
   ```javascript
   // Open browser console (F12)
   // Check Network tab for API calls
   // Check Console tab for errors
   ```

### Test Individual Components

1. **Test MongoDB:**
   ```bash
   python -c "from utils.mongo_connector import mongo_connector; print(mongo_connector.count_documents())"
   ```

2. **Test Query Agent:**
   ```bash
   python -c "from agents.query_agent import query_agent; from utils.mongo_connector import mongo_connector; schema = mongo_connector.get_collection_schema(); print(query_agent.generate_pipeline('test query', schema))"
   ```

3. **Test API:**
   ```bash
   curl -X POST http://localhost:8000/generate_chart \
     -H "Content-Type: application/json" \
     -d '{"prompt": "show sales by category"}'
   ```

---

## 📞 Getting Help

If issues persist:

1. **Check logs:**
   - Backend: Terminal where `python app.py` is running
   - Frontend: Browser console (F12)
   - MongoDB: Check MongoDB logs

2. **Run test script:**
   ```bash
   cd backend
   python test_api.py
   ```

3. **Verify environment:**
   ```bash
   # Check all environment variables
   cat backend/.env
   
   # Check installed packages
   pip list
   npm list
   ```

4. **Clean installation:**
   ```bash
   # Backend
   rm -rf backend/venv
   python -m venv backend/venv
   source backend/venv/bin/activate
   pip install -r backend/requirements.txt
   
   # Frontend
   rm -rf frontend/node_modules
   npm install
   ```

---

## ✅ Health Check Checklist

Before reporting an issue, verify:

- [ ] MongoDB is running
- [ ] Backend server is running on port 8000
- [ ] Frontend is running on port 3000
- [ ] .env file exists with valid API keys
- [ ] Mock data is generated (1000 records)
- [ ] No firewall blocking ports
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Virtual environment activated

---

**Still having issues?** Create a detailed bug report with:
- Error messages (full stack trace)
- Steps to reproduce
- Environment details (OS, Python version, Node version)
- Screenshots if applicable
