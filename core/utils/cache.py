from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Lock
from typing import Dict, Any, Optional


@dataclass
class CacheEntry:
    data: Any
    expiry: datetime


class InMemoryCache:
    """Thread-safe in-memory cache with TTL support."""

    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = Lock()
        # Default TTLs for different types of data
        self._ttls = {
            'profile': 3600,     # 1 hour
            'contests': 1800,    # 30 minutes
            'submissions': 300,  # 5 minutes
            'problems': 3600,    # 1 hour
            'default': 300      # 5 minutes
        }

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if it exists and hasn't expired."""
        with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache[key]
            if datetime.now() > entry.expiry:
                del self._cache[key]
                return None

            return entry.data

    def set(self, key: str, value: Any, data_type: str = 'default') -> None:
        """Set value in cache with TTL based on data type."""
        ttl = self._ttls.get(data_type, self._ttls['default'])
        with self._lock:
            self._cache[key] = CacheEntry(
                data=value,
                expiry=datetime.now() + timedelta(seconds=ttl)
            )

    def delete(self, key: str) -> None:
        """Remove an item from cache."""
        with self._lock:
            self._cache.pop(key, None)

    def cleanup(self) -> int:
        """Remove all expired entries and return count of removed items."""
        with self._lock:
            now = datetime.now()
            expired = [k for k, v in self._cache.items() if now > v.expiry]
            for k in expired:
                del self._cache[k]
            return len(expired)

    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()

    def set_ttl(self, data_type: str, ttl: int) -> None:
        """Update TTL for a specific data type."""
        if ttl <= 0:
            raise ValueError("TTL must be positive")
        self._ttls[data_type] = ttl

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_entries = len(self._cache)
            now = datetime.now()
            expired = sum(1 for v in self._cache.values() if now > v.expiry)
            return {
                'total_entries': total_entries,
                'expired_entries': expired,
                'active_entries': total_entries - expired,
                'ttls': dict(self._ttls)
            }
