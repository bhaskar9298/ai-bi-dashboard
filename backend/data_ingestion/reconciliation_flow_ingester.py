"""
Reconciliation Flow Data Ingestion Module
Handles ingestion of complete reconciliation flow data with all related collections
"""
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import json
from typing import Dict, List, Any, Optional


class ReconciliationFlowIngester:
    """
    Handles ingestion of reconciliation flow data into MongoDB
    Supports the complete data structure with multiple collections
    """
    
    def __init__(self, mongo_uri: str, db_name: str):
        """
        Initialize the reconciliation flow ingester
        
        Args:
            mongo_uri: MongoDB connection URI
            db_name: Database name
        """
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.client = None
        self.db = None
        
        # Collection mappings
        self.collections = {
            'matchmethod': 'matchmethod',
            'matchingrules': 'matchingrules',
            'datasources': 'datasources',
            'matchingResult': 'matchingResult',
            'discrepancies': 'discrepancies',
            'discrepancyResolution': 'discrepancyResolution',
            'ticket': 'ticket'
        }
    
    def connect(self) -> bool:
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.server_info()
            self.db = self.client[self.db_name]
            return True
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            return False
    
    def convert_oid_strings(self, data: Any) -> Any:
        """
        Convert ObjectId string representations to actual ObjectId
        Recursively processes nested structures
        """
        if isinstance(data, dict):
            converted = {}
            for key, value in data.items():
                if key in ['_id', 'profileId', 'matchingMethodId', 'extractionMethodId',
                          'workspaceId', 'organizationId', 'matchResultsId', 'discrepancyId',
                          'ticketId', 'resolvedBy'] and isinstance(value, dict) and '$oid' in value:
                    converted[key] = ObjectId(value['$oid'])
                elif key == 'datasourceIds' and isinstance(value, list):
                    converted[key] = [
                        ObjectId(item['$oid']) if isinstance(item, dict) and '$oid' in item else item
                        for item in value
                    ]
                elif isinstance(value, dict) and '$date' in value:
                    # Convert date strings to datetime
                    try:
                        converted[key] = datetime.fromisoformat(value['$date'].replace('Z', '+00:00'))
                    except:
                        converted[key] = value
                elif isinstance(value, (dict, list)):
                    converted[key] = self.convert_oid_strings(value)
                else:
                    converted[key] = value
            return converted
        elif isinstance(data, list):
            return [self.convert_oid_strings(item) for item in data]
        else:
            return data
    
    def create_dynamic_data_collection(self, collection_id: str, 
                                      records: List[Dict]) -> int:
        """
        Create and populate a dynamic data collection (POS, Credit Card, etc.)
        
        Args:
            collection_id: Collection identifier
            records: List of records to insert
            
        Returns:
            Number of records inserted
        """
        try:
            collection = self.db[collection_id]
            
            # Convert ObjectId strings in records
            converted_records = [self.convert_oid_strings(record) for record in records]
            
            # Insert records
            if converted_records:
                result = collection.insert_many(converted_records)
                return len(result.inserted_ids)
            return 0
        except Exception as e:
            print(f"Failed to create dynamic collection {collection_id}: {e}")
            return 0
    
    def extract_and_create_data_tables(self, flow_data: Dict) -> Dict[str, int]:
        """
        Extract data from matching results and create data table collections
        
        Args:
            flow_data: Complete reconciliation flow data
            
        Returns:
            Dictionary with collection IDs and record counts
        """
        created_tables = {}
        
        try:
            # Get matching results
            matching_result = flow_data.get('matchingResult', {})
            
            if not matching_result:
                return created_tables
            
            # Get rows and extract source data
            rows = matching_result.get('rows', [])
            
            # Track collections and their records
            collection_records = {}
            
            for row in rows:
                cells = row.get('cells', [])
                for cell in cells:
                    sources = cell.get('sources', [])
                    for source in sources:
                        table_id = source.get('tableId')
                        full_row = source.get('fullRow')
                        
                        if table_id and full_row:
                            if table_id not in collection_records:
                                collection_records[table_id] = []
                            # Avoid duplicates
                            if full_row not in collection_records[table_id]:
                                collection_records[table_id].append(full_row)
            
            # Create collections
            for table_id, records in collection_records.items():
                count = self.create_dynamic_data_collection(table_id, records)
                created_tables[table_id] = count
                print(f"✅ Created collection {table_id} with {count} records")
            
            return created_tables
            
        except Exception as e:
            print(f"Failed to extract and create data tables: {e}")
            return created_tables
    
    def ingest_flow(self, flow_data: Dict, drop_existing: bool = False) -> Dict[str, Any]:
        """
        Ingest complete reconciliation flow data
        
        Args:
            flow_data: Complete flow data structure
            drop_existing: Whether to drop existing collections
            
        Returns:
            Ingestion result with statistics
        """
        result = {
            'success': False,
            'collections_processed': {},
            'data_tables_created': {},
            'error': None
        }
        
        try:
            if not self.connect():
                result['error'] = 'Failed to connect to MongoDB'
                return result
            
            # Drop existing collections if requested
            if drop_existing:
                for collection_name in self.collections.values():
                    self.db[collection_name].drop()
                print("✅ Dropped existing collections")
            
            # Process each collection type
            for key, collection_name in self.collections.items():
                if key in flow_data:
                    data = flow_data[key]
                    
                    # Handle both single document and list
                    if isinstance(data, dict):
                        data = [data]
                    elif not isinstance(data, list):
                        continue
                    
                    # Convert ObjectId strings
                    converted_data = [self.convert_oid_strings(doc) for doc in data]
                    
                    # Insert data
                    if converted_data:
                        collection = self.db[collection_name]
                        insert_result = collection.insert_many(converted_data)
                        result['collections_processed'][collection_name] = len(insert_result.inserted_ids)
                        print(f"✅ Inserted {len(insert_result.inserted_ids)} documents into {collection_name}")
            
            # Extract and create dynamic data tables
            result['data_tables_created'] = self.extract_and_create_data_tables(flow_data)
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = f'Ingestion failed: {str(e)}'
            import traceback
            traceback.print_exc()
        
        return result
    
    def ingest_from_json_string(self, json_data: str, 
                               drop_existing: bool = False) -> Dict[str, Any]:
        """
        Ingest reconciliation flow from JSON string
        
        Args:
            json_data: JSON string containing flow data
            drop_existing: Whether to drop existing collections
            
        Returns:
            Ingestion result
        """
        try:
            flow_data = json.loads(json_data)
            return self.ingest_flow(flow_data, drop_existing)
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Invalid JSON: {str(e)}',
                'collections_processed': {}
            }
    
    def ingest_from_file(self, file_path: str, 
                        drop_existing: bool = False) -> Dict[str, Any]:
        """
        Ingest reconciliation flow from JSON file
        
        Args:
            file_path: Path to JSON file
            drop_existing: Whether to drop existing collections
            
        Returns:
            Ingestion result
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = f.read()
            return self.ingest_from_json_string(json_data, drop_existing)
        except FileNotFoundError:
            return {
                'success': False,
                'error': f'File not found: {file_path}',
                'collections_processed': {}
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'File read error: {str(e)}',
                'collections_processed': {}
            }
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()


def ingest_reconciliation_flow(
    json_data: str,
    mongo_uri: str,
    db_name: str,
    drop_existing: bool = False
) -> Dict[str, Any]:
    """
    Helper function to ingest reconciliation flow data
    
    Args:
        json_data: JSON string
        mongo_uri: MongoDB URI
        db_name: Database name
        drop_existing: Whether to drop existing data
        
    Returns:
        Ingestion result
    """
    ingester = ReconciliationFlowIngester(mongo_uri, db_name)
    result = ingester.ingest_from_json_string(json_data, drop_existing)
    ingester.close()
    return result
