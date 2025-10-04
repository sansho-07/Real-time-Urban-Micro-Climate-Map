# Micro-Climate Map - Complete Setup Guide

Step-by-step guide to run the Real-time Urban Micro-Climate Map locally and deploy to production.

## Quick Start (Demo Mode)

The fastest way to see the application working:

### 1. Install Dependencies

\`\`\`bash
# Install Node.js dependencies
npm install

# Install Python dependencies (optional for demo mode)
pip install -r requirements.txt
\`\`\`

### 2. Start the Application

\`\`\`bash
# Start Next.js development server
npm run dev
\`\`\`

### 3. Open Browser

Navigate to `http://localhost:3000`

You should see an interactive map with 5 webcam locations in NYC showing real-time climate data!

## How It Works

### Demo Mode (Default)

The application runs in **demo mode** by default, which:
- Generates realistic mock data based on time of day
- Updates automatically via Server-Sent Events
- Requires NO webcam configuration
- Perfect for testing and development

The demo data simulates:
- Sun exposure varying by time (high at midday, low at night)
- Random wetness conditions (20% chance)
- Realistic comfort levels
- Live updates every few seconds

### Production Mode

For real webcam analysis, you need to:
1. Configure real webcam URLs
2. Run the Python pipeline
3. Set up OpenCV for image analysis

## Detailed Setup

### Prerequisites

