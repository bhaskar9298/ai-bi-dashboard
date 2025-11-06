# 🚀 AI-BI Dashboard - Reconciliation DataFlow System

> **AI-powered reconciliation data analysis platform with multi-collection support and natural language querying**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/bhaskar9298/test-demo-server)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.6+-green.svg)](https://www.mongodb.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-orange.svg)](https://www.langchain.com/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

The **AI-BI Dashboard** is an intelligent reconciliation data analysis platform that combines the power of AI agents with business intelligence to streamline financial reconciliation processes. The system ingests complex reconciliation flows, analyzes discrepancies, and provides actionable insights through natural language queries and interactive visualizations.

### What It Does

- **Automated Data Ingestion**: Upload and process complex reconciliation JSON flows
- **AI-Powered Analysis**: Natural language queries to explore your data
- **Intelligent Matching**: Rule-based reconciliation with customizable matching logic
- **Discrepancy Detection**: Automatic identification and categorization of issues
- **Visual Analytics**: Interactive charts and dashboards powered by Plotly
- **Multi-Collection Support**: Query across multiple data sources simultaneously
- **Resolution Workflows**: Track and manage discrepancy resolution processes

---

## ✨ Key Features

### 🤖 AI & Machine Learning
- **Natural Language Processing**: Query your data using plain English
- **LLM Integration**: Support for Google Gemini and OpenAI
- **Intelligent Agents**: Orchestration, Query, and Visualization agents
- **Smart Suggestions**: AI-powered resolution recommendations

### 📊 Data Management
- **Complex Flow Ingestion**: Import complete reconciliation workflows with nested structures
- **Multi-Collection Support**: Work with multiple data sources simultaneously
- **Dynamic Schema Detection**: Automatic schema inference and validation
- **MongoDB Integration**: Robust NoSQL database with flexible queries

### 📈 Visualization & Reporting
- **Interactive Charts**: Bar charts, line graphs, pie charts, and more
- **Plotly Integration**: Professional, interactive visualizations
- **Custom Dashboards**: Build dashboards tailored to your needs
- **Real-time Updates**: Live data refresh and streaming

### 🔄 Reconciliation Workflows
- **Rule-Based Matching**: Define custom matching rules by vendor type
- **Discrepancy Management**: Track severity, type, and resolution status
- **Ticket System**: Create and manage resolution tickets
- **Audit Trail**: Complete history of reconciliation activities

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Data Upload │  │  Query UI    │  │  Chart View  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │ REST API
┌───────────────────────▼─────────────────────────────────────┐
│                        Backend API                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Orchestration Agent (LangGraph)           │    │
│  │   ┌──────────────┐  ┌──────────────┐  ┌─────────┐ │    │
│  │   │  Query Agent │  │   Viz Agent  │  │  Other  │ │    │
│  │   └──────────────┘  └──────────────┘  └─────────┘ │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────┐  ┌──────────────────────────────┐     │
│  │ Data Ingestion │  │    MongoDB Connector         │     │
│  └────────────────┘  └──────────────────────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      MongoDB Database                       │
│  ┌──────────┐ ┌────────────┐ ┌──────────────┐ ┌────────┐  │
│  │ Matching │ │Discrepancy │ │  Data Tables │ │Tickets │  │
│  │  Rules   │ │            │ │              │ │        │  │
│  └──────────┘ └────────────┘ └──────────────┘ └────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

**Backend (FastAPI + Python)**
- **Agents**: Orchestration, Query, and Visualization agents using LangChain & LangGraph
- **Data Ingestion**: JSON parsers for simple and complex flow structures
- **MongoDB Connector**: Robust database interface with multi-collection support
- **API Endpoints**: RESTful API for all operations

**Frontend (React)**
- **Data Upload**: File upload interface for JSON data
- **Query Interface**: Natural language query input
- **Visualizations**: Interactive charts using Plotly and Recharts
- **Dashboard**: Overview of reconciliation status

**Database (MongoDB)**
- **Collections**: Dynamic collections for matching rules, discrepancies, data sources, tickets, and resolution workflows
- **Indexing**: Optimized indexes for fast queries
- **Aggregation**: Complex aggregation pipelines for analysis

---

## 📦 Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.9+ | Backend runtime |
| Node.js | 14+ | Frontend runtime |
| MongoDB | 4.6+ | Database |
| npm/yarn | Latest | Package management |

### API Keys (Choose One)

- **Google Gemini API Key** (Recommended) - Free tier available
- **OpenAI API Key** - Requires paid account

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/bhaskar9298/test-demo-server.git
cd ai-bi-dashboard
```

### 2. Start MongoDB

```bash
# Windows
net start MongoDB

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### 3. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows CMD:
venv\Scripts\activate
# Windows PowerShell:
venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your API keys

# Start backend server
python app.py
```

Backend will be available at: **http://localhost:8000**

### 4. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
copy .env.example .env
# Edit .env if needed

# Start frontend
npm start
```

Frontend will be available at: **http://localhost:3000**

### 5. Ingest Sample Data

```bash
cd backend
python test_reconciliation_ingestion.py
```

---

## 💻 Installation

### Detailed Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows CMD
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```bash
   copy .env.example .env
   ```

5. **Configure environment variables in `.env`:**
   ```env
   # Database
   MONGODB_URI=mongodb://localhost:27017/
   MONGODB_DATABASE=reconciliation_system
   
   # API Configuration
   BACKEND_PORT=8000
   DEBUG=True
   
   # LLM Provider (choose one)
   LLM_PROVIDER=gemini
   # LLM_PROVIDER=openai
   
   # API Keys
   GOOGLE_API_KEY=your_gemini_api_key_here
   # OPENAI_API_KEY=your_openai_api_key_here
   ```

6. **Verify installation:**
   ```bash
   python test_connection.py
   ```

### Detailed Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env` file:**
   ```bash
   copy .env.example .env
   ```

4. **Configure environment variables:**
   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

5. **Start development server:**
   ```bash
   npm start
   ```

---

## ⚙️ Configuration

### Backend Configuration (`.env`)

```env
# ========================================
# Database Configuration
# ========================================
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=reconciliation_system

# ========================================
# API Configuration
# ========================================
BACKEND_PORT=8000
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]

# ========================================
# LLM Configuration
# ========================================
LLM_PROVIDER=gemini  # Options: gemini, openai
LLM_MODEL=gemini-1.5-flash  # or gpt-4, gpt-3.5-turbo
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2000

# ========================================
# API Keys
# ========================================
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key

# ========================================
# Agent Configuration
# ========================================
MAX_QUERY_RETRIES=3
QUERY_TIMEOUT=30
ENABLE_QUERY_CACHE=True
```

### Frontend Configuration (`.env`)

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENABLE_DEV_TOOLS=true
REACT_APP_MAX_FILE_SIZE=10485760  # 10MB
```

---

## 📖 Usage

### 1. Upload Reconciliation Data

#### Using the API

```bash
# Upload complete reconciliation flow
curl -X POST http://localhost:8000/upload-reconciliation-flow \
  -F "file=@your_reconciliation_data.json" \
  -F "drop_existing=false"
```

#### Using the Frontend

1. Navigate to **http://localhost:3000**
2. Click on **"Upload Data"** tab
3. Select your JSON file
4. Click **"Upload"**
5. Wait for confirmation

### 2. Query Your Data

#### Natural Language Queries

```bash
curl -X POST http://localhost:8000/generate_chart \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Show all American Express discrepancies",
    "collection": "discrepancies"
  }'
