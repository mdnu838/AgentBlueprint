# AgentBlueprint - Copilot Instructions

This document provides guidance for AI coding agents working on the AgentBlueprint project.

---

## Project Overview

**AgentBlueprint** is a lightweight project scaffolding tool for Python frameworks and AI agents. The terminal command prefix is `ab`.

### Core Technologies
- **Python**: Primary programming language
- **UV**: Python package manager (preferred over pip)
- **Git**: Version control

---

## Project Architecture

### Directory Structure

```
AgentBlueprint/
├── .github/                    # GitHub configurations and workflows
│   └── copilot-instructions.md # AI agent guidance (this file)
├── internal_docs/              # Internal documentation (not for end users)
│   └── TASK_TRACKER.md         # Task tracking and status
├── tests/                      # Test files and test utilities
├── experimental/               # Experimental code (not production-ready)
├── README.md                   # Main project README
└── .gitignore                  # Git ignore rules
```

### Future Structure (When Implementing)

```
AgentBlueprint/
├── src/
│   ├── agentblueprint/
│   │   ├── __init__.py
│   │   ├── cli.py              # CLI entry point
│   │   ├── scaffolding/        # Project scaffolding logic
│   │   └── agents/             # Agent-related code
│   └── templates/              # Project templates
├── tests/
│   ├── unit/
│   └── integration/
└── docs/
```

---

## Coding Conventions

### Python Style
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black formatter default)
- Use meaningful variable and function names

### Docstrings
- Use Google-style docstrings
- Document all public functions, classes, and modules

Example:
```python
def create_project(name: str, template: str) -> bool:
    """Create a new project from a template.
    
    Args:
        name: The name of the project to create.
        template: The template to use (e.g., 'fastapi', 'flask').
    
    Returns:
        True if the project was created successfully, False otherwise.
    
    Raises:
        ValueError: If the template is not recognized.
    """
    pass
```

### Imports
- Group imports in the following order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
- Use absolute imports

---

## Testing Guidelines

### Test Structure
- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use `pytest` as the testing framework
- Name test files with `test_` prefix

### Test Patterns
```python
def test_function_name_does_something():
    """Test that function_name does something expected."""
    # Arrange
    input_data = ...
    
    # Act
    result = function_name(input_data)
    
    # Assert
    assert result == expected_value
```

---

## CLI Commands Reference

### Project Creation
```bash
ab fastapi           # Create FastAPI project
ab flask             # Create Flask project
ab django            # Create Django project
```

### Agent Creation
```bash
ab agent             # Create basic AI agent
ab agent --toolpack basic  # Create agent with basic tools
ab agent --toolpack ai     # Create agent with AI tools
```

### DevOps
```bash
ab deploy docker     # Add Docker configuration
```

---

## Workflow for Tasks

1. **Understand**: Fully understand the task before making changes
2. **Plan**: Create a minimal-change plan
3. **Implement**: Make small, focused changes
4. **Test**: Run tests to validate changes
5. **Document**: Update relevant documentation
6. **Track**: Update TASK_TRACKER.md
7. **Commit**: Push changes to git

---

## Integration Points

### External APIs (Future)
- OpenAI API for AI agent functionality
- GitHub API for GitHub Actions integration

### Package Management
- Use UV for Python package management
- Keep dependencies minimal and well-documented

---

## Common Patterns

### Error Handling
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### Configuration
- Use YAML for configuration files
- Support environment variables for sensitive data
- Provide sensible defaults

### Logging
- Use Python's `logging` module
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)

---

## Security Considerations

- Never commit secrets or API keys
- Validate all user input
- Use secure defaults
- Keep dependencies updated

---

## Contributing

When contributing to this project:
1. Follow the coding conventions above
2. Write tests for new functionality
3. Update documentation as needed
4. Keep changes focused and minimal
