# 🤖 AI-Driven BI Dashboard

A production-ready, modular Business Intelligence dashboard that converts natural language queries into MongoDB aggregations and visualizations using LLM agents.

![Architecture](https://img.shields.io/badge/Architecture-Microservices%20Ready-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green)

## 🎯 Features

- **Natural Language Queries**: Ask questions in plain English
- **AI-Powered Query Generation**: LangChain agents convert NL to MongoDB pipelines
- **Automatic Visualization**: Smart chart type selection based on data
- **Modular Architecture**: Easily scalable to microservices
- **Real-time Processing**: Fast query execution and visualization
- **Export Capabilities**: Download data as JSON or CSV

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  - Natural Language Input                                │
│  - Plotly Visualizations                                 │
│  - Export Functionality                                  │
└──────────────────────┬──────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────┐
│              Backend (FastAPI)                           │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │      Orchestration Agent (LangGraph)           │    │
│  │                                                 │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │    │
│  │  │  Query   │→ │ Execute  │→ │Visualization │ │    │
│  │  │  Agent   │  │  Agent   │  │    Agent     │ │    │
│  │  └──────────┘  └──────────┘  └──────────────┘ │    │
│  └────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────┘
                       │ MongoDB Driver
┌──────────────────────▼──────────────────────────────────┐
│                    MongoDB Database                      │
│  - Sales Collection                                      │
│  - Indexed for Performance                               │
└──────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB 4.4+ (local or Atlas)
- Gemini API Key or OpenAI API Key

### Step 1: Clone and Setup Backend

```bash
cd ai-bi-dashboard/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys
```

### Step 2: Configure Environment Variables

Edit `backend/.env`:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=bi_dashboard
MONGODB_COLLECTION=sales

# LLM Configuration
GOOGLE_API_KEY=your_gemini_api_key_here
LLM_PROVIDER=gemini

# Server
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
DEBUG=True
```

### Step 3: Generate Mock Data

```bash
cd backend
python generate_mock_db.py
```

This creates 1,000 sample sales records with:
- Categories: Electronics, Clothing, Food, Books, etc.
- Regions: North, South, East, West, Central
- Date range: Last 12 months
- Realistic pricing and quantities

### Step 4: Start Backend Server

```bash
python app.py
```

Backend will be available at `http://localhost:8000`

Test the API:
```bash
curl http://localhost:8000/health
```

### Step 5: Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will open at `http://localhost:3000`

## 📁 Project Structure

```
ai-bi-dashboard/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── query_agent.py          # NL → MongoDB pipeline
│   │   ├── visualization_agent.py   # Chart type selection
│   │   └── orchestration_agent.py   # LangGraph workflow
│   ├── utils/
│   │   ├── __init__.py
│   │   └── mongo_connector.py       # MongoDB operations
│   ├── app.py                       # FastAPI application
│   ├── generate_mock_db.py          # Data generator
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChartView.js        # Visualization component
│   │   │   └── ChartView.css
│   │   ├── App.js                   # Main application
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env
└── README.md
```

## 🧠 Agent System

### 1. Query Agent
- **Input**: Natural language query + collection schema
- **Processing**: Uses LLM to generate MongoDB aggregation pipeline
- **Output**: Valid MongoDB pipeline JSON

### 2. Visualization Agent
- **Input**: Query results + original question
- **Processing**: Analyzes data structure and selects optimal chart type
- **Output**: Chart configuration + Plotly figure

### 3. Orchestration Agent (LangGraph)
- **Workflow**: Schema → Query → Execute → Visualize
- **Benefits**: Clear separation of concerns, easy to debug
- **Extensibility**: Add new nodes for data transformation, caching, etc.

## 📊 Example Queries

Try these natural language queries:

1. **Aggregations**
   - "show total sales by category"
   - "average price per region"
   - "sum of quantities sold by product"

2. **Time-based**
   - "total revenue by quarter"
   - "sales trend over the last 6 months"
   - "monthly sales comparison"

3. **Rankings**
   - "top 5 products by sales amount"
   - "best performing regions"
   - "highest revenue categories"

4. **Distributions**
   - "sales distribution by region"
   - "product category breakdown"
   - "revenue split by quarter"

## 🔧 API Endpoints

### POST `/generate_chart`
Main endpoint for natural language queries.

**Request:**
```json
{
  "prompt": "show total sales by category"
}
```

**Response:**
```json
{
  "success": true,
  "query": "show total sales by category",
  "pipeline": [
    {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
    {"$sort": {"total": -1}}
  ],
  "data": [...],
  "chart_config": {...},
  "plotly_figure": {...},
  "metadata": {
    "record_count": 7,
    "chart_type": "bar"
  }
}
```

### GET `/health`
Health check endpoint.

### GET `/schema`
Get collection schema information.

### POST `/execute_pipeline`
Execute custom MongoDB pipeline.

## 🎨 Customization

### Adding New Chart Types

Edit `backend/agents/visualization_agent.py`:

```python
CHART_TYPES = ['bar', 'line', 'pie', 'scatter', 'area', 'table', 'heatmap']

def create_plotly_figure(self, config):
    # Add your custom chart type
    elif chart_type == 'heatmap':
        fig = px.density_heatmap(...)
```

### Adding New Data Sources

1. Create new collection in MongoDB
2. Update `.env` with collection name
3. Generate schema-specific prompts in `query_agent.py`

### Extending Agent Workflow

Add new nodes to `orchestration_agent.py`:

```python
workflow.add_node("data_cleaning", self.clean_data_node)
workflow.add_node("anomaly_detection", self.detect_anomalies_node)
workflow.add_edge("execute_query", "data_cleaning")
workflow.add_edge("data_cleaning", "anomaly_detection")
```

## 🧪 Testing

### Test Backend

```bash
cd backend

# Test MongoDB connection
python -c "from utils.mongo_connector import mongo_connector; print(mongo_connector.count_documents())"

# Test query generation
python -c "from agents.query_agent import query_agent; from utils.mongo_connector import mongo_connector; schema = mongo_connector.get_collection_schema(); result = query_agent.generate_pipeline('total sales by category', schema); print(result)"
```

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Generate chart
curl -X POST http://localhost:8000/generate_chart \
  -H "Content-Type: application/json" \
  -d '{"prompt": "show total sales by category"}'
```

## 🚢 Deployment

### Docker Deployment

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/
    depends_on:
      - mongodb
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  mongodb_data:
```

### Environment-Specific Configuration

**Development:**
```env
DEBUG=True
MONGODB_URI=mongodb://localhost:27017/
```

**Production:**
```env
DEBUG=False
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
```

## 🔒 Security Considerations

1. **API Keys**: Never commit `.env` files
2. **MongoDB**: Use authentication in production
3. **CORS**: Restrict origins in production
4. **Rate Limiting**: Add rate limiting to API endpoints
5. **Input Validation**: Backend validates all inputs

## 📈 Performance Optimization

1. **MongoDB Indexes**: Created on frequently queried fields
2. **Connection Pooling**: MongoDB connection reused
3. **Caching**: Add Redis for query caching
4. **Async Operations**: FastAPI supports async by default

## 🔄 Scaling to Microservices

This architecture is designed for easy microservice conversion:

```
Service 1: Query Agent (Port 8001)
Service 2: Visualization Agent (Port 8002)
Service 3: Data Execution Service (Port 8003)
API Gateway: Orchestration Layer (Port 8000)
```

Each agent can be deployed independently with its own scaling rules.

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Check MongoDB is running
mongosh

# Check connection string in .env
MONGODB_URI=mongodb://localhost:27017/
```

### LLM API Errors
```bash
# Verify API key
echo $GOOGLE_API_KEY

# Check quota and billing
```

### Frontend Not Connecting
```bash
# Check CORS settings in backend/app.py
# Verify REACT_APP_API_URL in frontend/.env
```

### Empty Results
```bash
# Verify data exists
python backend/generate_mock_db.py

# Check collection name matches
echo $MONGODB_COLLECTION
```

## 📚 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [MongoDB Aggregation](https://docs.mongodb.com/manual/aggregation/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Plotly Documentation](https://plotly.com/python/)

## 🤝 Contributing

This is a prototype designed for learning and extension. Feel free to:
- Add new agent types
- Improve query accuracy
- Enhance visualizations
- Add authentication
- Implement caching

## 📝 License

MIT License - Feel free to use for personal and commercial projects

## 🎓 Next Steps

1. **Phase 6**: Add caching layer (Redis)
2. **Phase 7**: Implement user authentication
3. **Phase 8**: Multi-collection support
4. **Phase 9**: Real-time dashboard updates
5. **Phase 10**: Advanced analytics (ML predictions)

## 💡 Tips for Beginners

1. **Start Simple**: Run the basic setup first
2. **Check Logs**: Backend prints detailed execution logs
3. **Test Endpoints**: Use the `/health` endpoint to verify setup
4. **Modify Examples**: Change example queries to understand the flow
5. **Read Agent Code**: Each agent is well-documented

## 🌟 Key Highlights

- ✅ **Production-Ready**: Error handling, logging, validation
- ✅ **Modular Design**: Easy to extend and maintain
- ✅ **Well-Documented**: Comments in every file
- ✅ **Beginner-Friendly**: Clear separation of concerns
- ✅ **Scalable**: Ready for microservices architecture

---

**Built with ❤️ using Python, React, MongoDB, and AI**

For questions or issues, check the troubleshooting section or review the agent logs in the terminal.
