"""
Tool schemas for the agent using Pydantic Models.
Each tool uses a Pydantic BaseModel for input validation and schema generation.
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Literal
import inspect

class GetTimeInput(BaseModel):
    """Input schema for get_time tool."""
    location: str = Field(
        description="The city name (eg. 'Cape Town', 'New York', 'Bangkok', 'London', 'Tokyo', 'UTC')"
    )

class CalcInput(BaseModel):
    "Input Schema for calc tool."
    expression: str = Field(
        description="A mathematical expression as a string. Supports: basic arithmetic (2+2), percentages (18% of 24500), multiplication (*), division (/), addition (+), subtraction (-)"
    )

class LookupFaqInput(BaseModel):
    """Input schema for lookup_faq tool."""
    query: str = Field(
        description="The question or search query for the FAQ knowledge base. Topics include: refund policy, shipping, business hours, payment methods, warranty"
    )

@tool(args_schema=GetTimeInput)
def get_time(location: str) -> str:
    """Get the current time for a specific location.
    
    Use this tool when the user asks about the current time in a city.
    Supports multiple cities with timezone-aware time calculations.
    """
    from src.tools.execution import execute_get_time
    return execute_get_time(location)

@tool(args_schema=CalcInput)
def calc(expression: str) -> str:
    """Calculate a mathematical expression.
    
    Use this tool for any mathematical calculations, percentages, 
    arithmetic operations, or numerical computations.
    Handles percentage calculations (e.g., '18% of 24500') and 
    standard arithmetic expressions (e.g., '2 + 2 * 3').
    """
    from src.tools.execution import execute_calc
    return execute_calc(expression)

@tool(args_schema=LookupFaqInput)
def lookup_faq(query: str) -> str:
    """Look up information from the FAQ knowledge base.
    
    Use this tool to find answers to frequently asked questions.
    Returns a JSON object with 'answer' and 'source_title' fields.
    If no match is found, returns a helpful fallback message with available topics.
    """
    from src.tools.execution import execute_lookup_faq
    return execute_lookup_faq(query)

# Export all tools
TOOLS = [get_time, calc, lookup_faq]

def display_tool_schemas():
    """Display the schema for each tool."""
    print("=" * 60)
    print("PART B.1: Tool Schema Definitions")
    print("=" * 60)
    
    for tool in TOOLS:
        print(f"\n{'-' * 60}")
        print(f"Tool Name: {tool.name}")
        print(f"Description: {tool.description}")
        print(f"\nSchema:")
        
        # Check if args_schema is a class (Pydantic model)
        if tool.args_schema and inspect.isclass(tool.args_schema):
            print(f"  args_schema: {tool.args_schema.__name__}")
            
            # Display parameters
            if hasattr(tool.args_schema, 'model_fields'):
                print(f"\nParameters:")
                for field_name, field_info in tool.args_schema.model_fields.items():
                    print(f"  - {field_name}:")
                    print(f"      type: {field_info.annotation}")
                    print(f"      description: {field_info.description}")
                    print(f"      required: {field_info.is_required()}")
            
            print(f"\nFull JSON Schema:")
            import json
            if hasattr(tool.args_schema, 'model_json_schema'):
                schema_dict = tool.args_schema.model_json_schema()
            else:
                schema_dict = {}
            print(json.dumps(schema_dict, indent=2))
        else:
            print(f"  args_schema: {tool.args_schema}")


if __name__ == "__main__":
    display_tool_schemas()