"""
Integrated Pipeline: Combines data ingestion and CV analysis
This script fetches images and immediately analyzes them.
"""

import asyncio
import aiohttp
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional
from cv_analysis import analyze_image

# ----- Configuration -----
OUT_IMAGES = Path("data/webcam_images")
OUT_RESULTS = Path("data/analysis_results")
OUT_IMAGES.mkdir(parents=True, exist_ok=True)
OUT_RESULTS.mkdir(parents=True, exist_ok=True)

# Replace these URLs with your real webcam endpoints
WEBCAMS: List[Dict[str, str]] = [
    {"name": "Times Square", "url": "https://example.com/times_square.jpg"},
    {"name": "Downtown Plaza", "url": "https://example.com/downtown.jpg"},
    {"name": "Hudson Yards", "url": "https://example.com/hudson.jpg"},
    {"name": "Central Park North", "url": "https://example.com/central_park.jpg"},
    {"name": "Brooklyn Bridge", "url": "https://example.com/brooklyn.jpg"},
]

# Output directory for analysis results
RESULTS_DIR = Path("data/analysis_results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ----- Helpers -----

def _safe_filename(name: str, url: str) -> str:
    ext = Path(url).suffix or ".jpg"
    safe = "".join(c if c.isalnum() or c in "-._" else "_" for c in name).strip("_")
    if not safe:
        safe = "webcam"
    return f"{safe}{ext}"


async def _fetch_one(
    session: aiohttp.ClientSession,
    name: str,
    url: str,
    out_dir: Path,
    timeout_seconds: int,
    retries: int,
    backoff_factor: float,
) -> Dict[str, Optional[str]]:
    result: Dict[str, Optional[str]] = {"name": name, "url": url, "file_path": None, "status": None, "error": None}
    if not url:
        result["error"] = "no url"
        return result

    for attempt in range(1, retries + 1):
        try:
            async with session.get(url) as resp:
                result["status"] = str(resp.status)
                if resp.status == 200:
                    data = await resp.read()
                    fname = _safe_filename(name, url)
                    path = out_dir / fname
                    path.write_bytes(data)
                    result["file_path"] = str(path)
                    return result
                else:
                    result["error"] = f"HTTP {resp.status}"
                    # don't retry on client errors (4xx)
                    if 400 <= resp.status < 500:
                        break
        except asyncio.TimeoutError:
            result["error"] = f"timeout attempt {attempt}"
        except aiohttp.ClientError as e:
            result["error"] = f"client error: {e}"
        except Exception as e:
            result["error"] = f"unexpected: {e}"

        await asyncio.sleep(backoff_factor * attempt)

    return result


async def fetch_all_images(
    webcams: List[Dict[str, str]] = WEBCAMS,
    timeout_seconds: int = 10,
    retries: int = 3,
    backoff_factor: float = 0.5,
) -> List[Dict[str, Optional[str]]]:
    """
    Concurrently fetch images from webcams.
    Returns list of dicts: {name,url,file_path,status,error}
    """
    timeout = aiohttp.ClientTimeout(total=timeout_seconds)
    results: List[Dict[str, Optional[str]]] = []
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            _fetch_one(
                session,
                cam.get("name", "unknown"),
                cam.get("url", ""),
                OUT_IMAGES,
                timeout_seconds,
                retries,
                backoff_factor,
            )
            for cam in webcams
        ]
        for coro in asyncio.as_completed(tasks):
            res = await coro
            results.append(res)
    return results


def analyze_images(file_paths: List[str]) -> Dict:
    """
    Lightweight analysis example: compute file size and sha256 for each image.
    Replace with your CV/model analysis when ready.
    """
    images_info = []
    for p in file_paths:
        try:
            b = Path(p).read_bytes()
            sha = hashlib.sha256(b).hexdigest()
            images_info.append({"path": p, "bytes": len(b), "sha256": sha})
        except Exception as e:
            images_info.append({"path": p, "error": str(e)})
    return {"analyzed": len(images_info), "images": images_info, "timestamp": datetime.now(timezone.utc).isoformat() + "Z"}


