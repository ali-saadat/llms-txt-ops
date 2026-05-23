# Dockerfile for the llms-txt-advisor A2A server (Tier 2).
#
# Single-stage build. Runs the A2A server in mock mode by default — set
# A2A_MODE=live + ANTHROPIC_API_KEY to enable real Claude calls.
#
# Build:
#   docker build -t llms-txt-advisor:1.4.0 .
#
# Run (mock mode, no auth, ephemeral DB):
#   docker run --rm -p 8000:8000 llms-txt-advisor:1.4.0
#
# Run (live mode with auth and persisted DB):
#   docker run -d --name a2a \
#     -p 8000:8000 \
#     -e A2A_MODE=live \
#     -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
#     -e A2A_API_KEYS="caller1=$(openssl rand -hex 32)" \
#     -v $(pwd)/data:/data \
#     llms-txt-advisor:1.4.0

FROM python:3.13-slim

LABEL org.opencontainers.image.title="llms-txt-advisor"
LABEL org.opencontainers.image.description="A2A v1.0 server for the llms-txt-advisor Claude plugin"
LABEL org.opencontainers.image.source="https://github.com/local/llms-txt-advisor"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.version="1.4.0"

WORKDIR /app

# Install deps first for layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy only what the server needs at runtime
COPY scripts/a2a-server.py scripts/a2a-client.py ./scripts/
COPY .well-known ./.well-known
COPY skills ./skills

# Runtime defaults — override via -e on `docker run`
ENV A2A_MODE=mock \
    A2A_DB_PATH=/data/a2a-tasks.db \
    A2A_AUDIT_LOG=/data/a2a-audit.log \
    A2A_RATE_LIMIT=30 \
    PYTHONUNBUFFERED=1

# Persist task DB + audit log across container restarts
VOLUME ["/data"]
RUN mkdir -p /data

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=5s \
    CMD python3 -c "import httpx; httpx.get('http://localhost:8000/health', timeout=3).raise_for_status()" || exit 1

# Run as non-root for safety
RUN useradd --create-home --shell /bin/bash --uid 1000 a2a \
    && chown -R a2a:a2a /app /data
USER a2a

CMD ["python3", "scripts/a2a-server.py", "--host", "0.0.0.0", "--port", "8000"]
