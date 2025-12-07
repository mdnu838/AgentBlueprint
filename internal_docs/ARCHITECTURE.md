# AgentBlueprint Architecture & Design

**Last Updated:** 26 November 2025

---

## 🎯 Design Principles

1. **Separation of Concerns** - Each package has a single, well-defined responsibility
2. **Extensibility** - Easy to add new tools, agents, and workflows
3. **Type Safety** - Full type hints throughout (Python 3.10+)
4. **Config-First Option** - YAML configs for beginners, code API for developers
5. **Modern Python** - Use latest Python features and best practices
6. **Testability** - Every component can be tested in isolation
7. **Documentation** - Clear docstrings and examples everywhere

---

## 📦 Package Architecture

### Overview

```
agentblueprint/
├── agentblueprint-core      # Core runtime & abstractions
├── agentblueprint-config    # Configuration management
├── agentblueprint-tools     # Pre-built tool library
└── agentblueprint-cli       # Command-line interface
```

---

## 🔷 Package: agentblueprint-core

**Responsibility:** Core runtime for agents and workflows

### Key Classes

#### Tool Base Class

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Tool(ABC):
    """
    Base class for all tools that agents can use.
    
    Tools are callable units of functionality that agents can invoke
    to perform specific tasks (search, calculate, API calls, etc.)
    """
    
    # Class-level metadata
    name: str              # Unique identifier
    description: str       # What the tool does
    parameters: Optional[Dict[str, Any]] = None  # Parameter schema
    
    @abstractmethod
    def run(self, **kwargs) -> Any:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            Tool-specific output
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary for serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
```

#### Tool Registry

```python
from typing import Dict, List, Optional

