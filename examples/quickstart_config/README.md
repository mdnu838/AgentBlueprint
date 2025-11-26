# Quick Start: Config-First Workflow

This example shows how to create a multi-agent workflow using only YAML configuration.

## Files

- `workflow.yaml` - The workflow definition
- `run.py` - Simple script to run the workflow

## Usage

```bash
# Install dependencies
uv sync

# Run the workflow
uv run python run.py "Explain the benefits of uv package manager"
```

## How It Works

The workflow defines two agents:
1. **Researcher** - Searches for information
2. **Writer** - Synthesizes the research into clear text

They work sequentially: researcher → writer
