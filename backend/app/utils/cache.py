import time
from cachetools import TTLCache

# Simple in-memory TTL cache
cache = TTLCache(maxsize=1000, ttl=300)

def get_cached(key):
    return cache.get(key)

def set_cache(key, value):
    cache[key] = value