async def process_pipeline():
    """
    Run the complete pipeline: fetch images and analyze them.
    This version normalizes fetch results that may come from older/newer fetch functions.
    """
    print("[v0] Starting integrated pipeline...")

    # Step 1: Fetch images from all webcams
    print("\n[v0] Step 1: Fetching images from webcams...")
    fetch_results = await fetch_all_images()

    if not isinstance(fetch_results, list):
        print("[v0] Error: fetch_all_images did not return a list")
        return []

    # Step 2: Analyze each successfully fetched image
    print("\n[v0] Step 2: Analyzing images with computer vision...")
    analysis_results = []

    for fetch_result in fetch_results:
        # Normalize presence of success flag
        if "success" in fetch_result:
            success = bool(fetch_result.get("success"))
        else:
            # older/newer schema: success if a file path exists
            success = bool(fetch_result.get("file_path") or fetch_result.get("filepath"))

        # Normalize image path & identifiers
        image_path = fetch_result.get("filepath") or fetch_result.get("file_path") or None
        webcam_id = fetch_result.get("id") or fetch_result.get("name") or None
        webcam_name = fetch_result.get("name") or webcam_id or "unknown"
        timestamp = fetch_result.get("timestamp") or datetime.utcnow().isoformat()

        if not success or not image_path:
            err = fetch_result.get("error") or fetch_result.get("status") or "fetch failed"
            print(f"[v0] Skipping analysis for {webcam_name}: {err}")
            continue

        # Attempt to use project analyze_image (cv_analysis) if available, otherwise use local analyze_images fallback
        try:
            # prefer a single-image analyzer if available
            if "analyze_image" in globals() and callable(globals().get("analyze_image")):
                analysis = analyze_image(image_path)
            else:
                # analyze_images returns a dict for multiple images; compute for this single image
                analysis_multi = analyze_images([image_path])
                # unwrap if analyze_images used
                if "images" in analysis_multi and isinstance(analysis_multi["images"], list):
                    img_info = analysis_multi["images"][0] if analysis_multi["images"] else {}
                else:
                    img_info = {}
                # create a minimal analysis structure compatible with expected fields
                analysis = {
                    "sun_exposure": img_info.get("sun_exposure", 0),
                    "wetness": img_info.get("wetness", 0),
                    "details": img_info,
                    "timestamp": analysis_multi.get("timestamp") or datetime.utcnow().isoformat()
                }
        except Exception as e:
            print(f"[v0] Error analyzing {image_path}: {e}")
            analysis = {"error": str(e)}

        # Combine fetch + analysis into a single result record
        combined_result = {
            "webcam_id": webcam_id,
            "webcam_name": webcam_name,
            "image_path": image_path,
            "fetch_timestamp": timestamp,
            "sun_exposure": analysis.get("sun_exposure", 0),
            "wetness": analysis.get("wetness", 0),
            "analysis": analysis,
            "fetch_meta": fetch_result,
        }

        analysis_results.append(combined_result)

    # Step 3: Save results to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = RESULTS_DIR / f"analysis_{timestamp}.json"
    with open(results_file, "w") as f:
        json.dump(analysis_results, f, indent=2)

    print(f"\n[v0] Pipeline complete! Results saved to: {results_file}")
    print(f"[v0] Analyzed {len(analysis_results)} webcam images")

    # Print summary only if we have any analysis results
    if analysis_results:
        avg_sun = sum(r.get("sun_exposure", 0) for r in analysis_results) / len(analysis_results)
        avg_wetness = sum(r.get("wetness", 0) for r in analysis_results) / len(analysis_results)
        print(f"[v0] Average sun exposure: {avg_sun:.1%}")
        print(f"[v0] Average wetness: {avg_wetness:.1%}")

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
    # Ensure aiohttp is installed:
    #   python -m pip install aiohttp
    # Run a single pipeline cycle
    print("[v0] Running single pipeline cycle...")
    asyncio.run(process_pipeline())
    
    # Uncomment below to run continuous pipeline
    # asyncio.run(continuous_pipeline(interval_seconds=300))
