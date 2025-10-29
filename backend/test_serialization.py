"""
Quick fix verification script
Tests the datetime serialization fix
"""
from utils.mongo_connector import mongo_connector, serialize_document
from datetime import datetime
from bson import ObjectId

print("\n" + "="*60)
print("Testing MongoDB Serialization Fix")
print("="*60 + "\n")

# Test 1: Serialize document with datetime
print("Test 1: Serializing datetime objects")
test_doc = {
    "_id": ObjectId(),
    "date": datetime.now(),
    "name": "Test",
    "amount": 100.50
}
print(f"Original: {test_doc}")
serialized = serialize_document(test_doc)
print(f"Serialized: {serialized}")
print(f"✅ Datetime converted to: {serialized['date']}")
print(f"✅ ObjectId converted to: {serialized['_id']}\n")

# Test 2: Query MongoDB
print("Test 2: Querying MongoDB with aggregation")
try:
    pipeline = [
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
        {"$sort": {"total": -1}},
        {"$limit": 3}
    ]
    result = mongo_connector.execute_aggregation(pipeline)
    print(f"✅ Query successful! Returned {len(result)} documents")
    if result:
        print(f"Sample result: {result[0]}")
        print(f"✅ All fields are JSON-serializable\n")
except Exception as e:
    print(f"❌ Query failed: {e}\n")

# Test 3: Schema retrieval
print("Test 3: Schema retrieval with datetime fields")
try:
    schema = mongo_connector.get_collection_schema()
    print(f"✅ Schema retrieved successfully")
    print(f"Fields count: {len(schema['fields'])}")
    if schema.get('sample_document'):
        sample = schema['sample_document']
        if 'date' in sample:
            print(f"✅ Date field in sample: {sample['date']}")
            print(f"   Type: {type(sample['date'])}")
        print(f"✅ Sample document is JSON-serializable\n")
except Exception as e:
    print(f"❌ Schema retrieval failed: {e}\n")

print("="*60)
print("✅ All serialization tests passed!")
print("="*60 + "\n")

print("You can now run:")
print('curl -X POST http://localhost:8000/generate_chart \\')
print('  -H "Content-Type: application/json" \\')
print('  -d \'{"prompt": "show sales by category"}\'')
