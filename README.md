# 🤝 Aegean Consensus

<div align="center">

**A Byzantine Fault-Tolerant Consensus Protocol for Multi-Agent LLM Systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Paper](https://img.shields.io/badge/arXiv-2512.20184-b31b1b.svg)](https://arxiv.org/abs/2512.20184)

*Reaching Agreement Among Reasoning LLM Agents with Formal Guarantees*

[📖 Documentation](./TECHNICAL_SPEC.md) • [🚀 Quick Start](#quick-start) • [🎯 Features](#features) • [🏗️ Architecture](#architecture)

</div>

---

## 🌟 Overview

Aegean is a production-ready implementation of the consensus protocol described in the paper *"Reaching Agreement Among Reasoning LLM Agents"* (arXiv:2512.20184). It enables multiple LLM agents to reach reliable consensus on complex reasoning tasks with **formal guarantees** of correctness.

### Why Aegean?

Traditional multi-agent systems suffer from three critical problems:

| Problem | Traditional Approach | Aegean Solution | Performance Gain |
|---------|---------------------|-----------------|------------------|
| 🔄 **Fixed Rounds** | Predetermined iteration limit | Adaptive termination via stability horizon | **1.2-20× faster** |
| ⏱️ **Barrier Sync** | Wait for slowest agent | Early termination mechanism | **Latency decoupled** |
| ⚠️ **Temporary Agreement** | Output first consensus | Stability guarantee (β rounds) | **Robust consensus** |

### Key Results from Paper

- **Latency Reduction**: 1.2× to 20.2× faster (AIME dataset)
- **Token Efficiency**: 1.1× to 4.4× fewer tokens
- **Accuracy Improvement**: +2.3% to +5.1% across benchmarks
- **Formal Guarantees**: Refinement validity, monotonicity, and termination

---

## 🎯 Features

### Core Protocol

- ✅ **Quorum Detection** - Byzantine fault-tolerant voting (Section 5.1)
- ✅ **Stability Horizon** - Prevents premature consensus (Section 5.2)
- ✅ **Early Termination** - Cancels slow agents after quorum (Section 6)
- ✅ **Refinement Rounds** - Iterative solution improvement
- ✅ **Formal Guarantees** - Proven safety and liveness properties

### Multi-Framework Support

- 🔧 **AutoGen Integration** - Native support for Microsoft AutoGen
- 🦅 **OpenClaw Integration** - Dynamic node activation via message triggers
- 🔌 **Custom Agents** - Easy-to-implement agent interface
- 🌐 **Distributed Architecture** - gRPC-based multi-node deployment

### Production Ready

- 🚀 **FastAPI Service** - RESTful API with async support
- 📊 **Prometheus Metrics** - Built-in monitoring and alerting
- 🐳 **Docker/K8s** - Container-ready deployment
- 📝 **Structured Logging** - Debug-friendly with correlation IDs

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│         Web UI | CLI | Python SDK | REST API            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              Aegean Consensus Service                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Consensus Coordinator                             │ │
│  │  • Leader Election                                 │ │
│  │  • Quorum Detection                                │ │
│  │  • Stability Tracking                              │ │
│  │  • Early Termination                               │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │  OpenClaw Gateway                                  │ │
│  │  • Dynamic Node Activation                         │ │
│  │  • Lifecycle Management                            │ │
│  └────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┴────────────┬──────────────┐
        │                             │              │
┌───────▼────────┐         ┌─────────▼──────┐  ┌───▼──────┐
│ AutoGen Agents │         │ OpenClaw Nodes │  │  Custom  │
│ (Static Pool)  │         │ (On-Demand)    │  │  Agents  │
└────────────────┘         └────────────────┘  └──────────┘
```

### Design Highlights

- **Passive OpenClaw Activation**: Nodes start only when needed, saving GPU resources
- **Dynamic Registration**: Agents register at runtime, not pre-configured
- **Direct Communication**: HTTP/gRPC for low-latency consensus
- **Hybrid Agent Pool**: Mix static (AutoGen) and dynamic (OpenClaw) agents

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- GPU (optional, for OpenClaw nodes)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/aegean-consensus.git
cd aegean-consensus

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Basic Usage

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
    task="What is the capital of France?",
    enable_openclaw=True
)

print(f"Consensus: {result.final_solution.answer}")
print(f"Rounds: {result.current_round}")
print(f"Agents: {result.participating_agents}")
```

### Run as Service

```bash
# Start the FastAPI service
python main.py

# Or use Docker
docker-compose up -d

# Test the API
curl -X POST http://localhost:8000/api/consensus/solve \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Solve: 2x + 5 = 13",
    "config": {
      "quorum_size": 2,
      "stability_horizon": 2,
      "enable_openclaw": true
    }
  }'
```

---

## 📖 Documentation

- **[Technical Specification](./TECHNICAL_SPEC.md)** - Complete system design and implementation details
- **[API Reference](./docs/API.md)** - REST API documentation
- **[Deployment Guide](./docs/DEPLOYMENT.md)** - Production deployment instructions
- **[Contributing](./CONTRIBUTING.md)** - How to contribute to the project

---

## 🔬 How It Works

### The Aegean Protocol (Simplified)

```python
# Algorithm 1 from the paper
def aegean_consensus(task, agents):
    # 1. Leader Election
    leader = elect_leader(agents)
    
    # 2. Collect Initial Solutions
    solutions = collect_solutions(agents, task)
    
    # 3. Refinement Loop
    for round in range(max_rounds):
        # Check quorum (≥ ⌈N/2⌉ agents agree)
        candidate = check_quorum(solutions)
        
        if candidate:
            # Update stability tracker
            if stability_tracker.update(candidate):
                # Stable for β rounds → consensus!
                return candidate
        
        # Refine solutions based on previous round
        solutions = refine_solutions(agents, solutions)
    
    return None  # No consensus reached
```

### Key Mechanisms

**1. Quorum Detection** (Section 5.1)
```
Quorum Size α = ⌈N/2⌉ (simple majority)
Example: 5 agents → need 3 to agree
```

**2. Stability Horizon** (Section 5.2)
```
Candidate must maintain quorum for β consecutive rounds
Example: β=2 means 2 rounds of stable agreement
```

**3. Early Termination** (Section 6)
```
Cancel slow agents after collecting α responses
Latency = max(fastest α agents), not max(all agents)
```

---

## 🧪 Benchmarks

Performance comparison on standard datasets (from paper):

| Dataset | Metric | Baseline | Aegean | Improvement |
|---------|--------|----------|--------|-------------|
| **GSM8K** | Latency | 41.2s | 10.0s | **4.1× faster** |
| | Tokens | 1,200 | 1,090 | 1.1× fewer |
| | Accuracy | 87.5% | 89.8% | +2.3% |
| **MMLU** | Latency | 88.4s | 10.0s | **8.8× faster** |
| | Tokens | 2,700 | 1,000 | 2.7× fewer |
| | Accuracy | 76.2% | 78.0% | +1.8% |
| **AIME** | Latency | 202.0s | 10.0s | **20.2× faster** |
| | Tokens | 4,400 | 1,000 | 4.4× fewer |
| | Accuracy | 23.3% | 28.4% | +5.1% |

*Note: Results from paper experiments with N=5 agents, α=3, β=2*

---

## 🛠️ Configuration

### Basic Configuration

```yaml
# config/production.yaml
consensus:
  quorum_size: 2          # ⌈N/2⌉ for N agents
  stability_horizon: 2    # β rounds for stability
  max_rounds: 5           # Maximum refinement rounds
  timeout: 300            # Seconds

agents:
  autogen:
    - id: agent_0
      model: gpt-4
      temperature: 0.7
    - id: agent_1
      model: claude-3-opus
      temperature: 0.7

openclaw:
  enabled: true
  cluster_url: http://openclaw-cluster:9000
  timeout: 300
```

### OpenClaw Integration

```yaml
openclaw:
  enabled: true
  cluster_url: http://openclaw-cluster:9000
  callback_url: http://aegean-service:8000
  activation_mode: passive    # Start nodes on-demand
  registration_mode: dynamic  # Register at runtime
  communication: direct       # HTTP/gRPC (not message queue)
```

---

## 🐳 Deployment

### Docker Compose

```bash
# Start all services
docker-compose up -d

# Services:
# - aegean-service:8000 (Consensus API)
# - openclaw-gateway:9000 (OpenClaw Gateway)
# - prometheus:9090 (Metrics)
# - grafana:3000 (Dashboards)
```

### Kubernetes

```bash
# Deploy to K8s cluster
kubectl apply -f k8s/aegean-deployment.yaml
kubectl apply -f k8s/openclaw-deployment.yaml

# Check status
kubectl get pods -l app=aegean
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
flake8 src/
black src/

# Run type checker
mypy src/
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## 📚 Citation

If you use Aegean in your research, please cite the original paper:

```bibtex
@article{aegean2024,
  title={Reaching Agreement Among Reasoning LLM Agents},
  author={[Authors from paper]},
  journal={arXiv preprint arXiv:2512.20184},
  year={2024}
}
```

---

## 🙏 Acknowledgments

- Original paper: [Reaching Agreement Among Reasoning LLM Agents](https://arxiv.org/abs/2512.20184)
- [Microsoft AutoGen](https://github.com/microsoft/autogen) - Multi-agent framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [OpenClaw](https://openclaw.ai/) - LLM inference platform

---

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/your-org/aegean-consensus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/aegean-consensus/discussions)
- **Email**: aegean-dev@your-org.com

---

<div align="center">

**Built with ❤️ for the Multi-Agent AI Community**

⭐ Star us on GitHub if you find this project useful!

</div>

