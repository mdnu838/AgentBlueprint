# AgentBlueprint

**A modular, agentic workflow engine for Python.**

AgentBlueprint is a comprehensive toolkit for building and orchestrating AI agents. It supports sequential, parallel, and graph-based workflows, integrated with a powerful tool system and modern observability features.

## 🚀 Features

*   **Flexible Workflows**: Orchestrate agents using Sequential, Parallel, or DAG-based Graph workflows.
*   **Pluggable LLMs**: Switch between providers seamlessly (e.g., OpenAI, Mock) using a unified `LLMProvider` interface.
*   **Rich Tool Ecosystem**: Includes built-in tools for Python execution, Web Search, and HTTP requests, with an easy API to build your own.
*   **Agent Memory**: Built-in short-term memory system handling context windows.
*   **Observability First**: Real-time structured logging and event tracing (Callback system).
*   **Production Ready**: CLI tools for scaffolding (`ab init`), deployment (`ab docker`), and execution (`ab run`).

## 📦 Installation

This project is managed with `uv`.

```bash
# Clone the repository
git clone https://github.com/your-org/AgentBlueprint.git
cd AgentBlueprint

# Install dependencies
uv sync
```

## 🛠️ Quick Start

### 1. Initialize a Project

Create a new AgentBlueprint project with the standard structure:

```bash
uv run ab init my-agent-app
cd my-agent-app
uv sync
```

### 2. Configure Your Agent

Check `workflow.yaml` to define your agent and its behavior:

```yaml
agents:
  researcher:
    model: openai:gpt-4
    system_prompt: "You are a research assistant."
    tools:
      - web_search

workflow:
  type: sequential
  steps:
    - agent: researcher
```

Don't forget to set your API keys in `.env`:
```bash
cp .env.example .env
# Edit .env with your OPENAI_API_KEY
```

### 3. Run the Workflow

```bash
uv run ab run workflow.yaml --input "What is the latest version of Python?"
```

## 🏗️ Architecture

The project is structured as a mono-repo with the following packages:

*   **`agentblueprint-core`**: The runtime engine (Agents, Workflows, Memory, LLM Providers).
*   **`agentblueprint-cli`**: The command-line interface (`ab`).
*   **`agentblueprint-tools`**: A collection of standard tools (Search, Calculator, REPL).
*   **`agentblueprint-config`**: Configuration loading and parsing logic (YAML/JSON).

## 🧪 Testing

Run the test suite with `pytest`:

```bash
uv run pytest
```

## 🐳 Deployment

Generate a production-ready Dockerfile:

```bash
uv run ab docker
docker build -t my-agent-app .
```
