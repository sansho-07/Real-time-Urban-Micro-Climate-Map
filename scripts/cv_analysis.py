"""
Phase 2: Computer Vision Analysis Module
Analyzes webcam images to detect sun exposure and wetness using OpenCV.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime

def analyze_sun_exposure(image_path: str) -> float:
    """
    Analyze sun exposure by detecting shadow vs. bright areas.
    
    Algorithm:
    1. Convert image to grayscale
    2. Apply threshold to create binary image
    3. Calculate percentage of bright (sun) vs dark (shadow) pixels
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Sun exposure ratio (0.0 to 1.0)
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            print(f"[v0] Error: Could not read image {image_path}")
            return 0.0
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive threshold to handle varying lighting conditions
        # This creates a binary image: bright areas (sun) = white, dark areas (shadow) = black
        binary = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        
        # Calculate percentage of bright pixels (sun exposure)
        total_pixels = binary.size
        bright_pixels = np.sum(binary == 255)
        sun_exposure = bright_pixels / total_pixels
        
        print(f"[v0] Sun exposure analysis: {sun_exposure:.2%} bright pixels")
        return sun_exposure
        
    except Exception as e:
        print(f"[v0] Error analyzing sun exposure: {str(e)}")
        return 0.0

def analyze_wetness(image_path: str) -> float:
    """
    Analyze wetness by detecting reflections and dark wet surfaces.
    
    Algorithm:
    1. Convert to HSV color space
    2. Detect high saturation areas (reflections from water)
    3. Detect dark areas with low value (wet surfaces)
    4. Combine both indicators for wetness score
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Wetness ratio (0.0 to 1.0)
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            print(f"[v0] Error: Could not read image {image_path}")
            return 0.0
        
        # Convert to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Extract channels
        _, saturation, value = cv2.split(hsv)
        
        # Detect reflections (high saturation, high value)
        reflection_mask = cv2.bitwise_and(
            saturation > 100,
            value > 150
        )
        
        # Detect dark wet surfaces (low value, moderate saturation)
        wet_surface_mask = cv2.bitwise_and(
            value < 80,
            saturation > 30
        )
        
        # Combine both indicators
        wetness_mask = cv2.bitwise_or(reflection_mask.astype(np.uint8), wet_surface_mask.astype(np.uint8))
        
        # Calculate wetness percentage
        total_pixels = wetness_mask.size
        wet_pixels = np.sum(wetness_mask > 0)
        wetness = wet_pixels / total_pixels
        
        print(f"[v0] Wetness analysis: {wetness:.2%} wet indicators")
        return wetness
        
    except Exception as e:
        print(f"[v0] Error analyzing wetness: {str(e)}")
        return 0.0

def analyze_image(image_path: str) -> Dict[str, float]:
    """
    Perform complete analysis on an image.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary with analysis results
    """
    print(f"\n[v0] Analyzing image: {image_path}")
    
    sun_exposure = analyze_sun_exposure(image_path)
    wetness = analyze_wetness(image_path)
    
    result = {
        "sun_exposure": round(sun_exposure, 3),
        "wetness": round(wetness, 3),
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"[v0] Analysis complete: Sun={result['sun_exposure']:.1%}, Wetness={result['wetness']:.1%}")
    
    return result

def batch_analyze_images(image_dir: str = "data/webcam_images") -> Dict[str, Dict]:
    """
    Analyze all images in a directory.
    
    Args:
        image_dir: Directory containing webcam images
        
    Returns:
        Dictionary mapping image filenames to analysis results
    """
    image_path = Path(image_dir)
    
    if not image_path.exists():
        print(f"[v0] Error: Directory {image_dir} does not exist")
        return {}
    
    results = {}
    image_files = list(image_path.glob("*.jpg")) + list(image_path.glob("*.png"))
    
    print(f"[v0] Found {len(image_files)} images to analyze")
    
    for img_file in image_files:
        result = analyze_image(str(img_file))
        results[img_file.name] = result
    
    print(f"\n[v0] Batch analysis complete: {len(results)} images processed")
    return results

def create_visualization(image_path: str, output_path: str = None) -> str:
    """
    Create a visualization showing the analysis results overlaid on the image.
    
    Args:
        image_path: Path to the input image
        output_path: Path to save the visualization (optional)
        
    Returns:
        Path to the saved visualization
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return ""
        
        # Perform analysis
        result = analyze_image(image_path)
        
        # Create overlay
        overlay = img.copy()
        _, _ = img.shape[:2]
        
        # Add semi-transparent background for text
        cv2.rectangle(overlay, (10, 10), (300, 100), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        # Add text with results
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f"Sun Exposure: {result['sun_exposure']:.1%}", 
                    (20, 40), font, 0.7, (0, 255, 255), 2)
        cv2.putText(img, f"Wetness: {result['wetness']:.1%}", 
                    (20, 70), font, 0.7, (0, 255, 255), 2)
        
        # Save visualization
        if output_path is None:
            output_path = image_path.replace(".jpg", "_analyzed.jpg")
        
        cv2.imwrite(output_path, img)
        print(f"[v0] Visualization saved to: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"[v0] Error creating visualization: {str(e)}")
        return ""

if __name__ == "__main__":
    # Test with a sample image (you can replace with actual webcam image path)
    print("[v0] Computer Vision Analysis Module - Testing")
    
    # Example: Analyze a single image
    # result = analyze_image("data/webcam_images/cam-1_20250104_120000.jpg")
    # print(f"\nResult: {result}")
    
    # Example: Batch analyze all images
    # results = batch_analyze_images()
    
    # Example: Create visualization
    # create_visualization("data/webcam_images/cam-1_20250104_120000.jpg")
    
    print("\n[v0] CV Analysis module ready. Import functions to use in your pipeline.")
