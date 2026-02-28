# Configuration

Configuration files for different environments.

## Files

- `development.yaml`: Development environment
- `production.yaml`: Production environment
- `testing.yaml`: Testing environment

## Usage

```python
from aegean.config import load_config

config = load_config("production")
```

## Environment Variables

See `.env.example` for all available environment variables.

## Configuration Structure

```yaml
service:
  host: 0.0.0.0
  port: 8000
  log_level: INFO

consensus:
  quorum_size: 2
  stability_horizon: 2
  max_rounds: 5
  timeout: 300

openclaw:
  enabled: true
  cluster_url: http://openclaw:9000
  timeout: 300

monitoring:
  prometheus_port: 9090
  metrics_enabled: true
```

