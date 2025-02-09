# LeetCode API In-Memory Optimization Plan

## Architecture Overview

### 1. In-Memory Cache Implementation
```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Lock
from typing import Dict, Any, Optional

@dataclass
class CacheEntry:
    data: Any
    expiry: datetime

class InMemoryCache:
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = Lock()
        self._ttls = {
            'profile': 3600,    # 1 hour
            'contests': 1800,   # 30 minutes
            'submissions': 300   # 5 minutes
        }

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            entry = self._cache[key]
            if datetime.now() > entry.expiry:
                del self._cache[key]
                return None
            return entry.data

    def set(self, key: str, value: Any, ttl: int = 3600):
        with self._lock:
            self._cache[key] = CacheEntry(
                data=value,
                expiry=datetime.now() + timedelta(seconds=ttl)
            )

    def cleanup(self):
        """Remove expired entries"""
        with self._lock:
            now = datetime.now()
            expired = [k for k, v in self._cache.items() if now > v.expiry]
            for k in expired:
                del self._cache[k]
```

### 2. Batched GraphQL Query Client
```python
class BatchedGQLQuery:
    def __init__(self):
        self.cache = InMemoryCache()

    async def get_user_complete_data(self, username: str) -> Dict[str, Any]:
        """Fetch all user data in a single query"""
        cache_key = f"complete_data:{username}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        query = """
        query UserCompleteData($username: String!) {
            profile: matchedUser(username: $username) {
                profile {
                    # Profile fields
                }
                submitStats {
                    # Submission stats
                }
            }
            contestData: userContestRanking(username: $username) {
                # Contest fields
            }
            recentSubmissions: recentSubmissionList(username: $username) {
                # Submission fields
            }
            skillStats: matchedUser(username: $username) {
                tagProblemCounts {
                    # Skill stats fields
                }
            }
        }
        """
        
        response = await self._execute_query(query, {"username": username})
        self.cache.set(cache_key, response, ttl=300)  # Cache for 5 minutes
        return response
```

### 3. Background Data Prefetcher
```python
class DataPrefetcher:
    def __init__(self, gql_client: BatchedGQLQuery):
        self.client = gql_client
        self._prefetch_tasks = {}

    async def start_prefetch(self, username: str):
        """Start background prefetch for a user"""
        if username in self._prefetch_tasks:
            return
        
        self._prefetch_tasks[username] = asyncio.create_task(
            self._prefetch_loop(username)
        )

    async def _prefetch_loop(self, username: str):
        """Periodically prefetch user data"""
        try:
            while True:
                await self.client.get_user_complete_data(username)
                await asyncio.sleep(240)  # Refresh every 4 minutes
        except asyncio.CancelledError:
            del self._prefetch_tasks[username]
```

## Implementation Phases

### Phase 1: Core Cache and Query Batching
1. Implement InMemoryCache class
2. Create BatchedGQLQuery with the combined query
3. Update GQLQuery class to use the new batched system
4. Add basic error handling and retries

### Phase 2: Integration
1. Update AnalyzerManager to use batched queries
2. Modify analyzers to work with batched data
3. Add data transformation layer if needed
4. Implement proper error handling

### Phase 3: Optimization
1. Add background prefetching
2. Implement cache cleanup
3. Add monitoring/metrics
4. Optimize query fields

## Benefits

1. **Reduced API Calls**
   - Single query instead of multiple
   - In-memory caching reduces repeat calls
   - Background prefetching for active users

2. **Better Performance**
   - Faster response times
   - No Redis dependency
   - Simple, lightweight implementation

3. **Improved Reliability**
   - Less chance of rate limiting
   - Built-in error handling
   - Automatic cache cleanup

## Usage Example

```python
# Initialize components
cache = InMemoryCache()
gql_client = BatchedGQLQuery()
prefetcher = DataPrefetcher(gql_client)

# In your route handler
async def handle_profile_request(username: str):
    # Start prefetching for this user
    await prefetcher.start_prefetch(username)
    
    # Get data (will use cache if available)
    data = await gql_client.get_user_complete_data(username)
    
    # Process and return
    return process_user_data(data)
```

## Monitoring

1. **Cache Metrics**
   - Hit/miss rates
   - Entry counts
   - Expiration rates

2. **API Metrics**
   - Query response times
   - Error rates
   - Rate limit status

This implementation provides a lightweight but effective solution for optimizing API interactions without external dependencies.