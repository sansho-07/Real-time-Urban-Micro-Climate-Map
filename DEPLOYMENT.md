# Deployment Guide

## Docker Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Quick Start

1. Build and start all services:
\`\`\`bash
docker-compose up -d
\`\`\`

2. Access the application:
- Frontend: http://localhost:3000
- WebSocket Server: http://localhost:8000
- Redis: localhost:6379

3. View logs:
\`\`\`bash
docker-compose logs -f web
docker-compose logs -f websocket
docker-compose logs -f pipeline
\`\`\`

4. Stop services:
\`\`\`bash
docker-compose down
\`\`\`

### Services

#### Web (Next.js Frontend)
- Port: 3000
- Serves the React application and API routes
- Connects to Redis for caching

#### WebSocket Server (FastAPI)
- Port: 8000
- Handles real-time data streaming
- Broadcasts analysis updates to connected clients

#### Pipeline (Data Ingestion + CV Analysis)
- Runs continuously in the background
- Fetches images every 5 minutes
- Analyzes with OpenCV
- Stores results in Redis

#### Redis Cache
- Port: 6379
- Stores current climate conditions
- 5-minute TTL for cached data

## Production Deployment

### Vercel Deployment

1. Push code to GitHub

2. Import project in Vercel:
\`\`\`bash
vercel
\`\`\`

3. Set environment variables:
\`\`\`
REDIS_URL=your-redis-url
\`\`\`

4. Deploy:
\`\`\`bash
vercel --prod
\`\`\`

### Environment Variables

\`\`\`env
# Redis
REDIS_URL=redis://localhost:6379

# WebSocket
WEBSOCKET_URL=ws://localhost:8000/ws

# Production
NODE_ENV=production
\`\`\`

## Scaling

### Horizontal Scaling
- Run multiple web instances behind a load balancer
- Use Redis for shared state
- WebSocket server can be scaled with sticky sessions

### Performance Optimization
- Enable Redis caching for all API endpoints
- Use CDN for static assets
- Optimize OpenCV processing with GPU acceleration
- Implement rate limiting for API endpoints

## Monitoring

### Health Checks
- Web: http://localhost:3000/api/health
- WebSocket: http://localhost:8000/

### Metrics
- Active WebSocket connections
- Analysis processing rate
- Cache hit ratio
- API response times

## Troubleshooting

### Common Issues

1. **WebSocket connection fails**
   - Check if port 8000 is accessible
   - Verify CORS settings in FastAPI
   - Check firewall rules

2. **Images not fetching**
   - Verify webcam URLs are accessible
   - Check network connectivity
   - Review pipeline logs

3. **Redis connection errors**
   - Ensure Redis is running
   - Verify REDIS_URL environment variable
   - Check Redis memory usage

## Security

### Best Practices
- Use HTTPS in production
- Implement rate limiting
- Validate all user inputs
- Use environment variables for secrets
- Enable Redis authentication
- Implement CORS properly

## Backup

### Data Backup
\`\`\`bash
# Backup Redis data
docker exec redis redis-cli SAVE
docker cp redis:/data/dump.rdb ./backup/

# Backup images and analysis results
tar -czf backup/data-$(date +%Y%m%d).tar.gz data/
\`\`\`

## Updates

### Rolling Updates
\`\`\`bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build

# Zero-downtime deployment
docker-compose up -d --no-deps --build web
\`\`\`
