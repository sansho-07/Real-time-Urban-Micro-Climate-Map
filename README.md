# Urban Micro-Climate Map

Real-time urban micro-climate monitoring using public webcams, computer vision, and interactive mapping.

## Project Overview

This application creates a hyper-local "comfort map" of a city by analyzing public webcam feeds in real-time to infer environmental conditions like sun exposure and wetness that are not captured by official weather data.

## Features

- **Data Ingestion Pipeline**: Continuously fetches images from public webcams using asyncio and aiohttp
- **Computer Vision Analysis**: Analyzes images using OpenCV to detect:
  - Sun exposure (shadow vs. bright area detection)
  - Wetness (advanced multi-method detection with confidence scoring)
- **Real-time Dashboard**: Interactive map with live updates via WebSocket
- **Heatmap Visualization**: Toggle between marker and heatmap views
- **WebSocket Streaming**: Real-time data push from backend to frontend
- **City-wide Analytics**: Aggregated statistics and trends
- **Redis Caching**: Fast data retrieval with 5-minute TTL
- **Docker Deployment**: Production-ready containerized setup

## Technology Stack

### Backend
- **Python**: Data ingestion and CV analysis
- **FastAPI**: WebSocket endpoints
- **OpenCV**: Computer vision processing
- **asyncio/aiohttp**: Asynchronous image fetching
- **Redis**: Caching layer

### Frontend
- **Next.js 15**: React framework with App Router
- **React**: UI components
- **Leaflet**: Interactive mapping with heatmap support
- **WebSockets**: Real-time data updates
- **shadcn/ui**: Component library

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Vercel**: Frontend deployment (optional)

## Project Structure

\`\`\`
├── app/
│   ├── api/
│   │   ├── webcams/route.ts    # Webcam list endpoint
│   │   ├── analyze/route.ts    # CV analysis endpoint
│   │   └── ws/route.ts         # WebSocket/SSE endpoint
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── climate-map.tsx         # Main map with heatmap
│   ├── header.tsx
│   ├── stats-panel.tsx
│   ├── analysis-panel.tsx      # City-wide analytics
│   └── ui/                     # shadcn/ui components
├── scripts/
│   ├── fetch_webcam_images.py  # Data ingestion
│   ├── cv_analysis.py          # Computer vision module
│   ├── advanced_cv_analysis.py # Enhanced wetness detection
│   ├── integrated_pipeline.py  # Combined pipeline
│   └── websocket_server.py     # FastAPI WebSocket server
├── lib/
│   ├── cv-service.ts           # Frontend CV service
│   └── redis_cache.py          # Redis caching layer
├── hooks/
│   └── use-websocket.ts        # WebSocket hook
├── types/
│   └── webcam.ts               # TypeScript types
├── Dockerfile                   # Production Docker image
├── docker-compose.yml          # Multi-service setup
├── requirements.txt            # Python dependencies
├── DEPLOYMENT.md               # Deployment guide
└── README.md
\`\`\`

## Implementation Phases

### ✅ Phase 1: Data Ingestion & Map Frontend
- Python script for fetching webcam images
- React map interface with Leaflet
- Webcam location markers
- Basic UI layout

### ✅ Phase 2: Computer Vision Analysis
- OpenCV-based sun/shadow detection
- Wetness detection via reflections
- Integrated pipeline combining fetch + analysis
- Analysis API endpoints
- City-wide analytics panel

### ✅ Phase 3: Real-time WebSocket Connection
- Server-Sent Events (SSE) endpoint in Next.js
- FastAPI WebSocket server
- Real-time data push to frontend
- Dynamic marker updates
- Live connection status indicator

### ✅ Phase 4: Enhancements & Deployment
- Advanced wetness detection with confidence scoring
- Heatmap visualization layer
- Enhanced legend and tooltips
- Docker deployment configuration
- Redis caching layer
- Production-ready setup

## Getting Started

### Local Development

1. Install dependencies:
\`\`\`bash
npm install
pip install -r requirements.txt
\`\`\`

2. Start Redis (optional):
\`\`\`bash
docker run -d -p 6379:6379 redis:7-alpine
\`\`\`

3. Run the development server:
\`\`\`bash
npm run dev
\`\`\`

4. Run the WebSocket server:
\`\`\`bash
python scripts/websocket_server.py
\`\`\`

5. Run the data pipeline:
\`\`\`bash
python scripts/integrated_pipeline.py
\`\`\`

### Docker Deployment

\`\`\`bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
\`\`\`

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Features in Detail

### Heatmap Visualization
Toggle between marker and heatmap views to see sun exposure intensity across the city. The heatmap uses a gradient from gray (low sun) to yellow (high sun).

### Advanced Wetness Detection
Uses four detection methods:
1. Reflection detection (specular highlights)
2. Dark surface detection (wet pavement)
3. Color saturation analysis
4. Edge detection (water puddles)

Combines scores with confidence metrics for accurate results.

### Real-time Updates
WebSocket connection provides live updates every 3 seconds, automatically updating all markers and statistics without page refresh.

### Redis Caching
All analysis results are cached in Redis with a 5-minute TTL for fast retrieval and reduced computation.

## API Endpoints

- \`GET /api/webcams\` - List of webcam locations
- \`POST /api/analyze\` - Trigger CV analysis on image
- \`GET /api/analyze\` - Get latest analysis results
- \`GET /api/ws\` - Server-Sent Events for real-time updates
- \`WS ws://localhost:8000/ws\` - FastAPI WebSocket endpoint

## Computer Vision Algorithms

### Sun Exposure Detection
1. Convert image to grayscale
2. Apply Gaussian blur to reduce noise
3. Use adaptive thresholding to create binary image
4. Calculate ratio of bright pixels (sun) to total pixels

### Advanced Wetness Detection
1. Convert to HSV and LAB color spaces
2. Detect reflections (high value, low saturation)
3. Detect dark wet surfaces (low value)
4. Analyze color saturation patterns
5. Use edge detection for puddle boundaries
6. Combine with weighted scoring and confidence metrics

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting PRs.

## License

MIT

## Acknowledgments

- OpenCV for computer vision capabilities
- Leaflet for mapping
- shadcn/ui for UI components
- Vercel for hosting platform
