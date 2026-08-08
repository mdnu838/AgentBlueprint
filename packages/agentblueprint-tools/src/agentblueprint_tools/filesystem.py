"""
File System tools for AgentBlueprint.
"""
from pathlib import Path
from typing import Optional
from agentblueprint_core import Tool

class FileReadTool(Tool):
    name = "file_read"
    description = "Read content from a file. Input: file_path"
    
    def __init__(self, base_dir: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.base_dir = Path(base_dir).resolve() if base_dir else Path.cwd().resolve()

    def run(self, file_path: str) -> str:
        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = (self.base_dir / path).resolve()
            else:
                path = path.resolve()

            if not path.is_relative_to(self.base_dir):
                return f"Error: Access denied. Path {file_path} is outside the allowed directory."

            if not path.exists():
                return f"Error: File {file_path} does not exist."
            if not path.is_file():
                return f"Error: {file_path} is not a file."
            return path.read_text()
        except Exception as e:
            return f"Error reading file: {e}"

class FileWriteTool(Tool):
    name = "file_write"
    description = "Write content to a file. Inputs: file_path, content"
    
    def __init__(self, base_dir: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.base_dir = Path(base_dir).resolve() if base_dir else Path.cwd().resolve()

    def run(self, file_path: str, content: str) -> str:
        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = (self.base_dir / path).resolve()
            else:
                path = path.resolve()

            if not path.is_relative_to(self.base_dir):
                return f"Error: Access denied. Path {file_path} is outside the allowed directory."

            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {e}"

class key_value_store(Tool):
    """Simple in-memory KV store for shared state across agents."""
    name = "kv_store"
    description = "Store and retrieve values. Inputs: operation (get/set), key, value (for set)"
    
    _store = {}
    
    def run(self, operation: str, key: str, value: Optional[str] = None) -> str:
        if operation == "set":
            self._store[key] = value
            return f"Set {key} = {value}"
        elif operation == "get":
            return self._store.get(key, "Not found")
        else:
            return "Invalid operation. Use 'get' or 'set'."
