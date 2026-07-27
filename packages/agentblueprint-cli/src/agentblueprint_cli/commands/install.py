"""
The 'install' command for AgentBlueprint CLI.
"""
import click
import subprocess
import sys
from rich.console import Console

console = Console()

@click.command(name="install")
@click.argument("package")
def install(package: str):
    """Install a plugin or tool package."""
    console.print(f"[bold blue]Installing {package}...[/bold blue]")
    try:
        # Run uv pip install
        result = subprocess.run(
            ["uv", "pip", "install", package],
            check=True,
            capture_output=True,
            text=True
        )
        console.print(f"[bold green]Successfully installed {package}.[/bold green]")
        if result.stdout:
            console.print(result.stdout)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Failed to install {package}.[/bold red]")
        if e.stderr:
            console.print(f"[red]{e.stderr}[/red]")
        sys.exit(1)
    except FileNotFoundError:
        console.print("[bold red]Error: 'uv' command not found. Please ensure uv is installed.[/bold red]")
        sys.exit(1)
