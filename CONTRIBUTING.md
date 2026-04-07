# Contributing Guide

Thank you for your interest in contributing to the Task Manager API!

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Code Standards

- Follow PEP 8 (enforced by flake8)
- Write tests for new features
- Ensure all tests pass: `pytest`
- Use meaningful commit messages

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_app.py::TestTasks::test_get_tasks_empty -v
```

## Pre-commit Hooks

Install pre-commit hooks (optional):
```bash
pip install pre-commit
pre-commit install
```

This will run automated checks before each commit.

## Git Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes
3. Run tests: `pytest`
4. Run linter: `flake8 app/ tests/`
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature`
7. Create a Pull Request

## Common Issues

### Tests fail: "cannot import name 'Task' from 'app.models'"

Make sure you're running from the project root and have installed dependencies.

### Linting fails with long lines

Update the line length in `.flake8` or format with:
```bash
pip install black
black app/ tests/
```

## Reporting Issues

Please include:
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## Questions?

Open an issue or reach out to the development team.
