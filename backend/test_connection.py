"""
Simple connection test
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

print("Testing imports...")

try:
    from utils.mongo_connector import mongo_connector
    print("✅ mongo_connector imported")
except Exception as e:
    print(f"❌ Failed to import mongo_connector: {e}")
    sys.exit(1)

try:
    from data_ingestion.reconciliation_flow_ingester import ingest_reconciliation_flow
    print("✅ reconciliation_flow_ingester imported")
except Exception as e:
    print(f"❌ Failed to import reconciliation_flow_ingester: {e}")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env loaded")
except Exception as e:
    print(f"❌ Failed to load .env: {e}")
    sys.exit(1)

print("\nTesting MongoDB connection...")
try:
    collections = mongo_connector.list_collections()
    print(f"✅ MongoDB connected")
    print(f"   Database: {mongo_connector.database_name}")
    print(f"   Collections: {len(collections)}")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    sys.exit(1)

print("\nTesting file path...")
json_file = backend_path / "utils" / "Reconciliation Data Flow.json"
print(f"   Looking for: {json_file}")
print(f"   Exists: {json_file.exists()}")

if not json_file.exists():
    print("\n❌ JSON file not found!")
    print("   Checking alternative locations...")
    
    # Check utils directory
    utils_dir = backend_path / "utils"
    print(f"   Utils directory: {utils_dir}")
    print(f"   Utils exists: {utils_dir.exists()}")
    
    if utils_dir.exists():
        files = list(utils_dir.glob("*.json"))
        print(f"   JSON files in utils: {[f.name for f in files]}")
else:
    print("✅ JSON file found")

print("\n✅ All basic tests passed!")
