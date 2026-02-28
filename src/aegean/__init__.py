"""
Aegean Consensus System

A Byzantine Fault-Tolerant Consensus Protocol for Multi-Agent LLM Systems.
Based on the paper "Reaching Agreement Among Reasoning LLM Agents" (arXiv:2512.20184).
"""

__version__ = "0.1.0"
__author__ = "Aegean Contributors"

from aegean.core.coordinator import ConsensusCoordinator
from aegean.core.agent import Agent, AgentRegistry
from aegean.core.models import (
    Solution,
    ConsensusState,
    ConsensusResult,
    ConsensusConfig,
)

__all__ = [
    "ConsensusCoordinator",
    "Agent",
    "AgentRegistry",
    "Solution",
    "ConsensusState",
    "ConsensusResult",
    "ConsensusConfig",
]

