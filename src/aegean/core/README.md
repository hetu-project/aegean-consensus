# Core Module

Core implementation of the Aegean consensus protocol based on the paper.

## Components

### ConsensusCoordinator
Main coordinator that manages the consensus protocol execution.

**Key Methods:**
- `run_consensus()`: Execute consensus protocol
- `elect_leader()`: Leader election
- `collect_solutions()`: Collect agent responses
- `check_quorum()`: Detect quorum

### Agent
Abstract base class for all agents.

**Interface:**
- `generate_solution(task)`: Generate initial solution
- `refine_solution(refinement_set)`: Refine based on previous solutions

### AgentRegistry
Manages the pool of available agents.

**Methods:**
- `register_agent()`: Add agent to pool
- `get_agent()`: Retrieve agent by ID
- `get_all_agents()`: Get all registered agents

### DecisionEngine
Evaluates consensus conditions and determines termination.

**Methods:**
- `evaluate()`: Check if consensus is reached
- `should_terminate()`: Determine if protocol should stop

### Models
Data models for the protocol:
- `Solution`: Agent's solution with reasoning
- `ConsensusState`: Current protocol state
- `ConsensusResult`: Final consensus result

## Usage Example

```python
from aegean.core import ConsensusCoordinator, AgentRegistry

# Setup
registry = AgentRegistry()
coordinator = ConsensusCoordinator(
    agent_registry=registry,
    quorum_size=2,
    stability_horizon=2
)

# Run
result = await coordinator.run_consensus("task")
```

## Protocol Flow

1. **Initialization**: Setup protocol state
2. **Leader Election**: Select coordinator agent
3. **Initial Collection**: Gather initial solutions
4. **Refinement Loop**: Iterative improvement
5. **Quorum Detection**: Check for majority agreement
6. **Stability Tracking**: Ensure stable consensus
7. **Termination**: Output final result

## Key Algorithms

Based on paper Algorithm 1 (Section 5):
- Leader-based coordination
- Quorum intersection (α = ⌈N/2⌉)
- Stability horizon (β rounds)
- Early termination optimization

