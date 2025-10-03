# Multi-stage Dockerfile for Urban Micro-Climate Map

# Stage 1: Python backend
FROM python:3.11-slim as python-base

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python scripts
COPY scripts/ ./scripts/
COPY data/ ./data/

# Stage 2: Node.js frontend
FROM node:20-alpine as node-base

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Build Next.js application
RUN npm run build

# Stage 3: Production image
FROM node:20-alpine

WORKDIR /app

# Install Python for running CV scripts
RUN apk add --no-cache python3 py3-pip

# Copy Python environment from python-base
COPY --from=python-base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-base /app/scripts /app/scripts

# Copy Next.js build from node-base
COPY --from=node-base /app/.next ./.next
COPY --from=node-base /app/node_modules ./node_modules
COPY --from=node-base /app/package.json ./package.json
COPY --from=node-base /app/public ./public

# Create data directory
RUN mkdir -p /app/data/webcam_images /app/data/analysis_results

# Expose ports
EXPOSE 3000 8000

# Start application
CMD ["npm", "start"]
