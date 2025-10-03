"""
Phase 4: Advanced Computer Vision Analysis
Enhanced wetness detection with multiple indicators and confidence scoring.
"""

import cv2
import numpy as np
from typing import Dict, Tuple
from datetime import datetime

def analyze_wetness_advanced(image_path: str) -> Dict[str, float]:
    """
    Advanced wetness analysis with multiple detection methods.
    
    Methods:
    1. Reflection detection (specular highlights)
    2. Dark surface detection (wet pavement)
    3. Color saturation analysis
    4. Edge detection (water puddles have distinct edges)
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary with wetness score and confidence
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {"wetness": 0.0, "confidence": 0.0}
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Method 1: Reflection detection (specular highlights)
        _, saturation, value = cv2.split(hsv)
        reflection_mask = cv2.bitwise_and(value > 200, saturation < 50)
        reflection_score = np.sum(reflection_mask) / reflection_mask.size
        
        # Method 2: Dark surface detection
        dark_mask = gray < 60
        dark_score = np.sum(dark_mask) / dark_mask.size
        
        # Method 3: Color saturation (wet surfaces often have lower saturation)
        low_sat_mask = saturation < 40
        low_sat_score = np.sum(low_sat_mask) / low_sat_mask.size
        
        # Method 4: Edge detection for puddles
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Combine scores with weights
        wetness = (
            reflection_score * 0.35 +
            dark_score * 0.25 +
            low_sat_score * 0.20 +
            edge_density * 0.20
        )
        
        # Calculate confidence based on agreement between methods
        scores = [reflection_score, dark_score, low_sat_score, edge_density]
        confidence = 1.0 - (np.std(scores) / np.mean(scores)) if np.mean(scores) > 0 else 0.5
        
        print(f"[v0] Advanced wetness analysis:")
        print(f"  - Reflection: {reflection_score:.2%}")
        print(f"  - Dark surfaces: {dark_score:.2%}")
        print(f"  - Low saturation: {low_sat_score:.2%}")
        print(f"  - Edge density: {edge_density:.2%}")
        print(f"  - Final wetness: {wetness:.2%} (confidence: {confidence:.2%})")
        
        return {
            "wetness": round(wetness, 3),
            "confidence": round(confidence, 3),
            "reflection_score": round(reflection_score, 3),
            "dark_score": round(dark_score, 3)
        }
        
    except Exception as e:
        print(f"[v0] Error in advanced wetness analysis: {str(e)}")
        return {"wetness": 0.0, "confidence": 0.0}

def analyze_image_advanced(image_path: str) -> Dict:
    """
    Perform advanced analysis with confidence scores.
    """
    from cv_analysis import analyze_sun_exposure
    
    print(f"\n[v0] Advanced analysis: {image_path}")
    
    sun_exposure = analyze_sun_exposure(image_path)
    wetness_result = analyze_wetness_advanced(image_path)
    
    result = {
        "sun_exposure": round(sun_exposure, 3),
        "wetness": wetness_result["wetness"],
        "wetness_confidence": wetness_result["confidence"],
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"[v0] Advanced analysis complete")
    return result

if __name__ == "__main__":
    print("[v0] Advanced CV Analysis Module - Testing")
    # Example usage
    # result = analyze_image_advanced("data/webcam_images/cam-1_20250104_120000.jpg")
    # print(f"\nResult: {result}")
