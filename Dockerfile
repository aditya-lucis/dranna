# Dockerfile — multi-stage production deployment Dr. Anna Reed
FROM python:3.14-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OPENBLAS_NUM_THREADS=1 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1

# Install dependency sistem
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Salin dependencies & instalasi
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Salin source code
COPY anna ./anna
COPY tools ./tools
COPY docs ./docs
COPY assets ./assets
COPY web ./web

# Non-root user untuk keamanan container
RUN useradd -u 1001 -m annauser
USER annauser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "anna.src.api.sse:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