```

**Example Queries:**
- "Show all high severity discrepancies"
- "What is the total amount reconciled?"
- "Compare POS data with bank statements"
- "Show reconciliation status by vendor type"
- "List all unresolved issues"

### 3. View Reconciliation Flow

```bash
# Get complete reconciliation flow
curl http://localhost:8000/reconciliation-flow

# Get flow for specific profile
curl "http://localhost:8000/reconciliation-flow?profile_id=PROF001"
```

### 4. Manage Discrepancies

```bash
# Get all discrepancies
curl http://localhost:8000/discrepancies

# Filter by severity
curl "http://localhost:8000/discrepancies?severity=high"
```

### 5. Query Matching Rules

```bash
# Get all matching rules
curl http://localhost:8000/matching-rules

# Filter by vendor
curl "http://localhost:8000/matching-rules?vendor_type=American Express"
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Health & Info Endpoints

#### `GET /`
Get API information and available features.

**Response:**
```json
{
  "service": "Reconciliation DataFlow Dashboard Agent",
  "version": "2.0.0",
  "status": "online",
  "features": [...]
}
```

#### `GET /health`
Detailed health check with MongoDB status.

#### `GET /data-source`
Get current data source information.

### Data Ingestion Endpoints

#### `POST /upload-reconciliation-flow`
Upload complete reconciliation flow JSON file.

