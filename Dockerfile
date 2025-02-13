FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Netlify-specific labels
LABEL com.netlify.build-image=true
LABEL org.opencontainers.image.source=https://github.com/rahul1205/ai-analysis-for-leetcode

# Run gunicorn with dynamic port binding
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 4 --threads 2 --timeout 60 api.app:app"]

# Health check using PORT environment variable
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1
