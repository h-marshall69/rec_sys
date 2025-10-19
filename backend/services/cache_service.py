import json
from datetime import datetime, timedelta
from config.settings import Config

class CacheService:
    """Gestiona caché en memoria"""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        if not Config.CACHE_ENABLED:
            return None
        
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.now() < expiry:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        if not Config.CACHE_ENABLED:
            return
        
        expiry = datetime.now() + timedelta(seconds=Config.CACHE_TTL)
        self.cache[key] = (value, expiry)
    
    def clear(self):
        self.cache.clear()