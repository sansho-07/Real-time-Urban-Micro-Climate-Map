"""
Redis caching layer for storing current climate conditions.
"""

import redis
import json
from typing import Dict, Optional
from datetime import datetime, timedelta

class ClimateCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        Initialize Redis cache connection.
        
        Args:
            redis_url: Redis connection URL
        """
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.cache_ttl = 300  # 5 minutes
    
    def set_webcam_data(self, webcam_id: str, data: Dict) -> bool:
        """
        Store webcam analysis data in cache.
        
        Args:
            webcam_id: Unique webcam identifier
            data: Analysis data dictionary
            
        Returns:
            True if successful
        """
        try:
            key = f"webcam:{webcam_id}"
            value = json.dumps(data)
            self.redis_client.setex(key, self.cache_ttl, value)
            print(f"[v0] Cached data for {webcam_id}")
            return True
        except Exception as e:
            print(f"[v0] Error caching data: {str(e)}")
            return False
    
    def get_webcam_data(self, webcam_id: str) -> Optional[Dict]:
        """
        Retrieve webcam data from cache.
        
        Args:
            webcam_id: Unique webcam identifier
            
        Returns:
            Cached data or None if not found
        """
        try:
            key = f"webcam:{webcam_id}"
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"[v0] Error retrieving cache: {str(e)}")
            return None
    
    def get_all_webcams(self) -> Dict[str, Dict]:
        """
        Retrieve all cached webcam data.
        
        Returns:
            Dictionary mapping webcam IDs to their data
        """
        try:
            keys = self.redis_client.keys("webcam:*")
            result = {}
            for key in keys:
                webcam_id = key.split(":")[1]
                data = self.get_webcam_data(webcam_id)
                if data:
                    result[webcam_id] = data
            return result
        except Exception as e:
            print(f"[v0] Error retrieving all webcams: {str(e)}")
            return {}
    
    def set_city_stats(self, stats: Dict) -> bool:
        """
        Store city-wide statistics.
        
        Args:
            stats: Statistics dictionary
            
        Returns:
            True if successful
        """
        try:
            key = "city:stats"
            value = json.dumps(stats)
            self.redis_client.setex(key, self.cache_ttl, value)
            return True
        except Exception as e:
            print(f"[v0] Error caching stats: {str(e)}")
            return False
    
    def get_city_stats(self) -> Optional[Dict]:
        """
        Retrieve city-wide statistics.
        
        Returns:
            Statistics dictionary or None
        """
        try:
            value = self.redis_client.get("city:stats")
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"[v0] Error retrieving stats: {str(e)}")
            return None

if __name__ == "__main__":
    # Test Redis cache
    cache = ClimateCache()
    
    # Test data
    test_data = {
        "sun_exposure": 0.75,
        "wetness": 0.15,
        "timestamp": datetime.now().isoformat()
    }
    
    # Set and get
    cache.set_webcam_data("cam-1", test_data)
    retrieved = cache.get_webcam_data("cam-1")
    print(f"[v0] Retrieved: {retrieved}")
