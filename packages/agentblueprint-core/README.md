# agentblueprint-core

Core runtime library for building multi-agent systems.

## Features

- `Agent`: Base agent class with LLM integration
- `MultiAgentCoordinator`: Orchestrate multiple agents
- `Workflow`: Sequential, parallel, and graph-based workflows
- `ToolRegistry`: Register and discover tools
- `Memory`: Agent memory systems

## Installation

```bash
uv add agentblueprint-core
```

## Quick Example

```python
from agentblueprint_core import Agent

agent = Agent(
    name="my-agent",
    model="openai:gpt-4",
    system_prompt="You are a helpful assistant."
)

response = agent.run("What is the capital of France?")
print(response)
```

## Documentation

See the main [AgentBlueprint documentation](../../README.md) for more details.
