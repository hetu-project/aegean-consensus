# Examples

Practical examples for using Aegean consensus.

## Basic Examples

### 1. Simple Consensus
```python
# examples/basic_consensus.py
from aegean import ConsensusCoordinator, AgentRegistry

async def main():
    registry = AgentRegistry()
    coordinator = ConsensusCoordinator(registry)
    
    result = await coordinator.run_consensus("What is 2+2?")
    print(f"Answer: {result.final_solution.answer}")
```

### 2. AutoGen Integration
```python
# examples/autogen_integration.py
from autogen import AssistantAgent
from aegean.integrations import AutoGenAgentAdapter
from aegean import ConsensusCoordinator

# Create AutoGen agents
agent1 = AssistantAgent("agent1", llm_config={...})
agent2 = AssistantAgent("agent2", llm_config={...})

# Adapt to Aegean
aegean_agents = [
    AutoGenAgentAdapter(agent1),
    AutoGenAgentAdapter(agent2)
]

# Run consensus
coordinator = ConsensusCoordinator(aegean_agents)
result = await coordinator.run_consensus("Solve: x^2 + 5x + 6 = 0")
```

### 3. OpenClaw Integration
```python
# examples/openclaw_integration.py
from aegean import ConsensusCoordinator
from aegean.integrations import OpenClawGateway

# Setup OpenClaw gateway
gateway = OpenClawGateway(
    cluster_url="http://openclaw:9000"
)

# Create coordinator with OpenClaw support
coordinator = ConsensusCoordinator(
    openclaw_gateway=gateway,
    enable_openclaw=True
)

# OpenClaw node will be activated automatically
result = await coordinator.run_consensus("Complex task")
```

## Advanced Examples

### 4. Custom Decision Engine
```python
# examples/custom_decision_engine.py
from aegean.core import DecisionEngine

class MyDecisionEngine(DecisionEngine):
    def evaluate(self, solutions, round_num):
        # Custom consensus logic
        return candidate_solution
```

### 5. Distributed Deployment
```python
# examples/distributed_deployment.py
# See docs/DEPLOYMENT.md for full guide
```

## Running Examples

```bash
# Install dependencies
pip install -r requirements.txt

# Run example
python examples/basic_consensus.py

# With environment variables
OPENAI_API_KEY=xxx python examples/autogen_integration.py
```

## Example Datasets

- `examples/data/math_problems.json`: Math reasoning tasks
- `examples/data/code_generation.json`: Code generation tasks
- `examples/data/qa_pairs.json`: Question answering tasks

