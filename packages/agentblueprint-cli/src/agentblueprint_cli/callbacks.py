"""
Rich console callbacks for AgentBlueprint CLI.
"""
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from agentblueprint_core.callbacks import CallbackHandler

class RichCallbackHandler(CallbackHandler):
    """CallbackHandler that prints to a Rich Console."""
    
    def __init__(self, console: Console = None):
        self.console = console or Console()
        
    def on_workflow_start(self, name: str, input_data: Any) -> None:
        self.console.print(f"[bold cyan]Workflow Started:[/bold cyan] {name}")
        self.console.print(f"[dim]Input: {str(input_data)[:100]}...[/dim]")

    def on_workflow_end(self, name: str, output_data: Any) -> None:
        self.console.print(f"[bold cyan]Workflow Finished:[/bold cyan] {name}")

    def on_agent_start(self, name: str, input_text: str) -> None:
        self.console.print(Panel(
            Text(input_text, style="white"),
            title=f"[bold green]Agent Start: {name}[/bold green]",
            border_style="green",
            expand=False
        ))

    def on_agent_end(self, name: str, response: str) -> None:
        self.console.print(Panel(
            Text(response, style="white"),
            title=f"[bold green]Agent End: {name}[/bold green]",
            border_style="green",
            subtitle="Response",
            expand=False
        ))
