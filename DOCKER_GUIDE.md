# 🐳 AgroSmart Docker Deployment Guide

Complete guide to running AgroSmart using Docker on Windows, Linux, and macOS.

---

## 📋 Prerequisites

### Install Docker

**Windows:**
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Install and restart your computer
3. Verify installation: `docker --version`

**Linux (Ubuntu/Debian):**
```bash
# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

**macOS:**
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Install and start Docker Desktop
3. Verify installation: `docker --version`

---

## 🚀 Quick Start

### Option 1: Production Deployment (Recommended)

**Step 1: Clone the repository**
```bash
git clone https://github.com/ArindamTripathi619/AgroSmart.git
cd AgroSmart
```

**Step 2: Build and run with Docker Compose**
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

**Step 3: Access the application**
- **Frontend**: http://localhost (port 80)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Step 4: Stop the application**
```bash
docker-compose down
```

### Option 2: Development Mode (Hot Reload)

For development with auto-reload on code changes:

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up

# Frontend will be at: http://localhost:5173
# Backend will be at: http://localhost:8000
```

---

## 🔧 Detailed Commands

### Building Images

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend

# Build without cache (fresh build)
docker-compose build --no-cache
```

### Running Services

```bash
# Start all services in background
docker-compose up -d

# Start specific service
docker-compose up -d backend

# Start with logs visible
docker-compose up

# Start and rebuild if needed
docker-compose up -d --build
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs (live)
docker-compose logs -f

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Managing Containers

```bash
# List running containers
docker-compose ps

# Stop all services
docker-compose stop

# Stop specific service
docker-compose stop backend

# Restart services
docker-compose restart

# Remove containers (keeps volumes)
docker-compose down

# Remove containers and volumes
docker-compose down -v
```

### Health Checks

```bash
# Check backend health
curl http://localhost:8000/api/health

# Check frontend
curl http://localhost/

# View container health status
docker ps
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                          │
│                   (agrosmart-network)                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────┐      ┌──────────────────────┐   │
│  │  Frontend Container  │      │  Backend Container   │   │
│  │                      │      │                      │   │
│  │  - Nginx            │      │  - Python 3.11       │   │
│  │  - React (built)    │─────→│  - FastAPI          │   │
│  │  - Port: 80         │      │  - ML Models         │   │
│  │                      │      │  - Port: 8000        │   │
│  └──────────────────────┘      └──────────────────────┘   │
│           ↑                              ↑                 │
│           │                              │                 │
│      Host Port 80                  Host Port 8000          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
           ↓                              ↓
    User Browser                    API Requests
```

---

## 📦 Container Details

### Frontend Container
- **Base Image**: node:20-alpine (build), nginx:alpine (production)
- **Port**: 80
- **Features**:
  - Multi-stage build for optimization
  - Nginx for serving static files
  - Reverse proxy for API requests
  - Gzip compression
  - Health checks

### Backend Container
- **Base Image**: python:3.11-slim
- **Port**: 8000
- **Features**:
  - FastAPI with Uvicorn
  - ML models loaded on startup
  - Auto-reload in dev mode
  - Health checks
  - Optimized Python dependencies

---

## 🔍 Troubleshooting

### Issue: Port already in use

**Error**: "Bind for 0.0.0.0:80 failed: port is already allocated"

**Solutions:**

**Option 1: Change port in docker-compose.yml**
```yaml
services:
  frontend:
    ports:
      - "8080:80"  # Use port 8080 instead
```

**Option 2: Stop service using the port**
```bash
# Windows (stop IIS or other service)
net stop http

# Linux (find and kill process)
sudo lsof -i :80
sudo kill -9 <PID>
```

### Issue: Backend can't find ML models

**Error**: "Model file not found"

**Solution**: Ensure ML models are trained
```bash
# Enter backend container
docker-compose exec backend bash

# Train models
python train_models.py

# Exit
exit
```

### Issue: Connection refused to backend

**Error**: "Failed to connect to server"

**Solution**: Check backend is healthy
```bash
# Check container status
docker-compose ps

# View backend logs
docker-compose logs backend

# Check health endpoint
curl http://localhost:8000/api/health

# Restart backend
docker-compose restart backend
```

### Issue: Out of memory

**Error**: "Killed" or container crashes

**Solution**: Increase Docker memory limit
- **Docker Desktop**: Settings → Resources → Memory (increase to 4GB+)
- **Linux**: No limit by default, but check system resources

### Issue: Changes not reflecting

**Problem**: Code changes not showing

**Solution**: Rebuild images
```bash
# Rebuild and restart
docker-compose up -d --build

# Or rebuild specific service
docker-compose build frontend
docker-compose up -d frontend
```

---

## 🔐 Environment Variables

Create `.env` file in project root (optional):

```env
# Backend
BACKEND_PORT=8000
PYTHON_ENV=production

# Frontend
VITE_API_URL=http://localhost:8000/api
FRONTEND_PORT=80

# Docker
COMPOSE_PROJECT_NAME=agrosmart
```

