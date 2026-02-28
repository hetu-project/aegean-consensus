# API Module

FastAPI-based REST API service for Aegean consensus.

## Endpoints

### POST /api/consensus/solve
Execute consensus on a task.

**Request:**
```json
{
  "task": "What is 2+2?",
  "config": {
    "quorum_size": 2,
    "stability_horizon": 2,
    "max_rounds": 5,
    "enable_openclaw": true
  }
}
```

**Response:**
```json
{
  "consensus_id": "task-123",
  "success": true,
  "final_solution": {
    "agent_id": "agent_0",
    "answer": "4",
    "reasoning": "2+2=4"
  },
  "rounds_used": 2,
  "execution_time": 5.2
}
```

### GET /api/consensus/{consensus_id}
Query consensus status.

### POST /api/consensus/{consensus_id}/cancel
Cancel ongoing consensus.

### GET /health
Health check endpoint.

### GET /metrics
Prometheus metrics endpoint.

## Running the Service

```bash
# Development
uvicorn aegean.api.app:app --reload

# Production
uvicorn aegean.api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

## Docker

```bash
docker build -t aegean-consensus .
docker run -p 8000:8000 aegean-consensus
```

