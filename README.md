# AgentBlueprint

**A uv-powered Python toolkit for building multi-agent systems with flexible workflows.**

🚀 **Build multi-agent systems in minutes, not hours**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## ✨ Key Features

- 🖥️ **CLI & Config-First**: Use code OR YAML/JSON configs
- 🧩 **Modular Design**: Mix and match tools, agents, workflows
- ⚡ **Modern Python**: Built with uv, Pydantic, and type hints
- 🔧 **Extensible**: Easy to add custom tools and agents
- 📦 **Mono-Repo**: Clean workspace structure for teams

---

## 🎯 Who Is This For?

✅ **Beginners** - No coding required! Use YAML configs to create agents  
✅ **Developers** - Code-first API for full control  
✅ **Teams** - Mono-repo structure with clear separation

---

## 🚀 Quick Start

### Installation

```bash
# Install via uv
uv tool install agentblueprint

# Verify
ab --version
```

### Create Your First Agent (YAML)

```yaml
# workflow.yaml
agents:
  assistant:
    model: openai:gpt-4
    system_prompt: "You are a helpful assistant."
    tools: []

workflow:
  type: sequential
  steps:
    - agent: assistant
      input: "{{ user_input }}"
```

```bash
ab run workflow.yaml --input "Hello, world!"
```

### Create Your First Agent (Code)

```python
from agentblueprint_core import Agent

agent = Agent(
    name="assistant",
    model="openai:gpt-4",
    system_prompt="You are a helpful assistant."
)

response = agent.run("Hello, world!")
print(response)
```

---

## 📚 Documentation

- **[Full Design Doc](README_v2.md)** - Complete architecture and roadmap
- **[Examples](examples/)** - Code samples and workflows
- **[Contributing](CONTRIBUTING.md)** - How to contribute

---

## 🏗️ Project Structure

```
agentblueprint/
├── packages/
│   ├── agentblueprint-core/     # Core agent runtime
│   ├── agentblueprint-cli/      # CLI tool
│   ├── agentblueprint-tools/    # Pre-built tools
│   └── agentblueprint-config/   # Config management
├── examples/                     # Example workflows
├── tests/                        # Integration tests
├── experiments/                  # Internal experiments (gitignored)
└── internal_docs/                # Internal docs (gitignored)
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Clone and setup
git clone https://github.com/yourusername/agentblueprint.git
cd agentblueprint
uv sync

# Run tests
uv run pytest

# Format code
uv run ruff format .
```

---

## 📄 License

Apache-2.0 - see [LICENSE](LICENSE) for details.

---

## 🌟 Why AgentBlueprint?

| Feature | AgentBlueprint | Others |
|---------|---------------|--------|
| **uv-native** | ✅ | ❌ |
| **Config-first option** | ✅ | Limited |
| **Mono-repo structure** | ✅ | ❌ |
| **Beginner-friendly** | ✅ YAML configs | Code-only |
| **Production-ready** | ✅ | Varies |

---

**Build smarter agents, faster. 🚀**

[Get Started](README_v2.md) | [Examples](examples/) | [Documentation](README_v2.md)

* **FastAPI**
* **Flask**
* **Django**
* **OpenAPI-based services**
* **TensorFlow inference API basics**
* **Simple combinations** (e.g., FastAPI + OpenAI)

No over-complicated integrations. Only essential boilerplate.

### 🧠 Agent Generator (`ab agent`)

Bootstrap an AI agent with:

* Basic agent loop
* Configurable tool system
* A small set of built-in tools:

  * Search
  * Math/Calculator
  * File Reader
  * Simple HTTP Request tool

The goal: a clean starting point, not an overloaded framework.

### 🧩 Optional Tool Packs (Simplified)

Add minimal optional packs:

```
ab agent --toolpack basic
ab agent --toolpack ai
```

These packs remain lightweight.

### 🔨 Optional DevOps Essentials

(Optional, not required)

* Dockerfile
* requirements.txt
* Basic GitHub Actions workflow

### 📘 Documentation Templates

* Simple README
* Basic API docs (if generating FastAPI)

---

## 🧱 Example Folder Structure

```
myproject/
  app/
    main.py
  agent/
    core.py
    tools/
  config/
    settings.yaml
  requirements.txt
  README.md
```

---

## 🖥 Basic Commands

### Create a web project

```
ab fastapi
ab flask
ab django
```

### Create an AI agent

```
ab agent
ab agent --toolpack basic
```

### Add optional devops

```
ab deploy docker
```

---

## 🧭 Roadmap (Simplified)

* Expand clean templates for more frameworks
* Add a few more lightweight tools for agents
* Improve CLI help & ergonomics

---

## 📄 License

MIT

---

## 🤝 Contributions

Contributions welcome — keep additions simple and focused.

---

## 🌟 Summary

AgentBlueprint is a **simple, clean, and practical** scaffolding generator for Python projects and AI agents. It avoids bloat and focuses on what developers need most: a strong, minimal foundation to build on.
