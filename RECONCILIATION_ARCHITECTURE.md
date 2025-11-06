# 🏗️ Reconciliation System Architecture
## Based on Actual Data Flow

## System Overview

This system processes **multi-source reconciliation data** with complex matching rules, discrepancy detection, and resolution workflows.

## Core Collections

```
reconciliation_system/
├── matchmethod          # Reconciliation profiles
├── matchingrules        # Business rules (aggregate + arithmetic)
├── datasources          # Source data references (POS, Bank, etc.)
├── [dynamic_collections] # Actual transaction data
├── matchingResult       # Reconciliation results
├── discrepancies        # Identified mismatches
├── discrepancyResolution # Resolution tracking
└── ticket               # Workflow tickets
```

## Data Flow

```
1. Data Sources (POS + Bank) → datasources
2. Apply Matching Rules → matchingrules
3. Execute Aggregations → matchingResult
4. Detect Discrepancies → discrepancies
5. Create Tickets → ticket
6. Resolve & Document → discrepancyResolution
```

## Key Features

### 1. Multi-Source Matching
- Compare POS vendor data vs Bank statements
- Filter by vendor type (American Express, Mastercard)
- Aggregate amounts across multiple transactions

### 2. Rule Engine
- **Aggregate Operations**: `$sum` with filters
- **Arithmetic Operations**: `$subtract`, `$equals`
- **Cascading Rules**: Output from one rule feeds into next

### 3. Discrepancy Detection
- Automatic identification of mismatches
- Severity classification (high/medium/low)
- AI-powered root cause analysis

### 4. Resolution Workflow
- Ticket creation and assignment
- Document attachment (S3)
- Status tracking (Approved/Rejected/Pending)
- Comment history

## API Endpoints (Updated)

```
GET  /reconciliation-flow          # Complete data flow
GET  /match-methods                # All matching methods
GET  /matching-rules/:methodId     # Rules for a method
GET  /matching-results/:methodId   # Results for a method
GET  /discrepancies                # All discrepancies
GET  /discrepancies/:id            # Single discrepancy with details
POST /analyze-discrepancy          # AI analysis
GET  /resolutions                  # All resolutions
POST /create-resolution            # Create new resolution
GET  /tickets                      # All tickets
POST /create-ticket                # Create new ticket
GET  /data-sources                 # All data sources
POST /upload-source-data           # Upload POS/Bank data
```

## Implementation Plan

### Phase 1: Data Model (✅ Documented)
- [x] Define collections
- [x] Document relationships
- [x] Plan indexes

### Phase 2: Backend Updates
- [ ] Update MongoDB connector for multi-collection
- [ ] Create reconciliation engine
- [ ] Implement rule executor
- [ ] Add discrepancy detector
- [ ] Build resolution manager

### Phase 3: AI Agents
- [ ] Discrepancy analysis agent
- [ ] Resolution suggestion agent
- [ ] Pattern recognition agent
- [ ] Query translation agent (NL → MongoDB)

### Phase 4: Frontend
- [ ] Reconciliation dashboard
- [ ] Rule builder UI
- [ ] Discrepancy viewer
- [ ] Resolution workflow UI
- [ ] Ticket management

### Phase 5: Testing & Deployment
- [ ] Unit tests
- [ ] Integration tests
- [ ] Load testing
- [ ] Documentation
- [ ] Deployment scripts

---

**Next Steps:**
1. Create reconciliation engine module
2. Update MongoDB connector
3. Implement new API endpoints
4. Build AI analysis agents
5. Update frontend for reconciliation workflow
