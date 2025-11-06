"""
FastAPI Backend Application
Reconciliation DataFlow Dashboard Agent (Updated for Multi-Collection Support)
AI-driven dashboard for reconciliation data analysis
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from contextlib import asynccontextmanager
import os
import json
from dotenv import load_dotenv

from agents.orchestration_agent import orchestration_agent
from utils.mongo_connector import mongo_connector
from data_ingestion.json_ingester import ingest_reconciliation_data
from data_ingestion.reconciliation_flow_ingester import ingest_reconciliation_flow

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("\n" + "="*70)
    print("🚀 Reconciliation DataFlow Dashboard Agent (Multi-Collection)")
    print("="*70)
    
    try:
        # Test MongoDB connection
        collections = mongo_connector.list_collections()
        print(f"✅ MongoDB connected: {len(collections)} collections available")
    except Exception as e:
        print(f"⚠️  MongoDB connection warning: {e}")
    
    # Check LLM configuration
    llm_provider = os.getenv('LLM_PROVIDER', 'not_configured')
    print(f"🤖 LLM Provider: {llm_provider}")
    
    print("="*70)
    print("✅ API is ready to accept requests")
    print(f"📍 Access at: http://localhost:{os.getenv('BACKEND_PORT', 8000)}")
    print("="*70 + "\n")
    
    yield  # Application runs here
    
    # Shutdown
    print("\n🛑 Shutting down API...")
    mongo_connector.close()
    print("✅ Cleanup complete\n")


# Initialize FastAPI app
app = FastAPI(
    title="Reconciliation DataFlow Dashboard Agent",
    description="AI-powered reconciliation data analysis with multi-collection support",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Request/Response Models ====================

class QueryRequest(BaseModel):
    """Request model for natural language queries"""
    prompt: str
    collection: Optional[str] = None


class QueryResponse(BaseModel):
    """Response model for query results"""
    success: bool
    query: str
    pipeline: list
    data: list
    chart_config: dict
    plotly_figure: dict
    metadata: dict
    error: Optional[str] = None


class FlowIngestionResponse(BaseModel):
    """Response model for reconciliation flow ingestion"""
    success: bool
    collections_processed: Dict[str, int]
    data_tables_created: Dict[str, int]
    error: Optional[str] = None


class IngestionResponse(BaseModel):
    """Response model for simple data ingestion"""
    success: bool
    records_inserted: int
    indexes_created: List[str]
    statistics: dict
    error: Optional[str] = None


class DataSourceInfo(BaseModel):
    """Information about current data source"""
    has_data: bool
    collections: List[str]
    database: str


# ==================== Health & Info Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Reconciliation DataFlow Dashboard Agent",
        "version": "2.0.0",
        "status": "online",
        "description": "AI-powered reconciliation data analysis platform with multi-collection support",
        "features": [
            "Simple reconciliation data ingestion",
            "Complex flow data ingestion",
            "Multi-collection querying",
            "Natural language queries",
            "AI-powered visualization"
        ]
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        collections = mongo_connector.list_collections()
        mongo_status = "connected"
    except Exception as e:
        collections = []
        mongo_status = f"error: {str(e)}"
    
    return {
        "api": "healthy",
        "mongodb": mongo_status,
        "collections_count": len(collections),
        "collections": collections[:10],  # First 10 collections
        "llm_provider": os.getenv('LLM_PROVIDER', 'not_configured'),
        "database": os.getenv('MONGODB_DATABASE', 'reconciliation_system')
    }


@app.get("/data-source", response_model=DataSourceInfo)
async def get_data_source_info():
    """Get information about current data source"""
    try:
        if not mongo_connector._connected:
            return DataSourceInfo(
                has_data=False,
                collections=[],
                database=os.getenv('MONGODB_DATABASE', 'reconciliation_system')
            )
        
        collections = mongo_connector.list_collections()
        has_data = len(collections) > 0
        
        return DataSourceInfo(
            has_data=has_data,
            collections=collections,
            database=os.getenv('MONGODB_DATABASE', 'reconciliation_system')
        )
    except Exception as e:
        return DataSourceInfo(
            has_data=False,
            collections=[],
            database=os.getenv('MONGODB_DATABASE', 'reconciliation_system')
        )


# ==================== Data Ingestion Endpoints ====================

@app.post("/upload-reconciliation-flow", response_model=FlowIngestionResponse)
async def upload_reconciliation_flow(
    file: UploadFile = File(...),
    drop_existing: bool = Form(default=False)
):
    """
    Upload and ingest complete reconciliation flow JSON
    
    Args:
        file: JSON file with complete flow structure
        drop_existing: Whether to drop existing collections
        
    Returns:
        Ingestion result with statistics
    """
    try:
        if not file.filename.endswith('.json'):
            raise HTTPException(
                status_code=400,
                detail="Only JSON files are supported"
            )
        
        content = await file.read()
        json_data = content.decode('utf-8')
        
        try:
            json.loads(json_data)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON format: {str(e)}"
            )
        
        result = ingest_reconciliation_flow(
            json_data=json_data,
            mongo_uri=os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'),
            db_name=os.getenv('MONGODB_DATABASE', 'reconciliation_system'),
            drop_existing=drop_existing
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return FlowIngestionResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@app.post("/ingest-reconciliation-flow", response_model=FlowIngestionResponse)
async def ingest_flow_from_text(
    json_data: str = Form(...),
    drop_existing: bool = Form(default=False)
):
    """
    Ingest reconciliation flow from JSON text
    
    Args:
        json_data: JSON string with complete flow structure
        drop_existing: Whether to drop existing collections
        
    Returns:
        Ingestion result
    """
    try:
        try:
            json.loads(json_data)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON format: {str(e)}"
            )
        
        result = ingest_reconciliation_flow(
            json_data=json_data,
            mongo_uri=os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'),
            db_name=os.getenv('MONGODB_DATABASE', 'reconciliation_system'),
            drop_existing=drop_existing
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return FlowIngestionResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )


@app.post("/upload-json", response_model=IngestionResponse)
async def upload_json_file(
    file: UploadFile = File(...),
    drop_existing: bool = Form(default=False),
    collection_name: str = Form(default="reconciliation_records")
):
    """
    Upload and ingest simple JSON file (legacy support)
    
    Args:
        file: JSON file upload
        drop_existing: Whether to drop existing data
        collection_name: Target collection name
        
    Returns:
        Ingestion result with statistics
    """
    try:
        if not file.filename.endswith('.json'):
            raise HTTPException(
                status_code=400,
                detail="Only JSON files are supported"
            )
        
        content = await file.read()
        json_data = content.decode('utf-8')
        
        try:
            json.loads(json_data)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON format: {str(e)}"
            )
        
        result = ingest_reconciliation_data(
            json_data=json_data,
            mongo_uri=os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'),
            db_name=os.getenv('MONGODB_DATABASE', 'reconciliation_system'),
            collection_name=collection_name,
            drop_existing=drop_existing
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return IngestionResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@app.post("/ingest-json-text", response_model=IngestionResponse)
async def ingest_json_text(
    json_data: str = Form(...),
    drop_existing: bool = Form(default=False),
    collection_name: str = Form(default="reconciliation_records")
):
    """
    Ingest simple JSON data from text (legacy support)
    
    Args:
        json_data: JSON string
        drop_existing: Whether to drop existing data
        collection_name: Target collection name
        
    Returns:
        Ingestion result with statistics
    """
    try:
        try:
            json.loads(json_data)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON format: {str(e)}"
            )
        
        result = ingest_reconciliation_data(
            json_data=json_data,
            mongo_uri=os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'),
            db_name=os.getenv('MONGODB_DATABASE', 'reconciliation_system'),
            collection_name=collection_name,
            drop_existing=drop_existing
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return IngestionResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )


@app.delete("/clear-data")
async def clear_data(collection_name: Optional[str] = None):
    """Clear data from specified collection or all collections"""
    try:
        if collection_name:
            collection = mongo_connector.get_collection(collection_name)
            result = collection.delete_many({})
            return {
                "success": True,
                "deleted_count": result.deleted_count,
                "collection": collection_name,
                "message": f"Deleted {result.deleted_count} records from {collection_name}"
            }
        else:
            # Clear all collections
            collections = mongo_connector.list_collections()
            total_deleted = 0
            for coll_name in collections:
                coll = mongo_connector.get_collection(coll_name)
                result = coll.delete_many({})
                total_deleted += result.deleted_count
            
            return {
                "success": True,
                "deleted_count": total_deleted,
                "collections_cleared": len(collections),
                "message": f"Cleared {len(collections)} collections, deleted {total_deleted} records"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Reconciliation Flow Endpoints ====================

@app.get("/reconciliation-flow")
async def get_reconciliation_flow(profile_id: Optional[str] = None):
    """
    Get complete reconciliation flow with all related data
    
    Args:
        profile_id: Optional profile ID to filter
        
    Returns:
        Complete flow structure
    """
    try:
        flow = mongo_connector.get_reconciliation_flow(profile_id)
        return {
            "success": True,
            "flow": flow
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/matching-rules")
async def get_matching_rules(vendor_type: Optional[str] = None):
    """Get matching rules, optionally filtered by vendor type"""
    try:
        if vendor_type:
            rules = mongo_connector.get_matching_rules_by_vendor(vendor_type)
        else:
            rules = list(mongo_connector.get_collection('matchingrules').find({}))
            rules = [mongo_connector.serialize_document(r) for r in rules]
        
        return {
            "success": True,
            "rules": rules,
            "count": len(rules)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/discrepancies")
async def get_discrepancies(severity: Optional[str] = None):
    """Get discrepancies, optionally filtered by severity"""
    try:
        if severity:
            discrepancies = mongo_connector.get_discrepancies_by_severity(severity)
        else:
            discrepancies = list(mongo_connector.get_collection('discrepancies').find({}))
            discrepancies = [mongo_connector.serialize_document(d) for d in discrepancies]
        
        return {
            "success": True,
            "discrepancies": discrepancies,
            "count": len(discrepancies)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Query & Visualization Endpoints ====================

@app.get("/schema")
async def get_schema(collection: str):
    """Get collection schema"""
    try:
        schema = mongo_connector.get_collection_schema(collection)
        return {
            "success": True,
            "collection": collection,
            "schema": schema
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_chart", response_model=QueryResponse)
async def generate_chart(request: QueryRequest):
    """
    Main endpoint: Process natural language query and generate visualization
    
    Args:
        request: QueryRequest with prompt and optional collection name
        
    Returns:
        Complete response with data, visualization, and metadata
    """
    print(f"Received query: {request.prompt} (Collection: {request.collection})")
    try:
        # Check if data exists
        collections = mongo_connector.list_collections()
        if len(collections) == 0:
            raise HTTPException(
                status_code=400,
                detail="No data available. Please upload JSON data first."
            )
        
        # Validate input
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(
                status_code=400,
                detail="Prompt cannot be empty"
            )
        
        # Process query through orchestration agent
        # Pass collection as keyword argument
        result = orchestration_agent.process_query(
            query=request.prompt,
            collection=request.collection
        )
        
        
        return QueryResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/execute_pipeline")
async def execute_pipeline(pipeline: list, collection: str):
    """
    Execute a custom MongoDB aggregation pipeline
    
    Args:
        pipeline: MongoDB aggregation pipeline
        collection: Collection name
        
    Returns:
        Query results
    """
    try:
        data = mongo_connector.execute_aggregation(pipeline, collection)
        return {
            "success": True,
            "data": data,
            "count": len(data),
            "collection": collection
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/collections")
async def list_collections():
    """List all available collections in the database"""
    try:
        collections = mongo_connector.list_collections()
        
        # Get document counts for each collection
        collection_info = []
        for coll_name in collections:
            count = mongo_connector.count_documents(coll_name)
            collection_info.append({
                "name": coll_name,
                "count": count
            })
        
        return {
            "success": True,
            "collections": collection_info,
            "total": len(collections)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sample-data")
async def get_sample_data(collection: str, limit: int = 5):
    """Get sample records from a collection"""
    try:
        coll = mongo_connector.get_collection(collection)
        sample = list(coll.find({}).limit(limit))
        sample = [mongo_connector.serialize_document(doc) for doc in sample]
        
        return {
            "success": True,
            "collection": collection,
            "sample": sample,
            "count": len(sample)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Main Entry Point ====================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('BACKEND_PORT', 8000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=debug
    )
