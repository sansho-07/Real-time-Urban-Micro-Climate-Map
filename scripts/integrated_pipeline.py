"""
Integrated Pipeline: Combines data ingestion and CV analysis
This script fetches images and immediately analyzes them.
Includes DEMO MODE for testing without real webcam URLs.
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime, timezone
import sys
import argparse

DEMO_MODE = True  # Set to False to use real webcam URLs

if not DEMO_MODE:
    from fetch_webcam_images import fetch_all_images
    from cv_analysis import analyze_image

# Output directory for analysis results
RESULTS_DIR = Path("data/analysis_results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_demo_data():
    """Generate realistic demo data based on time of day"""
    hour = datetime.now().hour
    
    # Adjust sun exposure based on time of day
    if 6 <= hour < 10:  # Morning
        base_sun = 0.6
    elif 10 <= hour < 15:  # Midday
        base_sun = 0.85
    elif 15 <= hour < 19:  # Afternoon
        base_sun = 0.7
    else:  # Night
        base_sun = 0.2
    
    # Demo webcam locations in NYC
    webcams = [
        {"id": "downtown-plaza", "name": "Downtown Plaza", "lat": 40.7589, "lng": -73.9851},
        {"id": "brooklyn-bridge", "name": "Brooklyn Bridge", "lat": 40.7061, "lng": -73.9969},
        {"id": "central-park", "name": "Central Park North", "lat": 40.7967, "lng": -73.9496},
        {"id": "times-square", "name": "Times Square", "lat": 40.7580, "lng": -73.9855},
        {"id": "hudson-yards", "name": "Hudson Yards", "lat": 40.7536, "lng": -74.0014},
    ]
    
    results = []
    for webcam in webcams:
        # Add some randomness to sun exposure
        import random
        sun_exposure = max(0.01, min(0.99, base_sun + (random.random() - 0.5) * 0.3))
        
        # Random wetness (20% chance of wet conditions)
        is_wet = random.random() < 0.2
        wetness = random.uniform(0.6, 0.9) if is_wet else random.uniform(0.0, 0.2)
        
        # Calculate comfort level
        if sun_exposure > 0.7:
            comfort = "comfortable"
        elif sun_exposure > 0.4:
            comfort = "moderate"
        else:
            comfort = "low"
        
        result = {
            "webcam_id": webcam["id"],
            "webcam_name": webcam["name"],
            "location": {"lat": webcam["lat"], "lng": webcam["lng"]},
            "analysis": {
                "sun_exposure": round(sun_exposure, 3),
                "shadow_ratio": round(1 - sun_exposure, 3),
                "brightness_avg": round(sun_exposure * 200 + 55, 1),
                "wetness_detected": is_wet,
                "wetness_confidence": round(wetness, 2),
                "comfort_level": comfort,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success",
        }
        results.append(result)
    
    return results

async def process_pipeline():
    """
    Run the complete pipeline: fetch images and analyze them.
    """
    print("[v0] Starting integrated pipeline...")
    
    if DEMO_MODE:
        print("\n[v0] Running in DEMO MODE - generating realistic mock data...")
        analysis_results = generate_demo_data()
        print(f"[v0] Generated {len(analysis_results)} demo results")
    else:
        # Step 1: Fetch images from all webcams
        print("\n[v0] Step 1: Fetching images from webcams...")
        fetch_results = await fetch_all_images()
        
        # Step 2: Analyze each successfully fetched image
        print("\n[v0] Step 2: Analyzing images with computer vision...")
        analysis_results = []
        
        for fetch_result in fetch_results:
            if fetch_result["success"]:
                # Analyze the image
                image_path = fetch_result["filepath"]
                analysis = analyze_image(image_path)
                
                # Combine fetch and analysis results
                combined_result = {
                    "webcam_id": fetch_result["id"],
                    "webcam_name": fetch_result["name"],
                    "image_path": image_path,
                    "timestamp": fetch_result["timestamp"],
                    "sun_exposure": analysis["sun_exposure"],
                    "wetness": analysis["wetness"],
                    "analysis_timestamp": analysis["timestamp"]
                }
                
                analysis_results.append(combined_result)
            else:
                print(f"[v0] Skipping analysis for {fetch_result['name']}: {fetch_result.get('error', 'Unknown error')}")
    
    # Step 3: Save results to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = RESULTS_DIR / f"analysis_{timestamp}.json"
    
    output_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": analysis_results,
        "total_analyzed": len(analysis_results),
        "mode": "demo" if DEMO_MODE else "production"
    }
    
    with open(results_file, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n[v0] Pipeline complete! Results saved to: {results_file}")
    print(f"[v0] Analyzed {len(analysis_results)} webcam images")
    
    # Print summary
    if analysis_results:
        if DEMO_MODE:
            avg_sun = sum(r["analysis"]["sun_exposure"] for r in analysis_results) / len(analysis_results)
            wet_count = sum(1 for r in analysis_results if r["analysis"]["wetness_detected"])
        else:
            avg_sun = sum(r["sun_exposure"] for r in analysis_results) / len(analysis_results)
            avg_wetness = sum(r["wetness"] for r in analysis_results) / len(analysis_results)
            print(f"[v0] Average sun exposure: {avg_sun:.1%}")
            print(f"[v0] Average wetness: {avg_wetness:.1%}")
            return analysis_results
        
        print(f"[v0] Average sun exposure: {avg_sun:.1%}")
        print(f"[v0] Wet locations: {wet_count}/{len(analysis_results)}")
    
    return analysis_results

async def continuous_pipeline(interval_seconds: int = 300):
    """
    Run the pipeline continuously at regular intervals.
    
    Args:
        interval_seconds: Time between pipeline runs (default: 5 minutes)
    """
    print(f"[v0] Starting continuous pipeline (interval: {interval_seconds}s)")
    
    while True:
        print(f"\n{'='*60}")
        print(f"[v0] Pipeline cycle starting at {datetime.now()}")
        print(f"{'='*60}")
        
        await process_pipeline()
        
        print(f"\n[v0] Waiting {interval_seconds} seconds until next cycle...")
        await asyncio.sleep(interval_seconds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Urban Micro-Climate Pipeline")
    parser.add_argument("--continuous", type=int, metavar="SECONDS", 
                       help="Run continuously with specified interval in seconds")
    parser.add_argument("--production", action="store_true",
                       help="Run in production mode with real webcams (requires webcam URLs)")
    
    args = parser.parse_args()
    
    # Override demo mode if production flag is set
    if args.production:
        DEMO_MODE = False
        print("[v0] Running in PRODUCTION MODE")
    else:
        print("[v0] Running in DEMO MODE")
    
    if args.continuous:
        # Run continuous pipeline
        print(f"[v0] Starting continuous mode with {args.continuous}s interval...")
        asyncio.run(continuous_pipeline(interval_seconds=args.continuous))
    else:
        # Run a single pipeline cycle
        print("[v0] Running single pipeline cycle...")
        asyncio.run(process_pipeline())