**Parameters:**
- `file` (multipart/form-data): JSON file
- `drop_existing` (boolean): Clear existing data (default: false)

**Response:**
```json
{
  "success": true,
  "collections_processed": {
    "matchingrules": 2,
    "discrepancies": 5,
    ...
  },
  "data_tables_created": {
    "pos_data": 1000,
    "bank_data": 950
  }
}
```

#### `POST /upload-json`
Upload simple JSON data (legacy support).

#### `DELETE /clear-data`
Clear data from collections.

**Query Parameters:**
- `collection_name` (optional): Specific collection to clear

### Query Endpoints

#### `POST /generate_chart`
Generate visualization from natural language query.

**Request:**
```json
{
  "prompt": "Show all high severity discrepancies",
  "collection": "discrepancies"
}
```

**Response:**
```json
{
  "success": true,
  "query": "High severity discrepancies",
  "pipeline": [...],
  "data": [...],
  "chart_config": {...},
  "plotly_figure": {...},
  "metadata": {...}
}
```

#### `POST /execute_pipeline`
Execute custom MongoDB aggregation pipeline.

#### `GET /collections`
List all available collections with document counts.

#### `GET /schema?collection=<name>`
Get schema for a specific collection.

#### `GET /sample-data?collection=<name>&limit=5`
Get sample records from a collection.

### Reconciliation Flow Endpoints

#### `GET /reconciliation-flow`
Get complete reconciliation flow.

**Query Parameters:**
- `profile_id` (optional): Filter by profile ID

#### `GET /matching-rules`
Get matching rules.

**Query Parameters:**
- `vendor_type` (optional): Filter by vendor type

#### `GET /discrepancies`
Get discrepancies.

**Query Parameters:**
- `severity` (optional): Filter by severity (high, medium, low)

---

## 📁 Project Structure

```
ai-bi-dashboard/
│
├── backend/                          # Backend application
│   ├── app.py                        # Main FastAPI application
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment configuration
│   ├── Dockerfile                    # Docker configuration
│   │
│   ├── agents/                       # AI agent modules
│   │   ├── orchestration_agent.py   # Main orchestration logic
│   │   ├── query_agent.py           # Query generation agent
│   │   └── visualization_agent.py   # Chart generation agent
│   │
│   ├── data_ingestion/              # Data ingestion modules
│   │   ├── json_ingester.py         # Simple JSON ingestion
│   │   └── reconciliation_flow_ingester.py  # Complex flow ingestion
│   │
│   ├── utils/                       # Utility modules
│   │   ├── mongo_connector.py       # MongoDB operations
│   │   └── Reconciliation Data Flow.json  # Sample data
│   │
│   └── tests/                       # Test files
│       ├── test_connection.py
│       ├── test_api.py
│       └── test_reconciliation_ingestion.py
│
├── frontend/                        # Frontend application
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── App.js                   # Main app component
│   │   ├── index.js                 # Entry point
│   │   │
│   │   └── components/              # React components
│   │       ├── DataUpload.js        # File upload component
│   │       └── ChartView.js         # Visualization component
│   │
│   ├── package.json                 # Node dependencies
│   ├── .env                         # Frontend configuration
│   └── Dockerfile                   # Docker configuration
│
├── docs/                            # Documentation
│   ├── QUICKSTART_V2.md
│   ├── SYSTEM_STATUS.md
│   ├── UPDATED_ARCHITECTURE.md
│   └── VERIFICATION_CHECKLIST.md
│
└── README.md                        # This file
```

