# LeetCode API Optimization Plan

## Current Architecture Issues
- Multiple separate API calls for different data types (profile, contests, submissions)
- Each analyzer making independent requests
- No data caching mechanism
- Repeated requests for the same data
- Rate limiting causing delays in user experience

## Proposed Improvements

### 1. GraphQL Query Batching
```graphql
# Example of a batched query
query UserCompleteData($username: String!) {
  profile: matchedUser(username: $username) {
    # Profile data
  }
  contestData: userContestRanking(username: $username) {
    # Contest data
  }
  submissions: recentSubmissionList(username: $username) {
    # Submission data
  }
  skillStats: matchedUser(username: $username) {
    # Skill stats
  }
}
```
- Combine multiple queries into a single request
- Reduces network overhead
- Minimizes rate limit impact

### 2. Redis Caching Layer
```python
class CacheableGQLQuery:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.cache_ttl = {
            'profile': 3600,  # 1 hour
            'contests': 1800, # 30 minutes
            'submissions': 300  # 5 minutes
        }

    async def get_cached_or_fetch(self, query_type, username):
        cache_key = f"{query_type}:{username}"
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        
        data = await self._fetch_from_api(query_type, username)
        await self.redis.setex(cache_key, self.cache_ttl[query_type], json.dumps(data))
        return data
```
- Cache frequently accessed data
- Different TTLs for different data types
- Reduces API calls for repeated requests

### 3. Background Data Synchronization
```python
class DataSyncService:
    def __init__(self):
        self.sync_intervals = {
            'profile': 3600,      # Sync every hour
            'contests': 1800,     # Sync every 30 minutes
            'submissions': 300     # Sync every 5 minutes
        }

    async def start_sync(self, username):
        """Start background sync tasks for a user"""
        for data_type, interval in self.sync_intervals.items():
            asyncio.create_task(self._sync_loop(username, data_type, interval))

    async def _sync_loop(self, username, data_type, interval):
        while True:
            await self._sync_data(username, data_type)
            await asyncio.sleep(interval)
```
- Proactively fetch and cache data
- Different sync intervals for different data types
- Ensures data freshness without impacting user requests

### 4. Request Queue Management
```python
class APIRequestQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.workers = 3

    async def start_workers(self):
        """Start worker tasks to process API requests"""
        workers = [asyncio.create_task(self._worker()) 
                  for _ in range(self.workers)]
        return workers

    async def _worker(self):
        while True:
            request = await self.queue.get()
            try:
                await self._process_request(request)
            finally:
                self.queue.task_done()
```
- Queue and prioritize requests
- Multiple workers for parallel processing
- Better rate limit management

### 5. Data Model Optimization
```python
class UserDataManager:
    def __init__(self, redis_client):
        self.cache = redis_client
        self.gql_client = CacheableGQLQuery(redis_client)

    async def get_user_data(self, username):
        """Get complete user data with optimized fetching"""
        cached_data = await self.get_cached_data(username)
        if self._needs_refresh(cached_data):
            fresh_data = await self._fetch_missing_data(username, cached_data)
            await self.update_cache(username, fresh_data)
            return fresh_data
        return cached_data
```
- Single entry point for data access
- Smart data refresh logic
- Efficient cache updates

## Implementation Phases

1. **Phase 1: Query Optimization**
   - Implement GraphQL query batching
   - Optimize query structures
   - Reduce redundant data fetching

2. **Phase 2: Caching Layer**
   - Set up Redis caching
   - Implement cache management
   - Configure TTLs

3. **Phase 3: Background Sync**
   - Implement sync service
   - Configure sync intervals
   - Add monitoring

4. **Phase 4: Request Management**
   - Implement request queue
   - Add worker pool
   - Add request prioritization

5. **Phase 5: Data Model Updates**
   - Update data access patterns
   - Implement optimized data manager
   - Update analyzers to use new system

## Benefits

1. **Performance**
   - Reduced API calls
   - Faster response times
   - Better resource utilization

2. **Reliability**
   - Reduced rate limit issues
   - Better error handling
   - Improved data consistency

3. **Scalability**
   - Better handling of concurrent users
   - Efficient resource usage
   - Easy to add new data types

4. **User Experience**
   - Faster page loads
   - More consistent response times
   - Reduced errors

## Monitoring and Maintenance

1. **Metrics to Track**
   - Cache hit rates
   - API call frequency
   - Response times
   - Error rates

2. **Maintenance Tasks**
   - Regular cache cleanup
   - Sync interval adjustments
   - Query optimization reviews

This plan provides a comprehensive approach to optimizing API interactions while maintaining data freshness and reliability.