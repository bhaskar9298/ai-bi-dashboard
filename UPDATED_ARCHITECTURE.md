# 🏗️ Updated System Architecture
## Reconciliation DataFlow Dashboard Agent v2.0

## Overview

The system has been updated to support complex multi-collection reconciliation workflows based on the actual data flow structure. It now handles:

- **Multi-source reconciliation** (POS Data, Credit Card Details, Bank Statements)
- **Rule-based matching** (Aggregate and arithmetic operations)
- **Discrepancy detection and tracking**
- **Resolution management with tickets**
- **AI-powered analysis and suggestions**

## Database Schema

### Collections Structure

```
reconciliation_system (Database)
├── matchmethod              - Match method configurations
├── matchingrules            - Matching rules with operations
├── datasources              - Data source metadata
├── matchingResult           - Reconciliation results
├── discrepancies            - Identified discrepancies
├── discrepancyResolution    - Resolution records
├── ticket                   - Workflow tickets
└── [Dynamic Collections]    - Actual data tables (POS, Credit Card, etc.)
```

### Collection Schemas

#### 1. matchmethod
```javascript
{
  _id: ObjectId,
  profileId: ObjectId,
  datasourceIds: [ObjectId],
  displayFields: [],
  createdAt: ISODate,
  updatedAt: ISODate
}
```

#### 2. matchingrules
```javascript
{
  _id: ObjectId,
  matchingMethodId: ObjectId,
  ruleName: String,
  descp: String,
  rules: [[
    {
      type: "aggregate" | "arithmetic",
      dataSourceIds: [String],
      fieldId: String,
      operation: "$sum" | "$subtract" | "$equals",
      output: { name: String, datatype: String },
      filter: { field: String, value: String, mode: String }
    }
  ]],
  active: Boolean,
  status: "pass" | "fail",
  display: { fields: [...] },
  order: Number
}
```

#### 3. datasources
```javascript
{
  _id: ObjectId,
  name: String,
  description: String,
  source: { sourceType: String, subType: String },
  collectionId: String,  // References dynamic collection
  extractionMethodId: ObjectId,
  extractionStatus: String,
  workspaceId: ObjectId,
  organizationId: ObjectId
}
```

#### 4. matchingResult
```javascript
{
  _id: ObjectId,
  matchId: String,
  matchingMethodId: ObjectId,
  profileId: String,
  columns: [{ name: String, type: String }],
  rows: [{
    cells: [{
      value: Any,
      matchType: "exact" | "aggregated" | "computed",
      sources: [{
        tableId: String,
        rowIndex: Number,
        colIndex: Number,
        originalValue: Any,
        documentId: String,
        fullRow: {...}
      }]
    }],
    sourceRows: [{ tableId: String, rowIndex: Number }],
    matchingRules: [String]
  }],
  metadata: { matchSummary: {...}, documentIds: [...] }
}
```

#### 5. discrepancies
```javascript
{
  _id: ObjectId,
  type: "data_mismatch" | "missing_data" | ...,
  severity: "high" | "medium" | "low",
  details: String,
  suggestedResolution: {
    aiSummary: String,
    smartFacts: [String]
  },
  collection: String,  // JSON string of related data
  matchResultsId: ObjectId,
  profileId: ObjectId,
  workspaceId: ObjectId,
  organizationId: ObjectId
}
```

#### 6. discrepancyResolution
```javascript
{
  _id: ObjectId,
  discrepancyId: ObjectId,
  ticketId: ObjectId,
  resolvedBy: ObjectId,
  resolvedAt: ISODate,
  status: "Approved" | "Rejected" | "Pending",
  resolvedCollection: String,  // JSON string of updated data
  comment: String,  // HTML formatted
  link: String,
  document: {
    s3Url: String,
    url: String,
    name: String
  }
}
```

#### 7. ticket
```javascript
{
  _id: ObjectId,
  name: String,
  instruction: String,
  status: "Progress" | "Completed" | "Pending",
  risk: "High" | "Medium" | "Low",
  discrepancyId: ObjectId,
  profileId: ObjectId,
  workspaceId: ObjectId,
  organizationId: ObjectId,
  expiresAt: ISODate
}
```

#### 8. Dynamic Data Collections
```javascript
// Example: POS Vendor Data
{
  _id: ObjectId,
  date: String | ISODate,
  vendortype: String,
  amount: Number,
  sourceType: "document",
  sourceId: String
}

// Example: Credit Card Details
{
  _id: ObjectId,
  date: String,
  vendorType: String,
  amount: String | Number,
  sourceType: "document",
  sourceId: String
}
```

## API Endpoints

### Data Ingestion
- `POST /upload-reconciliation-flow` - Upload complete flow JSON
- `POST /ingest-reconciliation-flow` - Ingest flow from text
- `POST /upload-json` - Upload simple JSON (legacy)
- `POST /ingest-json-text` - Ingest simple JSON text (legacy)
- `DELETE /clear-data` - Clear collections