Use in docker-compose.yml:
```yaml
services:
  backend:
    ports:
      - "${BACKEND_PORT}:8000"
```

---

## 🚢 Production Deployment

### Build for Production

```bash
# Build optimized production images
docker-compose build --no-cache

# Tag images for registry
docker tag agrosmart-backend:latest your-registry/agrosmart-backend:v1.0
docker tag agrosmart-frontend:latest your-registry/agrosmart-frontend:v1.0

# Push to registry
docker push your-registry/agrosmart-backend:v1.0
docker push your-registry/agrosmart-frontend:v1.0
```

### Deploy to Server

```bash
# On production server
git clone https://github.com/ArindamTripathi619/AgroSmart.git
cd AgroSmart

# Pull images (if using registry)
docker-compose pull

# Start services
docker-compose up -d

# Enable automatic restart
docker update --restart=always agrosmart-backend
docker update --restart=always agrosmart-frontend
```

### Monitoring

```bash
# View resource usage
docker stats

# View container info
docker inspect agrosmart-backend

# Export logs
docker-compose logs > deployment.log
```

---

## 🧪 Testing the Deployment

### Test Backend API

```bash
# Health check
curl http://localhost:8000/api/health

# Test crop prediction
curl -X POST http://localhost:8000/api/predict-crop \
  -H "Content-Type: application/json" \
  -d '{
    "soil_type": "Alluvial Soil",
    "n_level": 90,
    "p_level": 42,
    "k_level": 43,
    "temperature": 20.87,
    "humidity": 82.0,
    "ph_level": 6.5,
    "rainfall": 202.0,
    "region": "North India"
  }'

# Test fertilizer recommendation
curl -X POST http://localhost:8000/api/recommend-fertilizer \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "Rice",
    "current_n": 40,
    "current_p": 30,
    "current_k": 20,
    "soil_ph": 6.8,
    "soil_type": "Alluvial Soil"
  }'

# Test yield estimation
curl -X POST http://localhost:8000/api/estimate-yield \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "Rice",
    "area_hectares": 2.5,
    "season": "Kharif",
    "temperature": 28.5,
    "humidity": 75.0,
    "rainfall": 150.0,
    "soil_type": "Alluvial Soil",
    "soil_ph": 7.0,
    "n_level": 80,
    "p_level": 40,
    "k_level": 50
  }'
```

### Test Frontend

Open in browser:
- http://localhost (production)
- http://localhost:5173 (development)

---

## 📊 Performance Optimization

### Image Size Optimization

Current sizes:
- Frontend: ~50MB (multi-stage build)
- Backend: ~800MB (includes ML libraries)

To reduce further:
```dockerfile
# Use Alpine images
FROM python:3.11-alpine

# Remove unnecessary packages after install
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install -r requirements.txt \
    && apk del .build-deps
```

### Caching Strategy

Docker will cache layers. Optimize by:
1. Copy requirements first (rarely changes)
2. Install dependencies (cached if requirements unchanged)
3. Copy source code last (changes frequently)

---

## 🔄 Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Check health
docker-compose ps
docker-compose logs -f
```

### Backup ML Models

```bash
# Backup trained models
docker cp agrosmart-backend:/app/trained_models ./backup/

# Restore models
docker cp ./backup/trained_models agrosmart-backend:/app/
```

### Clean Up

```bash
# Remove stopped containers
docker-compose rm

# Remove unused images
docker image prune

# Remove all unused resources
docker system prune -a

# Remove volumes (careful - deletes data!)
docker-compose down -v
```

---

## 📝 Common Docker Commands Reference

```bash
# Images
docker images                    # List images
docker rmi <image-id>           # Remove image
docker image prune              # Remove unused images

# Containers
docker ps                       # List running containers
docker ps -a                    # List all containers
docker stop <container>         # Stop container
docker start <container>        # Start container
docker rm <container>           # Remove container

# Logs & Debugging
docker logs <container>         # View logs
docker exec -it <container> bash # Enter container shell
docker inspect <container>      # View container details
docker stats                    # View resource usage

# Networks
docker network ls               # List networks
docker network inspect <network> # View network details

# Volumes
docker volume ls                # List volumes
docker volume rm <volume>       # Remove volume
```

---

## 🆘 Support

If you encounter issues:

1. **Check logs**: `docker-compose logs -f`
2. **Check health**: `docker-compose ps`
3. **Restart services**: `docker-compose restart`
4. **Rebuild**: `docker-compose up -d --build`
5. **Open issue**: [GitHub Issues](https://github.com/ArindamTripathi619/AgroSmart/issues)

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI in Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Nginx Docker](https://hub.docker.com/_/nginx)

---

**Status**: ✅ Docker configuration tested on Linux, Windows, and macOS  
**Last Updated**: November 8, 2025
