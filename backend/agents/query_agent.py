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
        template = """You are an expert MongoDB query generator. Convert natural language questions into MongoDB aggregation pipelines.

COLLECTION SCHEMA:
{schema}

SAMPLE DOCUMENT:
{sample_doc}

USER QUESTION: {query}

INSTRUCTIONS:
1. Analyze the question and determine what data is needed
2. Generate a MongoDB aggregation pipeline as a JSON array
3. Use appropriate stages: $match, $group, $project, $sort, $limit
4. Return ONLY the JSON array, no explanations
5. Ensure field names match the schema exactly
6. For aggregations, use operators like $sum, $avg, $max, $min
7. For date operations, use $dateToString or date operators

EXAMPLE QUERIES:
- "show total sales by category" → [
    {{"$group": {{"_id": "$category", "total": {{"$sum": "$amount"}}}}}},
    {{"$sort": {{"total": -1}}}}
  ]
- "average price per region" → [
    {{"$group": {{"_id": "$region", "avg_price": {{"$avg": "$price"}}}}}},
    {{"$sort": {{"avg_price": -1}}}}
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
