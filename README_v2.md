# AgentBlueprint - Multi-Agent System Builder

A **uv-powered** Python mono-repo for building multi-agent systems with flexible workflows. Accessible for beginners, powerful for experienced developers.

**Create multi-agent workflows via:**
- 🖥️ **CLI commands** (`ab ...`)
- 📄 **YAML/JSON config files**

---

## 🎯 Project Vision

AgentBlueprint makes it easy to:
- Spin up multi-agent systems in minutes
- Choose between code-first or config-first approaches
- Use modern Python tooling (uv package manager)
- Extend with custom tools, agents, and workflows

**Target Users:**
- Beginners learning AI agents
- Developers building agent applications  
- ML engineers creating production agent systems

---

## 🏗️ Mono-Repo Structure

```
agentblueprint/                           # mono-repo root
├── README.md                              # main documentation
├── pyproject.toml                         # uv workspace configuration
├── .gitignore                             # excludes experiments/ internal_docs/
│
├── packages/                              # publishable packages
│   ├── agentblueprint-core/               # core agent runtime
│   │   ├── src/
│   │   │   └── agentblueprint_core/
│   │   │       ├── __init__.py
│   │   │       ├── agent.py               # Agent, MultiAgentCoordinator
│   │   │       ├── workflow.py            # workflow orchestration
│   │   │       ├── tools.py               # tool registry & base classes
│   │   │       └── memory.py              # agent memory systems
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   ├── agentblueprint-cli/                # CLI tool (`ab` command)
│   │   ├── src/
│   │   │   └── agentblueprint_cli/
│   │   │       ├── __init__.py
│   │   │       ├── main.py                # CLI entrypoint
│   │   │       ├── commands/
│   │   │       │   ├── init.py            # ab init
│   │   │       │   ├── run.py             # ab run
│   │   │       │   └── config.py          # ab config
│   │   │       └── templates/             # project templates
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   ├── agentblueprint-tools/              # pre-built tools library
│   │   ├── src/
│   │   │   └── agentblueprint_tools/
│   │   │       ├── __init__.py
│   │   │       ├── web_search.py          # web search tool
│   │   │       ├── http_client.py         # HTTP request tool
│   │   │       ├── shell.py               # shell executor
│   │   │       ├── python_repl.py         # Python REPL tool
│   │   │       └── file_ops.py            # file operations
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   └── agentblueprint-config/             # config management
│       ├── src/
│       │   └── agentblueprint_config/
│       │       ├── __init__.py
│       │       ├── loader.py              # YAML/JSON config loader
│       │       ├── schema.py              # config validation (Pydantic)
│       │       └── env.py                 # .env support
│       ├── tests/
│       ├── pyproject.toml
│       └── README.md
│
├── examples/                              # user-facing examples
│   ├── quickstart_cli/                    # code-first example
│   │   ├── main.py
│   │   └── README.md
│   ├── quickstart_config/                 # config-first example
│   │   ├── workflow.yaml
│   │   ├── run.py
│   │   └── README.md
│   ├── multi_agent_team/                  # multi-agent collaboration
│   └── rag_agent/                         # RAG workflow example
│
├── tests/                                 # integration tests (cross-package)
├── experiments/                           # 🔒 INTERNAL: scratch code (gitignored)
├── internal_docs/                         # 🔒 INTERNAL: design docs (gitignored)
│
├── docs/ # documentation site / mkdocs
│ ├── mkdocs.yml
│ └── docs_src/
|
└── .github/
    └── workflows/
        ├── test.yml
        └── publish.yml
```

### 🔒 Internal-Only Folders (Gitignored)

- **`experiments/`**: Throwaway scripts, prototypes, benchmarks
- **`internal_docs/`**: Design notes, diagrams, meeting notes

Add to `.gitignore`:
```gitignore
experiments/
internal_docs/
```

---

## 📦 Package Overview

### `agentblueprint-core`
Core runtime for agents and workflows.

**Key Components:**
- `Agent`: Single agent with LLM + tools
- `MultiAgentCoordinator`: Orchestrates multiple agents  
- `Workflow`: Sequential, parallel, and graph-based workflows
- `ToolRegistry`: Register and discover tools

### `agentblueprint-cli`
Command-line interface for scaffolding and running agents.

**Commands:**
```bash
ab init my-project              # Create new project
ab run workflow.yaml            # Run config-based workflow
ab config new workflow.yaml     # Generate config template
ab tools list                   # List available tools
```

### `agentblueprint-tools`
Pre-built tools for common tasks.

**Included Tools:**
- Web search
- HTTP requests
- Shell commands
- Python REPL
- File operations

### `agentblueprint-config`
Configuration management with YAML/JSON support.

**Features:**
- Pydantic validation
- Environment variable substitution  
- Multi-file configs
- Hot reload (optional)

---

## 🚀 Installation (uv)

### For End Users

```bash
# Install the CLI globally
uv tool install agentblueprint

# Verify installation
ab --version
```

### For Development

