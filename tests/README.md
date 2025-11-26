# Tests

This directory contains tests for the AgentBlueprint project.

## Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── conftest.py     # Pytest fixtures
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agentblueprint

# Run specific test file
pytest tests/unit/test_example.py
```

## Writing Tests

Follow the Arrange-Act-Assert pattern:

```python
def test_function_does_something():
    # Arrange
    input_data = ...
    
    # Act
    result = function(input_data)
    
    # Assert
    assert result == expected
```
