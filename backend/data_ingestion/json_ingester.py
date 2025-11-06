"""
Reconciliation Data Ingestion Module
Handles JSON file upload and MongoDB ingestion for reconciliation data
"""
from pymongo import MongoClient
from datetime import datetime
import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


class ReconciliationDataIngester:
    """
    Handles ingestion of reconciliation JSON data into MongoDB
    Supports various JSON structures and enriches data with metadata
    """
    
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        """
        Initialize the data ingester
        
        Args:
            mongo_uri: MongoDB connection URI
            db_name: Database name
            collection_name: Collection name
        """
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self) -> bool:
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Test connection
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            return True
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            return False
    
    def validate_and_extract_records(self, data: Any) -> List[Dict]:
        """
        Validate and extract records from various JSON structures
        
        Supports:
        - List of records: [{}, {}, ...]
        - Dict with records key: {"records": [...]}
        - Dict with data key: {"data": [...]}
        - Single record: {...}
        
        Args:
            data: Parsed JSON data
            
        Returns:
            List of record dictionaries
        """
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Check common keys that might contain the records
            for key in ['records', 'data', 'reconciliations', 'transactions', 'items']:
                if key in data and isinstance(data[key], list):
                    return data[key]
            # Single record
            return [data]
        else:
            raise ValueError(f"Unsupported JSON structure: {type(data)}")
    
    def enrich_record(self, record: Dict, index: int) -> Dict:
        """
        Enrich record with additional metadata and standardization
        
        Args:
            record: Original record
            index: Record index
            
        Returns:
            Enriched record with metadata
        """
        enriched = record.copy()
        
        # Add internal tracking ID
        if 'id' not in enriched and '_id' not in enriched:
            enriched['record_id'] = f'REC-{index+1:06d}'
        
        # Parse and standardize date fields
        date_fields = [
            'date', 'transaction_date', 'reconciliation_date', 
            'created_at', 'updated_at', 'timestamp'
        ]
        
        for field in date_fields:
            if field in enriched and isinstance(enriched[field], str):
                try:
                    # Handle ISO format with timezone
                    date_str = enriched[field].replace('Z', '+00:00')
                    enriched[field] = datetime.fromisoformat(date_str)
                except:
                    try:
                        # Try common formats
                        enriched[field] = datetime.strptime(enriched[field], '%Y-%m-%d')
                    except:
                        pass
        
        # Add ingestion metadata
        enriched['_ingested_at'] = datetime.utcnow()
        enriched['_ingestion_source'] = 'json_upload'
        
        # Extract temporal features if date exists
        date_obj = None
        for field in date_fields:
            if field in enriched and isinstance(enriched[field], datetime):
                date_obj = enriched[field]
                break
        
        if date_obj:
            enriched['_year'] = date_obj.year
            enriched['_month'] = date_obj.month
            enriched['_quarter'] = f"Q{(date_obj.month - 1) // 3 + 1} {date_obj.year}"
            enriched['_day_of_week'] = date_obj.strftime('%A')
            enriched['_month_name'] = date_obj.strftime('%B')
        
        # Standardize numeric fields
        numeric_fields = [
            'amount', 'value', 'total', 'balance', 'difference',
            'debit', 'credit', 'net_amount', 'quantity', 'price'
        ]
        
        for field in numeric_fields:
            if field in enriched:
                try:
                    enriched[field] = float(enriched[field])
                except:
                    pass
        
        # Standardize status field
        if 'status' in enriched and isinstance(enriched[field], str):
            enriched['status'] = enriched['status'].lower().strip()
        
        return enriched
    
    def create_indexes(self) -> List[str]:
        """
        Create indexes based on data structure
        
        Returns:
            List of created index names
        """
        sample = self.collection.find_one()
        if not sample:
            return []
        
        indexes_created = []
        
        # Date field indexes
        date_fields = ['date', 'transaction_date', 'reconciliation_date', '_ingested_at']
        for field in date_fields:
            if field in sample:
                self.collection.create_index([(field, -1)])
                indexes_created.append(field)
        
        # Categorical field indexes
        categorical_fields = [
            'status', 'type', 'category', 'source', 'destination',
            'account', 'currency', 'region', 'department', 'product'
        ]
        for field in categorical_fields:
            if field in sample:
                self.collection.create_index([(field, 1)])
                indexes_created.append(field)
        
        # Temporal indexes
        temporal_fields = ['_year', '_quarter', '_month']
        for field in temporal_fields:
            if field in sample:
                self.collection.create_index([(field, 1)])
                indexes_created.append(field)
        
        # Compound indexes for common patterns
        if 'status' in sample and 'amount' in sample:
            self.collection.create_index([('status', 1), ('amount', -1)])
            indexes_created.append('status+amount')
        
        if '_year' in sample and '_month' in sample:
            self.collection.create_index([('_year', 1), ('_month', 1)])
            indexes_created.append('_year+_month')
        
        return indexes_created
    
    def ingest_json(self, json_data: str, drop_existing: bool = False) -> Dict[str, Any]:
        """
        Main ingestion method from JSON string
        
        Args:
            json_data: JSON string to ingest
            drop_existing: Whether to drop existing collection
            
        Returns:
            Result dictionary with statistics
        """
        result = {
            'success': False,
            'records_inserted': 0,
            'indexes_created': [],
            'error': None,
            'statistics': {}
        }
        
        try:
            # Connect to MongoDB
            if not self.connect():
                result['error'] = 'Failed to connect to MongoDB'
                return result
            
            # Drop existing collection if requested
            if drop_existing:
                existing_count = self.collection.count_documents({})
                if existing_count > 0:
                    self.collection.drop()
            
            # Parse JSON
            try:
                data = json.loads(json_data)
            except json.JSONDecodeError as e:
                result['error'] = f'Invalid JSON format: {str(e)}'
                return result
            
            # Extract records
            try:
                records = self.validate_and_extract_records(data)
            except ValueError as e:
                result['error'] = str(e)
                return result
            
            if not records:
                result['error'] = 'No records found in JSON data'
                return result
            
            # Enrich records
            enriched_records = []
            for idx, record in enumerate(records):
                try:
                    enriched = self.enrich_record(record, idx)
                    enriched_records.append(enriched)
                except Exception as e:
                    print(f"Warning: Failed to enrich record {idx}: {e}")
                    enriched_records.append(record)
            
            # Insert data
            insert_result = self.collection.insert_many(enriched_records)
            result['records_inserted'] = len(insert_result.inserted_ids)
            
            # Create indexes
            result['indexes_created'] = self.create_indexes()
            
            # Gather statistics
            result['statistics'] = self.get_collection_stats()
            result['success'] = True
            
        except Exception as e:
            result['error'] = f'Ingestion failed: {str(e)}'
        
        return result
    
    def ingest_from_file(self, file_path: str, drop_existing: bool = False) -> Dict[str, Any]:
        """
        Ingest data from JSON file
        
        Args:
            file_path: Path to JSON file
            drop_existing: Whether to drop existing collection
            
        Returns:
            Result dictionary with statistics
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = f.read()
            return self.ingest_json(json_data, drop_existing)
        except FileNotFoundError:
            return {
                'success': False,
                'error': f'File not found: {file_path}',
                'records_inserted': 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'File read error: {str(e)}',
                'records_inserted': 0
            }
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get collection statistics
        
        Returns:
            Dictionary with collection statistics
        """
        stats = {
            'total_records': self.collection.count_documents({}),
            'database': self.db_name,
            'collection': self.collection_name
        }
        
        # Get sample record structure
        sample = self.collection.find_one({}, {'_id': 0})
        if sample:
            stats['fields'] = list(sample.keys())
            stats['sample_record'] = sample
        
        return stats
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()


def ingest_reconciliation_data(
    json_data: str,
    mongo_uri: str,
    db_name: str,
    collection_name: str,
    drop_existing: bool = False
) -> Dict[str, Any]:
    """
    Helper function to ingest reconciliation data
    
    Args:
        json_data: JSON string
        mongo_uri: MongoDB URI
        db_name: Database name
        collection_name: Collection name
        drop_existing: Whether to drop existing data
        
    Returns:
        Ingestion result
    """
    ingester = ReconciliationDataIngester(mongo_uri, db_name, collection_name)
    result = ingester.ingest_json(json_data, drop_existing)
    ingester.close()
    return result
