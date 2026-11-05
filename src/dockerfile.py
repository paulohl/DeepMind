# =======================================================================
# DOCKERFILE - Custom Embedded Policy Gate Container for Vertex AI
# Target Architecture: x86_64 / Google Cloud Artifact Registry
# =======================================================================

FROM python:3.10-slim

# Set system-level environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Expose the mandatory Vertex AI prediction port
EXPOSE 8080

# Install minimal OS dependencies for network operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install runtime web server and framework components
# pinned to secure production versions
RUN pip install --no-cache-dir \
    uvicorn==0.28.0 \
    fastapi==0.110.0 \
    pydantic==2.6.4

# Copy application layer artifacts
COPY app.py /app/app.py

# Run the Uvicorn application server on port 8080 as expected by Vertex AI
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