---

## 🛠️ Development

### Running in Development Mode

**Backend:**
```bash
cd backend
python app.py
# Backend runs with auto-reload enabled
```

**Frontend:**
```bash
cd frontend
npm start
# Frontend runs with hot-reload
```

### Code Style

**Python (Backend):**
- Follow PEP 8 guidelines
- Use type hints where applicable
- Document functions with docstrings

**JavaScript (Frontend):**
- Use ESLint configuration
- Follow React best practices
- Use functional components with hooks

### Adding New Features

1. **New Agent:**
   - Create agent in `backend/agents/`
   - Inherit from base agent pattern
   - Register in orchestration agent

2. **New API Endpoint:**
   - Add endpoint in `app.py`
   - Define request/response models
   - Update API documentation

3. **New Frontend Component:**
   - Create component in `frontend/src/components/`
   - Add routing if needed
   - Update main App.js

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Test MongoDB connection
python test_connection.py

# Test data ingestion
python test_reconciliation_ingestion.py

# Test API endpoints
python test_api.py

# Test data serialization
python test_serialization.py
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- DataUpload.test.js
```

### Integration Tests

```bash
# Start both backend and frontend
# Then run integration tests
cd backend
python -m pytest tests/integration/
```

### API Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# List collections
curl http://localhost:8000/collections

# Get sample data
curl "http://localhost:8000/sample-data?collection=discrepancies&limit=3"

# Natural language query
curl -X POST http://localhost:8000/generate_chart \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Show all records", "collection": "discrepancies"}'
```

---

## 🐳 Deployment

### Docker Deployment

#### Build Images

```bash
# Backend
cd backend
docker build -t ai-bi-dashboard-backend:latest .

# Frontend
cd frontend
docker build -t ai-bi-dashboard-frontend:latest .
```

#### Run with Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=reconciliation_system

  backend:
    build: ./backend
    container_name: ai-bi-backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/
      - MONGODB_DATABASE=reconciliation_system
      - LLM_PROVIDER=gemini
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    container_name: ai-bi-frontend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend

volumes:
  mongodb_data:
```

Run:
```bash
docker-compose up -d
```

### Production Deployment

#### Environment Variables (Production)

```env
# Security
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]

# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DATABASE=reconciliation_production

# API Keys (use secrets management)
GOOGLE_API_KEY=production_key_from_secrets
```

#### Security Checklist

- [ ] Update CORS origins to specific domains
- [ ] Set DEBUG=False
- [ ] Use environment-specific API keys
- [ ] Enable HTTPS/SSL
- [ ] Implement rate limiting
- [ ] Set up authentication/authorization
- [ ] Configure MongoDB authentication
- [ ] Enable logging and monitoring
- [ ] Set up backup automation
- [ ] Configure firewall rules

---

## 🔧 Troubleshooting

### Common Issues

#### 1. MongoDB Connection Failed

**Error:** `pymongo.errors.ServerSelectionTimeoutError`

**Solutions:**
```bash
# Check if MongoDB is running
# Windows:
sc query MongoDB

# Start MongoDB
net start MongoDB

