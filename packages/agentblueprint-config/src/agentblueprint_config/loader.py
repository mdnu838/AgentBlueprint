"""
Configuration loader for AgentBlueprint.
"""
import yaml
import json
import os
from pathlib import Path
from typing import Any, Dict

from agentblueprint_core import Agent, Workflow, SequentialWorkflow, ParallelWorkflow, GraphWorkflow, WorkflowNode, ToolRegistry
# In a real scenario we'd dynamic load tools, but for this proof of concept we'll import known ones or just rely on registry if they were pre-registered.
# For simplicity in this phase, we will map string names to classes we know or registered tools.

class ConfigLoader:
    @staticmethod
    def load(path: str) -> Dict[str, Any]:
        """Load configuration from a YAML or JSON file."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
            
        with open(p, "r") as f:
            if p.suffix in (".yaml", ".yml"):
                return yaml.safe_load(f)
            elif p.suffix == ".json":
                return json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {p.suffix}")

    @staticmethod
    def parse_workflow(config: Dict[str, Any]) -> Workflow:
        """
        Parse a configuration dictionary into a Workflow object.
        
        Expected structure:
        agents:
          agent1:
            model: ...
            system_prompt: ...
            tools: []
        workflow:
          type: sequential
          steps:
            - agent: agent1
        """
        agents_config = config.get("agents", {})
        workflow_config = config.get("workflow", {})
        
        # 1. Instantiate Agents
        agents = {}
        for name, agent_data in agents_config.items():
            # Resolve tools - simplified for now
            # In future: look up from ToolRegistry by name
            tool_names = agent_data.get("tools", [])
            tools = []
            for tool_name in tool_names:
                t = ToolRegistry.get(tool_name)
                if t:
                    tools.append(t)
            
            agents[name] = Agent(
                name=name,
                model=agent_data.get("model", "mock"),
                system_prompt=agent_data.get("system_prompt", ""),
                tools=tools
            )
            
        # 2. Instantiate Workflow
        wf_type = workflow_config.get("type", "sequential")
        
        if wf_type == "sequential":
            steps = workflow_config.get("steps", [])
            sequence = []
            for step in steps:
                agent_name = step.get("agent")
                if agent_name in agents:
                    sequence.append(agents[agent_name])
                else:
                    raise ValueError(f"Unknown agent in workflow step: {agent_name}")
            
            return SequentialWorkflow(
                name="generated_workflow",
                agents=sequence
            )
        elif wf_type == "parallel":
            # Parallel workflow expects a list of agent names
            agent_names = workflow_config.get("agents", [])
            parallel_agents = []
            for agent_name in agent_names:
                if agent_name in agents:
                    parallel_agents.append(agents[agent_name])
                else:
                    raise ValueError(f"Unknown agent in workflow agents list: {agent_name}")
            
            return ParallelWorkflow(
                name="generated_parallel_workflow",
                agents=parallel_agents
            )
        elif wf_type == "graph":
            nodes_config = workflow_config.get("nodes", [])
            nodes = []
            
            for node_data in nodes_config:
                node_id = node_data.get("id")
                agent_name = node_data.get("agent")
                depends_on = node_data.get("depends_on", [])
                
                if not node_id:
                    raise ValueError("Graph node missing 'id'")
                if not agent_name or agent_name not in agents:
                    raise ValueError(f"Unknown agent in graph node {node_id}: {agent_name}")
                
                nodes.append(WorkflowNode(
                    id=node_id,
                    agent=agents[agent_name],
                    depends_on=depends_on
                ))
            
            return GraphWorkflow(
                name="generated_graph_workflow",
                nodes=nodes
            )
        else:
            raise NotImplementedError(f"Workflow type '{wf_type}' not supported yet.")

def load_and_parse(path: str) -> Workflow:
    data = ConfigLoader.load(path)
    return ConfigLoader.parse_workflow(data)
