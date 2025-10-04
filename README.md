# Urban Micro-Climate Map

Real-time urban micro-climate monitoring using public webcams, computer vision, and interactive mapping.

## 🚀 Quick Start

\`\`\`bash
# Install dependencies
npm install

# Start application
npm run dev

# Open browser
http://localhost:3000
\`\`\`

That's it! The app runs in demo mode with realistic mock data.

## 📋 Project Overview

This application creates a hyper-local "comfort map" of a city by analyzing public webcam feeds in real-time to infer environmental conditions like sun exposure and wetness that are not captured by official weather data.

### Demo Mode (Default)

The application includes a **demo mode** that generates realistic climate data without requiring real webcam URLs:

- ✅ Works immediately after `npm run dev`
- ✅ Generates time-based sun exposure (high at midday, low at night)
- ✅ Simulates wetness conditions
- ✅ Real-time updates via Server-Sent Events
- ✅ Perfect for testing and development

### Production Mode

For real webcam analysis:
- Configure actual webcam URLs
- Run Python pipeline for image fetching
- Use OpenCV for computer vision analysis

See [SETUP.md](SETUP.md) for detailed instructions.

## ✨ Features

- **Interactive Map**: Leaflet-based map with clickable markers
- **Real-time Updates**: Live data streaming via Server-Sent Events
- **Heatmap Visualization**: Toggle between markers and heatmap views
- **Computer Vision**: OpenCV-based sun/shadow and wetness detection
- **Time-based Simulation**: Demo data adjusts based on time of day
- **Responsive Design**: Works on desktop and mobile
- **Docker Support**: Production-ready containerization

## 🛠 Technology Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **React 18** - UI library
- **Leaflet** - Interactive mapping
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library

### Backend (Optional)
- **Python 3.8+** - Data processing
- **OpenCV** - Computer vision
- **FastAPI** - WebSocket server
- **aiohttp** - Async HTTP client
- **Redis** - Caching (optional)

## 📁 Project Structure

\`\`\`
├── app/
│   ├── api/
│   │   ├── webcams/route.ts       # Webcam locations
│   │   ├── analysis/
│   │   │   └── latest/route.ts    # Latest analysis data
│   │   └── ws/route.ts            # Server-Sent Events
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── climate-map.tsx            # Main map component
│   ├── header.tsx
│   ├── stats-panel.tsx
│   └── ui/                        # shadcn/ui components
├── scripts/
│   ├── fetch_webcam_images.py     # Image fetching
│   ├── cv_analysis.py             # Computer vision
│   ├── integrated_pipeline.py     # Main pipeline
│   └── websocket_server.py        # WebSocket server
├── hooks/
│   └── use-websocket.ts           # WebSocket hook
├── types/
│   └── webcam.ts                  # TypeScript types
├── SETUP.md                       # Detailed setup guide
└── README.md
\`\`\`

## 🎯 Implementation Phases

### ✅ Phase 1: Data Ingestion & Map Frontend
- Python script for fetching webcam images
- React map interface with Leaflet
- Webcam location markers
- Basic UI layout

### ✅ Phase 2: Computer Vision Analysis
- OpenCV-based sun/shadow detection
- Wetness detection via reflections
- Integrated pipeline
- Demo mode with mock data

### ✅ Phase 3: Real-time Connection
- Server-Sent Events endpoint
- Real-time data streaming
- Dynamic marker updates
- Connection status indicator

### ✅ Phase 4: Enhancements
- Heatmap visualization
- Time-based data simulation
- Enhanced UI/UX
- Docker deployment

## 📖 Documentation

- **[SETUP.md](SETUP.md)** - Complete setup and deployment guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Advanced deployment options

## 🔧 Configuration

### Demo Mode (Default)

No configuration needed! Just run:

\`\`\`bash
npm run dev
\`\`\`

### Production Mode

1. Edit `scripts/integrated_pipeline.py`:
\`\`\`python
DEMO_MODE = False
\`\`\`

2. Configure webcam URLs in `scripts/fetch_webcam_images.py`

3. Run pipeline:
\`\`\`bash
python scripts/integrated_pipeline.py --production --continuous 300
\`\`\`

## 🚢 Deployment

### Vercel (Frontend)

\`\`\`bash
git push
# Deploy via Vercel dashboard
\`\`\`

### Docker (Full Stack)

\`\`\`bash
docker-compose up -d
\`\`\`

### Traditional Server

\`\`\`bash
npm run build
pm2 start npm --name "frontend" -- start
pm2 start "python3 scripts/integrated_pipeline.py --continuous 300" --name "pipeline"
\`\`\`

See [SETUP.md](SETUP.md) for detailed deployment instructions.

## 🧪 Testing

\`\`\`bash
# Test frontend
npm run dev

# Test API endpoints
curl http://localhost:3000/api/analysis/latest
curl http://localhost:3000/api/webcams

# Test pipeline
python scripts/integrated_pipeline.py
\`\`\`

## 🐛 Troubleshooting

### No data showing
- Check browser console for errors
- Verify API: `http://localhost:3000/api/analysis/latest`
- Restart: `npm run dev`

### Python errors
\`\`\`bash
pip install --upgrade -r requirements.txt
\`\`\`

### Port conflicts
\`\`\`bash
npx kill-port 3000
PORT=3001 npm run dev
\`\`\`

See [SETUP.md](SETUP.md) for more troubleshooting tips.

## 🎨 Features in Detail

### Interactive Map
- 5 webcam locations in NYC
- Color-coded markers (yellow=high sun, orange=medium, gray=low)
- Click markers for detailed data
- Smooth animations

### Heatmap Layer
- Toggle heatmap visualization
- Gradient from gray (low) to yellow (high sun)
- Smooth interpolation between points

### Real-time Updates
- Server-Sent Events for live data
- Updates every 3 seconds
- Connection status indicator
- Automatic reconnection

### Demo Data
- Time-based sun exposure
- Morning: 60% sun
- Midday: 85% sun
- Afternoon: 70% sun
- Night: 20% sun
- Random wetness (20% chance)

## 🔮 Future Enhancements

- [ ] Historical data visualization
- [ ] Weather alerts and notifications
- [ ] Mobile app (React Native)
- [ ] Multi-city support
- [ ] User-submitted webcams
- [ ] Advanced CV models
- [ ] Predictive analytics

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Support

- GitHub Issues for bugs
- Check SETUP.md for common issues
- Review documentation

## 🙏 Acknowledgments

- OpenCV for computer vision
- Leaflet for mapping
- shadcn/ui for components
- Vercel for hosting
