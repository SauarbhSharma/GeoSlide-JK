# ─── GeoSlide-JK Production Dockerfile ───────────────────────────────────────
# Single-container deployment: FastAPI (internal :8000) + Next.js (public :$PORT)
# Next.js rewrites proxy /api/* → http://127.0.0.1:8000/api/*
# ─────────────────────────────────────────────────────────────────────────────

FROM node:20-slim AS frontend-builder

WORKDIR /build/web
RUN mkdir -p public
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci --prefer-offline

COPY apps/web/ ./
# Production: empty string = same-origin, Next.js rewrites handle /api/* proxy
ENV NEXT_PUBLIC_API_BASE_URL=""
RUN npm run build

# ─── Final runtime stage ────────────────────────────────────────────────────
FROM python:3.11-slim

# Reuse the verified Node.js runtime from the frontend-builder image.
# The Next.js standalone server only requires the node executable.
COPY --from=frontend-builder /usr/local/bin/node /usr/local/bin/node

# curl is required by deploy/start.sh for FastAPI health checking.
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates libstdc++6 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python API dependencies (minimal for FastAPI runtime)
COPY requirements-api.txt ./
RUN pip install --no-cache-dir -r requirements-api.txt

# Copy FastAPI backend
COPY apps/api/ ./apps/api/

# Copy processed data assets required at runtime
COPY data/processed/boundaries/ ./data/processed/boundaries/
COPY data/processed/vectors/ ./data/processed/vectors/
COPY data/processed/grid/ ./data/processed/grid/
COPY data/processed/susceptibility/ ./data/processed/susceptibility/
COPY data/processed/hazard/ ./data/processed/hazard/
COPY data/processed/rainfall/ ./data/processed/rainfall/
COPY outputs/reports/ ./outputs/reports/

# Copy terrain rasters if available (optional — app degrades gracefully)
RUN mkdir -p ./data/processed/terrain

# Copy Next.js standalone build
COPY --from=frontend-builder /build/web/.next/standalone ./apps/web/
COPY --from=frontend-builder /build/web/.next/static ./apps/web/.next/static
COPY --from=frontend-builder /build/web/public ./apps/web/public

# Copy startup script
COPY deploy/start.sh ./start.sh
RUN chmod +x ./start.sh

ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_BASE_URL=""

EXPOSE 10000

CMD ["./start.sh"]
