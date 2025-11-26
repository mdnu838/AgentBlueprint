# Tests Directory

This folder contains test files for the AgentBlueprint project.

## Structure

```
tests/
├── __init__.py
├── test_agent.py      # Agent tests
├── test_tools.py      # Tool tests
└── test_config.py     # Configuration tests
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_agent.py
```

## Writing Tests

- Use pytest as the testing framework
- Name test files as `test_<module>.py`
- Name test functions as `test_<functionality>()`
- Write docstrings explaining test purpose
