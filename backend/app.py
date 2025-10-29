"""
FastAPI Backend Application
Main entry point for the AI-driven BI Dashboard
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from agents.orchestration_agent import orchestration_agent
from utils.mongo_connector import mongo_connector

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    Replaces deprecated on_event decorators
    """
    # Startup
    print("\n" + "="*60)
    print("🚀 AI BI Dashboard API Starting...")
    print("="*60)
    
    try:
        # Test MongoDB connection
        count = mongo_connector.count_documents()
        print(f"✅ MongoDB connected: {count} documents in collection")
    except Exception as e:
        print(f"⚠️  MongoDB connection warning: {e}")
    
    # Check LLM configuration
    llm_provider = os.getenv('LLM_PROVIDER', 'not_configured')
    print(f"🤖 LLM Provider: {llm_provider}")
    
    print("="*60)
    print("✅ API is ready to accept requests")
    print(f"📍 Access at: http://localhost:{os.getenv('BACKEND_PORT', 8000)}")
    print("="*60 + "\n")
    
    yield  # Application runs here
    
    # Shutdown
    print("\n🛑 Shutting down API...")
    mongo_connector.close()
    print("✅ Cleanup complete\n")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="AI-Driven BI Dashboard API",
    description="Natural language to data visualization powered by LLM agents",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
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


# Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "AI BI Dashboard API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Check MongoDB connection
        count = mongo_connector.count_documents()
        mongo_status = "connected"
    except Exception as e:
        count = 0
        mongo_status = f"error: {str(e)}"
    
    return {
        "api": "healthy",
        "mongodb": mongo_status,
        "document_count": count,
        "llm_provider": os.getenv('LLM_PROVIDER', 'not_configured')
    }


@app.get("/schema")
async def get_schema(collection: Optional[str] = None):
    """Get collection schema"""
    try:
        schema = mongo_connector.get_collection_schema(collection)
        return {
            "success": True,
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
    try:
        # Validate input
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(
                status_code=400,
                detail="Prompt cannot be empty"
            )
        
        # Process query through orchestration agent
        result = orchestration_agent.process_query(request.prompt)
        
        # Return response
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
async def execute_pipeline(pipeline: list, collection: Optional[str] = None):
    """
    Execute a custom MongoDB aggregation pipeline
    
    Args:
        pipeline: MongoDB aggregation pipeline
        collection: Optional collection name
        
    Returns:
        Query results
    """
    try:
        data = mongo_connector.execute_aggregation(pipeline, collection)
        return {
            "success": True,
            "data": data,
            "count": len(data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/collections")
async def list_collections():
    """List all available collections in the database"""
    try:
        db = mongo_connector._db
        collections = db.list_collection_names()
        return {
            "success": True,
            "collections": collections
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
