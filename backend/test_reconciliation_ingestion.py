"""
Test script to verify reconciliation flow ingestion
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from data_ingestion.reconciliation_flow_ingester import ingest_reconciliation_flow
from utils.mongo_connector import mongo_connector
from dotenv import load_dotenv

load_dotenv()


def test_ingestion():
    """Test the reconciliation flow ingestion"""
    
    print("\n" + "="*70)
    print("Testing Reconciliation Flow Ingestion")
    print("="*70 + "\n")
    
    # Read the sample data - correct path
    json_file = backend_path / "utils" / "Reconciliation Data Flow.json"
    
    if not json_file.exists():
        print(f"❌ JSON file not found: {json_file}")
        print(f"   Looking in: {json_file.absolute()}")
        print(f"   Backend path: {backend_path.absolute()}")
        return
    
    print(f"📁 Reading file: {json_file}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = f.read()
    
    print("✅ File read successfully")
    
    # Ingest the data
    print("\n🔄 Starting ingestion...")
    
    result = ingest_reconciliation_flow(
        json_data=json_data,
        mongo_uri=os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'),
        db_name=os.getenv('MONGODB_DATABASE', 'reconciliation_system'),
        drop_existing=True  # Clean slate for testing
    )
    
    print("\n" + "="*70)
    print("Ingestion Result")
    print("="*70)
    
    if result['success']:
        print("✅ Ingestion successful!")
        
        print("\n📊 Collections Processed:")
        for collection, count in result['collections_processed'].items():
            print(f"  • {collection}: {count} documents")
        
        print("\n📊 Data Tables Created:")
        for table_id, count in result['data_tables_created'].items():
            print(f"  • {table_id}: {count} records")
    else:
        print(f"❌ Ingestion failed: {result['error']}")
        return
    
    # Verify the data
    print("\n" + "="*70)
    print("Verifying Data")
    print("="*70 + "\n")
    
    try:
        collections = mongo_connector.list_collections()
        print(f"✅ Found {len(collections)} collections:")
        for coll in collections:
            count = mongo_connector.count_documents(coll)
            print(f"  • {coll}: {count} documents")
        
        # Get a sample of matching rules
        print("\n📋 Sample Matching Rule:")
        rules = mongo_connector.get_matching_rules_by_vendor("American Express")
        if rules:
            rule = rules[0]
            print(f"  Rule Name: {rule.get('ruleName')}")
            print(f"  Description: {rule.get('descp')}")
            print(f"  Status: {rule.get('status')}")
            print(f"  Active: {rule.get('active')}")
        else:
            print("  No matching rules found for American Express")
        
        # Get discrepancies
        print("\n⚠️  Discrepancies:")
        discrepancies = mongo_connector.get_discrepancies_by_severity('high')
        print(f"  Found {len(discrepancies)} high-severity discrepancies")
        if discrepancies:
            disc = discrepancies[0]
            print(f"  Type: {disc.get('type')}")
            print(f"  Details: {disc.get('details')}")
        else:
            print("  No high-severity discrepancies found")
        
        print("\n✅ Verification complete!")
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_ingestion()
