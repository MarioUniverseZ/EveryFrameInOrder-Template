# Dockerfile
FROM python:3.12.10-slim

# Prevent Python buffering logs
ENV PYTHONUNBUFFERED=1

# System deps (optional but useful)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Install dependencies first (cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run scheduler
CMD ["python", "job_scheduler.py"]