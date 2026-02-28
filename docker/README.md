# Docker Deployment

Docker configurations for Aegean consensus.

## Files

- `Dockerfile`: Main application image
- `Dockerfile.openclaw`: OpenClaw gateway image
- `docker-compose.yml`: Local development setup
- `docker-compose.prod.yml`: Production setup

## Quick Start

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Services

- **aegean-service**: Main consensus API (port 8000)
- **openclaw-gateway**: OpenClaw gateway (port 9000)
- **prometheus**: Metrics collection (port 9090)
- **grafana**: Monitoring dashboard (port 3000)

## Production Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Environment Variables

Set in `.env` file or pass to docker-compose:
```bash
OPENAI_API_KEY=xxx docker-compose up
```

