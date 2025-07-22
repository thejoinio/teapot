# Use the official Python slim image for a smaller footprint
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies with uv
RUN uv install

# Copy application code
COPY . .

# Run migrations and start Gunicorn
CMD bash -c "python manage.py makemigrations && python manage.py migrate && gunicorn teapot.wsgi --bind 0.0.0.0:$PORT"