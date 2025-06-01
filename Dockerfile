FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install --no-cache -e .[mcp]

# Copy application code
COPY ./app ./app
COPY run.py .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
