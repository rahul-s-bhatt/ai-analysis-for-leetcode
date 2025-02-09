<?xml version="1.0" encoding="UTF-8"?>

## LeetCode Unofficial API Documentation

### Last Updated: {Current Date}  

---

### Table of Contents

- [Authentication](#authentication)
- [Rate Limits](#rate-limits)
- [Endpoints](#endpoints)
  - [User Profile](https://chatopenia.com/#user-profile)
  - [Submission History](https://chatopenia.com/#submission-history)
  - [Contest Ranking](https://chatopenia.com/#contest-ranking)
---

### Authentication

Type | Access Level | Requirements
-------|--------------|----------

- Public | Basic user data | None  
- Private | Full submission access | Requires Session Cookie

<br>

### Rate Limits

- **Public Endpoints**: ~200 requests/hour
- **Authenticated Endpoints**: ~500 requests/hour

- Recommendations:
  - Cache responses for 1 hour
  - Use exponential backoff for retries

<br>

### Endpoints

#### User Profile

**Operation Name**: `detUserProfile`

\Language: GraphQL\\
\Query:

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
    recentSubmissionList(username: $username) {
      title
      statusDisplay
      timestamp
      lang
    }
  }
}
```

\Public Fields\:

- Ranking, reputation, userAvatar  
- Problem statistics `{difficulty, count}`
- Last 20 submissions metadata

<br>

#### Submission History

**Operation Name**: `recentSubmissionList`

\Query:

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

<br>

#### Contest Ranking

**Operation Name**: `userContestRanking`

\Query:

```graphql
query userContestRanking($username: String!) {
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
  }
}
```

<br>

#### Skill Stats

**Operation Name**: `skillStats`

\Query:

```graphql
query skillStats($username: String!) {
  matchedUser(username: $username) {
    tagProblemCounts {
      advanced {
        tagName
        problemsSolved
      }
      intermediate {
        tagName
        problemsSolved
      }
    }
  }
}
```

<br>

### Response Structure

```json
{
  "data": {
    "matchedUser": {
      "profile": {
        "ranking": 188899,
        "reputation": 36
      },
      "submitStats": {
        "acSubmissionNum": [
          { "difficulty": "All", "count": 412 }
        ]
      },
      "recentSubmissionList": [
        { "title": "Two Sum", "statusDisplay": "Accepted" }
      ]
    }
  }
}
```

<br>

### Common Errors

Error Code | Message | Solution
-------|----------|----------

- **400**: "Code field unavailable" | Remove `code` in query
- __404__: "User not found" | Check username
- __429__: Rate limit | Wait 1 minute

<br>

### Limitations
1. __No Code Access__: Public API does not provide:
   `code`: Submission content
   `redirectUrl`: Submission details 
2. __Data Latency__: Submissions may take up to 5 mins to appear in API

<br>

### Sample Request Flow

```mmermaid
sequenceDiagram
    Client->>LeetCode API: GET /graphql (User Profile)
    LeetCode API-->>Client: 200 OK (Profile Data)
    Client->>LeetCode API: GET /graphql (Submission History)
    LeetCode API-->>Client: 200 OK (Submissions Metadata)
```

<br>

### Compatibility

- **LeetCode API Version**: 2023.08.01
- __Project Version__: leetcode-analyzer v1.0

<br>

---

Documentation generated using AI assistance. Revise as needed for your project.