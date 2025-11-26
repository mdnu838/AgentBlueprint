# AgentBlueprint - Developer Guide

**AgentBlueprint** is a lightweight, fast, and flexible project scaffolding tool for Python frameworks and AI agents. This guide helps developers and beginners get started quickly.

**Terminal command prefix**: `ab`

---

## 📖 Table of Contents

1. [Quick Start](#-quick-start)
2. [Installation](#-installation)
3. [Creating Your First Project](#-creating-your-first-project)
4. [Building AI Agents](#-building-ai-agents)
5. [Multi-Agent Workflows](#-multi-agent-workflows)
6. [Project Structure](#-project-structure)
7. [Configuration](#-configuration)
8. [Tools and Tool Packs](#-tools-and-tool-packs)
9. [Deployment](#-deployment)
10. [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

```bash
# Install AgentBlueprint
pip install agentblueprint

# Create a FastAPI project
ab fastapi myproject

# Create an AI agent
ab agent myagent
```

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install via pip

```bash
pip install agentblueprint
```

### Verify Installation

```bash
ab --version
```

---

## 🏗️ Creating Your First Project

### Web Framework Projects

AgentBlueprint supports multiple Python frameworks:

#### FastAPI

```bash
ab fastapi myapi
cd myapi
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Flask

```bash
ab flask myflask
cd myflask
pip install -r requirements.txt
python app/main.py
```

#### Django

```bash
ab django mydjango
cd mydjango
pip install -r requirements.txt
python manage.py runserver
```

---

## 🤖 Building AI Agents

Create intelligent agents with built-in tools and configurations.

### Basic Agent

```bash
ab agent myagent
cd myagent
pip install -r requirements.txt
python agent/core.py
```

### Agent with Tool Pack

```bash
ab agent myagent --toolpack basic
```

### Agent File Structure

```
myagent/
  agent/
    core.py           # Main agent logic
    tools/
      __init__.py     # Tool registry
      search.py       # Search tool
      calculator.py   # Math operations
      file_reader.py  # File operations
      http_request.py # HTTP calls
  config/
    settings.yaml     # Agent configuration
  requirements.txt
  README.md
```

---

## 🔗 Multi-Agent Workflows

Create systems where multiple agents collaborate to solve complex tasks.

### Workflow Pattern

```python
# Example multi-agent workflow
from agent.core import Agent

# Create specialized agents
researcher = Agent(name="researcher", tools=["search", "http_request"])
analyzer = Agent(name="analyzer", tools=["calculator", "file_reader"])
writer = Agent(name="writer", tools=["file_writer"])

# Define workflow
def research_workflow(topic):
    # Step 1: Researcher gathers information
    research_data = researcher.run(f"Research {topic}")
    
    # Step 2: Analyzer processes data
    analysis = analyzer.run(f"Analyze: {research_data}")
    
    # Step 3: Writer creates report
    report = writer.run(f"Write report: {analysis}")
    
    return report
```

### Communication Between Agents

Agents can share data through:

1. **Direct passing**: Pass output from one agent as input to another
2. **Shared state**: Use a common data store
3. **Event-based**: Publish/subscribe pattern for loose coupling

### Example: Research and Report Pipeline

```bash
# Create the project
ab agent research_pipeline --toolpack ai

# File: agent/workflows/research_report.py
```

```python
class ResearchReportWorkflow:
    def __init__(self):
        self.researcher = Agent(role="researcher")
        self.writer = Agent(role="writer")
    
    def execute(self, topic):
        # Research phase
        data = self.researcher.search(topic)
        
        # Writing phase
        report = self.writer.summarize(data)
        
        return report
```

---

## 📁 Project Structure

### Standard Layout

```
myproject/
├── app/                    # Application code
│   └── main.py             # Entry point
├── agent/                  # AI agent code
│   ├── core.py             # Agent logic
│   └── tools/              # Agent tools
├── config/                 # Configuration
│   └── settings.yaml       # Settings file
├── tests/                  # Test files
│   └── test_*.py           # Test modules
├── experimental/           # Experimental code
├── internal_docs/          # Internal documentation
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

### Folder Purposes

| Folder | Purpose |
|--------|---------|
| `app/` | Main application code |
| `agent/` | AI agent components |
| `config/` | Configuration files |
| `tests/` | Test files |
| `experimental/` | Work-in-progress code (git ignored) |
| `internal_docs/` | Internal documentation |

---

## ⚙️ Configuration

### settings.yaml

```yaml
# config/settings.yaml
agent:
  name: "my-agent"
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 2000

tools:
  enabled:
    - search
    - calculator
    - file_reader
    - http_request

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Environment Variables

For sensitive data, use environment variables:

```bash
export OPENAI_API_KEY="your-api-key"
export DATABASE_URL="your-database-url"
```

---

## 🧰 Tools and Tool Packs

### Built-in Tools

| Tool | Description |
|------|-------------|
| `search` | Web search functionality |
| `calculator` | Mathematical operations |
| `file_reader` | Read local files |
| `http_request` | Make HTTP API calls |

### Tool Packs

#### Basic Pack

```bash
ab agent myagent --toolpack basic
```

Includes: search, calculator, file_reader, http_request

#### AI Pack

```bash
ab agent myagent --toolpack ai
```

Includes: Basic tools + LLM-specific utilities

### Creating Custom Tools

```python
# agent/tools/custom_tool.py
from agent.tools import BaseTool

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "Description of what this tool does"
    
    def run(self, input_data):
        # Tool logic here
        result = self.process(input_data)
        return result
```

---

## 🐳 Deployment

### Add Docker Support

```bash
ab deploy docker
```

This creates:
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

### Build and Run

```bash
docker-compose up --build
```

### GitHub Actions

```bash
ab deploy github-actions
```

Creates `.github/workflows/main.yml` for CI/CD.

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Command not found: ab

```bash
# Ensure AgentBlueprint is installed
pip install agentblueprint

# Or check PATH
python -m agentblueprint --version
```

#### 2. Missing dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configuration errors

Check `config/settings.yaml` for syntax errors.

#### 4. Agent not responding

- Verify API keys are set
- Check network connectivity
- Review logs for errors

### Getting Help

- Check [internal_docs/TASK_TRACKER.md](internal_docs/TASK_TRACKER.md) for known issues
- Review [.github/copilot-instructions.md](.github/copilot-instructions.md) for development guidance

---

## 📄 License

MIT

---

## 🤝 Contributing

Contributions welcome! Please keep additions simple and focused.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## 🌟 Summary

AgentBlueprint provides a **simple, clean, and practical** foundation for:

- Python web framework projects
- AI agent development
- Multi-agent workflows

Start building today with `ab`!