```bash
# Clone the mono-repo
git clone https://github.com/yourusername/agentblueprint.git
cd agentblueprint

# Install with uv workspace
uv sync

# Run from source
uv run ab --help
```

---

## 💡 Quick Start

### Method 1: CLI-First (Code)

Create an agent programmatically:

```python
from agentblueprint_core import Agent, MultiAgentCoordinator
from agentblueprint_tools import WebSearchTool, PythonREPLTool

# Define agents
researcher = Agent(
    name="researcher",
    model="openai:gpt-4",
    system_prompt="You research topics thoroughly.",
    tools=[WebSearchTool(), PythonREPLTool()]
)

writer = Agent(
    name="writer",
    model="openai:gpt-4",
    system_prompt="You write clear summaries.",
    tools=[]
)

# Coordinate agents
coordinator = MultiAgentCoordinator(
    agents=[researcher, writer],
    workflow_type="sequential"
)

# Run
result = coordinator.run("Explain how uv package manager works")
print(result)
```

### Method 2: Config-First (YAML)

Create `workflow.yaml`:

```yaml
agents:
  researcher:
    model: openai:gpt-4
    system_prompt: "You research topics thoroughly."
    tools:
      - web_search
      - python_repl
  
  writer:
    model: openai:gpt-4
    system_prompt: "You write clear summaries."
    tools: []

workflow:
  type: sequential
  steps:
    - agent: researcher
      input: "{{ user_input }}"
    - agent: writer
      input_from: researcher
```

Run it:

```bash
ab run workflow.yaml --input "Explain how uv package manager works"
```

---

## 🛠️ Workflow Types

### Sequential
Agents run one after another.

```yaml
workflow:
  type: sequential
  steps:
    - agent: researcher
    - agent: writer
```

### Parallel
Agents run simultaneously.

```yaml
workflow:
  type: parallel
  agents:
    - researcher1
    - researcher2
    - researcher3
```

### Graph
Complex dependencies between agents.

```yaml
workflow:
  type: graph
  nodes:
    - id: research
      agent: researcher
    - id: write
      agent: writer
      depends_on: [research]
    - id: review
      agent: reviewer
      depends_on: [write]
```

---

## 🧩 Creating Custom Tools

Tools are simple Python functions:

```python
from agentblueprint_core import Tool

class CalculatorTool(Tool):
    name = "calculator"
    description = "Performs mathematical calculations"
    
    def run(self, expression: str) -> float:
        """Evaluate a mathematical expression."""
        return eval(expression)  # Use safe_eval in production

# Register the tool
from agentblueprint_core import ToolRegistry
ToolRegistry.register(CalculatorTool())
```

---

## 📝 Project Scaffolding

When users run `ab init my-project`, they get:

```
my-project/
├── pyproject.toml
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       └── workflows/
│           └── default.yaml
├── tests/
│   └── test_workflow.py
├── experiments/          # gitignored
├── internal_docs/        # gitignored
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Testing

Run tests across all packages:

```bash
# Run all tests
uv run pytest

# Run specific package tests
uv run pytest packages/agentblueprint-core/tests

# Run with coverage
uv run pytest --cov=agentblueprint_core
```

---

## 🗺️ Roadmap

### Phase 1: Core Foundation ✅
- [x] Basic Agent abstraction
- [x] Sequential workflows
- [x] YAML config loading
- [x] CLI scaffolding

### Phase 2: Enhanced Workflows 🚧
- [ ] Parallel workflows
- [ ] Graph-based workflows
- [ ] Agent memory systems
- [ ] Tool marketplace

### Phase 3: Production Features 📋
- [ ] Observability (OpenTelemetry)
- [ ] Authentication & security
- [ ] Web dashboard
- [ ] Docker deployment templates

### Phase 4: Advanced Features 💡
- [ ] Multi-modal agents
- [ ] Plugin system
- [ ] Cloud integrations
- [ ] Visual workflow builder

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/agentblueprint.git
cd agentblueprint
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest

# Format code
uv run ruff format .
uv run ruff check --fix .
```

---

## 📚 Documentation

- **User Guide**: [docs/user-guide.md](docs/user-guide.md)
- **API Reference**: [docs/api-reference.md](docs/api-reference.md)
- **Examples**: [examples/](examples/)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

Apache-2.0 License - see [LICENSE](LICENSE) file for details.

---

## 🌟 Why AgentBlueprint?

**For Beginners:**
- No complex setup - just YAML configs
- Pre-built tools and examples
- Clear documentation

**For Developers:**
- Code-first or config-first
- Extensible architecture
- Modern Python tooling (uv, Pydantic)

**For Teams:**
- Mono-repo structure
- Consistent patterns
- Production-ready templates

---

## 💬 Community

- **Discord**: [Join our community](#)
- **GitHub Discussions**: [Ask questions](https://github.com/yourusername/agentblueprint/discussions)
- **Twitter**: [@agentblueprint](#)

---

**Build multi-agent systems the modern way. 🚀**
