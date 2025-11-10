"""
MongoDB Connection Utility for Reconciliation System
Handles multi-collection database connections and provides helper methods

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
    Handles ObjectId and datetime conversions recursively
    """
    if doc is None:
        return None
    
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, dict):
            serialized[key] = serialize_document(value)
        elif isinstance(value, list):
            serialized[key] = [
                serialize_document(item) if isinstance(item, dict) else 
                str(item) if isinstance(item, ObjectId) else
                item.isoformat() if isinstance(item, datetime) else
                item
                for item in value
            ]
        else:
            serialized[key] = value
    return serialized


class ReconciliationMongoConnector:
    """
    MongoDB connector for reconciliation system
    Manages multiple collections and complex relationships
    """
    
    _instance = None
    _client = None
    _db = None
    
    # Collection names based on the reconciliation data flow
    COLLECTIONS = {
        'MATCH_METHOD': 'matchmethod',
        'MATCHING_RULES': 'matchingrules',
        'DATASOURCES': 'datasources',
        'MATCHING_RESULTS': 'matchingResult',
        'DISCREPANCIES': 'discrepancies',
        'RESOLUTIONS': 'discrepancyResolution',
        'TICKETS': 'ticket'
    }
    
    @staticmethod
    def serialize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
        """Static method wrapper for serialize_document function"""
        return serialize_document(doc)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ReconciliationMongoConnector, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize MongoDB connection"""
        self.uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.database_name = os.getenv('MONGODB_DATABASE', 'reconciliation_system')
        self._connected = False
        
        try:
            self._client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self._client.server_info()
            self._db = self._client[self.database_name]
            self._connected = True
            print(f"✅ Connected to MongoDB: {self.database_name}")
            self._ensure_indexes()
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            print(f"⚠️  Running in offline mode. Please start MongoDB.")
            self._connected = False
            self._client = None
            self._db = None
    
    def _ensure_indexes(self):
        """Create necessary indexes for all collections"""
        if not self._connected:
            return
        
        try:
            # Match Method indexes
            self._db[self.COLLECTIONS['MATCH_METHOD']].create_index([('profileId', 1)])
            
            # Matching Rules indexes
            rules_col = self._db[self.COLLECTIONS['MATCHING_RULES']]
            rules_col.create_index([('matchingMethodId', 1)])
            rules_col.create_index([('status', 1)])
            rules_col.create_index([('active', 1)])
            
            # Datasources indexes
            ds_col = self._db[self.COLLECTIONS['DATASOURCES']]
            ds_col.create_index([('collectionId', 1)])
            ds_col.create_index([('workspaceId', 1)])
            ds_col.create_index([('organizationId', 1)])
            
            # Matching Results indexes
            results_col = self._db[self.COLLECTIONS['MATCHING_RESULTS']]
            results_col.create_index([('matchingMethodId', 1)])
            results_col.create_index([('profileId', 1)])
            
            # Discrepancies indexes
            disc_col = self._db[self.COLLECTIONS['DISCREPANCIES']]
            disc_col.create_index([('matchResultsId', 1)])
            disc_col.create_index([('severity', 1)])
            disc_col.create_index([('type', 1)])
            disc_col.create_index([('workspaceId', 1)])
            
            # Resolutions indexes
            res_col = self._db[self.COLLECTIONS['RESOLUTIONS']]
            res_col.create_index([('discrepancyId', 1)])
            res_col.create_index([('ticketId', 1)])
            res_col.create_index([('status', 1)])
            
            # Tickets indexes
            ticket_col = self._db[self.COLLECTIONS['TICKETS']]
            ticket_col.create_index([('discrepancyId', 1)])
            ticket_col.create_index([('status', 1)])
            ticket_col.create_index([('risk', 1)])
            ticket_col.create_index([('workspaceId', 1)])
            
            print("✅ Indexes created successfully")
        except Exception as e:
            print(f"⚠️  Warning: Failed to create some indexes: {e}")
    
    def get_collection(self, collection_name: str):
        """Get a MongoDB collection by name"""
        if not self._connected or self._db is None:
            raise Exception("MongoDB is not connected. Please start MongoDB service.")
        return self._db[collection_name]
    
    def get_reconciliation_flow(self, profile_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get complete reconciliation flow with all related data
        
        Args:
            profile_id: Optional profile ID to filter
            
        Returns:
            Complete reconciliation flow structure
        """
        try:
            flow = {}
            
            # Get match method
            match_method_query = {}
            if profile_id:
                match_method_query['profileId'] = ObjectId(profile_id)
            
            match_method = self.get_collection(self.COLLECTIONS['MATCH_METHOD']).find_one(
                match_method_query
            )
            
            if match_method:
                flow['matchmethod'] = serialize_document(match_method)
                method_id = match_method['_id']
                
                # Get matching rules
                rules = list(self.get_collection(self.COLLECTIONS['MATCHING_RULES']).find({
                    'matchingMethodId': method_id
                }))
                flow['matchingrules'] = [serialize_document(r) for r in rules]
                
                # Get datasources
                datasource_ids = match_method.get('datasourceIds', [])
                datasources = list(self.get_collection(self.COLLECTIONS['DATASOURCES']).find({
                    '_id': {'$in': datasource_ids}
                }))
                flow['datasources'] = [serialize_document(ds) for ds in datasources]
                
                # Get matching results
                results = list(self.get_collection(self.COLLECTIONS['MATCHING_RESULTS']).find({
                    'matchingMethodId': method_id
                }))
                flow['matchingResult'] = [serialize_document(r) for r in results]
                
                # Get discrepancies
                if results:
                    result_ids = [r['_id'] for r in results]
                    discrepancies = list(self.get_collection(self.COLLECTIONS['DISCREPANCIES']).find({
                        'matchResultsId': {'$in': result_ids}
                    }))
                    flow['discrepancies'] = [serialize_document(d) for d in discrepancies]
                    
                    # Get resolutions
                    if discrepancies:
                        disc_ids = [d['_id'] for d in discrepancies]
                        resolutions = list(self.get_collection(self.COLLECTIONS['RESOLUTIONS']).find({
                            'discrepancyId': {'$in': disc_ids}
                        }))
                        flow['discrepancyResolution'] = [serialize_document(r) for r in resolutions]
                        
                        # Get tickets
                        tickets = list(self.get_collection(self.COLLECTIONS['TICKETS']).find({
                            'discrepancyId': {'$in': disc_ids}
                        }))
                        flow['ticket'] = [serialize_document(t) for t in tickets]
            
            return flow
            
        except Exception as e:
            print(f"❌ Failed to get reconciliation flow: {e}")
            raise
    
    def execute_aggregation(self, pipeline: List[Dict[str, Any]], 
                           collection_name: str) -> List[Dict[str, Any]]:
        """
        Execute a MongoDB aggregation pipeline
        
        Args:
            pipeline: MongoDB aggregation pipeline
            collection_name: Collection name
            
        Returns:
            List of JSON-serializable documents
        """
        collection = self.get_collection(collection_name)
        try:
            result = list(collection.aggregate(pipeline))
            serialized_result = [serialize_document(doc) for doc in result]
            print(f"✅ Query executed successfully. Found {len(serialized_result)} documents")
            return serialized_result
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            raise
    
    def get_collection_schema(self, collection_name: str, 
                            sample_size: int = 100) -> Dict[str, Any]:
        """
        Analyze collection schema by sampling documents
        
        Args:
            collection_name: Collection name
            sample_size: Number of documents to sample
            
        Returns:
            Schema information including fields and types
        """
        collection = self.get_collection(collection_name)
        
        try:
            sample = list(collection.aggregate([
                {"$sample": {"size": sample_size}},
                {"$limit": sample_size}
            ]))
            
            if not sample:
                return {"fields": [], "sample_count": 0}
            
            serialized_sample = [serialize_document(doc) for doc in sample]
            
            field_types = {}
            for doc in serialized_sample:
                for key, value in doc.items():
                    if key not in field_types:
                        field_types[key] = set()
                    field_types[key].add(type(value).__name__)
            
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
    
    def get_matching_rules_by_vendor(self, vendor_type: str) -> List[Dict[str, Any]]:
        """
        Get matching rules filtered by vendor type
        
        Args:
            vendor_type: Vendor type (e.g., 'American Express', 'Mastercard')
            
        Returns:
            List of matching rules
        """
        try:
            rules = list(self.get_collection(self.COLLECTIONS['MATCHING_RULES']).find({
                'ruleName': {'$regex': vendor_type, '$options': 'i'}
            }))
            return [serialize_document(r) for r in rules]
        except Exception as e:
            print(f"❌ Failed to get matching rules: {e}")
            return []
    
    def get_discrepancies_by_severity(self, severity: str = 'high') -> List[Dict[str, Any]]:
        """
        Get discrepancies by severity level
        
        Args:
            severity: Severity level ('high', 'medium', 'low')
            
        Returns:
            List of discrepancies
        """
        try:
            discrepancies = list(self.get_collection(self.COLLECTIONS['DISCREPANCIES']).find({
                'severity': severity
            }))
            return [serialize_document(d) for d in discrepancies]
        except Exception as e:
            print(f"❌ Failed to get discrepancies: {e}")
            return []
    
    def get_data_from_dynamic_collection(self, collection_id: str, 
                                        filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Get data from dynamic data collections (POS, Credit Card, etc.)
        
        Args:
            collection_id: Collection ID
            filters: Optional query filters
            
        Returns:
            List of records
        """
        try:
            query = filters or {}
            records = list(self._db[collection_id].find(query))
            return [serialize_document(r) for r in records]
        except Exception as e:
            print(f"❌ Failed to get data from collection {collection_id}: {e}")
            return []
    
    def insert_many(self, documents: List[Dict[str, Any]], 
                   collection_name: str):
        """Insert multiple documents into a collection"""
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        return result.inserted_ids
    
    def count_documents(self, collection_name: str, 
                       query: Optional[Dict] = None) -> int:
        """Count documents in a collection"""
        if not self._connected or self._db is None:
            return 0
        try:
            collection = self.get_collection(collection_name)
            return collection.count_documents(query or {})
        except Exception:
            return 0
    
    def list_collections(self) -> List[str]:
        """List all collections in the database"""
        if not self._connected:
            return []
        return self._db.list_collection_names()
    
    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            print("✅ MongoDB connection closed")


# Singleton instance
mongo_connector = ReconciliationMongoConnector()