### Reconciliation Flow
- `GET /reconciliation-flow?profile_id={id}` - Get complete flow
- `GET /matching-rules?vendor_type={type}` - Get matching rules
- `GET /discrepancies?severity={level}` - Get discrepancies

### Queries & Analysis
- `POST /generate_chart` - Natural language query
- `POST /execute_pipeline` - Execute custom pipeline
- `GET /schema?collection={name}` - Get collection schema
- `GET /collections` - List all collections
- `GET /sample-data?collection={name}` - Get sample data

### System
- `GET /` - API info
- `GET /health` - Health check
- `GET /data-source` - Data source info

## Data Flow

### 1. Ingestion Flow
```
JSON File → Parse → Convert ObjectIds → Split Collections
    ↓           ↓            ↓                  ↓
  Validate  Structure   MongoDB    Create Dynamic Tables
                         Types      (POS, CC, etc.)
```

### 2. Reconciliation Flow
```
Data Sources → Matching Rules → Execute Operations → Compare Results
     ↓              ↓                   ↓                  ↓
   Filter      Aggregate           Calculate          Identify
  Records      Amounts            Differences       Discrepancies
```

### 3. Resolution Flow
```
Discrepancy → AI Analysis → Create Ticket → Manual Review → Resolution
     ↓             ↓              ↓              ↓             ↓
  Classify    Root Cause     Assign User    Add Comments  Update Data
  Severity    Suggestion     Set Priority   Upload Docs   Change Status
```

## Key Features

### 1. Multi-Collection Support
- Automatic collection creation from flow data
- Dynamic data table management
- Cross-collection queries and joins

### 2. Rule-Based Matching
- **Aggregate Operations**: Sum amounts by filters
- **Arithmetic Operations**: Calculate differences
- **Filter Operations**: Match by vendor type, date, etc.
- **Output Mapping**: Store intermediate results

### 3. AI Integration
- Discrepancy classification
- Root cause analysis
- Resolution suggestions
- Natural language queries

### 4. Workflow Management
- Ticket creation and tracking
- Status management
- Document attachments
- Comment threads

## MongoDB Indexes

```javascript
// matchmethod
profileId (ascending)

// matchingrules
matchingMethodId (ascending)
status (ascending)
active (ascending)

// datasources
collectionId (ascending)
workspaceId (ascending)
organizationId (ascending)

// matchingResult
matchingMethodId (ascending)
profileId (ascending)

// discrepancies
matchResultsId (ascending)
severity (ascending)
type (ascending)
workspaceId (ascending)

// discrepancyResolution
discrepancyId (ascending)
ticketId (ascending)
status (ascending)

// ticket
discrepancyId (ascending)
status (ascending)
risk (ascending)
workspaceId (ascending)
```

## Usage Examples

### 1. Ingest Reconciliation Flow
```python
POST /upload-reconciliation-flow
Content-Type: multipart/form-data

file: <Reconciliation Data Flow.json>
drop_existing: true
```

### 2. Get Complete Flow
```python
GET /reconciliation-flow?profile_id=68df98cc83106149bead8193

Response:
{
  "success": true,
  "flow": {
    "matchmethod": {...},
    "matchingrules": [...],
    "datasources": [...],
    "matchingResult": [...],
    "discrepancies": [...],
    "discrepancyResolution": [...],
    "ticket": [...]
  }
}
```

### 3. Query Discrepancies
```python
GET /discrepancies?severity=high

Response:
{
  "success": true,
  "discrepancies": [
    {
      "type": "data_mismatch",
      "severity": "high",
      "details": "Data not reconciled due to data mismatch",
      "suggestedResolution": {
        "aiSummary": "...",
        "smartFacts": [...]
      }
    }
  ]
}
```

## Testing

Run the test script to verify ingestion:

```bash
cd backend
python test_reconciliation_ingestion.py
```

Expected output:
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
  • e9b0b93f-8733-4104-8742-d54b53f6f3f11758625269533: X records
  • 0de75acb-91bb-4abb-9fd1-b9868cfd9ed71759437830583: Y records
```

## Migration Notes

### From v1.0 to v2.0

1. **Database Name Change**:
   - Old: `reconciliation_dashboard`
   - New: `reconciliation_system`

2. **New Collections**:
   - Added 7 new system collections
   - Support for dynamic data collections

3. **Backward Compatibility**:
   - Legacy endpoints still supported
   - Simple JSON ingestion works as before
   - Old collection name can still be used

4. **New Features**:
   - Multi-collection queries
   - Reconciliation flow management
   - Discrepancy tracking
   - Resolution workflows

## Next Steps

1. **Update Frontend**: Add UI components for:
   - Flow visualization
   - Discrepancy management
   - Ticket workflow
   - Resolution tracking

2. **Enhanced AI Agents**:
   - Discrepancy analysis agent
   - Resolution suggestion agent
   - Pattern recognition agent

3. **Advanced Features**:
   - Real-time reconciliation
   - Automated matching
   - Notification system
   - Audit trail

---

**Updated**: November 2024
**Version**: 2.0.0
**Status**: ✅ Production Ready
