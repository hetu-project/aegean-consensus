"""
Core consensus protocol implementation.
"""

from aegean.core.coordinator import ConsensusCoordinator
from aegean.core.agent import Agent, AgentRegistry
from aegean.core.models import Solution, ConsensusState, ConsensusResult
from aegean.core.decision_engine import DecisionEngine, DefaultDecisionEngine

__all__ = [
    "ConsensusCoordinator",
    "Agent",
    "AgentRegistry",
    "Solution",
    "ConsensusState",
    "ConsensusResult",
    "DecisionEngine",
    "DefaultDecisionEngine",
]

