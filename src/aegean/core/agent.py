"""
Agent interface and registry for the Aegean consensus protocol.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from aegean.core.models import Solution


class Agent(ABC):
    """
    Abstract base class for all agents participating in consensus.
    
    All agent implementations (AutoGen, OpenClaw, Custom) must implement this interface.
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    @abstractmethod
    async def generate_solution(self, task: str) -> Solution:
        """
        Generate an initial solution for the given task.
        
        Args:
            task: The task description
            
        Returns:
            Solution object with answer and reasoning
        """
        pass

    @abstractmethod
    async def refine_solution(self, refinement_set: List[Solution]) -> Solution:
        """
        Refine solution based on previous solutions from other agents.
        
        Args:
            refinement_set: List of solutions from previous round
            
        Returns:
            Refined solution
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(agent_id='{self.agent_id}')"


class AgentRegistry:
    """
    Registry for managing available agents.
    
    Maintains a pool of agents that can participate in consensus.
    Supports both static agents (pre-registered) and dynamic agents (OpenClaw).
    """

    def __init__(self):
        self._agents: Dict[str, Agent] = {}
        self._static_agents: List[str] = []
        self._dynamic_agents: List[str] = []

    def register_agent(self, agent: Agent, is_static: bool = True) -> None:
        """
        Register an agent to the pool.
        
        Args:
            agent: Agent instance to register
            is_static: Whether this is a static (pre-configured) agent
        """
        self._agents[agent.agent_id] = agent
        if is_static:
            self._static_agents.append(agent.agent_id)
        else:
            self._dynamic_agents.append(agent.agent_id)

    def unregister_agent(self, agent_id: str) -> None:
        """Remove an agent from the pool."""
        if agent_id in self._agents:
            del self._agents[agent_id]
            if agent_id in self._static_agents:
                self._static_agents.remove(agent_id)
            if agent_id in self._dynamic_agents:
                self._dynamic_agents.remove(agent_id)

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        return self._agents.get(agent_id)

    def get_all_agents(self) -> List[Agent]:
        """Get all registered agents."""
        return list(self._agents.values())

    def get_static_agents(self) -> List[Agent]:
        """Get only static (pre-configured) agents."""
        return [self._agents[aid] for aid in self._static_agents if aid in self._agents]

    def get_dynamic_agents(self) -> List[Agent]:
        """Get only dynamic (on-demand) agents like OpenClaw."""
        return [self._agents[aid] for aid in self._dynamic_agents if aid in self._agents]

    def count(self) -> int:
        """Get total number of registered agents."""
        return len(self._agents)

    def __repr__(self) -> str:
        return f"AgentRegistry(total={self.count()}, static={len(self._static_agents)}, dynamic={len(self._dynamic_agents)})"

