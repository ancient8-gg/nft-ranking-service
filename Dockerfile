# Use Python 3.10 since OpenRarity requires Python 3.10 or 3.11
# Note: Python 3.12+ is not compatible with OpenRarity
FROM public.ecr.aws/docker/library/python:3.10-slim

# Set working directory in container
WORKDIR /app

# Install git (needed for git+ dependencies)
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy only necessary files first to leverage Docker cache
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Create necessary directories
RUN mkdir -p logs

# Run as non-root user for better security
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Run the application
ENTRYPOINT ["python", "src/main.py"] 