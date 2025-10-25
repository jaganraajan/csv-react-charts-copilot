"""
CSV Agent using LangGraph with Azure OpenAI and tool binding.

This module implements a minimal agent using LangGraph's StateGraph pattern
that integrates Azure OpenAI LLM with tool binding for CSV file operations.
"""

from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import pandas as pd
import os
from pathlib import Path


# Define the agent state
class AgentState(TypedDict):
    """State definition for the agent graph."""
    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]
    csv_file_path: str


# CSV file storage path
UPLOAD_DIR = Path("/tmp/csv_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def _get_csv_path(file_path: str = "") -> str:
    """
    Helper function to get the CSV file path.
    Returns the demo file path if the provided path is empty or doesn't exist.
    
    Args:
        file_path: Path to the CSV file. If empty or non-existent, returns demo file path.
    
    Returns:
        Valid CSV file path.
    """
    if not file_path or not os.path.exists(file_path):
        return os.path.join(os.path.dirname(__file__), "demo_data.csv")
    return file_path


@tool
def read_csv_tool(file_path: str = "") -> str:
    """
    Reads CSV file and returns shape, column names, and first 5 rows.
    
    Args:
        file_path: Path to the CSV file. If empty or not provided, uses the default demo file.
    
    Returns:
        String containing CSV metadata and preview.
    """
    try:
        csv_path = _get_csv_path(file_path)
        df = pd.read_csv(csv_path)
        
        result = f"CSV File Information:\n"
        result += f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n\n"
        result += f"Column Names: {', '.join(df.columns.tolist())}\n\n"
        result += f"First 5 rows:\n{df.head().to_string()}\n"
        
        return result
    except Exception as e:
        return f"Error reading CSV file: {str(e)}"


@tool
def analyze_csv_column(column_name: str, file_path: str = "") -> str:
    """
    Provides detailed statistics for a specific column in the CSV file.
    
    For numeric columns: mean, std, min, quartiles, max, missing values
    For categorical columns: unique values, value counts, missing values
    
    Args:
        column_name: Name of the column to analyze
        file_path: Path to the CSV file. If empty or not provided, uses the default demo file.
    
    Returns:
        String containing detailed column statistics.
    """
    try:
        csv_path = _get_csv_path(file_path)
        df = pd.read_csv(csv_path)
        
        if column_name not in df.columns:
            return f"Error: Column '{column_name}' not found. Available columns: {', '.join(df.columns.tolist())}"
        
        col = df[column_name]
        result = f"Analysis of column '{column_name}':\n\n"
        
        # Check for missing values
        missing_count = col.isna().sum()
        result += f"Missing values: {missing_count} ({(missing_count/len(col)*100):.2f}%)\n\n"
        
        # Numeric column analysis
        if pd.api.types.is_numeric_dtype(col):
            result += "Column Type: Numeric\n\n"
            stats = col.describe()
            result += f"Mean: {stats['mean']:.2f}\n"
            result += f"Standard Deviation: {stats['std']:.2f}\n"
            result += f"Min: {stats['min']:.2f}\n"
            result += f"25th Percentile (Q1): {stats['25%']:.2f}\n"
            result += f"50th Percentile (Median): {stats['50%']:.2f}\n"
            result += f"75th Percentile (Q3): {stats['75%']:.2f}\n"
            result += f"Max: {stats['max']:.2f}\n"
        else:
            # Categorical column analysis
            result += "Column Type: Categorical\n\n"
            result += f"Unique values: {col.nunique()}\n\n"
            result += "Value counts:\n"
            value_counts = col.value_counts().head(10)
            for value, count in value_counts.items():
                result += f"  {value}: {count}\n"
            
            if len(value_counts) == 10 and col.nunique() > 10:
                result += f"  ... and {col.nunique() - 10} more unique values\n"
        
        return result
    except Exception as e:
        return f"Error analyzing column: {str(e)}"


@tool
def query_csv_data(query: str, file_path: str = "") -> str:
    """
    Handles natural language queries for common CSV operations.
    
    Supports queries like:
    - "count rows" or "how many rows"
    - "list columns" or "what columns are there"
    - "summary statistics" or "describe the data"
    - "show unique values in <column>"
    - "calculate sum/mean/max/min of <column>"
    
    Args:
        query: Natural language query about the CSV data
        file_path: Path to the CSV file. If empty or not provided, uses the default demo file.
    
    Returns:
        String containing the query result.
    """
    try:
        csv_path = _get_csv_path(file_path)
        df = pd.read_csv(csv_path)
        query_lower = query.lower()
        
        # Count rows
        if any(phrase in query_lower for phrase in ["count rows", "how many rows", "number of rows", "row count"]):
            return f"The CSV file has {len(df)} rows."
        
        # List columns
        if any(phrase in query_lower for phrase in ["list columns", "what columns", "column names", "show columns"]):
            return f"Columns in the CSV file: {', '.join(df.columns.tolist())}"
        
        # Summary statistics
        if any(phrase in query_lower for phrase in ["summary statistics", "describe", "overview", "summary"]):
            result = "Summary Statistics:\n\n"
            result += df.describe(include='all').to_string()
            return result
        
        # Unique values in column
        if "unique" in query_lower:
            # Try to extract column name
            for col in df.columns:
                if col.lower() in query_lower:
                    unique_vals = df[col].unique()
                    result = f"Unique values in '{col}': "
                    if len(unique_vals) <= 20:
                        result += ", ".join(str(v) for v in unique_vals)
                    else:
                        result += ", ".join(str(v) for v in unique_vals[:20])
                        result += f", ... and {len(unique_vals) - 20} more"
                    return result
            return "Please specify which column to show unique values for."
        
        # Aggregate operations (sum, mean, max, min)
        for operation in ["sum", "mean", "average", "max", "min"]:
            if operation in query_lower:
                # Try to extract column name
                for col in df.columns:
                    if col.lower() in query_lower and pd.api.types.is_numeric_dtype(df[col]):
                        if operation == "sum":
                            result = df[col].sum()
                        elif operation in ["mean", "average"]:
                            result = df[col].mean()
                        elif operation == "max":
                            result = df[col].max()
                        elif operation == "min":
                            result = df[col].min()
                        return f"The {operation} of '{col}' is: {result:.2f}"
                return f"Could not find a numeric column for {operation} operation in the query."
        
        # Default response
        return ("I can help with queries like:\n"
                "- Count rows\n"
                "- List columns\n"
                "- Summary statistics\n"
                "- Show unique values in a column\n"
                "- Calculate sum/mean/max/min of a column\n\n"
                f"Your query: '{query}' didn't match any of these patterns. Please rephrase.")
    
    except Exception as e:
        return f"Error processing query: {str(e)}"


# Create the tools list
tools = [read_csv_tool, analyze_csv_column, query_csv_data]


def create_agent(azure_endpoint: str, azure_api_key: str, azure_deployment: str):
    """
    Creates and returns a LangGraph agent with CSV tools.
    
    Args:
        azure_endpoint: Azure OpenAI endpoint URL
        azure_api_key: Azure OpenAI API key
        azure_deployment: Azure OpenAI deployment name
    
    Returns:
        Compiled LangGraph agent
    """
    
    # Initialize Azure OpenAI LLM
    llm = AzureChatOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=azure_api_key,
        azure_deployment=azure_deployment,
        api_version="2024-02-15-preview",
        temperature=0.7,
    )
    
    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools(tools)
    
    # Define the agent node
    def agent_node(state: AgentState) -> AgentState:
        """Agent node that processes messages and decides on tool usage."""
        messages = state["messages"]
        csv_file_path = state.get("csv_file_path", "")
        
        # Add system message with context about available tools
        system_message = (
            "You are a helpful assistant that can analyze CSV files. "
            "You have access to tools to read CSV files, analyze specific columns, and query data. "
            "When a user asks about CSV data, use the appropriate tool to help them. "
            f"The current CSV file path is: {csv_file_path or 'demo_data.csv (default)'}"
        )
        
        # Create messages list with system context
        messages_with_system = [HumanMessage(content=system_message)] + list(messages)
        
        # Get response from LLM
        response = llm_with_tools.invoke(messages_with_system)
        
        # Return updated state with new message
        return {"messages": messages + [response]}
    
    # Define the routing function
    def should_continue(state: AgentState) -> str:
        """Determines whether to continue to tools or end."""
        messages = state["messages"]
        last_message = messages[-1]
        
        # If there are tool calls, continue to tools node
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        
        # Otherwise, end
        return "end"
    
    # Create the tool node
    tool_node = ToolNode(tools)
    
    # Build the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Compile the graph
    return workflow.compile()


def run_agent(agent, user_message: str, csv_file_path: str = None) -> str:
    """
    Runs the agent with a user message.
    
    Args:
        agent: Compiled LangGraph agent
        user_message: User's input message
        csv_file_path: Optional path to uploaded CSV file
    
    Returns:
        Agent's response as a string
    """
    try:
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=user_message)],
            "csv_file_path": csv_file_path or ""
        }
        
        # Run the agent
        result = agent.invoke(initial_state)
        
        # Extract the final response
        final_message = result["messages"][-1]
        
        if isinstance(final_message, AIMessage):
            return final_message.content
        else:
            return str(final_message)
    
    except Exception as e:
        return f"Error running agent: {str(e)}"
