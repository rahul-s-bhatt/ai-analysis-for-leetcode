[FEATURE] Implement In-Memory Caching System

## Feature Description
Design and implement an efficient in-memory caching system to improve response times and reduce API calls to LeetCode.

## Problem Statement
The application currently fetches data from LeetCode's API for every request, which is inefficient and can hit rate limits. We need a caching solution that doesn't require additional infrastructure while maintaining data freshness.

## Proposed Solution
Implement an in-memory caching system using Python's built-in tools:
1. Use `functools.lru_cache` for function-level caching
2. Implement a TTL (Time-To-Live) based cache manager
3. Add memory usage monitoring and optimization

## Technical Details
Example implementation structure:
```python
from functools import lru_cache
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class CacheManager:
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, tuple[Any, datetime]] = {}
        self.max_size = max_size

    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.now() < expiry:
                return value
            del self.cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 300):
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        expiry = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = (value, expiry)

    def _evict_oldest(self):
        if not self.cache:
            return
        oldest_key = min(self.cache.items(), key=lambda x: x[1][1])[0]
        del self.cache[oldest_key]
```

### Required Skills
- [x] Python
- [x] Data Structures
- [x] Memory Management
- [ ] Other: Performance Optimization

### Difficulty Level
- [ ] Beginner Friendly
- [x] Intermediate
- [ ] Advanced

### Estimated Time
- [ ] Small (< 2 hours)
- [x] Medium (2-4 hours)
- [ ] Large (4-8 hours)
- [ ] Extra Large (> 8 hours)

## Implementation Checklist
- [ ] Design cache data structure
- [ ] Implement basic caching functionality
- [ ] Add TTL support
- [ ] Add memory monitoring
- [ ] Implement cache eviction strategy
- [ ] Write unit tests
- [ ] Add usage documentation
- [ ] Benchmark performance

## Additional Context
This implementation should focus on being lightweight and efficient, using only Python's standard library to avoid additional dependencies.

Labels: enhancement, priority: high, type: performance, good first issue
