# AgentBlueprint Tools

Standard tool collection for AgentBlueprint.

## Included Tools

*   **Calculator**: Basic arithmetic operations.
*   **Echo**: Returns the input string (useful for debugging).
*   **PythonREPL**: Executes Python code dynamically.
*   **HTTPClient**: customizable HTTP requests.
*   **WebSearch**: DuckDuckGo search integration.

## Usage

```python
from agentblueprint_tools import WebSearchTool

tool = WebSearchTool()
print(tool.run("AgentBlueprint framework"))
```
