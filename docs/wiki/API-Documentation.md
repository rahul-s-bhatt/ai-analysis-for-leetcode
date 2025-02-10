# API Documentation

This documentation covers both the LeetCode API integration and our Analytics API endpoints.

## LeetCode API Integration

⚠️ **Disclaimer**: The LeetCode API integration is based on reverse-engineered endpoints and may change without notice.

### Authentication

| Type | Access Level | Requirements |
|------|--------------|--------------|
| Public | Basic user data | None |
| Private | Full submission access | Requires Session Cookie |

### Rate Limits

- **Public Endpoints**: ~200 requests/hour
- **Authenticated Endpoints**: ~500 requests/hour

#### Best Practices
- Cache responses for 1 hour
- Use exponential backoff for retries

### Core GraphQL Queries

#### 1. User Profile Query
```graphql
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    profile {
      ranking
      reputation
      userAvatar
    }
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
```

#### 2. Submission History Query
```graphql
query recentSubmissionList($username: String! $limit: Int) {
  recentSubmissionList(username: $username, limit: $limit) {
    title
    titleSlug
    timestamp
    statusDisplay
    lang
  }
}
```

## Analytics API

Our Analytics API provides AI-powered insights into LeetCode problem-solving patterns.

### Base URL
```
http://localhost:5000/api/v1
```

### Endpoints

#### 1. Pattern Analysis
```http
GET /analytics/patterns
```
Analyzes problem-solving patterns across submissions.

**Parameters:**
- `username` (required): LeetCode username
- `timeframe` (optional): Analysis period (default: "all")

#### 2. Skill Analysis
```http
GET /analytics/skills
```
Evaluates technical skills based on solved problems.

**Parameters:**
- `username` (required): LeetCode username
- `categories` (optional): Specific skill categories to analyze

#### 3. Learning Path
```http
GET /analytics/learning-path
```
Generates personalized learning recommendations.

**Parameters:**
- `username` (required): LeetCode username
- `target_area` (optional): Specific area for improvement

### Error Handling

All endpoints follow standard HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - User/resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

### Example Response

```json
{
  "status": "success",
  "data": {
    "patterns": {
      "strengths": ["Dynamic Programming", "Tree Traversal"],
      "areas_for_improvement": ["Graph Algorithms"],
      "completion_rates": {
        "easy": 75,
        "medium": 45,
        "hard": 20
      }
    },
    "recommendations": [
      {
        "topic": "Graph Theory",
        "problems": ["Course Schedule", "Network Delay Time"],
        "confidence_score": 0.85
      }
    ]
  }
}
```

### SDKs and Client Libraries

- Python Client: `leetcode_analyzer_client`
- JavaScript Client: `leetcode-analyzer-js`

### Rate Limiting

- Anonymous: 30 requests per minute
- Authenticated: 100 requests per minute

For higher limits, please contact the maintainers.

### Versioning

API versioning is included in the URL path (e.g., `/api/v1/`). Breaking changes will result in a new version number.