"""
The 'tools' command group for AgentBlueprint CLI.
"""
import click
from rich.console import Console
from rich.table import Table

from agentblueprint_core import ToolRegistry
# Import all tools to ensure they are registered for listing
from agentblueprint_tools import (
    CalculatorTool, EchoTool, PythonREPLTool, HTTPClientTool, WebSearchTool,
    FileReadTool, FileWriteTool, SystemTimeTool, SystemInfoTool
)

console = Console()

@click.group()
def tools():
    """Manage and inspect tools."""
    pass

@tools.command(name="list")
def list_tools():
    """List all available tools."""
    # Ensure standard tools are registered
    ToolRegistry.register(CalculatorTool())
    ToolRegistry.register(EchoTool())
    ToolRegistry.register(PythonREPLTool())
    ToolRegistry.register(HTTPClientTool())
    ToolRegistry.register(WebSearchTool())
    ToolRegistry.register(FileReadTool())
    ToolRegistry.register(FileWriteTool())
    ToolRegistry.register(SystemTimeTool())
    ToolRegistry.register(SystemInfoTool())
    
    available_tools = ToolRegistry.list_all()
    
    table = Table(title="Available Tools")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    
    for tool in available_tools:
        table.add_row(tool.name, tool.description)
        
    console.print(table)
