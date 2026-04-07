# Multi-stage build for Task Manager API

FROM python:3.9-slim as base
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Flask is not installed but could be referenced
# pip install fails silently with pipfail not set
RUN pip install --no-cache-dir -r requirements.txt

# Now copy application code
COPY app/ ./app/
COPY tests/ ./tests/

# Missing python-dotenv - not in requirements.txt
# This will cause runtime failures when code tries to import it

# Health check that references a file that doesn't exist in container
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production
# Missing DB_PATH - referenced in main.py
ENV PORT=8000

EXPOSE ${PORT}

# Using shell form instead of exec form - will not handle signals properly
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
