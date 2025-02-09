# Problem List Fetching Optimization

## Current Issues

1. Multiple API Calls:
   - Separate calls for each category
   - Separate calls for each difficulty level
   - Up to 10+ API calls for a complete fetch

2. Inefficient Data Retrieval:
   - No caching of problem lists
   - Problem data refreshed too frequently
   - Redundant data fetching

## Proposed Solution

### 1. Batched Query Design
```graphql
query AllProblemsQuery($filters: QuestionListFilterInput) {
    problemsetQuestionList: questionList(
        # Get maximum allowed per query
        limit: 100
        filters: $filters
    ) {
        total: totalNum
        questions: data {
            acRate
            difficulty
            questionFrontendId
            title
            titleSlug
            topicTags {
                name
                id
                slug
            }
            status
        }
        hasMore
    }
}
```

### 2. Implementation Strategy

```python
class ProblemListManager:
    def __init__(self, cache):
        self.cache = cache
        self.cache_key = "leetcode_problems_list"
        self.cache_ttl = 3600 * 24  # Cache for 24 hours

    async def get_all_problems(self):
        """Get complete problems list with caching."""
        cached = self.cache.get(self.cache_key)
        if cached:
            return cached

        problems = await self._fetch_all_problems()
        self.cache.set(self.cache_key, problems, "problems")
        return problems

    async def _fetch_all_problems(self):
        """Single efficient fetch for all problems."""
        all_problems = []
        cursor = 0
        
        while True:
            batch = await self._fetch_problems_batch(cursor)
            if not batch or not batch['questions']:
                break
                
            all_problems.extend(batch['questions'])
            cursor += len(batch['questions'])
            
            if not batch.get('hasMore'):
                break
                
        return all_problems
```

### 3. Caching Strategy

1. **Long-Term Caching**
   - Cache complete problem list for 24 hours
   - Problem data rarely changes
   - Heavy cache validation

2. **Cache Structure**
   ```python
   {
       'timestamp': datetime,
       'problems': {
           'all': [...],  # Complete list
           'by_difficulty': {
               'Easy': [...],
               'Medium': [...],
               'Hard': [...]
           },
           'by_category': {
               'algorithms': [...],
               'database': [...],
               # etc
           }
       }
   }
   ```

3. **Cache Updates**
   - Background refresh before expiry
   - Partial updates for changed problems
   - Keep old cache until new fetch completes

### 4. Implementation Steps

1. **Phase 1: Core Implementation**
   - Implement ProblemListManager class
   - Add caching integration
   - Create batched query method

2. **Phase 2: AnalyzerManager Integration**
   - Update _get_available_problems
   - Modify recommendation logic
   - Add error handling

3. **Phase 3: Optimization**
   - Add background refresh
   - Implement partial updates
   - Add monitoring

### 5. Benefits

1. **Performance**
   - Reduced API calls (10+ → 1-2)
   - Faster response times
   - Better resource utilization

2. **Reliability**
   - Less rate limiting risk
   - More consistent responses
   - Better error handling

3. **Maintainability**
   - Centralized problem data
   - Easier to modify filters
   - Better monitoring

### 6. Monitoring

1. **Metrics to Track**
   - Cache hit rate
   - Fetch time
   - Problem count
   - Error rate

2. **Health Checks**
   - Cache freshness
   - Data completeness
   - API response times

This optimization will significantly reduce API calls while improving data availability and system reliability.