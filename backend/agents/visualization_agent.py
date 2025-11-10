"""
Visualization Agent - Determines chart type and generates visualization configuration
"""
from typing import Dict, Any, List
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()


class VisualizationAgent:
    """
    Determines optimal chart type and generates visualization configuration
    """
    
    # Supported chart types
    CHART_TYPES = ['bar', 'line', 'pie', 'scatter', 'area', 'table']
    
    def __init__(self):
        """Initialize the Visualization Agent"""
        self.llm = self._initialize_llm()
        self.prompt_template = self._create_prompt_template()
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def _initialize_llm(self):
        """Initialize LLM based on environment configuration"""
        provider = os.getenv('LLM_PROVIDER', 'gemini').lower()
        
        if provider == 'gemini':
            api_key = os.getenv('GOOGLE_API_KEY')
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=api_key,
                temperature=0.1
            )
        elif provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            return ChatOpenAI(
                model="gpt-4",
                openai_api_key=api_key,
                temperature=0.1
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create prompt template for chart type selection"""
        template = """You are a data visualization expert. Analyze the data and recommend the best chart type.

USER QUERY: {query}

DATA PREVIEW (first 5 rows):
{data_preview}

DATA SUMMARY:
- Total rows: {row_count}
- Columns: {columns}

AVAILABLE CHART TYPES:
- bar: Compare categories or show rankings
- line: Show trends over time or continuous data
- pie: Show proportions of a whole (max 10 categories)
- scatter: Show correlation between two variables
- area: Show cumulative totals or trends
- table: Display raw data when no clear visualization pattern

INSTRUCTIONS:
1. Choose the MOST appropriate chart type
2. Identify which columns to use for X and Y axes (or labels/values for pie)
3. Provide a clear title for the chart
4. Return ONLY a JSON object in this exact format:

{{
  "chart_type": "bar",
  "x_axis": "column_name",
  "y_axis": "column_name",
  "title": "Descriptive Chart Title",
  "reasoning": "Brief explanation"
}}

For pie charts, use "labels" and "values" instead of x_axis and y_axis.

GENERATE THE JSON RESPONSE:"""

        return PromptTemplate(
            input_variables=["query", "data_preview", "row_count", "columns"],
            template=template
        )    
    def generate_chart_config(self, data: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """
        Generate chart configuration based on data and query
        
        Args:
            data: Query results from MongoDB
            query: Original user query
            
        Returns:
            Chart configuration with type, axes, and styling
        """
        try:
            if not data:
                return self._empty_chart_config("No data available")
            
            # Convert to pandas for analysis
            df = pd.DataFrame(data)
            
            # Clean column names (remove _id if it's the only grouping key)
            df = self._clean_dataframe(df)
            
            # Generate preview and summary
            data_preview = df.head(5).to_string()
            columns = list(df.columns)
            row_count = len(df)
            
            print(f"📊 Analyzing data for visualization...")
            print(f"   Rows: {row_count}, Columns: {columns}")
            
            # Get LLM recommendation
            response = self.chain.invoke({
                "query": query,
                "data_preview": data_preview,
                "row_count": row_count,
                "columns": ", ".join(columns)
            })
            
            # Parse response
            config = self._parse_chart_config(response['text'])
            
            # Enhance with actual data
            config['data'] = df.to_dict('records')
            config['columns'] = columns
            
            return config
            
        except Exception as e:
            print(f"❌ Chart generation failed: {e}")
            return self._empty_chart_config(f"Error: {str(e)}")
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare dataframe for visualization"""
        # Rename _id to more meaningful name if it's the only grouping
        if '_id' in df.columns and len(df.columns) == 2:
            # Get the other column name
            other_col = [col for col in df.columns if col != '_id'][0]
            # Rename _id based on context
            df = df.rename(columns={'_id': 'category'})
        
        return df
    
    def _parse_chart_config(self, text: str) -> Dict[str, Any]:
        """Parse LLM response into chart configuration"""
        text = text.strip()
        
        # Remove markdown code blocks
        if text.startswith('```'):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1]) if len(lines) > 2 else text
        
        text = text.replace('```json', '').replace('```', '').strip()
        
        try:
            config = json.loads(text)
            
            # Validate required fields
            if 'chart_type' not in config:
                config['chart_type'] = 'bar'
            
            if config['chart_type'] not in self.CHART_TYPES:
                config['chart_type'] = 'bar'
            
            return {
                "success": True,
                "chart_type": config.get('chart_type', 'bar'),
                "x_axis": config.get('x_axis'),
                "y_axis": config.get('y_axis'),
                "labels": config.get('labels'),
                "values": config.get('values'),
                "title": config.get('title', 'Data Visualization'),
                "reasoning": config.get('reasoning', '')
            }
            
        except json.JSONDecodeError as e:
            print(f"⚠️  Failed to parse chart config: {e}")
            # Fallback to rule-based selection
            return self._rule_based_chart_selection()
    
    def _rule_based_chart_selection(self) -> Dict[str, Any]:
        """Fallback rule-based chart type selection"""
        return {
            "success": True,
            "chart_type": "bar",
            "title": "Data Visualization",
            "reasoning": "Using default bar chart"
        }
    
    def _empty_chart_config(self, message: str) -> Dict[str, Any]:
        """Return empty chart configuration"""
        return {
            "success": False,
            "chart_type": "table",
            "title": "No Visualization",
            "data": [],
            "error": message
        }
    
    def create_plotly_figure(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a Plotly figure configuration
        
        Args:
            config: Chart configuration from generate_chart_config
            
        Returns:
            Plotly figure JSON (fully serializable)
        """
        import plotly.graph_objects as go
        import plotly.express as px
        
        if not config.get('success') or not config.get('data'):
            return {"data": [], "layout": {"title": "No data to display"}}
        
        df = pd.DataFrame(config['data'])
        chart_type = config['chart_type']
        
        try:
            if chart_type == 'bar':
                fig = px.bar(
                    df,
                    x=config.get('x_axis') or df.columns[0],
                    y=config.get('y_axis') or df.columns[1],
                    title=config['title']
                )
            
            elif chart_type == 'line':
                fig = px.line(
                    df,
                    x=config.get('x_axis') or df.columns[0],
                    y=config.get('y_axis') or df.columns[1],
                    title=config['title']
                )
            
            elif chart_type == 'pie':
                fig = px.pie(
                    df,
                    names=config.get('labels') or df.columns[0],
                    values=config.get('values') or df.columns[1],
                    title=config['title']
                )
            
            elif chart_type == 'scatter':
                fig = px.scatter(
                    df,
                    x=config.get('x_axis') or df.columns[0],
                    y=config.get('y_axis') or df.columns[1],
                    title=config['title']
                )
            
            elif chart_type == 'area':
                fig = px.area(
                    df,
                    x=config.get('x_axis') or df.columns[0],
                    y=config.get('y_axis') or df.columns[1],
                    title=config['title']
                )
            
            else:  # table
                fig = go.Figure(data=[go.Table(
                    header=dict(values=list(df.columns)),
                    cells=dict(values=[df[col] for col in df.columns])
                )])
                fig.update_layout(title=config['title'])
            
            # Convert to JSON using Plotly's built-in JSON encoder
            # This ensures all Plotly objects are properly serialized
            fig_dict = json.loads(fig.to_json())
            
            return fig_dict
            
        except Exception as e:
            print(f"❌ Plotly figure creation failed: {e}")
            import traceback
            traceback.print_exc()
            return {"data": [], "layout": {"title": f"Error: {str(e)}"}}


# Create singleton instance

visualization_agent = VisualizationAgent()
