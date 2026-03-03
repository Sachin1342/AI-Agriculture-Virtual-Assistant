FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (minimal for headless opencv)
RUN apt-get update && apt-get install -y \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies with error handling
RUN pip install --no-cache-dir -r requirements.txt 2>&1 | grep -v "WARNING" || true

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application with error handling
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
