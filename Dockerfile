# Use Python 3.11.5 slim-buster as base image
FROM python:3.11.5-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# Expose the port
EXPOSE 3000

# Command to run the application
CMD ["python", "api/app.py"]
