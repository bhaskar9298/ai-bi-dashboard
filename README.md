# 📊 Reconciliation DataFlow Dashboard Agent (Prototype 1)

An AI-driven dashboard system that ingests reconciliation JSON data, stores it in MongoDB, and allows natural-language queries to generate interactive analytical charts.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Key Features

### 🚀 Core Capabilities
- **JSON File Upload**: Upload reconciliation data via intuitive web interface
- **Flexible Data Formats**: Supports multiple JSON structures automatically
- **Natural Language Queries**: Ask questions in plain English
- **AI-Powered Analysis**: LangChain agents convert queries to MongoDB aggregations
- **Smart Visualizations**: Automatic chart type selection based on data
- **Real-time Processing**: Fast query execution and visualization
- **Data Management**: Upload, replace, or clear data easily

### 🤖 AI Agent System
- **Query Agent**: Converts natural language to MongoDB pipelines
- **Visualization Agent**: Selects optimal chart types and creates visualizations
- **Orchestration Agent**: Manages the complete workflow using LangGraph

## 📋 Table of Contents

- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Data Upload](#data-upload)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Frontend (React) - Port 3000                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  • JSON File Upload (Drag & Drop / Paste)       │   │
│  │  • Natural Language Query Interface              │   │
│  │  • Plotly Visualizations                         │   │
│  │  • Data Management Controls                      │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │ REST API (CORS Enabled)
┌──────────────────────▼──────────────────────────────────┐
│         Backend (FastAPI) - Port 8000                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Data Ingestion Module                    │   │
│  │  • JSON Validation & Parsing                     │   │
│  │  • Data Enrichment & Metadata                    │   │
│  │  • Index Creation                                │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │      Orchestration Agent (LangGraph)             │   │
│  │                                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │   │
│  │  │  Query   │→ │ Execute  │→ │Visualization │  │   │
│  │  │  Agent   │  │  Agent   │  │    Agent     │  │   │
│  │  └──────────┘  └──────────┘  └──────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │ MongoDB Driver
┌──────────────────────▼──────────────────────────────────┐
│               MongoDB Database                           │
│  • Reconciliation Records Collection                     │
│  • Automatic Indexing                                    │
│  • Enriched with Temporal Metadata                       │
└──────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **MongoDB 4.4+** (local or Atlas)
- **Gemini API Key** or OpenAI API Key

### Step 1: Clone and Setup Backend

```bash
cd ai-bi-dashboard/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env file with your settings
```

**Required `.env` Configuration:**

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=reconciliation_dashboard
MONGODB_COLLECTION=reconciliation_records

# LLM Configuration
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here

# Server
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
DEBUG=True
```

### Step 3: Start MongoDB

```bash
# If using local MongoDB
mongod

# If using MongoDB Atlas, ensure your connection string is in .env
```

### Step 4: Start Backend Server

```bash
cd backend
python app.py
```

You should see:
```
🚀 Reconciliation DataFlow Dashboard Agent (Prototype 1)
✅ MongoDB connected
🤖 LLM Provider: gemini
✅ API is ready to accept requests
📍 Access at: http://localhost:8000
```

### Step 5: Setup and Start Frontend

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

## 📤 Data Upload

### Supported JSON Formats

The system automatically handles multiple JSON structures:

**1. Array of Records:**
```json
[
  {
    "id": "TXN001",
    "date": "2024-01-15",
    "type": "payment",
    "status": "reconciled",
    "amount": 1250.50,
    "source": "Bank A",
    "destination": "Account 123"
  },
  {
    "id": "TXN002",
    "date": "2024-01-16",
    "type": "refund",
    "status": "pending",
    "amount": 320.00
  }
]
```

**2. Object with Records Key:**
```json
{
  "records": [
    { "id": "TXN001", "amount": 1250.50, ... },
    { "id": "TXN002", "amount": 320.00, ... }
  ]
}
```

**3. Object with Data/Reconciliations Key:**
```json
{
  "data": [ ... ],
  "reconciliations": [ ... ],
  "transactions": [ ... ]
}
```

**4. Single Record:**
```json
{
  "id": "TXN001",
  "date": "2024-01-15",
  "amount": 1250.50
}
```

### Upload Methods

#### Method 1: File Upload (Drag & Drop)
1. Click "Upload JSON Data" button
2. Drag and drop your .json file
3. Or click "Choose File" to browse
4. Click "Upload & Ingest"

#### Method 2: Paste JSON Text
1. Click "Upload JSON Data" button
2. Select "Paste JSON" tab
3. Paste your JSON data
4. Click "Upload & Ingest"

#### Method 3: Sample Data
1. Click "Upload JSON Data" button
2. Select "Paste JSON" tab
3. Click "Load Sample Data"
4. Click "Upload & Ingest"

### Data Enrichment

The system automatically enriches your data with:

- **Temporal Features**: `_year`, `_month`, `_quarter`, `_day_of_week`, `_month_name`
- **Ingestion Metadata**: `_ingested_at`, `_ingestion_source`
- **Standardized Dates**: Converts various date formats to datetime objects
- **Numeric Normalization**: Converts amount fields to floats
- **Automatic Indexing**: Creates indexes on key fields for performance

## 💬 Usage Examples

### Example Queries

Once data is uploaded, try these natural language queries:

#### Aggregation Queries
```
"show total amount by status"
"sum of amounts by type"
"count of records by category"
"average transaction amount by region"
```

#### Time-based Queries
```
"reconciliation records by month"
"monthly reconciliation trend"
"transactions by quarter"
"daily reconciliation summary"
```

#### Ranking Queries
```
"top 10 records by amount"
"highest value transactions"
"top 5 sources by total amount"
"largest reconciliation differences"
```

#### Distribution Queries
```
"status distribution breakdown"
"transaction type breakdown"
"amount distribution by category"
"reconciliation status by source"
```

### Example Workflow

1. **Upload Data**:
   - Click "Upload JSON Data"
   - Upload your reconciliation file
   - System confirms: "✅ Upload Successful! 1,234 records inserted"

2. **Check Data Status**:
   - Green badge shows: "✅ Data Loaded: 1,234 records"
   - Available fields are displayed below query section

3. **Query Your Data**:
   - Type: "show total amount by status"
   - System generates visualization automatically
   - View interactive chart with data table

4. **Explore More**:
   - Try example queries
   - Export results as JSON/CSV
   - Upload new data to analyze

## 🔌 API Reference

### Data Ingestion Endpoints

#### `POST /upload-json`
Upload JSON file for ingestion.

**Request:**
- `Content-Type: multipart/form-data`
- `file`: JSON file
- `drop_existing`: boolean (optional, default: false)

**Response:**
```json
{
  "success": true,
  "records_inserted": 1234,
  "indexes_created": ["date", "status", "amount"],
  "statistics": {
    "total_records": 1234,
    "database": "reconciliation_dashboard",
    "collection": "reconciliation_records",
    "fields": ["id", "date", "amount", ...]
  }
}
```

#### `POST /ingest-json-text`
Ingest JSON from text string.

**Request:**
- `Content-Type: application/x-www-form-urlencoded`
- `json_data`: JSON string
- `drop_existing`: boolean (optional)

#### `DELETE /clear-data`
Clear all records from collection.

**Response:**
```json
{
  "success": true,
  "deleted_count": 1234,
  "message": "Deleted 1234 records"
}
```

### Query Endpoints

#### `POST /generate_chart`
Generate visualization from natural language query.

**Request:**
```json
{
  "prompt": "show total amount by status"
}
```

**Response:**
```json
{
  "success": true,
  "query": "show total amount by status",
  "pipeline": [...],
  "data": [...],
  "chart_config": {...},
  "plotly_figure": {...},
  "metadata": {
    "record_count": 5,
    "chart_type": "bar"
  }
}
```

#### `GET /data-source`
Get current data source information.

**Response:**
```json
{
  "has_data": true,
  "record_count": 1234,
  "collection": "reconciliation_records",
  "database": "reconciliation_dashboard",
  "sample_fields": ["id", "date", "amount", "status"]
}
```

#### `GET /schema`
Get collection schema information.

#### `GET /sample-data?limit=5`
Get sample records from collection.

#### `GET /health`
Comprehensive health check.

**Response:**
```json
{
  "api": "healthy",
  "mongodb": "connected",
  "document_count": 1234,
  "llm_provider": "gemini",
  "database": "reconciliation_dashboard",
  "collection": "reconciliation_records"
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/` | Yes |
| `MONGODB_DATABASE` | Database name | `reconciliation_dashboard` | Yes |
| `MONGODB_COLLECTION` | Collection name | `reconciliation_records` | Yes |
| `LLM_PROVIDER` | LLM provider (`gemini` or `openai`) | `gemini` | Yes |
| `GOOGLE_API_KEY` | Gemini API key | - | If using Gemini |
| `OPENAI_API_KEY` | OpenAI API key | - | If using OpenAI |
| `BACKEND_PORT` | Backend server port | `8000` | No |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:3000` | No |
| `DEBUG` | Enable debug mode | `True` | No |

### MongoDB Atlas Setup

For cloud MongoDB:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=reconciliation_dashboard
MONGODB_COLLECTION=reconciliation_records
```

### LLM Provider Setup

**For Gemini (Recommended):**
1. Get API key from: https://makersuite.google.com/app/apikey
2. Set in `.env`:
   ```env
   LLM_PROVIDER=gemini
   GOOGLE_API_KEY=your_api_key_here
   ```

**For OpenAI:**
1. Get API key from: https://platform.openai.com/api-keys
2. Set in `.env`:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_api_key_here
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
    environment:
      - MONGO_INITDB_DATABASE=reconciliation_dashboard

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/
      - MONGODB_DATABASE=reconciliation_dashboard
      - MONGODB_COLLECTION=reconciliation_records
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - LLM_PROVIDER=gemini
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend

volumes:
  mongodb_data:
```

Deploy with:
```bash
docker-compose up -d
```

### Production Checklist

- [ ] Set `DEBUG=False` in backend `.env`
- [ ] Configure proper MongoDB authentication
- [ ] Set specific CORS origins (not `*`)
- [ ] Use environment-specific API keys
- [ ] Enable HTTPS/SSL
- [ ] Set up rate limiting
- [ ] Configure logging and monitoring
- [ ] Set up backups for MongoDB
- [ ] Use production-grade web server (nginx)

## 🐛 Troubleshooting

### Common Issues

#### 1. MongoDB Connection Failed

**Symptoms:**
```
⚠️ MongoDB connection warning: Connection refused
```

**Solutions:**
- Ensure MongoDB is running: `mongod` or check MongoDB service
- Verify connection string in `.env`
- Check MongoDB is accessible on port 27017
- For Atlas: Check IP whitelist and credentials

#### 2. LLM API Errors

**Symptoms:**
```
Error: API key not valid
```

**Solutions:**
- Verify API key in `.env` file
- Check API key has not expired
- Ensure billing is enabled for API
- Check API quota limits

#### 3. No Data Available Error

**Symptoms:**
```
No data available. Please upload JSON data first.
```

**Solutions:**
- Upload JSON data using the Upload button
- Verify upload was successful (green success message)
- Check MongoDB connection is working
- Verify collection name in `.env` matches uploaded data

#### 4. Frontend Not Connecting to Backend

**Symptoms:**
- API calls fail with network errors
- CORS errors in browser console

**Solutions:**
- Verify backend is running on port 8000
- Check `REACT_APP_API_URL` in frontend `.env`
- Ensure CORS is properly configured in backend
- Check firewall/antivirus isn't blocking connections

#### 5. Invalid JSON Format Error

**Symptoms:**
```
Invalid JSON format: Unexpected token
```

**Solutions:**
- Validate JSON using online validator (jsonlint.com)
- Ensure proper quotes (double quotes, not single)
- Check for trailing commas
- Verify file encoding is UTF-8

### Debug Mode

Enable detailed logging:

**Backend:**
```env
DEBUG=True
```

**Check Backend Logs:**
```bash
cd backend
python app.py
# Watch console output for detailed error messages
```

**Test API Endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# Data source info
curl http://localhost:8000/data-source

# Test query
curl -X POST http://localhost:8000/generate_chart \
  -H "Content-Type: application/json" \
  -d '{"prompt": "show total amount by status"}'
```

## 📚 Project Structure

```
ai-bi-dashboard/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── query_agent.py           # NL → MongoDB pipeline
│   │   ├── visualization_agent.py   # Chart type selection
│   │   └── orchestration_agent.py   # LangGraph workflow
│   ├── data_ingestion/
│   │   ├── __init__.py
│   │   └── json_ingester.py         # JSON upload & processing
│   ├── utils/
│   │   ├── __init__.py
│   │   └── mongo_connector.py       # MongoDB operations
│   ├── app.py                       # FastAPI application
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChartView.js        # Visualization component
│   │   │   ├── ChartView.css
│   │   │   ├── DataUpload.js       # Upload component
│   │   │   └── DataUpload.css
│   │   ├── App.js                   # Main application
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env
├── README.md
├── docker-compose.yml
└── .gitignore
```

## 🎓 How It Works

### 1. Data Ingestion Flow

```
JSON File → Validation → Parsing → Enrichment → MongoDB → Indexing
```

- **Validation**: Checks JSON format and structure
- **Parsing**: Extracts records from various JSON structures
- **Enrichment**: Adds temporal features and metadata
- **MongoDB**: Stores enriched documents
- **Indexing**: Creates indexes for performance

### 2. Query Processing Flow

```
Natural Language → Query Agent → MongoDB Pipeline → Execution → 
Visualization Agent → Chart Generation → Display
```

- **Query Agent**: Uses LLM to generate MongoDB aggregation pipeline
- **Execution**: Runs pipeline against MongoDB
- **Visualization Agent**: Analyzes results and selects chart type
- **Display**: Renders interactive Plotly visualization

### 3. AI Agent System

**Orchestration Agent (LangGraph):**
- Manages overall workflow
- Coordinates between agents
- Handles error recovery

**Query Agent:**
- Input: Natural language query + schema
- Processing: LLM generates MongoDB pipeline
- Output: Valid MongoDB aggregation pipeline

**Visualization Agent:**
- Input: Query results + original question
- Processing: Analyzes data structure
- Output: Chart configuration + Plotly figure

## 🔐 Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use environment variables** for all sensitive data
3. **Enable MongoDB authentication** in production
4. **Restrict CORS origins** to specific domains
5. **Implement rate limiting** on API endpoints
6. **Validate all user inputs** before processing
7. **Use HTTPS** in production
8. **Regularly update dependencies** for security patches

## 🤝 Contributing

This is a prototype system designed for learning and extension. Feel free to:

- Add new data enrichment features
- Improve query accuracy
- Enhance visualizations
- Add authentication system
- Implement caching layer
- Add more chart types
- Improve error handling

## 📝 License

MIT License - Free to use for personal and commercial projects

## 🌟 Future Enhancements

- [ ] Multi-file upload support
- [ ] Real-time data updates
- [ ] User authentication & authorization
- [ ] Query history and saved queries
- [ ] Advanced analytics (ML predictions)
- [ ] Data export in multiple formats
- [ ] Custom dashboard creation
- [ ] Scheduled data ingestion
- [ ] Data validation rules
- [ ] Webhook integration

## 💡 Tips & Best Practices

### For Best Query Results:

1. **Be specific** in your queries
   - Good: "show total reconciled amount by month"
   - Avoid: "show data"

2. **Use field names** from your data
   - Check "Available Data Fields" section
   - Reference actual column names

3. **Start simple** then refine
   - First: "total amount by status"
   - Then: "average amount by status for January 2024"

4. **Check data quality** before querying
   - Ensure dates are properly formatted
   - Verify numeric fields are numbers
   - Check for missing values

### For Data Upload:

1. **Prepare your JSON** properly
   - Use consistent field names
   - Include dates in ISO format (YYYY-MM-DD)
   - Ensure numeric fields are not quoted

2. **Start with sample data**
   - Test with small dataset first
   - Verify queries work correctly
   - Then upload full dataset

3. **Use meaningful field names**
   - Good: `transaction_date`, `reconciliation_status`
   - Avoid: `col1`, `field_x`

---

**Built with ❤️ for reconciliation data analysis**

For questions or issues, please check the troubleshooting section or review the application logs.

**Happy Analyzing! 📊✨**
