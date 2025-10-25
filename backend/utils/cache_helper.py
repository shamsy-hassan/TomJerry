# Redis cache helpers
# ============================================================
# File: backend/utils/cache_helper.py
# Description:
#   This module provides a simple in-memory caching system
#   for storing and retrieving temporary data such as
#   active sessions, leaderboard snapshots, or player states.
#   It’s designed for easy upgrade to Redis or Memcached later.
# ============================================================

import time
from threading import Lock

# ============================================================
# SECTION 1: Simple Thread-Safe Cache Class
# ------------------------------------------------------------
# This cache class is a lightweight dictionary-based cache
# that supports:
#   - Setting and getting values with expiration.
#   - Automatic cleanup of expired keys.
#   - Thread-safety via a lock mechanism.
# ============================================================

class SimpleCache:
    def __init__(self):
        """Initialize an empty cache dictionary and a thread lock."""
        self._cache = {}
        self._lock = Lock()

    def set(self, key, value, ttl=None):
        """
        Store a key-value pair in the cache.
        :param key: Unique identifier for the cached item.
        :param value: Data to cache.
        :param ttl: Optional time-to-live (seconds) for automatic expiry.
        """
        with self._lock:
            expire_at = time.time() + ttl if ttl else None
            self._cache[key] = {"value": value, "expire_at": expire_at}
            print(f"[Cache] Set key='{key}' (ttl={ttl}s)")

    def get(self, key):
        """
        Retrieve a value from cache if it exists and is not expired.
        Returns None if the key is missing or expired.
        """
        with self._lock:
            item = self._cache.get(key)
            if not item:
                return None

            expire_at = item["expire_at"]
            if expire_at and expire_at < time.time():
                # Item expired; remove it
                print(f"[Cache] Key '{key}' expired and removed.")
                del self._cache[key]
                return None

            return item["value"]

    def delete(self, key):
        """Manually remove a key from cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                print(f"[Cache] Deleted key='{key}'")

    def clear(self):
        """Completely clear all cached data."""
        with self._lock:
            self._cache.clear()
            print("[Cache] Cleared all cache data.")

# ============================================================
# SECTION 2: Global Cache Instance
# ------------------------------------------------------------
# This global instance can be imported anywhere in the backend
# to store temporary values such as active socket sessions,
# tokens, or gameplay state.
# ============================================================

cache = SimpleCache()

# ============================================================
# SECTION 3: Helper Functions
# ------------------------------------------------------------
# These are utility wrappers around the cache instance.
# They make usage simpler across the backend code.
# ============================================================

def cache_set(key, value, ttl=None):
    """Convenience wrapper to set a cache item."""
    cache.set(key, value, ttl)

def cache_get(key):
    """Convenience wrapper to retrieve a cache item."""
    return cache.get(key)

def cache_delete(key):
    """Convenience wrapper to delete a cache item."""
    cache.delete(key)

def cache_clear():
    """Convenience wrapper to clear the cache."""
    cache.clear()
