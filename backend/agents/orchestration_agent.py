"""
Orchestration Agent - Coordinates the entire workflow using LangGraph
"""
import os
from typing import Dict, Any, TypedDict, Optional
from langgraph.graph import StateGraph, END
from agents.query_agent import query_agent
from agents.visualization_agent import visualization_agent
from utils.mongo_connector import mongo_connector


class AgentState(TypedDict):
    """State shared across all agent nodes"""
    query: str
    collection: Optional[str]
    schema: Dict[str, Any]
    pipeline: list
    data: list
    chart_config: Dict[str, Any]
    plotly_figure: Dict[str, Any]
    error: str
    step: str


class OrchestrationAgent:
    """
    Orchestrates the entire BI pipeline using LangGraph
    Workflow: Query → Parse → Execute → Visualize
    """
    
    def __init__(self):
        """Initialize the orchestration graph"""
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Define nodes
        workflow.add_node("fetch_schema", self.fetch_schema_node)
        workflow.add_node("generate_query", self.generate_query_node)
        workflow.add_node("execute_query", self.execute_query_node)
        workflow.add_node("create_visualization", self.create_visualization_node)
        
        # Define edges (workflow)
        workflow.set_entry_point("fetch_schema")
        workflow.add_edge("fetch_schema", "generate_query")
        workflow.add_edge("generate_query", "execute_query")
        workflow.add_edge("execute_query", "create_visualization")
        workflow.add_edge("create_visualization", END)
        
        return workflow.compile()
    
    def fetch_schema_node(self, state: AgentState) -> AgentState:
        """Node 1: Fetch collection schema"""
        print("\n📋 Step 1: Fetching collection schema...")
        
        try:
            collection = state.get('collection') or os.getenv('MONGODB_COLLECTION', 'reconciliation_records')
            schema = mongo_connector.get_collection_schema(collection)
            state['schema'] = schema
            state['step'] = 'schema_fetched'
            print(f"✅ Schema fetched: {len(schema.get('fields', []))} fields from {collection}")
        except Exception as e:
            state['error'] = f"Schema fetch failed: {str(e)}"
            print(f"❌ {state['error']}")
        
        return state
    
    def generate_query_node(self, state: AgentState) -> AgentState:
        """Node 2: Generate MongoDB query using LLM"""
        print("\n🤖 Step 2: Generating MongoDB query...")
        
        if state.get('error'):
            return state
        
        try:
            result = query_agent.generate_pipeline(
                query=state['query'],
                schema=state['schema']
            )
            
            if result['success']:
                state['pipeline'] = result['pipeline']
                state['step'] = 'query_generated'
                print(f"✅ Pipeline generated with {len(result['pipeline'])} stages")
            else:
                state['error'] = result.get('error', 'Unknown error')
                print(f"❌ {state['error']}")
        
        except Exception as e:
            state['error'] = f"Query generation failed: {str(e)}"
            print(f"❌ {state['error']}")
        
        return state
    
    def execute_query_node(self, state: AgentState) -> AgentState:
        """Node 3: Execute query on MongoDB"""
        print("\n⚡ Step 3: Executing MongoDB query...")
        
        if state.get('error'):
            return state
        
        try:
            collection = state.get('collection') or os.getenv('MONGODB_COLLECTION', 'reconciliation_records')
            data = mongo_connector.execute_aggregation(state['pipeline'], collection)
            state['data'] = data
            state['step'] = 'query_executed'
            print(f"✅ Query executed: {len(data)} records returned from {collection}")
        
        except Exception as e:
            state['error'] = f"Query execution failed: {str(e)}"
            print(f"❌ {state['error']}")
        
        return state
    
    def create_visualization_node(self, state: AgentState) -> AgentState:
        """Node 4: Create visualization configuration"""
        print("\n📊 Step 4: Creating visualization...")
        
        if state.get('error'):
            return state
        
        try:
            # Generate chart configuration
            chart_config = visualization_agent.generate_chart_config(
                data=state['data'],
                query=state['query']
            )
            state['chart_config'] = chart_config
            
            # Create Plotly figure
            if chart_config.get('success'):
                plotly_figure = visualization_agent.create_plotly_figure(chart_config)
                state['plotly_figure'] = plotly_figure
                state['step'] = 'visualization_created'
                print(f"✅ Visualization created: {chart_config['chart_type']}")
            else:
                state['error'] = chart_config.get('error', 'Visualization failed')
                print(f"❌ {state['error']}")
        
        except Exception as e:
            state['error'] = f"Visualization creation failed: {str(e)}"
            print(f"❌ {state['error']}")
        
        return state
    
    def process_query(self, query: str, collection: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a natural language query through the entire pipeline
        
        Args:
            query: Natural language question
            collection: Optional collection name to query
            
        Returns:
            Complete result with data, visualization, and metadata
        """
        print(f"\n{'='*60}")
        print(f"🚀 Processing Query: '{query}'")
        if collection:
            print(f"📊 Collection: {collection}")
        print(f"{'='*60}")
        
        # Initialize state
        initial_state: AgentState = {
            'query': query,
            'collection': collection,
            'schema': {},
            'pipeline': [],
            'data': [],
            'chart_config': {},
            'plotly_figure': {},
            'error': '',
            'step': 'initialized'
        }
        
        # Execute workflow
        final_state = self.graph.invoke(initial_state)
        
        # Format response
        response = {
            'success': not final_state.get('error'),
            'query': query,
            'pipeline': final_state.get('pipeline', []),
            'data': final_state.get('data', []),
            'chart_config': final_state.get('chart_config', {}),
            'plotly_figure': final_state.get('plotly_figure', {}),
            'metadata': {
                'step': final_state.get('step'),
                'record_count': len(final_state.get('data', [])),
                'chart_type': final_state.get('chart_config', {}).get('chart_type')
            }
        }
        
        if final_state.get('error'):
            response['error'] = final_state['error']
        
        print(f"\n{'='*60}")
        print(f"✅ Pipeline Complete: {response['success']}")
        print(f"{'='*60}\n")
        
        return response


# Create singleton instance
orchestration_agent = OrchestrationAgent()
