# AgentBlueprint - Developer Guide

A comprehensive guide for developers and beginners to create multi-agent workflows using AgentBlueprint.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Installation](#installation)
4. [Creating Your First Project](#creating-your-first-project)
5. [Creating AI Agents](#creating-ai-agents)
6. [Multi-Agent Workflows](#multi-agent-workflows)
7. [Configuration](#configuration)
8. [Folder Structure](#folder-structure)
9. [Tool Packs](#tool-packs)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

---

## Introduction

**AgentBlueprint** is a lightweight, fast, and flexible project scaffolding tool for Python frameworks and AI agents. It generates clean, ready-to-run project templates so you can focus on building rather than setup.

### Key Features
- 🔧 **Clean Framework Scaffolding**: FastAPI, Flask, Django templates
- 🧠 **AI Agent Generator**: Bootstrap agents with configurable tools
- 🧩 **Tool Packs**: Add optional functionality with minimal overhead
- 🔨 **DevOps Ready**: Docker, GitHub Actions support

---

## Quick Start

```bash
# Install AgentBlueprint
pip install agentblueprint

# Create a FastAPI project
ab fastapi myproject

# Create an AI agent
ab agent myagent

# Create an agent with tools
ab agent myagent --toolpack basic
```

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip or uv package manager

### Using pip
```bash
pip install agentblueprint
```

### Using uv (Recommended)
```bash
uv pip install agentblueprint
```

### From Source
```bash
git clone https://github.com/yourusername/AgentBlueprint.git
cd AgentBlueprint
pip install -e .
```

---

## Creating Your First Project

### Step 1: Choose a Framework

AgentBlueprint supports multiple frameworks:

| Command | Framework | Best For |
|---------|-----------|----------|
| `ab fastapi` | FastAPI | REST APIs, async services |
| `ab flask` | Flask | Simple web apps, quick prototypes |
| `ab django` | Django | Full-featured web applications |

### Step 2: Generate the Project

```bash
ab fastapi myproject
cd myproject
```

### Step 3: Explore the Structure

```
myproject/
├── app/
│   └── main.py          # Application entry point
├── config/
│   └── settings.yaml    # Configuration file
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

### Step 4: Run Your Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

---

## Creating AI Agents

### Basic Agent

```bash
ab agent myagent
```

This creates:
```
myagent/
├── agent/
│   ├── core.py          # Main agent loop
│   └── tools/           # Agent tools directory
├── config/
│   └── settings.yaml    # Agent configuration
└── requirements.txt
```

### Agent with Tools

```bash
ab agent myagent --toolpack basic
```

The basic toolpack includes:
- 🔍 **Search**: Web search functionality
- 🔢 **Calculator**: Math operations
- 📄 **File Reader**: Read local files
- 🌐 **HTTP Request**: Make web requests

---

## Multi-Agent Workflows

### Concept

Multi-agent workflows allow multiple AI agents to work together, each with specialized roles and capabilities.

### Setting Up a Multi-Agent System

#### Step 1: Create Individual Agents

```bash
# Create a research agent
ab agent researcher --toolpack basic

# Create a writer agent
ab agent writer --toolpack basic

# Create a reviewer agent
ab agent reviewer --toolpack basic
```

#### Step 2: Configure Agent Communication

Create a workflow configuration file:

```yaml
# workflow.yaml
agents:
  - name: researcher
    role: "Research and gather information"
    tools:
      - search
      - http_request
    
  - name: writer
    role: "Write content based on research"
    tools:
      - file_reader
      - calculator
    
  - name: reviewer
    role: "Review and provide feedback"
    tools:
      - file_reader

workflow:
  - step: 1
    agent: researcher
    action: "Research the topic"
    
  - step: 2
    agent: writer
    action: "Write based on research"
    input_from: researcher
    
  - step: 3
    agent: reviewer
    action: "Review the content"
    input_from: writer
```

#### Step 3: Run the Workflow

```python
from agentblueprint import Workflow

# Load the workflow
workflow = Workflow.from_yaml("workflow.yaml")

# Execute
result = workflow.run(topic="AI in healthcare")
```

### Agent Communication Patterns

1. **Sequential**: Agents work one after another
2. **Parallel**: Multiple agents work simultaneously
3. **Hierarchical**: A supervisor agent coordinates others
4. **Collaborative**: Agents share a common workspace

---

## Configuration

### Settings File (settings.yaml)

```yaml
# Agent Configuration
agent:
  name: "MyAgent"
  model: "gpt-4"
  max_iterations: 10
  timeout: 30

# Tool Configuration
tools:
  enabled:
    - search
    - calculator
  
  search:
    api_key: "${SEARCH_API_KEY}"  # Use environment variable
    max_results: 5

# Logging
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Environment Variables

Create a `.env` file for sensitive configuration:

```bash
# .env
OPENAI_API_KEY=your-api-key
SEARCH_API_KEY=your-search-key
```

---

## Folder Structure

### Recommended Project Layout

```
myproject/
├── .github/                 # GitHub configurations
│   └── workflows/           # GitHub Actions
├── app/                     # Application code
│   ├── __init__.py
│   └── main.py
├── agent/                   # Agent-related code
│   ├── core.py              # Agent loop
│   ├── tools/               # Custom tools
│   └── prompts/             # Agent prompts
├── config/                  # Configuration files
│   └── settings.yaml
├── tests/                   # Test files
│   ├── unit/
│   └── integration/
├── docs/                    # Documentation
├── experimental/            # Experimental code (gitignored)
├── requirements.txt
├── README.md
└── .gitignore
```

### What to Include in .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
.env

# Virtual environments
venv/
.venv/

# IDE
.vscode/
.idea/

# Experimental (don't commit work-in-progress)
experimental/

# Test outputs
.pytest_cache/
coverage/
```

---

## Tool Packs

### Available Tool Packs

| Pack | Contents | Use Case |
|------|----------|----------|
| `basic` | search, calculator, file_reader, http_request | General purpose |
| `ai` | llm_call, embedding, summarizer | AI/ML tasks |

### Using Tool Packs

```bash
# Single pack
ab agent myagent --toolpack basic

# Multiple packs
ab agent myagent --toolpack basic --toolpack ai
```

### Creating Custom Tools

```python
# agent/tools/custom_tool.py
from agentblueprint.tools import Tool, tool

@tool(name="my_custom_tool", description="Does something useful")
def my_custom_tool(input_text: str) -> str:
    """Process the input text and return a result.
    
    Args:
        input_text: The text to process
        
    Returns:
        The processed result
    """
    # Your custom logic here
    result = process(input_text)
    return result
```

---

## Best Practices

### 1. Keep Agents Focused
Each agent should have a specific, well-defined role. Avoid creating "do-everything" agents.

### 2. Use Configuration Files
Don't hardcode settings. Use YAML configuration files and environment variables.

### 3. Test Your Agents
Write tests for agent behavior and tool functionality.

```python
def test_agent_responds():
    agent = MyAgent()
    response = agent.run("Hello")
    assert response is not None
```

### 4. Handle Errors Gracefully
Implement proper error handling in tools and agent logic.

### 5. Log Everything
Use logging to track agent actions and decisions for debugging.

### 6. Version Control
- Commit frequently
- Use meaningful commit messages
- Keep experimental code in the `experimental/` folder

---

## Troubleshooting

### Common Issues

#### Agent Not Responding
1. Check API keys in environment variables
2. Verify network connectivity
3. Check agent configuration in settings.yaml

#### Tool Not Working
1. Ensure the tool is in the enabled list
2. Check tool-specific configuration
3. Review logs for error messages

#### Import Errors
1. Verify all dependencies are installed
2. Check Python version compatibility
3. Try reinstalling: `pip install -r requirements.txt`

### Getting Help

- Check the [GitHub Issues](https://github.com/yourusername/AgentBlueprint/issues)
- Review the documentation
- Join the community discussions

---

## Next Steps

1. **Explore Examples**: Check the `examples/` directory for sample projects
2. **Read the API Docs**: Detailed API documentation at `/docs/api`
3. **Join the Community**: Contribute and share your experiences

---

*AgentBlueprint - Simple, Clean, Practical*
