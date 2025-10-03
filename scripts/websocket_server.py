"""
Phase 3: WebSocket Server (FastAPI)
This script sets up a FastAPI WebSocket endpoint that pushes analysis results in real-time.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from datetime import datetime
from typing import List
import random

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections: List[WebSocket] = []

async def broadcast_analysis_results():
    """
    Continuously broadcast analysis results to all connected clients.
    In production, this would read from the CV analysis pipeline.
    """
    while True:
        if active_connections:
            # Simulate analysis results for all webcams
            updates = []
            for i in range(1, 11):
                updates.append({
                    "webcamId": f"cam-{i}",
                    "sunExposure": round(random.uniform(0.3, 0.95), 3),
                    "wetness": round(random.uniform(0.0, 0.35), 3),
                    "timestamp": datetime.now().isoformat()
                })
            
            message = {
                "type": "analysis_update",
                "data": updates
            }
            
            # Broadcast to all connected clients
            disconnected = []
            for connection in active_connections:
                try:
                    await connection.send_json(message)
                    print(f"[v0] Sent update to client: {len(updates)} webcams")
                except Exception as e:
                    print(f"[v0] Error sending to client: {e}")
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for conn in disconnected:
                active_connections.remove(conn)
        
        # Wait 3 seconds before next update
        await asyncio.sleep(3)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time climate data updates.
    """
    await websocket.accept()
    active_connections.append(websocket)
    
    print(f"[v0] Client connected. Total connections: {len(active_connections)}")
    
    # Send initial connection message
    await websocket.send_json({
        "type": "connected",
        "message": "WebSocket connection established"
    })
    
    try:
        # Keep connection alive and listen for messages
        while True:
            data = await websocket.receive_text()
            print(f"[v0] Received from client: {data}")
            
            # Echo back or handle client messages
            await websocket.send_json({
                "type": "ack",
                "message": "Message received"
            })
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"[v0] Client disconnected. Total connections: {len(active_connections)}")

@app.on_event("startup")
async def startup_event():
    """
    Start the background task for broadcasting analysis results.
    """
    print("[v0] Starting WebSocket server...")
    asyncio.create_task(broadcast_analysis_results())

@app.get("/")
async def root():
    return {
        "message": "Urban Micro-Climate WebSocket Server",
        "active_connections": len(active_connections),
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    print("[v0] Starting FastAPI WebSocket server on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
