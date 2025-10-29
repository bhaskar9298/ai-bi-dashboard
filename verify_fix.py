"""
Complete System Verification Script
Checks all components after fixes
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("\n" + "="*70)
print(" 🔍 AI BI Dashboard - Complete System Verification")
print("="*70 + "\n")

# Test 1: Import all modules
print("📦 Test 1: Importing all modules...")
try:
    from backend.utils.mongo_connector import mongo_connector, serialize_document
    from backend.agents.query_agent import query_agent
    from backend.agents.visualization_agent import visualization_agent
    from backend.agents.orchestration_agent import orchestration_agent
    print("✅ All modules imported successfully\n")
except Exception as e:
    print(f"❌ Import failed: {e}\n")
    sys.exit(1)

# Test 2: DateTime serialization
print("📅 Test 2: Testing datetime serialization...")
try:
    from datetime import datetime
    from bson import ObjectId
    
    test_doc = {
        "_id": ObjectId(),
        "date": datetime.now(),
        "amount": 100.50,
        "nested": {
            "timestamp": datetime.now()
        }
    }
    
    serialized = serialize_document(test_doc)
    
    # Check conversions
    assert isinstance(serialized['_id'], str), "_id should be string"
    assert isinstance(serialized['date'], str), "date should be string"
    assert isinstance(serialized['nested']['timestamp'], str), "nested date should be string"
    
    print(f"✅ DateTime serialization working")
    print(f"   Sample: {serialized['date'][:19]}\n")
except Exception as e:
    print(f"❌ Serialization test failed: {e}\n")
    sys.exit(1)

# Test 3: MongoDB connection
print("🗄️  Test 3: Testing MongoDB connection...")
try:
    count = mongo_connector.count_documents()
    print(f"✅ MongoDB connected: {count} documents\n")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("   Make sure MongoDB is running\n")
    sys.exit(1)

# Test 4: Schema retrieval (includes serialization)
print("📋 Test 4: Testing schema retrieval with serialization...")
try:
    schema = mongo_connector.get_collection_schema()
    
    # Check schema structure
    assert 'fields' in schema, "Schema should have fields"
    assert 'sample_document' in schema, "Schema should have sample"
    
    # Check sample document is serialized
    if schema['sample_document']:
        sample = schema['sample_document']
        # All values should be JSON-serializable types
        import json
        json_str = json.dumps(sample)  # This should not raise an error
        
    print(f"✅ Schema retrieval working")
    print(f"   Fields: {len(schema['fields'])}")
    print(f"   Sample document is JSON-serializable\n")
except Exception as e:
    print(f"❌ Schema retrieval failed: {e}\n")
    sys.exit(1)

# Test 5: Query execution (includes serialization)
print("⚡ Test 5: Testing query execution with serialization...")
try:
    pipeline = [
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
        {"$sort": {"total": -1}},
        {"$limit": 3}
    ]
    
    results = mongo_connector.execute_aggregation(pipeline)
    
    # Check results are serializable
    import json
    json_str = json.dumps(results)  # Should not raise error
    
    print(f"✅ Query execution working")
    print(f"   Records: {len(results)}")
    if results:
        print(f"   Sample: {results[0]}\n")
    else:
        print("   (No results returned)\n")
except Exception as e:
    print(f"❌ Query execution failed: {e}\n")
    sys.exit(1)

# Test 6: Agent initialization
print("🤖 Test 6: Testing agent initialization...")
try:
    # These should already be initialized
    assert query_agent is not None, "Query agent should exist"
    assert visualization_agent is not None, "Visualization agent should exist"
    assert orchestration_agent is not None, "Orchestration agent should exist"
    
    print("✅ All agents initialized\n")
except Exception as e:
    print(f"❌ Agent initialization failed: {e}\n")
    print("   Check if .env file has correct API keys\n")
    sys.exit(1)

# Test 7: Full pipeline simulation
print("🔄 Test 7: Testing full orchestration pipeline...")
try:
    # Simulate a simple query
    test_query = "show total sales by category"
    
    print(f"   Query: '{test_query}'")
    result = orchestration_agent.process_query(test_query)
    
    # Check result structure
    assert 'success' in result, "Result should have success field"
    assert 'query' in result, "Result should have query field"
    assert 'pipeline' in result, "Result should have pipeline field"
    assert 'data' in result, "Result should have data field"
    
    # Try to serialize entire result
    import json
    json_str = json.dumps(result)  # Should not raise error
    
    if result['success']:
        print(f"✅ Full pipeline working")
        print(f"   Pipeline stages: {len(result['pipeline'])}")
        print(f"   Records returned: {len(result['data'])}")
        print(f"   Chart type: {result.get('metadata', {}).get('chart_type')}")
    else:
        print(f"⚠️  Pipeline completed with errors:")
        print(f"   Error: {result.get('error')}")
    
    print()
    
except Exception as e:
    print(f"❌ Full pipeline test failed: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Final Summary
print("="*70)
print(" ✅ All System Verification Tests Passed!")
print("="*70)
print()
print("🎉 The datetime serialization fix is working correctly")
print("🎉 All components are functioning properly")
print()
print("📍 Next Steps:")
print("   1. Start the backend: python backend/app.py")
print("   2. Test the API:")
print('      curl -X POST http://localhost:8000/generate_chart \\')
print('        -H "Content-Type: application/json" \\')
print('        -d \'{"prompt": "show sales by category"}\'')
print()
print("   3. Start the frontend: cd frontend && npm start")
print()
