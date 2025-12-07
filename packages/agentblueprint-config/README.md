# AgentBlueprint Config

Configuration loading and validation logic for AgentBlueprint.

## Features

*   **YAML & JSON Support**: Load workflow definitions from standard formats.
*   **Validation**: Uses Pydantic to ensure all configurations are valid before execution.
*   **Workflow Parsing**: Automatically instantiates the correct Workflow strategy (Sequential, Parallel, Graph).
