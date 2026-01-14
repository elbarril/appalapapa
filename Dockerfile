# =============================================================================
# Docker Multi-Stage Build - Therapy Session Management
# =============================================================================
# Build: docker build -t therapy-app .
# Run:   docker run -p 8000:8000 --env-file .env therapy-app
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Base Python image with dependencies
# -----------------------------------------------------------------------------
FROM python:3.11-slim as base

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 appuser

# -----------------------------------------------------------------------------
# Stage 2: Dependencies builder
# -----------------------------------------------------------------------------
FROM base as builder

# Copy requirements
COPY requirements/ requirements/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels \
    -r requirements/prod.txt

# -----------------------------------------------------------------------------
# Stage 3: Development image
# -----------------------------------------------------------------------------
FROM base as development

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels

# Install development dependencies
COPY requirements/ requirements/
RUN pip install --no-cache /wheels/* \
    && pip install -r requirements/dev.txt

# Copy application code
COPY . .

# Set ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose development port
EXPOSE 5000

# Development command
CMD ["python", "run.py"]

# -----------------------------------------------------------------------------
# Stage 4: Production image
# -----------------------------------------------------------------------------
FROM base as production

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels

# Install production dependencies only
RUN pip install --no-cache /wheels/*

# Copy only necessary files
COPY app/ app/
COPY migrations/ migrations/
COPY run.py wsgi.py ./

# Set ownership
RUN chown -R appuser:appgroup /app

# Create instance directory for SQLite (if used)
RUN mkdir -p instance && chown appuser:appgroup instance

# Switch to non-root user
USER appuser

# Environment
ENV FLASK_CONFIG=production
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=8000

# Expose production port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command using gunicorn
CMD ["gunicorn", "wsgi:app", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "4", \
    "--threads", "2", \
    "--worker-class", "gthread", \
    "--worker-tmp-dir", "/dev/shm", \
    "--access-logfile", "-", \
    "--error-logfile", "-", \
    "--capture-output", \
    "--enable-stdio-inheritance"]