# Verify connection
mongosh --eval "db.adminCommand('ping')"
```

#### 2. Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

#### 3. Frontend Cannot Connect to Backend

**Error:** `Network Error` or `CORS Error`

**Solutions:**
- Verify backend is running: `curl http://localhost:8000/health`
- Check `.env` file has correct `REACT_APP_API_URL`
- Verify CORS settings in `backend/app.py`
- Clear browser cache and restart

#### 4. LLM API Errors

**Error:** `Authentication failed` or `API key invalid`

**Solutions:**
- Verify API key in `.env` file
- Check API key has correct permissions
- Verify LLM_PROVIDER matches your key (gemini/openai)
- Check API quota/limits

#### 5. Data Not Showing Up

**Error:** Collections are empty

**Solutions:**
```bash
# Re-run data ingestion
cd backend
python test_reconciliation_ingestion.py

# Verify data was loaded
curl http://localhost:8000/collections
```

### Debug Mode

Enable detailed logging:

```bash
# Backend
cd backend
set DEBUG=True  # Windows CMD
export DEBUG=True  # macOS/Linux
python app.py

# Frontend
cd frontend
set REACT_APP_ENABLE_DEV_TOOLS=true
npm start
```

### Getting Help

1. Check existing documentation in `/docs`
2. Review `SYSTEM_STATUS.md` for known issues
3. Check logs in terminal where services are running
4. Open an issue on GitHub with detailed error information

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Description of your feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

### Code Standards

- Follow existing code style
- Add tests for new features
- Update documentation
- Ensure all tests pass
- Add comments for complex logic

### Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and logs

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework for Python
- **React** - UI library for building user interfaces
- **MongoDB** - NoSQL database for flexible data storage
- **LangChain** - Framework for building LLM applications
- **Plotly** - Interactive visualization library
- **Google Gemini** - Large language model for AI features

---

## 📞 Contact

- **GitHub**: [@bhaskar9298](https://github.com/bhaskar9298)
- **Repository**: [test-demo-server](https://github.com/bhaskar9298/test-demo-server)

---

## 🗺️ Roadmap

### Current Version (2.0.0)
- ✅ Multi-collection support
- ✅ Complex flow ingestion
- ✅ Natural language queries
- ✅ Interactive visualizations

### Upcoming Features (2.1.0)
- ⏳ Enhanced frontend UI for flow visualization
- ⏳ Advanced AI analysis agents
- ⏳ Resolution workflow management
- ⏳ Ticket system integration

### Future (3.0.0)
- ⏳ Real-time reconciliation monitoring
- ⏳ Email/webhook notifications
- ⏳ Advanced reporting and analytics
- ⏳ Scheduled reconciliation jobs
- ⏳ Multi-tenancy support
- ⏳ Advanced security features

---

## 📊 Project Status

| Component | Status | Coverage |
|-----------|--------|----------|
| Backend API | ✅ Complete | 100% |
| Data Ingestion | ✅ Complete | 100% |
| AI Agents | 🟡 Partial | 40% |
| Frontend UI | 🟡 Partial | 60% |
| Testing | 🟡 Partial | 30% |
| Documentation | ✅ Complete | 100% |
| Production Ready | 🟡 Partial | 70% |

**Legend:**
- ✅ Complete (90-100%)
- 🟡 Partial (40-89%)
- 🔴 Minimal (0-39%)

---

## 📚 Additional Resources

- [Quick Start Guide](QUICKSTART_V2.md)
- [System Architecture](UPDATED_ARCHITECTURE.md)
- [System Status](SYSTEM_STATUS.md)
- [Verification Checklist](VERIFICATION_CHECKLIST.md)
- [API Documentation](http://localhost:8000/docs) (when backend is running)

---

<div align="center">

**Built with ❤️ using AI and Modern Web Technologies**

⭐ **Star this repo if you find it helpful!** ⭐

</div>
