"""
The 'init' command for AgentBlueprint CLI.
"""
import click
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

TEMPLATE_PYPROJECT = """[project]
name = "{project_name}"
version = "0.1.0"
description = "A new AgentBlueprint project"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "agentblueprint-core",
    "agentblueprint-tools",
    "agentblueprint-config",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

TEMPLATE_README = """# {project_name}

Created with AgentBlueprint.

## Getting Started

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the default workflow:
   ```bash
   ab run workflow.yaml --input "Hello World"
   ```
"""

TEMPLATE_WORKFLOW = """agents:
  assistant:
    model: mock:gpt-4
    system_prompt: "You are a helpful assistant."
    tools:
      - echo

workflow:
  type: sequential
  steps:
    - agent: assistant
"""

TEMPLATE_MAIN = """from agentblueprint_core import Agent, SequentialWorkflow
from agentblueprint_tools import EchoTool

def main():
    agent = Agent(
        name="assistant",
        model="mock:gpt-4",
        system_prompt="You are a helpful assistant.",
        tools=[EchoTool()]
    )
    
    workflow = SequentialWorkflow(
        name="default",
        agents=[agent]
    )
    
    print(workflow.run("Hello from code!"))

if __name__ == "__main__":
    main()
"""

TEMPLATE_ENV = """# API Keys
OPENAI_API_KEY=sk-...
"""

TEMPLATE_GITIGNORE = """
__pycache__/
*.pyc
.env
.venv/
dist/
.DS_Store
"""

@click.command()
@click.argument("project_name")
def init(project_name):
    """Initialize a new AgentBlueprint project."""
    console.print(f"[bold blue]AgentBlueprint[/bold blue]: Initializing project [green]{project_name}[/green]...")
    
    base_path = Path(project_name)
    
    if base_path.exists():
        console.print(f"[red]Error: Directory '{project_name}' already exists.[/red]")
        return
    
    # Create directories
    try:
        base_path.mkdir(parents=True)
        (base_path / "src" / project_name).mkdir(parents=True)
        
        # Create files
        (base_path / "pyproject.toml").write_text(TEMPLATE_PYPROJECT.format(project_name=project_name))
        (base_path / "README.md").write_text(TEMPLATE_README.format(project_name=project_name))
        (base_path / "workflow.yaml").write_text(TEMPLATE_WORKFLOW)
        (base_path / ".env.example").write_text(TEMPLATE_ENV)
        (base_path / ".gitignore").write_text(TEMPLATE_GITIGNORE)
        (base_path / "src" / project_name / "__init__.py").write_text("")
        (base_path / "src" / project_name / "main.py").write_text(TEMPLATE_MAIN)
        
        console.print(Panel(
            f"Project ready at [bold]{base_path.absolute()}[/bold]\n\n"
            "Run [bold]cd {project_name} && uv sync[/bold] to get started.\n"
            "Don't forget to copy [bold].env.example[/bold] to [bold].env[/bold] and set your keys!",
            title="Success",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[bold red]Error creating project:[/bold red] {e}")
        # Cleanup
        import shutil
        if base_path.exists():
            shutil.rmtree(base_path)
