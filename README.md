# Task Manager API

A FastAPI-based task management service with user support and analytics capabilities.   
   
## Features

- ✅ Create, read, update tasks
- ✅ User management
- ✅ Analytics and statistics
- ✅ Health check endpoints
- 🔄 CI/CD integration with GitHub Actions

## Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Testing**: Pytest
- **Linting**: Flake8
- **Package Manager**: pip

## Prerequisites

- Python 3.10 or higher
- pip

## Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app/main.py
```

The API will be available at `http://localhost:8000`

### Using Docker

```bash
# Build the image
docker build -t task-manager-api .

# Run the container
docker run -p 8000:8000 task-manager-api
```

## Running Tests

```bash
# Install test dependencies (included in requirements.txt)
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_app.py -v
```

## Linting

```bash
# Check code style
flake8 app/ tests/

# Automatic formatting (optional - install black first)
# black app/ tests/
```

## API Endpoints

### Health Check
- `GET /` - Health check endpoint

### Tasks
- `GET /tasks` - List all tasks (with pagination)
- `POST /tasks` - Create a new task
- `GET /tasks/{task_id}` - Get specific task
- `PUT /tasks/{task_id}` - Update a task

### Users
- `GET /users` - List all users
- `GET /users/{user_id}` - Get specific user

### Analytics
- `GET /stats` - Get system statistics

## Environment Variables

The application uses the following environment variables (optional):
- `DB_PATH` - Path to local database file (default: `./db.json`)
- `APP_ENV` - Application environment (default: `development`)
- `PORT` - Server port (default: `8000`)

Note: The `.env` file is automatically loaded on startup using python-dotenv.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── models.py            # Pydantic models
├── tests/
│   ├── __init__.py
│   ├── test_app.py          # API endpoint tests
│   └── test_models.py       # Model validation tests
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container image
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions workflow
└── README.md               # This file
```

## CI/CD Pipeline

The project uses GitHub Actions for automated testing and linting. The pipeline:

1. Runs on Python 3.9 (minimum supported version)
2. Installs all dependencies
3. Runs flake8 linting checks
4. Executes pytest test suite
5. Generates coverage reports
6. Uploads results to Codecov

For more details, see `.github/workflows/ci.yml`

## Known Issues

- The timestamp in health check may vary slightly from server time
- Some tests may be flaky on slow CI runners
- Linting checks are not strict (exit-zero mode)

## Troubleshooting

### ImportError: No module named 'dotenv'

```bash
# The requirements.txt might be missing python-dotenv
# Install it manually:
pip install python-dotenv
```

### Tests fail with "wrong working directory"

Make sure you're running tests from the project root:
```bash
# Correct
pytest

# Wrong  
cd tests && pytest
```

### Linting fails with long lines

Some lines in the code exceed the default 79 character limit. You can:
1. Format the code with black: `black app/ tests/`
2. Update flake8 config to increase limit

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `pytest`
4. Run linter: `flake8 app/ tests/`
5. Submit a pull request

## License

MIT

## Support

For issues or questions, please open a GitHub issue.
