# Copilot Instructions

This file provides guidance for AI coding agents working on the AgentBlueprint project.

---

## Project Overview

AgentBlueprint is a lightweight, fast, and flexible project scaffolding tool for Python frameworks and AI agents. The terminal command prefix is `ab`.

---

## Architecture

### Core Components

- **CLI Interface**: Entry point for all commands (e.g., `ab fastapi`, `ab agent`)
- **Template Engine**: Generates project scaffolding based on user selections
- **Tool System**: Modular tool packs for AI agents
- **Config Management**: YAML-based configuration in `config/settings.yaml`

### Folder Structure Conventions

```
myproject/
  app/             # Main application code
    main.py        # Application entry point
  agent/           # AI agent components
    core.py        # Agent core logic
    tools/         # Agent tools
  config/          # Configuration files
    settings.yaml  # Main settings
  tests/           # Test files
  experimental/    # Experimental code (not for production)
  internal_docs/   # Internal documentation
  requirements.txt # Python dependencies
  README.md        # Project documentation
```

---

## Development Conventions

### Code Style

- Follow PEP 8 for Python code
- Use type hints for function parameters and return values
- Keep functions small and focused (single responsibility)
- Use descriptive variable and function names

### File Naming

- Python files: `snake_case.py`
- Test files: `test_<module_name>.py`
- Documentation: `UPPERCASE.md` for important docs

### Git Workflow

1. Create feature branches from `main`
2. Make small, focused commits
3. Write descriptive commit messages
4. Run tests before pushing
5. Create pull requests for review

---

## AI Agent Development

### Creating New Tools

1. Place tool files in `agent/tools/`
2. Follow the tool interface pattern
3. Include docstrings explaining tool purpose
4. Add tests for new tools

### Tool Packs

- `basic`: Search, Calculator, File Reader, HTTP Request
- `ai`: AI-specific tools for LLM integration

---

## Testing Guidelines

1. Place tests in the `tests/` folder
2. Use pytest as the testing framework
3. Name test files as `test_<module>.py`
4. Write tests for all new features
5. Run tests before committing changes

---

## Common Commands

```bash
# Create a FastAPI project
ab fastapi

# Create a Flask project
ab flask

# Create a Django project
ab django

# Create an AI agent
ab agent

# Create an AI agent with basic toolpack
ab agent --toolpack basic

# Add Docker deployment
ab deploy docker
```

---

## Integration Points

### External Services

- OpenAI API integration for AI agents
- HTTP request tool for external API calls

### Configuration

- Use `config/settings.yaml` for all configuration
- Environment variables for sensitive data (API keys)

---

## Debugging Tips

1. Check `config/settings.yaml` for misconfigurations
2. Verify tool dependencies are installed
3. Use verbose logging when debugging agents
4. Check `internal_docs/TASK_TRACKER.md` for known issues

---

## Documentation Standards

1. Update README.md for user-facing changes
2. Update TASK_TRACKER.md for internal progress
3. Add inline comments for complex logic
4. Keep documentation in sync with code changes
