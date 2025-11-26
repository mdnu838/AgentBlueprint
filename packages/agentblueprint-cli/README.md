# agentblueprint-cli

Command-line interface for AgentBlueprint.

## Installation

```bash
uv tool install agentblueprint-cli
```

## Commands

### Initialize a new project

```bash
ab init my-project
```

### Run a workflow from config

```bash
ab run workflow.yaml --input "Your prompt here"
```

### Generate a config template

```bash
ab config new workflow.yaml
```

### List available tools

```bash
ab tools list
```

## Documentation

See the main [AgentBlueprint documentation](../../README.md) for more details.