- **Node.js** v18+ - [Download](https://nodejs.org/)
- **Python** 3.8+ - [Download](https://www.python.org/) (optional for demo)
- **Git** - [Download](https://git-scm.com/)

### Installation

#### Frontend Dependencies

\`\`\`bash
npm install
\`\`\`

This installs:
- Next.js 15
- React 18
- Leaflet (mapping)
- shadcn/ui components
- TypeScript

#### Backend Dependencies (Optional)

\`\`\`bash
pip install -r requirements.txt
\`\`\`

This installs:
- opencv-python (computer vision)
- aiohttp (async HTTP)
- fastapi (WebSocket server)
- numpy (numerical processing)

## Running Locally

### Option 1: Demo Mode (Recommended)

\`\`\`bash
# Start frontend only
npm run dev
\`\`\`

Open `http://localhost:3000` - that's it!

### Option 2: With Python Pipeline

\`\`\`bash
# Terminal 1: Start frontend
npm run dev

# Terminal 2: Run pipeline once
python scripts/integrated_pipeline.py

# Or run continuously (updates every 5 minutes)
python scripts/integrated_pipeline.py --continuous 300
\`\`\`

### Option 3: Full Stack with WebSocket

\`\`\`bash
# Terminal 1: Start frontend
npm run dev

# Terminal 2: Start WebSocket server
python scripts/websocket_server.py

# Terminal 3: Run pipeline continuously
python scripts/integrated_pipeline.py --continuous 300
\`\`\`

## Production Setup

### Step 1: Configure Real Webcams

Edit `scripts/fetch_webcam_images.py`:

\`\`\`python
WEBCAM_URLS = [
    {
        "id": "downtown-plaza",
        "name": "Downtown Plaza",
        "url": "https://your-webcam-url.com/image.jpg"  # Real URL here
    },
    # Add more webcams...
]
\`\`\`

### Step 2: Enable Production Mode

Edit `scripts/integrated_pipeline.py`:

\`\`\`python
DEMO_MODE = False  # Disable demo mode
\`\`\`

Or run with flag:

\`\`\`bash
python scripts/integrated_pipeline.py --production
\`\`\`

### Step 3: Run Pipeline

\`\`\`bash
# Single run
python scripts/integrated_pipeline.py --production

# Continuous (every 5 minutes)
python scripts/integrated_pipeline.py --production --continuous 300
\`\`\`

## Finding Public Webcams

### Free Public Webcam Sources

1. **EarthCam** - https://www.earthcam.com/
   - Many free public webcams
   - Look for direct image URLs (usually end in .jpg)

2. **Windy Webcams** - https://www.windy.com/webcams
   - Weather webcams worldwide
   - Some provide direct image access

3. **City Traffic Cameras**
   - Many cities publish traffic camera feeds
   - Example: NYC DOT cameras, London traffic cams

### How to Get Image URLs

1. Find a webcam on a public site
2. Right-click on the image → "Open image in new tab"
3. Copy the direct image URL (should end in .jpg or .png)
4. Test the URL in your browser - it should show just the image
5. Add to your `WEBCAM_URLS` list

### Example Real URLs

\`\`\`python
# Example structure (these are not real working URLs)
WEBCAM_URLS = [
    {
        "id": "times-square",
        "name": "Times Square NYC",
        "url": "https://webcam-site.com/cameras/timessquare/current.jpg"
    },
]
\`\`\`

## Deployment

### Deploy to Vercel (Easiest)

1. Push code to GitHub:
\`\`\`bash
git init
git add .
git commit -m "Initial commit"
git push
\`\`\`

2. Go to [vercel.com](https://vercel.com)
3. Click "Import Project"
4. Select your repository
5. Click "Deploy"

Done! Your frontend is live.

### Deploy Python Backend

#### Option A: Separate Server

Deploy to any cloud provider:
- AWS EC2
- DigitalOcean Droplet
- Google Cloud Compute Engine
- Azure VM

\`\`\`bash
# On server
git clone your-repo
cd micro-climate-map
pip install -r requirements.txt
python scripts/integrated_pipeline.py --continuous 300
\`\`\`

#### Option B: Docker

\`\`\`bash
# Build image
docker build -t micro-climate-map .

# Run container
docker run -d -p 3000:3000 micro-climate-map
\`\`\`

#### Option C: Docker Compose

\`\`\`bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
\`\`\`

### Full Production Stack

\`\`\`bash
# On Ubuntu server
sudo apt update
sudo apt install nodejs npm python3 python3-pip nginx

# Clone and setup
git clone your-repo
cd micro-climate-map
npm install
pip3 install -r requirements.txt

# Build frontend
npm run build

# Start with PM2
npm install -g pm2
pm2 start npm --name "frontend" -- start
pm2 start "python3 scripts/integrated_pipeline.py --continuous 300" --name "pipeline"

# Configure Nginx
sudo nano /etc/nginx/sites-available/micro-climate
\`\`\`

Nginx config:
\`\`\`nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
    }
}
\`\`\`

## Troubleshooting

### "Module not found" errors

\`\`\`bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
\`\`\`

### Python import errors

\`\`\`bash
# Reinstall Python packages
pip install --upgrade -r requirements.txt
\`\`\`

### Port 3000 already in use

\`\`\`bash
# Kill process on port 3000
npx kill-port 3000

# Or use different port
PORT=3001 npm run dev
\`\`\`

### OpenCV errors on Linux

\`\`\`bash
# Install system dependencies
sudo apt install libgl1-mesa-glx libglib2.0-0
pip install opencv-python-headless
\`\`\`

### No data showing on map

1. Check browser console for errors
2. Verify API endpoint: `http://localhost:3000/api/analysis/latest`
3. Check if pipeline is running: `ls data/analysis_results/`
4. Restart frontend: `npm run dev`

## Testing

### Test Frontend
\`\`\`bash
npm run dev
# Visit http://localhost:3000
\`\`\`

### Test API
\`\`\`bash
# Latest analysis
curl http://localhost:3000/api/analysis/latest

# Webcam list
curl http://localhost:3000/api/webcams

# SSE stream
curl http://localhost:3000/api/ws
\`\`\`

### Test Pipeline
\`\`\`bash
# Run once
python scripts/integrated_pipeline.py

# Check output
cat data/analysis_results/analysis_*.json
\`\`\`

## Features

### Interactive Map
- Click markers to see detailed climate data
- Toggle heatmap layer for sun exposure visualization
- Real-time updates via Server-Sent Events
- Responsive design for mobile and desktop

### Climate Analysis
- Sun exposure detection (shadow vs. bright areas)
- Wetness detection (reflections and wet surfaces)
- Comfort level calculation
- Time-based data generation in demo mode

### Real-time Updates
- Automatic data refresh every 3 seconds
- Live connection status indicator
- Smooth marker animations
- No page refresh needed

## Next Steps

1. **Customize Locations**: Edit webcam locations in the code
2. **Add Real Webcams**: Configure actual webcam URLs
3. **Enhance Analysis**: Improve CV algorithms
4. **Add Features**: Historical data, alerts, mobile app
5. **Scale Up**: Add more cities and webcams

## Support

- Check [README.md](README.md) for project overview
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for advanced deployment
- Open GitHub issues for bugs

## License

MIT License

