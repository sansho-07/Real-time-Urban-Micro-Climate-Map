"""
Phase 1: Data Ingestion Script
This script fetches images from public webcam URLs at regular intervals.
Uses asyncio and aiohttp for efficient concurrent image downloads.
"""

import asyncio
import aiohttp
from datetime import datetime
from pathlib import Path

# Predefined list of public webcam URLs
WEBCAM_URLS = [
    {
        "id": "cam-1",
        "name": "Downtown Plaza",
        "url": "https://example.com/cam1/image.jpg"
    },
    {
        "id": "cam-2",
        "name": "Central Park North",
        "url": "https://example.com/cam2/image.jpg"
    },
    {
        "id": "cam-3",
        "name": "Brooklyn Bridge",
        "url": "https://example.com/cam3/image.jpg"
    },
    {
        "id": "cam-4",
        "name": "Times Square",
        "url": "https://example.com/cam4/image.jpg"
    },
    {
        "id": "cam-5",
        "name": "Hudson Yards",
        "url": "https://example.com/cam5/image.jpg"
    },
]

# Create output directory for downloaded images
OUTPUT_DIR = Path("data/webcam_images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def fetch_image(session: aiohttp.ClientSession, webcam: dict) -> dict:
    """
    Fetch a single image from a webcam URL.
    
    Args:
        session: aiohttp ClientSession for making requests
        webcam: Dictionary containing webcam id, name, and url
        
    Returns:
        Dictionary with fetch result including success status and file path
    """
    try:
        async with session.get(webcam["url"], timeout=10) as response:
            if response.status == 200:
                # Save image with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{webcam['id']}_{timestamp}.jpg"
                filepath = OUTPUT_DIR / filename

                content = await response.read()
                import aiofiles
                async with aiofiles.open(filepath, "wb") as f:
                    await f.write(content)

                print(f"[v0] Successfully fetched {webcam['name']}: {filepath}")
                return {
                    "id": webcam["id"],
                    "name": webcam["name"],
                    "success": True,
                    "filepath": str(filepath),
                    "timestamp": timestamp
                }
            else:
                print(f"[v0] Failed to fetch {webcam['name']}: HTTP {response.status}")
                return {
                    "id": webcam["id"],
                    "name": webcam["name"],
                    "success": False,
                    "error": f"HTTP {response.status}"
                }
    except Exception as e:
        print(f"[v0] Error fetching {webcam['name']}: {str(e)}")
        return {
            "id": webcam["id"],
            "name": webcam["name"],
            "success": False,
            "error": str(e)
        }

async def fetch_all_images():
    """
    Fetch images from all webcams concurrently.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_image(session, webcam) for webcam in WEBCAM_URLS]
        results = await asyncio.gather(*tasks)
        
        # Summary
        successful = sum(1 for r in results if r["success"])
        print(f"\n[v0] Fetch complete: {successful}/{len(results)} successful")
        
        return results

async def continuous_fetch(interval_seconds: int = 300):
    """
    Continuously fetch images at regular intervals.
    
    Args:
        interval_seconds: Time between fetch cycles (default: 5 minutes)
    """
    print(f"[v0] Starting continuous image fetching (interval: {interval_seconds}s)")
    
    while True:
        print(f"\n[v0] Starting fetch cycle at {datetime.now()}")
        await fetch_all_images()
        print(f"[v0] Waiting {interval_seconds} seconds until next cycle...")
        await asyncio.sleep(interval_seconds)

if __name__ == "__main__":
    # Run a single fetch cycle for testing
    print("[v0] Running single fetch cycle...")
    asyncio.run(fetch_all_images())
    
    # Uncomment below to run continuous fetching
    # asyncio.run(continuous_fetch(interval_seconds=300))
