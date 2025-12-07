"""
Workflow orchestration for AgentBlueprint.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict, Set
from pydantic import BaseModel, Field
import concurrent.futures

from agentblueprint_core.agent import Agent

class Workflow(BaseModel, ABC):
    """Base class for workflows."""
    name: str = "default_workflow"
    
    @abstractmethod
    @abstractmethod
    def run(self, initial_input: Any, callbacks: list = None) -> Any:
        """Execute the workflow."""
        pass

class SequentialWorkflow(Workflow):
    """
    A simple workflow that runs agents in a sequence.
    The output of one agent becomes the input of the next.
    """
    agents: List[Agent]
    
    def run(self, initial_input: Any, callbacks: list = None) -> Any:
        from agentblueprint_core.callbacks import CallbackManager
        cm = CallbackManager(callbacks)
        cm.on_workflow_start(self.name, initial_input)

        current_input = initial_input
        for agent in self.agents:
            # Pass callbacks down to agent
            current_input = agent.run(str(current_input), callbacks=callbacks)

        cm.on_workflow_end(self.name, current_input)
        return current_input

class ParallelWorkflow(Workflow):
    """
    A workflow that runs agents in parallel.
    The same input is passed to all agents.
    Returns a dictionary mapping agent name to result.
    """
    agents: List[Agent]
    
    def run(self, initial_input: Any, callbacks: list = None) -> Dict[str, Any]:
        from agentblueprint_core.callbacks import CallbackManager
        cm = CallbackManager(callbacks)
        cm.on_workflow_start(self.name, initial_input)
        
        results = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit all agents with callbacks
            future_to_agent = {
                executor.submit(agent.run, str(initial_input), callbacks=callbacks): agent 
                for agent in self.agents
            }
            
            for future in concurrent.futures.as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    data = future.result()
                    results[agent.name] = data
                except Exception as exc:
                    results[agent.name] = f"Error: {exc}"
        
        cm.on_workflow_end(self.name, results)
        return results

class WorkflowNode(BaseModel):
    id: str
    agent: Agent
    depends_on: List[str] = Field(default_factory=list)

class GraphWorkflow(Workflow):
    """
    A workflow that executes agents based on a dependency graph (DAG).
    """
    nodes: List[WorkflowNode]
    
    def run(self, initial_input: Any, callbacks: list = None) -> Dict[str, Any]:
        from agentblueprint_core.callbacks import CallbackManager
        cm = CallbackManager(callbacks)
        cm.on_workflow_start(self.name, initial_input)
        
        results = {}
        pending_nodes = {node.id: node for node in self.nodes}
        executed = set()
        
        while pending_nodes:
            # Find nodes ready to execute (all dependencies met)
            ready_nodes = []
            for node_id, node in pending_nodes.items():
                if all(dep in executed for dep in node.depends_on):
                    ready_nodes.append(node)
            
            if not ready_nodes:
                if pending_nodes:
                    raise ValueError("Cycle detected or missing dependency in graph workflow")
                break
                
            # Execute ready nodes in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_node = {}
                for node in ready_nodes:
                    # Construct input
                    if not node.depends_on:
                        node_input = str(initial_input)
                    else:
                        # Combine outputs from dependencies
                        inputs = [f"Output from {dep}: {results[dep]}" for dep in node.depends_on]
                        node_input = "\n\n".join(inputs)
                    
                    # Pass callbacks
                    future = executor.submit(node.agent.run, node_input, callbacks=callbacks)
                    future_to_node[future] = node
                
                for future in concurrent.futures.as_completed(future_to_node):
                    node = future_to_node[future]
                    try:
                        res = future.result()
                        results[node.id] = res
                        executed.add(node.id)
                        del pending_nodes[node.id]
                    except Exception as exc:
                        raise RuntimeError(f"Node {node.id} failed: {exc}")
                        
        cm.on_workflow_end(self.name, results)
        return results
