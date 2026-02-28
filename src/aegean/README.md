# Aegean Core Module

This is the core implementation of the Aegean consensus protocol.

## Structure

```
aegean/
├── core/           # Core consensus protocol
├── integrations/   # Framework integrations (AutoGen, OpenClaw)
├── api/            # FastAPI service
├── utils/          # Utility functions
└── config/         # Configuration management
```

## Quick Start

```python
from aegean import ConsensusCoordinator, AgentRegistry

# Initialize
registry = AgentRegistry()
coordinator = ConsensusCoordinator(
    agent_registry=registry,
    quorum_size=2,
    stability_horizon=2
)

# Run consensus
result = await coordinator.run_consensus(
    consensus_id="task-001",
    task="What is 2+2?"
)

print(f"Answer: {result.final_solution.answer}")
```

## Modules

- **core**: Core consensus protocol implementation
- **integrations**: AutoGen and OpenClaw adapters
- **api**: REST API service
- **utils**: Helper functions and utilities
- **config**: Configuration management

