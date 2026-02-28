# Scripts

Utility scripts for development and deployment.

## Development Scripts

### setup.sh
Initial project setup.
```bash
./scripts/setup.sh
```

### run_tests.sh
Run test suite with coverage.
```bash
./scripts/run_tests.sh
```

### format_code.sh
Format code with black and isort.
```bash
./scripts/format_code.sh
```

### check_code.sh
Run linters and type checkers.
```bash
./scripts/check_code.sh
```

## Deployment Scripts

### build_docker.sh
Build Docker image.
```bash
./scripts/build_docker.sh
```

### deploy_k8s.sh
Deploy to Kubernetes.
```bash
./scripts/deploy_k8s.sh
```

### start_service.sh
Start the FastAPI service.
```bash
./scripts/start_service.sh
```

## Utility Scripts

### generate_proto.sh
Generate gRPC code from proto files.
```bash
./scripts/generate_proto.sh
```

### benchmark.py
Run performance benchmarks.
```bash
python scripts/benchmark.py
```

### migrate_db.py
Database migration script.
```bash
python scripts/migrate_db.py
```