class ToolRegistry:
    """
    Global registry for tool discovery and management.
    
    Provides a centralized location for registering and
    retrieving tools by name.
    """
    
    _tools: Dict[str, Tool] = {}
    
    @classmethod
    def register(cls, tool: Tool) -> None:
        """Register a tool in the registry"""
        cls._tools[tool.name] = tool
    
    @classmethod
    def get(cls, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return cls._tools.get(name)
    
    @classmethod
    def list_all(cls) -> List[Tool]:
        """List all registered tools"""
        return list(cls._tools.values())
    
    @classmethod
    def clear(cls) -> None:
        """Clear the registry (mainly for testing)"""
        cls._tools.clear()
```

#### Agent

```python
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class Agent(BaseModel):
    """
    Single agent with LLM capabilities and tools.
    
    An agent:
    - Has a name and purpose (system prompt)
    - Uses an LLM for reasoning
    - Can use tools to perform actions
    - Maintains conversation memory
    """
    
    name: str
    model: str  # e.g., "openai:gpt-4", "anthropic:claude-3"
    system_prompt: str
    tools: List[Tool] = []
    memory: Optional['Memory'] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    
    class Config:
        arbitrary_types_allowed = True
    
    def run(self, input: str) -> str:
        """
        Execute the agent with given input.
        
        Args:
            input: User input or prompt
            
        Returns:
            Agent response
        """
        # Implementation will call LLM with tools
        pass
    
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent"""
        self.tools.append(tool)
    
    def reset_memory(self) -> None:
        """Clear agent memory"""
        if self.memory:
            self.memory.clear()
```

#### LLM Provider Interface

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMProvider(ABC):
    """
    Interface for LLM providers (OpenAI, Anthropic, etc.)
    """
    
    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tools: Optional[List[Tool]] = None
    ) -> str:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    def supports_function_calling(self) -> bool:
        """Check if provider supports function calling"""
        pass
```

#### Memory Interface

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Memory(ABC):
    """
    Interface for agent memory systems.
    
    Memory stores conversation history and context.
    """
    
    @abstractmethod
    def add(self, role: str, content: str) -> None:
        """Add a message to memory"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Dict[str, str]]:
        """Get all messages"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all messages"""
        pass
    
    @abstractmethod
    def get_recent(self, n: int) -> List[Dict[str, str]]:
        """Get n most recent messages"""
        pass
```

#### Workflow Base Class

```python
from abc import ABC, abstractmethod
from typing import Any, List

class Workflow(ABC):
    """
    Base class for agent workflows.
    
    Workflows define how agents collaborate and in what order.
    """
    
    agents: List[Agent]
    
    @abstractmethod
    def execute(self, input: Any) -> Any:
        """
        Execute the workflow.
        
        Args:
            input: Initial input to the workflow
            
        Returns:
            Final output from the workflow
        """
        pass
```

#### Sequential Workflow

```python
class SequentialWorkflow(Workflow):
    """
    Execute agents one after another.
    
    Output of agent N becomes input to agent N+1.
    """
    
    def execute(self, input: str) -> str:
        """Execute agents sequentially"""
        current_output = input
        
        for agent in self.agents:
            current_output = agent.run(current_output)
        
        return current_output
```

#### Multi-Agent Coordinator

```python
class MultiAgentCoordinator:
    """
    Coordinates multiple agents using a workflow.
    
    This is the main entry point for multi-agent systems.
    """
    
    agents: List[Agent]
    workflow: Workflow
    
    def __init__(self, agents: List[Agent], workflow: Workflow):
        self.agents = agents
        self.workflow = workflow
        self.workflow.agents = agents
    
    def run(self, input: str) -> str:
        """Execute the multi-agent workflow"""
        return self.workflow.execute(input)
```

### Dependencies

```toml
[project.dependencies]
pydantic = ">=2.0.0"
python-dotenv = ">=1.0.0"

[project.optional-dependencies]
openai = ["openai>=1.0.0"]
anthropic = ["anthropic>=0.7.0"]
all = ["openai>=1.0.0", "anthropic>=0.7.0"]
```

---

## 🔷 Package: agentblueprint-config

**Responsibility:** Configuration management and validation

### Key Classes

#### Config Schemas (Pydantic)

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AgentConfig(BaseModel):
    """Configuration for a single agent"""
    model: str = Field(..., description="LLM model to use")
    system_prompt: str = Field(..., description="System prompt for agent")
    tools: List[str] = Field(default_factory=list, description="Tool names")
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=1000, gt=0)
    max_iterations: Optional[int] = Field(default=None, description="Max reasoning iterations")


class WorkflowStepConfig(BaseModel):
    """Configuration for a workflow step"""
    id: Optional[str] = None
    agent: str = Field(..., description="Agent name")
    input: Optional[str] = None
    input_from: Optional[str] = Field(None, description="Get input from previous step")
    output_var: Optional[str] = Field(None, description="Store output in variable")
    depends_on: List[str] = Field(default_factory=list)


class WorkflowSettings(BaseModel):
    """Workflow configuration"""
    type: str = Field(..., description="Workflow type: sequential, parallel, graph")
    steps: List[WorkflowStepConfig] = Field(default_factory=list)
    agents: Optional[List[str]] = None  # For parallel workflows
    nodes: Optional[List[Dict]] = None  # For graph workflows
    output: Optional[str] = None


class GlobalConfig(BaseModel):
    """Global configuration settings"""
    max_total_iterations: int = Field(default=10)
    timeout_seconds: int = Field(default=300)
    log_level: str = Field(default="INFO")


class WorkflowConfig(BaseModel):
    """Complete workflow configuration"""
    agents: Dict[str, AgentConfig]
    workflow: WorkflowSettings
    config: GlobalConfig = Field(default_factory=GlobalConfig)
```

#### Config Loader

```python
import yaml
import json
from pathlib import Path
from typing import Union

class ConfigLoader:
    """
    Loads and validates workflow configurations.
    
    Supports YAML and JSON formats with environment variable substitution.
    """
    
    @staticmethod
    def load(path: Union[str, Path]) -> WorkflowConfig:
        """
        Load configuration from file.
        
        Args:
            path: Path to YAML or JSON config file
            
        Returns:
            Validated WorkflowConfig
        """
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        # Read file
        content = path.read_text()
        
        # Substitute environment variables
        content = ConfigLoader._substitute_env_vars(content)
        
        # Parse based on extension
        if path.suffix in ['.yaml', '.yml']:
            data = yaml.safe_load(content)
        elif path.suffix == '.json':
            data = json.loads(content)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")
        
        # Validate with Pydantic
        return WorkflowConfig(**data)
    
    @staticmethod
    def _substitute_env_vars(content: str) -> str:
        """Substitute ${VAR} with environment variables"""
        import os
        import re
        
        def replace_var(match):
            var_name = match.group(1)
            return os.getenv(var_name, match.group(0))
        
        return re.sub(r'\$\{([^}]+)\}', replace_var, content)
    
    @staticmethod
    def save_template(path: Union[str, Path], workflow_type: str = "sequential") -> None:
        """Generate a template configuration file"""
        templates = {
            "sequential": {
                "agents": {
                    "agent1": {
                        "model": "openai:gpt-4",
                        "system_prompt": "You are a helpful assistant.",
                        "tools": []
                    }
                },
                "workflow": {
                    "type": "sequential",
                    "steps": [
                        {"agent": "agent1", "input": "{{ user_input }}"}
                    ]
                }
            }
        }
        
        template = templates.get(workflow_type, templates["sequential"])
        
        path = Path(path)
        with open(path, 'w') as f:
            yaml.dump(template, f, default_flow_style=False)
```

### Dependencies

```toml
[project.dependencies]
pydantic = ">=2.0.0"
pyyaml = ">=6.0.0"
python-dotenv = ">=1.0.0"
```

---

## 🔷 Package: agentblueprint-tools

**Responsibility:** Pre-built tool library

### Tool Examples

```python
# Web Search Tool
class WebSearchTool(Tool):
    name = "web_search"
    description = "Search the web for information"
    
    def run(self, query: str) -> str:
        # Use DuckDuckGo or other search API
        pass


# HTTP Client Tool
class HTTPClientTool(Tool):
    name = "http_request"
    description = "Make HTTP requests"
    
    def run(self, url: str, method: str = "GET", **kwargs) -> str:
        # Use httpx
        pass


# Python REPL Tool
class PythonREPLTool(Tool):
    name = "python_repl"
    description = "Execute Python code"
    
    def run(self, code: str) -> Any:
        # Execute in sandboxed environment
        pass
```

### Dependencies

```toml
[project.dependencies]
agentblueprint-core = "*"
httpx = ">=0.25.0"
beautifulsoup4 = ">=4.12.0"

[project.optional-dependencies]
search = ["duckduckgo-search>=4.0.0"]
all = ["duckduckgo-search>=4.0.0"]
```

---

## 🔷 Package: agentblueprint-cli

**Responsibility:** Command-line interface

### CLI Structure

```python
import click

@click.group()
def cli():
    """AgentBlueprint CLI"""
    pass


@cli.command()
@click.argument('name')
@click.option('--template', default='basic', help='Project template')
def init(name: str, template: str):
    """Initialize a new agent project"""
    pass


@cli.command()
@click.argument('config_path')
@click.option('--input', required=True, help='Input prompt')
def run(config_path: str, input: str):
    """Run a workflow from config file"""
    pass


@cli.command()
@click.argument('output_path')
@click.option('--type', default='sequential', help='Workflow type')
def config(output_path: str, type: str):
    """Generate a config template"""
    pass
```

### Dependencies

```toml
[project.dependencies]
agentblueprint-core = "*"
agentblueprint-config = "*"
click = ">=8.1.0"
rich = ">=13.0.0"
pyyaml = ">=6.0.0"

[project.scripts]
ab = "agentblueprint_cli.main:cli"
```

---

## 🔄 Data Flow

### Config-First Workflow

```
1. User creates workflow.yaml
                ↓
2. CLI reads file with ConfigLoader
                ↓
3. Pydantic validates → WorkflowConfig
                ↓
4. Create Agent instances from config
                ↓
5. Create Workflow instance
                ↓
6. MultiAgentCoordinator executes
                ↓
7. Agents call LLM + Tools
                ↓
8. Return result to user
```

### Code-First Workflow

```
1. User writes Python code
                ↓
2. Create Agent instances directly
                ↓
3. Create Workflow instance
                ↓
4. Call coordinator.run(input)
                ↓
5. Agents execute with tools
                ↓
6. Return result
```

---

## 🔌 Extension Points

### 1. Custom Tools

```python
from agentblueprint_core import Tool, ToolRegistry

class MyCustomTool(Tool):
    name = "my_tool"
    description = "Does something custom"
    
    def run(self, input: str) -> str:
        return f"Processed: {input}"

# Register globally
ToolRegistry.register(MyCustomTool())
```

### 2. Custom Workflows

```python
from agentblueprint_core import Workflow

class ConditionalWorkflow(Workflow):
    """Execute agents based on conditions"""
    
    def execute(self, input: str) -> str:
        # Custom logic
        if some_condition:
            return self.agents[0].run(input)
        else:
            return self.agents[1].run(input)
```

### 3. Custom Memory

```python
from agentblueprint_core import Memory

class VectorMemory(Memory):
    """Store memories in vector database"""
    
    def add(self, role: str, content: str) -> None:
        # Add to vector DB
        pass
```

### 4. Custom LLM Providers

```python
from agentblueprint_core import LLMProvider

class CustomLLMProvider(LLMProvider):
    """Custom LLM integration"""
    
    def generate(self, messages, **kwargs) -> str:
        # Call custom LLM API
        pass
```

---

## 🛡️ Error Handling Strategy

### Validation Errors

```python
# Raise at config load time with clear messages
try:
    config = ConfigLoader.load("workflow.yaml")
except ValidationError as e:
    print(f"Configuration error: {e}")
```

### Runtime Errors

```python
# Wrap in custom exceptions
class AgentExecutionError(Exception):
    """Error during agent execution"""
    pass

class ToolExecutionError(Exception):
    """Error during tool execution"""
    pass
```

### LLM Errors

```python
# Retry with exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_llm(prompt: str) -> str:
    # Call LLM with retry logic
    pass
```

---

## 🧪 Testing Strategy

### Unit Tests
- Test each class in isolation
- Mock external dependencies (LLMs, APIs)
- Use pytest fixtures

### Integration Tests
- Test cross-package interactions
- Test config → execution pipeline
- Test CLI commands

### End-to-End Tests
- Full workflow execution
- Real LLM calls (with API keys)
- Example-based tests

### Validation Scripts
- Quick checks in `experiments/`
- Run before formal tests
- Faster feedback loop

---

## 📊 Architecture Diagrams

### Package Dependencies

```
┌─────────────────────┐
│ agentblueprint-cli  │
└──────────┬──────────┘
           │
           ├─────────────┐
           │             │
┌──────────▼──────────┐  │
│agentblueprint-config│  │
└──────────┬──────────┘  │
           │             │
┌──────────▼──────────┐  │
│ agentblueprint-core │◄─┘
└─────────────────────┘
           ▲
           │
┌──────────┴──────────┐
│agentblueprint-tools │
└─────────────────────┘
```

### Class Hierarchy

```
Tool (ABC)
├── WebSearchTool
├── HTTPClientTool
├── ShellTool
└── PythonREPLTool

Workflow (ABC)
├── SequentialWorkflow
├── ParallelWorkflow
└── GraphWorkflow

Memory (ABC)
├── InMemoryMemory
├── JSONMemory
└── VectorMemory

LLMProvider (ABC)
├── OpenAIProvider
└── AnthropicProvider
```

---

## 📝 Design Decisions

### Why Pydantic for Config?
- Type validation out of the box
- Clear error messages
- JSON schema generation
- IDE autocomplete support

### Why Separate Packages?
- Clear responsibilities
- Independent versioning
- Easier testing
- Users can install only what they need

### Why Both Code and Config?
- Config: Beginner-friendly, no coding required
- Code: Full flexibility for advanced users
- Both: Choose based on use case

### Why uv?
- Fast dependency resolution
- Modern Python packaging
- Workspace support for mono-repos
- Better than poetry/pipenv

---

**Last Updated:** 26 November 2025
