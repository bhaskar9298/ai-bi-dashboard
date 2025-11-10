📘 Reconciliation DataFlow Dashboard Agent - Complete Technical Documentation
🎯 Project Overview
The Reconciliation DataFlow Dashboard Agent is an AI-powered business intelligence system that transforms complex financial reconciliation data into actionable insights through natural language queries. Built on a multi-agent architecture, the system ingests reconciliation flow data from JSON files, stores it in MongoDB, and enables users to query and visualize data using plain English commands.
Key Capabilities

Natural Language Processing: Convert English questions to MongoDB aggregation pipelines using LLMs (Gemini/GPT-4)
Intelligent Visualization: Automatically select and generate appropriate charts (bar, line, pie, scatter, area, table)
Multi-Collection Support: Handle complex reconciliation workflows across 7+ interconnected MongoDB collections
End-to-End Data Flow: From JSON ingestion → MongoDB storage → NL query → AI analysis → Interactive visualization
Production-Ready: Complete error handling, CORS support, health monitoring, and graceful degradation

Use Case: Financial Reconciliation
The system is specifically designed for financial reconciliation scenarios where organizations need to:

Match POS (Point of Sale) data with Credit Card statements
Identify discrepancies between vendor transactions (American Express, Mastercard)
Track resolution workflows and ticket management
Generate compliance reports and audit trails
Visualize reconciliation metrics and KPIs


🏗️ System Architecture
High-Level Architecture
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                          │
│  • Natural Language Input Interface                          │
│  • Plotly.js Interactive Visualizations                      │
│  • Data Upload Component (JSON files)                        │
│  • Export Functionality (JSON/CSV)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API (CORS Enabled)
┌──────────────────────▼──────────────────────────────────────┐
│              Backend (FastAPI + Python)                      │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │    Orchestration Agent (LangGraph State Machine)   │    │
│  │                                                     │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │    │
│  │  │  Query   │→ │ Execution│→ │  Visualization   │ │    │
│  │  │  Agent   │  │  Agent   │  │      Agent       │ │    │
│  │  │ (LLM)    │  │ (MongoDB)│  │     (LLM)        │ │    │
│  │  └──────────┘  └──────────┘  └──────────────────┘ │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Data Ingestion Layer                       │    │
│  │  • JSON Parser & Validator                         │    │
│  │  • ObjectId Converter (MongoDB Extended JSON)     │    │
│  │  • Multi-Collection Coordinator                    │    │
│  │  • Dynamic Table Extractor                         │    │
│  └────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │ PyMongo Driver
┌──────────────────────▼──────────────────────────────────────┐
│                MongoDB Database (Reconciliation System)      │
│                                                              │
│  Core Collections:              Dynamic Collections:        │
│  • matchmethod                  • POS_Data_<id>             │
│  • matchingrules                • Credit_Card_<id>          │
│  • datasources                  • Bank_Statement_<id>       │
│  • matchingResult               • (Created during ingestion)│
│  • discrepancies                                            │
│  • discrepancyResolution                                    │
│  • ticket                                                   │
│                                                              │
│  Features: Indexes, Relationships, Aggregation Pipelines   │
└─────────────────────────────────────────────────────────────┘
Agent-Based Workflow
The system employs a LangGraph-powered multi-agent architecture where specialized agents collaborate to process user queries:
User Query: "show discrepancies by severity"
                    ↓
┌─────────────────────────────────────────────┐
│   Orchestration Agent (State Machine)       │
│   Coordinates workflow across 4 nodes       │
└─────────────────────────────────────────────┘
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
[1] Schema Fetch Node    [2] Query Generation Node
    • Get collection          • LLM analyzes query
      metadata                • Generates MongoDB
    • Sample documents          aggregation pipeline
    • Field types             • Validates syntax
        ↓                           ↓
[3] Query Execution Node   [4] Visualization Node
    • Execute pipeline          • LLM selects chart type
    • Retrieve results          • Creates Plotly config
    • Serialize data            • Generates figure JSON
        ↓                           ↓
    JSON Response (Complete)

📂 Project Structure
ai-bi-dashboard/
├── backend/                          # FastAPI Backend
│   ├── agents/                       # AI Agent System
│   │   ├── orchestration_agent.py    # LangGraph State Machine
│   │   ├── query_agent.py            # NL → MongoDB Pipeline
│   │   ├── visualization_agent.py    # Chart Type Selection
│   │   └── __init__.py
│   │
│   ├── data_ingestion/               # Data Ingestion Layer
│   │   ├── reconciliation_flow_ingester.py  # Multi-collection ingestion
│   │   ├── json_data_ingester.py           # Simple JSON ingestion
│   │   └── __init__.py
│   │
│   ├── utils/                        # Utilities
│   │   ├── mongo_connector.py        # MongoDB Singleton Connector
│   │   ├── Reconciliation Data Flow.json  # Sample data
│   │   └── __init__.py
│   │
│   ├── app.py                        # FastAPI Application (Main Entry)
│   ├── requirements.txt              # Python Dependencies
│   ├── .env.example                  # Environment Variables Template
│   ├── Dockerfile                    # Docker Configuration
│   └── venv/                         # Virtual Environment
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChartView.js          # Plotly Chart Renderer
│   │   │   ├── ChartView.css
│   │   │   ├── DataUpload.js         # JSON File Upload
│   │   │   └── DataUpload.css
│   │   ├── App.js                    # Main React Component
│   │   ├── App.css
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   ├── package.json                  # NPM Dependencies
│   └── .env                          # Frontend Environment Variables
│
├── docker-compose.yml                # Docker Compose (MongoDB + Services)
├── README.md                         # Project Documentation
├── QUICKREF.md                       # Quick Reference Guide
└── start.bat / start.sh              # Startup Scripts
