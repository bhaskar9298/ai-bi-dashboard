"""
MongoDB Connection Utility
Handles database connections and provides helper methods for querying
"""
from pymongo import MongoClient
from typing import List, Dict, Any, Optional
from datetime import datetime
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()


def serialize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert MongoDB document to JSON-serializable format
    Handles ObjectId and datetime conversions
    """
    if doc is None:
        return None
    
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            # Convert ObjectId to string
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            # Convert datetime to ISO format string
            serialized[key] = value.isoformat()
        elif isinstance(value, dict):
            # Recursively serialize nested documents
            serialized[key] = serialize_document(value)
        elif isinstance(value, list):
            # Serialize list items if they are documents
            serialized[key] = [
                serialize_document(item) if isinstance(item, dict) else item 
                for item in value
            ]
        else:
            serialized[key] = value
    return serialized


class MongoConnector:
    """Singleton MongoDB connection handler"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnector, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize MongoDB connection"""
        self.uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.database_name = os.getenv('MONGODB_DATABASE', 'bi_dashboard')
        self.collection_name = os.getenv('MONGODB_COLLECTION', 'sales')
        
        try:
            self._client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self._client.server_info()
            self._db = self._client[self.database_name]
            print(f"✅ Connected to MongoDB: {self.database_name}")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            raise
    
    def get_collection(self, collection_name: Optional[str] = None):
        """Get a MongoDB collection"""
        col_name = collection_name or self.collection_name
        return self._db[col_name]
    
    def execute_aggregation(self, pipeline: List[Dict[str, Any]], 
                           collection_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Execute a MongoDB aggregation pipeline
        
        Args:
            pipeline: MongoDB aggregation pipeline
            collection_name: Optional collection name override
            
        Returns:
            List of JSON-serializable documents
        """
        collection = self.get_collection(collection_name)
        try:
            result = list(collection.aggregate(pipeline))
            # Serialize documents to make them JSON-safe
            serialized_result = [serialize_document(doc) for doc in result]
            print(f"✅ Query executed successfully. Found {len(serialized_result)} documents")
            return serialized_result
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            raise
    
    def get_collection_schema(self, collection_name: Optional[str] = None, 
                            sample_size: int = 100) -> Dict[str, Any]:
        """
        Analyze collection schema by sampling documents
        
        Args:
            collection_name: Optional collection name override
            sample_size: Number of documents to sample
            
        Returns:
            Schema information including fields and types (JSON-serializable)
        """
        collection = self.get_collection(collection_name)
        
        try:
            # Sample documents
            sample = list(collection.aggregate([
                {"$sample": {"size": sample_size}},
                {"$limit": sample_size}
            ]))
            
            if not sample:
                return {"fields": [], "sample_count": 0}
            
            # Serialize sample documents first
            serialized_sample = [serialize_document(doc) for doc in sample]
            
            # Analyze field types
            field_types = {}
            for doc in serialized_sample:
                for key, value in doc.items():
                    if key not in field_types:
                        field_types[key] = set()
                    field_types[key].add(type(value).__name__)
            
            # Convert sets to lists for JSON serialization
            schema = {
                "fields": [
                    {
                        "name": field,
                        "types": list(types)
                    }
                    for field, types in field_types.items()
                ],
                "sample_count": len(serialized_sample),
                "sample_document": serialized_sample[0] if serialized_sample else None
            }
            
            return schema
            
        except Exception as e:
            print(f"❌ Schema analysis failed: {e}")
            return {"fields": [], "sample_count": 0, "error": str(e)}
    
    def insert_many(self, documents: List[Dict[str, Any]], 
                   collection_name: Optional[str] = None):
        """Insert multiple documents"""
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        return result.inserted_ids
    
    def count_documents(self, collection_name: Optional[str] = None) -> int:
        """Count total documents in collection"""
        collection = self.get_collection(collection_name)
        return collection.count_documents({})
    
    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            print("✅ MongoDB connection closed")


# Singleton instance
mongo_connector = MongoConnector()
