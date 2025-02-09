# API Documentation

## GET `get_user_profile` for a Particular User

### `allQuestionsCount`
1. Helps you understand the count of problems categorized by difficulty on the LeetCode website.

### `contributions`
1. Overall contribution points on the LeetCode website.

### `profile`
1. Retrieves user details from the profile page.

### `submitStats`
1. Helps in understanding the number of accepted and total submissions of any problem along with its difficulty.

### Difficulty Levels:
- **EASY**
- **MEDIUM**
- **HARD**

### `recentSubmissionList`
1. Provides details on recent submissions, including time and space complexity and the submission page URL.

### GraphQL Query:
```graphql
query getUserProfile($username: String!) {
    allQuestionsCount {
        difficulty
        count
    }
    matchedUser(username: $username) {
        contributions {
            points
        }
        profile {
            realName
            userAvatar
            birthday
            ranking
            reputation
            websites
            countryName
            company
            school
            skillTags
            aboutMe
            starRating
        }
        badges {
            id
            displayName
            icon
            creationDate
        }
        upcomingBadges {
            name
            icon
        }
        activeBadge {
            id
            displayName
            icon
            creationDate
        }
        submissionCalendar
        submitStats {
            acSubmissionNum {
                difficulty
                count
                submissions
            }
            totalSubmissionNum {
                difficulty
                count
                submissions
            }
        }
    }
    recentSubmissionList(username: $username) {
        title
        titleSlug
        timestamp
        statusDisplay
        lang
        memory
        runtime
        url
    }
    matchedUserStats: matchedUser(username: $username) {
        submitStats: submitStatsGlobal {
            acSubmissionNum {
                difficulty
                count
                submissions
                __typename
            }
            totalSubmissionNum {
                difficulty
                count
                submissions
                __typename
            }
            __typename
        }
    }
}
```

---

## GET `get_user_difficulty_stats` for a Particular User

### `submitStats`
1. Helps in understanding the number of accepted and total submissions of any problem along with its difficulty.

### `problemsSolvedBeatsStats`
1. Shows the percentage of users the user has outperformed for a given difficulty.

### Difficulty Levels:
- **EASY**
- **MEDIUM**
- **HARD**

### GraphQL Query:
```graphql
query userSessionProgress($username: String!) {
    allQuestionsCount {
        difficulty
        count
    }
    matchedUser(username: $username) {
        submitStats {
            acSubmissionNum {
                difficulty
                count
                submissions
            }
            totalSubmissionNum {
                difficulty
                count
                submissions
            }
        }
        problemsSolvedBeatsStats {
            difficulty
            percentage
        }
    }
}
```

---

## GET `get_user_skill_stats`

### `tagProblemCounts`
1. Provides the number of problems solved for each tag, categorized into advanced, intermediate, or fundamental topics.

### GraphQL Query:
```graphql
query skillStats($username: String!) {
    matchedUser(username: $username) {
        tagProblemCounts {
            advanced {
                tagName
                tagSlug
                problemsSolved
            }
            intermediate {
                tagName
                tagSlug
                problemsSolved
            }
            fundamental {
                tagName
                tagSlug
                problemsSolved
            }
        }
    }
}
```

---

## GET `get_user_user_profile_user_question_progress_V2`

### `userProfileUserQuestionProgressV2`
1. Provides counts of accepted, failed, and untouched questions by difficulty.
2. `userSessionBeatsPercentage`: Displays the percentage of users the user has beaten for each difficulty level.

### Difficulty Levels:
- **EASY**
- **MEDIUM**
- **HARD**

### GraphQL Query:
```graphql
query userProfileUserQuestionProgressV2($userSlug: String!) {
    userProfileUserQuestionProgressV2(userSlug: $userSlug) {
        numAcceptedQuestions {
            count
            difficulty
        }
        numFailedQuestions {
            count
            difficulty
        }
        numUntouchedQuestions {
            count
            difficulty
        }
        userSessionBeatsPercentage {
            difficulty
            percentage
        }
    }
}
```

---

## GET `get_user_contest_ranking`

### `userContestRanking`
1. Provides contest participation statistics, including rating, global ranking, total participants, and top percentage.

### `userContestRankingHistory`
1. Displays history of contests attended, ranking, problems solved, total problems, finish time in seconds, contest title, and start time.

### GraphQL Query:
```graphql
query getUserContestRanking($username: String!) {
    userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
        badge {
            name
        }
    }
    userContestRankingHistory(username: $username) {
        attended
        rating
        ranking
        trendDirection
        problemsSolved
        totalProblems
        finishTimeInSeconds
        contest {
            title
            startTime
        }
    }
}
```

