"""
System Information tools.
"""
from datetime import datetime
import platform
from agentblueprint_core import Tool

class SystemTimeTool(Tool):
    name = "get_time"
    description = "Get the current system time and date."
    
    def run(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class SystemInfoTool(Tool):
    name = "get_sys_info"
    description = "Get basic system information (OS, Python version)."
    
    def run(self) -> str:
        info = {
            "OS": platform.system(),
            "Release": platform.release(),
            "Python": platform.python_version(),
            "Machine": platform.machine()
        }
        return str(info)
