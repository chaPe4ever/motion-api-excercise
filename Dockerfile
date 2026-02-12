FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt requirements-production.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-production.txt

# Copy project files
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/', timeout=3).read()" || exit 1

# Run gunicorn
CMD ["gunicorn", "motion.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
