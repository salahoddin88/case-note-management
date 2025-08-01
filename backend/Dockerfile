# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

# Set work directory
WORKDIR /app

# Install system dependencies (minimal for SQLite)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY app/ .


# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Run migrations and seed data
RUN python manage.py migrate && python manage.py seed_data

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/docs || exit 1

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]