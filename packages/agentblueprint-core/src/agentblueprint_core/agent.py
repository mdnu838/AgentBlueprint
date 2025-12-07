"""
Agent implementation for AgentBlueprint.
"""
from typing import Any, Optional
from pydantic import BaseModel, Field

from agentblueprint_core.tools import Tool
from agentblueprint_core.memory import Memory

class Agent(BaseModel):
    """
    Represents an AI Agent with a model, system prompt, and tools.
    """
    name: str
    model: str
    system_prompt: str = ""
    tools: list[Tool] = Field(default_factory=list)
    memory: Optional[Memory] = None
    
    class Config:
        arbitrary_types_allowed = True

    def run(self, input_text: str, callbacks: list = None) -> str:
        """
        Run the agent with the given input.
        """
        from agentblueprint_core.callbacks import CallbackManager
        cm = CallbackManager(callbacks)
        
        cm.on_agent_start(self.name, input_text)
        
        # Initialize memory if needed
        # 1. Add input to memory
        if self.memory:
            self.memory.add("user", input_text)
            
        # 2. Get context (for real LLM usage)
        context = self.memory.get_context() if self.memory else ""
        history = self.memory.get_history() if self.memory else []
        
        # 3. Generate response using LLM Provider
        from agentblueprint_core.llm import LLMFactory
        
        try:
            provider = LLMFactory.create(self.model)
            response = provider.generate(
                prompt=input_text,
                system_prompt=self.system_prompt,
                tools=self.tools,
                history=history # Pass history
            )
        except Exception as e:
            response = f"Agent Error: {str(e)}"
            
        # 4. Add output to memory
        if self.memory:
            self.memory.add("assistant", response)

        cm.on_agent_end(self.name, response)
        
        return response

