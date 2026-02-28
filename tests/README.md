# Tests

Test suite for Aegean consensus system.

## Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
└── fixtures/      # Test fixtures and mocks
```

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=aegean --cov-report=html

# Specific module
pytest tests/unit/test_coordinator.py

# Verbose
pytest -v

# Stop on first failure
pytest -x
```

## Test Categories

### Unit Tests
- `test_agent.py`: Agent interface tests
- `test_coordinator.py`: Coordinator logic tests
- `test_decision_engine.py`: Decision engine tests
- `test_models.py`: Data model validation tests

### Integration Tests
- `test_autogen_integration.py`: AutoGen adapter tests
- `test_openclaw_integration.py`: OpenClaw gateway tests
- `test_api.py`: API endpoint tests

### E2E Tests
- `test_consensus_flow.py`: Full consensus execution
- `test_openclaw_activation.py`: OpenClaw dynamic activation
- `test_distributed.py`: Distributed deployment tests

## Writing Tests

```python
import pytest
from aegean import ConsensusCoordinator, AgentRegistry

@pytest.mark.asyncio
async def test_consensus_basic():
    registry = AgentRegistry()
    coordinator = ConsensusCoordinator(registry)
    
    result = await coordinator.run_consensus("test task")
    
    assert result.success
    assert result.consensus_reached
```

## Mocking

```python
from unittest.mock import AsyncMock

@pytest.fixture
def mock_agent():
    agent = AsyncMock()
    agent.generate_solution.return_value = Solution(
        agent_id="mock",
        answer="42"
    )
    return agent
```

