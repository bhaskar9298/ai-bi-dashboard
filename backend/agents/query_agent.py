"""
Query Agent - Converts natural language to MongoDB aggregation pipeline
Uses LangChain with LLM to generate queries based on collection schema
"""
from typing import Dict, Any, List
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()


class QueryAgent:
    """
    Converts natural language queries into MongoDB aggregation pipelines
    """
    
    def __init__(self):
        """Initialize the Query Agent with LLM"""
        self.llm = self._initialize_llm()
        self.prompt_template = self._create_prompt_template()
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def _initialize_llm(self):
        """Initialize LLM based on environment configuration"""
        provider = os.getenv('LLM_PROVIDER', 'gemini').lower()
        
        if provider == 'gemini':
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment")
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=api_key,
                temperature=0.1
            )
        elif provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            return ChatOpenAI(
                model="gpt-4",
                openai_api_key=api_key,
                temperature=0.1
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def _create_prompt_template(self) -> PromptTemplate:
            """Create the prompt template for query generation"""
            template = """You are an expert MongoDB query generator specializing in financial reconciliation systems. Convert natural language questions into MongoDB aggregation pipelines.

        COLLECTION SCHEMA:
        {schema}

        SAMPLE DOCUMENT:
        {sample_doc}

        USER QUESTION: {query}

        RECONCILIATION SYSTEM CONTEXT:
        This is a financial reconciliation system with the following data flow:
        1. matchmethod - Main reconciliation configuration
        2. matchingrules - Rules for matching (e.g., "American Express", "Mastercard")
        3. datasources - Source data collections (POS data, Credit Card statements)
        4. matchingResult - Results of reconciliation matching with nested cell data
        5. discrepancies - Identified mismatches with severity levels (high, medium, low)
        6. discrepancyResolution - Resolution records with status (Approved, Rejected, Pending)
        7. ticket - Issue tracking with risk levels (High, Medium, Low) and status (Progress, Resolved, Closed)

        CRITICAL FIELD PATTERNS:
        - IDs: Use ObjectId references (_id, profileId, matchingMethodId, workspaceId, organizationId)
        - Amounts: Numeric fields in "amount" columns across collections
        - Dates: ISO date format in createdAt, updatedAt, resolvedAt, expiresAt
        - Status: String enums (Completed, Settled, Approved, Progress, etc.)
        - Vendor Types: "American Express", "Mastercard", "AMERICAN EXPRESS" (case-insensitive)
        - Nested Data: matchingResult contains deeply nested "cells" and "sources" arrays

        INSTRUCTIONS:
        1. Analyze the question and identify which collections are needed
        2. For reconciliation queries, consider joining multiple collections using $lookup
        3. Generate a MongoDB aggregation pipeline as a JSON array
        4. Use appropriate stages: $match, $group, $project, $sort, $limit, $lookup, $unwind
        5. Return ONLY the JSON array, no explanations or markdown
        6. Ensure field names match the schema exactly (case-sensitive)
        7. For aggregations, use operators: $sum, $avg, $max, $min, $count
        8. For date operations, use $dateToString, $dateFromString, or date operators
        9. For array operations in matchingResult, use $unwind and $arrayElemAt
        10. For discrepancy analysis, filter by severity or type fields

        RECONCILIATION-SPECIFIC EXAMPLES:

        - "Show total discrepancies by severity" → [
            {{"$match": {{"severity": {{"$exists": true}}}}}},
            {{"$group": {{"_id": "$severity", "count": {{"$sum": 1}}}}}},
            {{"$sort": {{"count": -1}}}}
        ]

        - "List American Express transactions with amounts" → [
            {{"$match": {{"vendorType": {{"$regex": "american express", "$options": "i"}}}}}},
            {{"$project": {{"date": 1, "amount": 1, "vendorType": 1}}}},
            {{"$sort": {{"date": -1}}}}
        ]

        - "Show matching results with their discrepancies" → [
            {{"$lookup": {{
            "from": "discrepancies",
            "localField": "_id",
            "foreignField": "matchResultsId",
            "as": "discrepancies"
            }}}},
            {{"$match": {{"discrepancies": {{"$ne": []}}}}}},
            {{"$project": {{"matchId": 1, "discrepancies.severity": 1, "discrepancies.type": 1}}}}
        ]

        - "Count tickets by status and risk" → [
            {{"$group": {{
            "_id": {{"status": "$status", "risk": "$risk"}},
            "count": {{"$sum": 1}}
            }}}},
            {{"$sort": {{"count": -1}}}}
        ]

        - "Total amount reconciled per vendor type" → [
            {{"$lookup": {{
            "from": "matchingResult",
            "localField": "_id",
            "foreignField": "matchingMethodId",
            "as": "results"
            }}}},
            {{"$unwind": "$results"}},
            {{"$unwind": "$results.rows"}},
            {{"$unwind": "$results.rows.cells"}},
            {{"$group": {{
            "_id": "$ruleName",
            "totalAmount": {{"$sum": "$results.rows.cells.value"}}
            }}}},
            {{"$sort": {{"totalAmount": -1}}}}
        ]

        - "Find unresolved high severity discrepancies" → [
            {{"$match": {{
            "severity": "high"
            }}}},
            {{"$lookup": {{
            "from": "discrepancyResolution",
            "localField": "_id",
            "foreignField": "discrepancyId",
            "as": "resolution"
            }}}},
            {{"$match": {{"resolution": []}}}},
            {{"$project": {{"type": 1, "details": 1, "severity": 1, "createdAt": 1}}}}
        ]

        GENERATE THE PIPELINE (JSON array only):"""

            return PromptTemplate(
                input_variables=["schema", "sample_doc", "query"],
                template=template
            )
    
    def generate_pipeline(self, query: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate MongoDB aggregation pipeline from natural language
        
        Args:
            query: Natural language query
            schema: Collection schema information
            
        Returns:
            Dictionary containing pipeline, explanation, and metadata
        """
        try:
            # Format schema for prompt
            schema_str = self._format_schema(schema)
            sample_doc = json.dumps(schema.get('sample_document', {}), indent=2)
            
            # Generate pipeline using LLM
            print(f"🤖 Generating pipeline for: '{query}'")
            response = self.chain.invoke({
                "schema": schema_str,
                "sample_doc": sample_doc,
                "query": query
            })
            
            # Extract and parse pipeline
            pipeline_text = response['text'].strip()
            pipeline = self._extract_pipeline(pipeline_text)
            
            return {
                "success": True,
                "pipeline": pipeline,
                "query": query,
                "raw_response": pipeline_text
            }
            
        except Exception as e:
            print(f"❌ Pipeline generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "pipeline": []
            }
    
    def _format_schema(self, schema: Dict[str, Any]) -> str:
        """Format schema information for prompt"""
        if not schema.get('fields'):
            return "No schema information available"
        
        field_list = []
        for field in schema['fields']:
            types = ', '.join(field['types'])
            field_list.append(f"  - {field['name']}: {types}")
        
        return "\n".join(field_list)
    
    def _extract_pipeline(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract and parse MongoDB pipeline from LLM response
        
        Args:
            text: Raw LLM response
            
        Returns:
            Parsed pipeline as list of dictionaries
        """
        # Remove markdown code blocks if present
        text = text.strip()
        if text.startswith('```'):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1]) if len(lines) > 2 else text
        
        # Remove any "json" language identifier
        text = text.replace('```json', '').replace('```', '').strip()
        
        try:
            # Try to parse as JSON
            pipeline = json.loads(text)
            
            # Ensure it's a list
            if not isinstance(pipeline, list):
                pipeline = [pipeline]
            
            return pipeline
            
        except json.JSONDecodeError as e:
            print(f"⚠️  Failed to parse pipeline JSON: {e}")
            print(f"Response text: {text[:200]}")
            
            # Fallback: return empty pipeline
            return []
    
    def validate_pipeline(self, pipeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate the generated pipeline structure
        
        Args:
            pipeline: MongoDB aggregation pipeline
            
        Returns:
            Validation result with any warnings
        """
        warnings = []
        
        if not pipeline:
            warnings.append("Empty pipeline generated")
        
        # Check for common issues
        valid_stages = {
            '$match', '$group', '$project', '$sort', '$limit', '$skip',
            '$unwind', '$lookup', '$addFields', '$count', '$sample'
        }
        
        for i, stage in enumerate(pipeline):
            if not isinstance(stage, dict):
                warnings.append(f"Stage {i} is not a dictionary")
                continue
            
            stage_names = set(stage.keys())
            invalid = stage_names - valid_stages
            if invalid:
                warnings.append(f"Stage {i} contains unknown operators: {invalid}")
        
        return {
            "valid": len(warnings) == 0,
            "warnings": warnings,
            "stage_count": len(pipeline)
        }


# Create singleton instance
query_agent = QueryAgent()
