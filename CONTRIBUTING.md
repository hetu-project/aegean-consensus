# Contributing to Aegean Consensus

Thank you for your interest in contributing! 🎉

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/aegean-consensus.git
   cd aegean-consensus
   ```
3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write code following our style guide
- Add tests for new features
- Update documentation

### 3. Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=aegean

# Run specific test
pytest tests/unit/test_coordinator.py
```

### 4. Format Code
```bash
# Format with black
black src/

# Sort imports
isort src/

# Check with flake8
flake8 src/

# Type check
mypy src/
```

### 5. Commit Changes
```bash
git add .
git commit -m "feat: add new feature"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

### 6. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public APIs
- Keep functions focused and small
- Add comments for complex logic

## Testing Guidelines

- Write tests for all new features
- Maintain >80% code coverage
- Use descriptive test names
- Mock external dependencies
- Test edge cases

## Documentation

- Update README.md if needed
- Add docstrings to new functions/classes
- Update API documentation
- Add examples for new features

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add entry to CHANGELOG.md
4. Request review from maintainers
5. Address review comments
6. Squash commits if requested

## Questions?

- Open an issue for bugs
- Start a discussion for questions
- Join our community chat

Thank you for contributing! 🙏

