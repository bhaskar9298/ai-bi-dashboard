# 📋 Quick Reference Guide

Essential commands and information for the AI BI Dashboard.

## 🚀 Quick Start Commands

### First Time Setup
```bash
# 1. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API key

# 2. Generate data
python generate_mock_db.py

# 3. Start backend
python app.py
```

### Start Frontend
```bash
cd frontend
npm install
npm start
```

### All-in-One (Use startup scripts)
```bash
# Windows
start.bat

# Mac/Linux
chmod +x start.sh
./start.sh
```

---

## 📡 API Endpoints

### Base URL
```
http://localhost:8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/schema` | Get collection schema |
| POST | `/generate_chart` | Main NL query endpoint |
| POST | `/execute_pipeline` | Execute custom pipeline |
| GET | `/collections` | List all collections |

### Example Request
```bash
curl -X POST http://localhost:8000/generate_chart \
  -H "Content-Type: application/json" \
  -d '{"prompt": "show total sales by category"}'
```

---

## 🗂️ Project Structure

```
ai-bi-dashboard/
├── backend/                    # Python FastAPI backend
│   ├── agents/                # AI agent modules
│   │   ├── query_agent.py    # NL → MongoDB
│   │   ├── visualization_agent.py  # Chart selection
│   │   └── orchestration_agent.py  # Workflow
│   ├── utils/                # Utilities
│   │   └── mongo_connector.py
│   ├── app.py                # Main FastAPI app
│   ├── generate_mock_db.py   # Data generator
│   └── requirements.txt      # Python deps
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.js           # Main component
│   │   └── components/
│   │       └── ChartView.js  # Visualization
│   └── package.json         # Node deps
└── README.md                 # Documentation
```

---

## 🔑 Environment Variables

### Backend (.env)
```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=bi_dashboard
MONGODB_COLLECTION=sales

# LLM (Choose one)
GOOGLE_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here
LLM_PROVIDER=gemini

# Server
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
DEBUG=True
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 💬 Example Natural Language Queries

### Aggregations
- "show total sales by category"
- "sum of revenue by region"
- "average price per product"
- "count of orders by status"

### Time-Based
- "sales by quarter"
- "monthly revenue trend"
- "yearly comparison"

### Rankings
- "top 5 products by revenue"
- "best performing regions"
- "highest selling categories"

### Distributions
- "sales distribution by region"
- "breakdown by category"
- "percentage split"

---

## 🗄️ MongoDB Quick Reference

### Connect to MongoDB
```bash
mongosh
# or
mongo
```

### Common Commands
```javascript
// Switch database
use bi_dashboard

// Count documents
db.sales.countDocuments()

// View sample data
db.sales.findOne()

// Show all documents
db.sales.find().limit(5)

// Create index
db.sales.createIndex({ category: 1 })

// Drop collection
db.sales.drop()

// Show collections
show collections
```

---

## 🧪 Testing

### Run Test Suite
```bash
cd backend
python test_api.py
```

### Test Individual Components
```bash
# Test MongoDB
python -c "from utils.mongo_connector import mongo_connector; print(mongo_connector.count_documents())"

# Test API
curl http://localhost:8000/health

# Test Query
curl -X POST http://localhost:8000/generate_chart \
  -H "Content-Type: application/json" \
  -d '{"prompt": "total sales by category"}'
```

---

## 🐛 Common Issues

### Backend won't start
```bash
# Check if port is in use
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows

# Check MongoDB is running
mongosh

# Verify .env file exists
ls backend/.env
```

### Frontend won't connect
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check frontend .env
cat frontend/.env

# Clear cache
rm -rf frontend/node_modules
npm install
```

### No data returned
```bash
# Regenerate mock data
python backend/generate_mock_db.py

# Verify data exists
mongosh
use bi_dashboard
db.sales.countDocuments()
```

---

## 🔧 Useful Scripts

### Reset Everything
```bash
# Drop database
mongosh --eval "use bi_dashboard; db.dropDatabase()"

# Regenerate data
python backend/generate_mock_db.py

# Restart backend
pkill -f "python app.py"
python backend/app.py
```

### Update Dependencies
```bash
# Backend
pip install --upgrade -r backend/requirements.txt

# Frontend
cd frontend
npm update
```

### Clear Caches
```bash
# Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# npm cache
npm cache clean --force
```

---

## 📊 Agent Workflow

```
User Query → Orchestration Agent
              ↓
         1. Fetch Schema (MongoDB)
              ↓
         2. Generate Query (LLM)
              ↓
         3. Execute Query (MongoDB)
              ↓
         4. Create Visualization (LLM + Plotly)
              ↓
         Response (JSON)
```

---

## 🎯 Performance Tips

1. **Create indexes** on frequently queried fields
2. **Limit results** in queries (add `$limit` stage)
3. **Use $match early** in aggregation pipelines
4. **Enable caching** for repeated queries
5. **Monitor LLM API usage** and costs

---

## 📚 Key Files to Modify

### Add New Chart Types
- `backend/agents/visualization_agent.py`
- Update `CHART_TYPES` list
- Add case in `create_plotly_figure()`

### Change Database Schema
- `backend/generate_mock_db.py`
- Modify `generate_mock_sales_data()`
- Regenerate data

### Customize Prompts
- `backend/agents/query_agent.py`
- Edit `_create_prompt_template()`
- Add more examples

### Modify UI
- `frontend/src/App.js` - Main layout
- `frontend/src/components/ChartView.js` - Visualization
- `frontend/src/App.css` - Styling

---

## 🔐 Security Checklist

- [ ] API keys in .env (never commit)
- [ ] CORS configured correctly
- [ ] MongoDB authentication enabled (production)
- [ ] Rate limiting added
- [ ] Input validation implemented
- [ ] HTTPS enabled (production)

---

## 📦 Deployment Checklist

- [ ] Environment variables set
- [ ] MongoDB production URI
- [ ] DEBUG=False
- [ ] Dependencies installed
- [ ] Indexes created
- [ ] Health check passing
- [ ] CORS configured for prod domain
- [ ] Logging configured
- [ ] Monitoring set up

---

## 🆘 Support

### Check These First
1. README.md - Full documentation
2. TROUBLESHOOTING.md - Common issues
3. ROADMAP.md - Future features
4. Terminal logs - Detailed error messages

### Debug Mode
```env
DEBUG=True  # In backend/.env
```

### Logs Location
- Backend: Terminal output
- Frontend: Browser console (F12)
- MongoDB: System logs

---

## 📈 Monitoring

### Health Check
```bash
watch -n 5 curl -s http://localhost:8000/health | jq
```

### MongoDB Stats
```javascript
db.sales.stats()
db.sales.aggregate([
  { $group: { _id: null, total: { $sum: "$amount" } } }
])
```

### API Performance
```bash
# Add timing
time curl -X POST http://localhost:8000/generate_chart \
  -H "Content-Type: application/json" \
  -d '{"prompt": "total sales"}'
```

---

**Last Updated**: October 2025
**Version**: 1.0.0
