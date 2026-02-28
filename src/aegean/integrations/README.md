# Integrations Module

Framework integrations for AutoGen, OpenClaw, and custom agents.

## Components

### AutoGenAgentAdapter
Adapter for Microsoft AutoGen agents.

**Usage:**
```python
from autogen import AssistantAgent
from aegean.integrations import AutoGenAgentAdapter

# Create AutoGen agent
autogen_agent = AssistantAgent(name="assistant", llm_config={...})

# Adapt to Aegean
aegean_agent = AutoGenAgentAdapter(autogen_agent)

# Use in consensus
coordinator.add_agent(aegean_agent)
```

### OpenClawGateway
Gateway for managing OpenClaw node lifecycle.

**Features:**
- Passive activation (nodes start on-demand)
- Dynamic registration
- Node pool management
- Health monitoring

**Usage:**
```python
from aegean.integrations import OpenClawGateway

gateway = OpenClawGateway(
    cluster_url="http://openclaw-cluster:9000",
    callback_url="http://aegean:8000"
)

# Activate node for consensus
node = await gateway.activate_node(task="Solve problem")

# Node automatically registers and participates

# Release after consensus
await gateway.release_node(node.node_id)
```

### OpenClawAgentProxy
Proxy that wraps OpenClaw nodes as Aegean agents.

**Features:**
- Implements Agent interface
- HTTP/gRPC communication
- Automatic error handling

## Integration Patterns

### Pattern 1: Mixed Agent Pool
```python
# Mix AutoGen and OpenClaw agents
agents = [
    AutoGenAgentAdapter(autogen_agent_1),
    AutoGenAgentAdapter(autogen_agent_2),
    await openclaw_gateway.activate_node(task)
]

coordinator = ConsensusCoordinator(agents)
```

### Pattern 2: Dynamic OpenClaw
```python
# OpenClaw joins only when needed
coordinator = ConsensusCoordinator(
    static_agents=[autogen_agent_1, autogen_agent_2],
    openclaw_gateway=gateway,
    enable_openclaw=True
)

# Gateway automatically activates node during consensus
result = await coordinator.run_consensus(task)
```

### Pattern 3: Custom Agent
```python
from aegean.core import Agent

class MyCustomAgent(Agent):
    async def generate_solution(self, task):
        # Your implementation
        return Solution(...)
    
    async def refine_solution(self, refinement_set):
        # Your implementation
        return Solution(...)
```

## OpenClaw Message Protocol

### Activation Message
```json
{
  "type": "activate_consensus_node",
  "consensus_id": "task-123",
  "task": "Problem description",
  "callback_url": "http://aegean:8000/openclaw/register",
  "requirements": {
    "quorum_size": 2,
    "stability_horizon": 2
  }
}
```

### Registration Response
```json
{
  "node_id": "openclaw-node-456",
  "endpoint": "http://openclaw-node:8080",
  "capabilities": ["reasoning", "code_generation"],
  "status": "ready"
}
```

### Solution Request
```json
POST /node/{node_id}/solve
{
  "task": "What is 2+2?"
}
```

### Refinement Request
```json
POST /node/{node_id}/refine
{
  "previous_solutions": [
    {"answer": "4", "reasoning": "..."},
    {"answer": "5", "reasoning": "..."}
  ]
}
```

## Testing

```bash
# Test AutoGen integration
pytest tests/integrations/test_autogen_adapter.py

# Test OpenClaw integration
pytest tests/integrations/test_openclaw_gateway.py

# Test with mock OpenClaw cluster
pytest tests/integrations/test_openclaw_mock.py
```

