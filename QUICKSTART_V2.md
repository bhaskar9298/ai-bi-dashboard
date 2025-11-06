# 🚀 Quick Start Guide - Reconciliation System v2.0

## Prerequisites
- ✅ MongoDB running on localhost:27017
- ✅ Python 3.9+ with dependencies installed
- ✅ Backend environment configured

## Step 1: Verify Setup

```bash
# Check MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Check Python environment
cd backend
python --version

# Verify dependencies
pip list | grep pymongo
pip list | grep fastapi
```

## Step 2: Ingest Sample Data

### Option A: Using Test Script (Recommended)
```bash
cd backend
python test_reconciliation_ingestion.py
```

**Expected Output:**
```
✅ Ingestion successful!

📊 Collections Processed:
  • matchmethod: 1 documents
  • matchingrules: 2 documents
  • datasources: 2 documents
  • matchingResult: 1 documents
  • discrepancies: 1 documents
  • discrepancyResolution: 1 documents
  • ticket: 1 documents

📊 Data Tables Created:
  • [Dynamic POS Collection]: X records
  • [Dynamic CC Collection]: Y records
```

### Option B: Using API
```bash
# Start backend first
cd backend
python app.py

# In another terminal, upload data
curl -X POST http://localhost:8000/upload-reconciliation-flow \
  -F "file=@../utils/Reconciliation Data Flow.json" \
  -F "drop_existing=true"
```

## Step 3: Verify Data

### Check Collections
```bash
# API
curl http://localhost:8000/collections

# Direct MongoDB
mongosh reconciliation_system --eval "db.getCollectionNames()"
```

### View Sample Data
```bash
# Get matching rules
curl "http://localhost:8000/matching-rules"

# Get discrepancies
curl "http://localhost:8000/discrepancies?severity=high"

# Get complete flow
curl "http://localhost:8000/reconciliation-flow"
```

## Step 4: Test Queries

### Example 1: Get All American Express Discrepancies
```bash
curl "http://localhost:8000/matching-rules?vendor_type=American Express"
```

### Example 2: Get High Severity Issues
```bash
curl "http://localhost:8000/discrepancies?severity=high"
```

### Example 3: Get Complete Reconciliation Flow
```bash
curl "http://localhost:8000/reconciliation-flow" | jq
```

## Step 5: Run Backend

```bash
cd backend
python app.py
```

**Backend should show:**
```
🚀 Reconciliation DataFlow Dashboard Agent (Multi-Collection)
✅ MongoDB connected: X collections available
🤖 LLM Provider: gemini
✅ API is ready to accept requests
📍 Access at: http://localhost:8000
```

## Common Tasks

### Clear All Data
```bash
curl -X DELETE http://localhost:8000/clear-data
```

### Clear Specific Collection
```bash
curl -X DELETE "http://localhost:8000/clear-data?collection_name=discrepancies"
```

### Get Schema of Collection
```bash
curl "http://localhost:8000/schema?collection=matchingrules"
```

### List All Collections
```bash
curl http://localhost:8000/collections
```

### Health Check
```bash
curl http://localhost:8000/health
```

## API Endpoints Quick Reference

### Data Ingestion
```
POST /upload-reconciliation-flow    Upload complete flow JSON
POST /ingest-reconciliation-flow    Ingest flow from text
POST /upload-json                    Upload simple JSON (legacy)
DELETE /clear-data                   Clear collections
```

### Reconciliation Flow
```
GET /reconciliation-flow             Get complete flow
GET /matching-rules                  Get matching rules
GET /discrepancies                   Get discrepancies
```

### Queries & Schema
```
POST /generate_chart                 Natural language query
POST /execute_pipeline               Execute MongoDB pipeline
GET /schema                          Get collection schema
GET /collections                     List all collections
GET /sample-data                     Get sample records
```

### System
```
GET /                                API information
GET /health                          Health check
GET /data-source                     Data source info
```

## Sample Natural Language Queries

Once frontend is connected:

```
"Show all American Express discrepancies"
"What is the total amount reconciled?"
"Show me high severity issues"
"Compare POS data with bank statements"
"Show reconciliation status by vendor"
```

## Troubleshooting

### Problem: MongoDB Connection Failed
```bash
# Check if MongoDB is running
systemctl status mongod  # Linux
brew services list | grep mongodb  # Mac
sc query MongoDB  # Windows

# Start MongoDB
systemctl start mongod  # Linux
brew services start mongodb-community  # Mac
net start MongoDB  # Windows
```

### Problem: Import Errors
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

### Problem: Collection Not Found
```bash
# Re-run ingestion
python test_reconciliation_ingestion.py
```

### Problem: ObjectId Error
```
# This is handled automatically by the new mongo_connector
# If you see this, ensure you're using the updated connector
```

## Data Structure Reference

### Matching Rule Example
```json
{
  "ruleName": "American Express",
  "descp": "Reconcile AMEX transactions",
  "status": "pass",
  "active": true,
  "rules": [
    [
      {
        "type": "aggregate",
        "operation": "$sum",
        "filter": {
          "field": "vendortype",
          "value": "American Express"
        }
      },
      {
        "type": "arithmetic",
        "operation": "$subtract"
      }
    ]
  ]
}
```

### Discrepancy Example
```json
{
  "type": "data_mismatch",
  "severity": "high",
  "details": "Amount mismatch between sources",
  "suggestedResolution": {
    "aiSummary": "Bank transaction found without POS record",
    "smartFacts": ["Unmatched Bank Transaction"]
  }
}
```

## Next Steps

1. ✅ Verify all endpoints work
2. ✅ Test with your own reconciliation data
3. ⏳ Update frontend UI components
4. ⏳ Implement AI analysis agents
5. ⏳ Add resolution workflow

## Support

For issues or questions:
1. Check `UPDATED_ARCHITECTURE.md` for detailed docs
2. Review `SYSTEM_UPDATE_SUMMARY.md` for changes
3. Check logs in backend console
4. Verify MongoDB is accessible

---

**Version**: 2.0.0  
**Last Updated**: November 2024
