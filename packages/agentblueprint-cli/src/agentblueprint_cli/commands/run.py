"""
The 'run' command for AgentBlueprint CLI.
"""
import click
import os
from rich.console import Console
from rich.panel import Panel

from agentblueprint_config import load_and_parse
from agentblueprint_core import ToolRegistry
from agentblueprint_tools import (
    CalculatorTool, EchoTool, PythonREPLTool, HTTPClientTool, WebSearchTool,
    FileReadTool, FileWriteTool, SystemTimeTool, SystemInfoTool
)

console = Console()

@click.command()
@click.argument("workflow_file", type=click.Path(exists=True))
@click.option("--input", "-i", help="Initial input for the workflow")
def run(workflow_file, input):
    """Run a workflow from a configuration file."""
    from agentblueprint_cli.callbacks import RichCallbackHandler
    
    console.print(f"[bold blue]AgentBlueprint[/bold blue]: Running workflow from {workflow_file}...")
    
    # Pre-register basic tools for now
    # In a real app this might happen via plugin loading
    ToolRegistry.register(CalculatorTool())
    ToolRegistry.register(EchoTool())
    ToolRegistry.register(PythonREPLTool())
    ToolRegistry.register(HTTPClientTool())
    ToolRegistry.register(WebSearchTool())
    
    # New Tools
    ToolRegistry.register(FileReadTool())
    ToolRegistry.register(FileWriteTool())
    ToolRegistry.register(SystemTimeTool())
    ToolRegistry.register(SystemInfoTool())
    
    try:
        workflow = load_and_parse(workflow_file)
        
        console.print(f"Loaded workflow: [bold green]{workflow.name}[/bold green]")
        
        if input:
            # console.print(f"Input: [italic]{input}[/italic]") # Handled by callback now
            
            # Use RichCallbackHandler
            # We pass the same console instance we use globally
            handler = RichCallbackHandler(console=console)
            
            result = workflow.run(input, callbacks=[handler])
            
            console.print(Panel(
                f"[bold]Result:[/bold]\n{result}",
                title="Workflow Execution",
                border_style="green"
            ))
        else:
             console.print("[yellow]No input provided. Use --input to send a message.[/yellow]")

    except Exception as e:
        console.print(f"[bold red]Error running workflow:[/bold red] {e}")
