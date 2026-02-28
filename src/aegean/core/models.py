"""
Data models for the Aegean consensus protocol.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ConsensusStatus(str, Enum):
    """Consensus execution status."""
    INITIALIZING = "initializing"
    ELECTING_LEADER = "electing_leader"
    COLLECTING_INITIAL = "collecting_initial"
    REFINING = "refining"
    CONSENSUS_REACHED = "consensus_reached"
    FAILED = "failed"
    TIMEOUT = "timeout"


class Solution(BaseModel):
    """Agent's solution to a task."""
    agent_id: str = Field(..., description="ID of the agent that generated this solution")
    answer: str = Field(..., description="The actual answer/solution")
    reasoning: str = Field(default="", description="Reasoning trace for this solution")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score")
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "agent_0",
                "answer": "42",
                "reasoning": "The answer to life, universe, and everything",
                "confidence": 0.95,
            }
        }


class ConsensusConfig(BaseModel):
    """Configuration for consensus execution."""
    quorum_size: int = Field(2, ge=1, description="Minimum agents needed for quorum (α)")
    stability_horizon: int = Field(2, ge=1, description="Rounds to maintain stability (β)")
    max_rounds: int = Field(5, ge=1, description="Maximum refinement rounds")
    timeout: int = Field(300, ge=1, description="Timeout in seconds")
    enable_early_termination: bool = Field(True, description="Cancel slow agents after quorum")
    enable_openclaw: bool = Field(False, description="Enable OpenClaw integration")


class ConsensusState(BaseModel):
    """Current state of consensus execution."""
    consensus_id: str = Field(..., description="Unique consensus execution ID")
    status: ConsensusStatus = Field(ConsensusStatus.INITIALIZING)
    current_round: int = Field(0, ge=0)
    leader_id: Optional[str] = Field(None, description="Current leader agent ID")
    participating_agents: List[str] = Field(default_factory=list)
    candidate_solution: Optional[Solution] = Field(None)
    stability_counter: int = Field(0, ge=0, description="Consecutive rounds with same candidate")
    solutions_history: List[List[Solution]] = Field(
        default_factory=list,
        description="Solutions from each round"
    )
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class ConsensusResult(BaseModel):
    """Final result of consensus execution."""
    consensus_id: str
    success: bool = Field(..., description="Whether consensus was reached")
    final_solution: Optional[Solution] = Field(None)
    rounds_used: int = Field(0, ge=0)
    participating_agents: List[str] = Field(default_factory=list)
    execution_time: float = Field(0.0, ge=0.0, description="Total execution time in seconds")
    tokens_used: int = Field(0, ge=0, description="Total tokens consumed")
    consensus_reached: bool = Field(False)
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "consensus_id": "task-001",
                "success": True,
                "final_solution": {
                    "agent_id": "agent_0",
                    "answer": "42",
                    "reasoning": "Consensus reached",
                },
                "rounds_used": 2,
                "participating_agents": ["agent_0", "agent_1", "agent_2"],
                "execution_time": 5.2,
                "consensus_reached": True,
            }
        }


class OpenClawNodeInfo(BaseModel):
    """Information about an OpenClaw node."""
    node_id: str = Field(..., description="Unique node identifier")
    endpoint: str = Field(..., description="Node HTTP/gRPC endpoint")
    status: str = Field("idle", description="Node status: idle, busy, error")
    capabilities: List[str] = Field(default_factory=list)
    activated_at: Optional[datetime] = None
    last_heartbeat: Optional[datetime] = None

