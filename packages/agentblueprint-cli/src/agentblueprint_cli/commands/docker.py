"""
The 'docker' command for AgentBlueprint CLI.
"""
import click
from pathlib import Path
from rich.console import Console

console = Console()

TEMPLATE_DOCKERFILE = """# Use a slim Python image
FROM python:3.11-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files
COPY pyproject.toml .
# Copy lock file if it exists, otherwise we'll lock during sync
# COPY uv.lock . 

# Install dependencies (only)
# We use --no-root to install dependencies first for caching layers
RUN uv sync --frozen --no-install-project || uv sync --no-install-project

# Copy source code
COPY . .

# Install the project itself
RUN uv sync --frozen || uv sync

# Default command
ENTRYPOINT ["uv", "run", "ab", "run", "workflow.yaml"]
CMD ["--input", "Hello Container"]
"""

TEMPLATE_DOCKERIGNORE = """
.git
.venv
__pycache__
*.pyc
.env
"""

@click.command()
def docker():
    """Generates a Dockerfile and .dockerignore for the project."""
    
    if Path("Dockerfile").exists():
        console.print("[yellow]Dockerfile already exists. Skipping.[/yellow]")
    else:
        Path("Dockerfile").write_text(TEMPLATE_DOCKERFILE)
        console.print("[green]Created Dockerfile[/green]")

    if Path(".dockerignore").exists():
        console.print("[yellow].dockerignore already exists. Skipping.[/yellow]")
    else:
        Path(".dockerignore").write_text(TEMPLATE_DOCKERIGNORE)
        console.print("[green]Created .dockerignore[/green]")
