from flask import Response
import aiohttp
import asyncio
import logging
import json
from time import time
from asyncio import sleep
from typing import Optional, Dict, Any, List
from core.utils.cache import InMemoryCache

logger = logging.getLogger(__name__)

# Rate limiting constants
RATE_LIMIT_REQUESTS = 20  # Number of requests allowed
RATE_LIMIT_PERIOD = 30    # Time period in seconds
DELAY_BETWEEN_REQUESTS = 0.2  # Delay between requests in seconds

# Batched query for fetching all user data at once
BATCH_QUERY = """
query UserCompleteData($username: String!) {
    matchedUser(username: $username) {
        username
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
        submitStats: submitStatsGlobal {
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
        contributions {
            points
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
        userCalendar {
            activeYears
            streak
            totalActiveDays
            dccBadges {
                timestamp
                badge {
                    name
                    icon
                }
            }
            submissionCalendar
        }
        problemsSolvedBeatsStats {
            difficulty
            percentage
        }
    }
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
    allQuestionsCount {
        difficulty
        count
    }
}
"""


class GQLQuery:
    def __init__(self, session_cookie=None):
        self.session_cookie = session_cookie
        self._request_timestamps = []  # Track request timestamps for rate limiting
        self._session: Optional[aiohttp.ClientSession] = None
        self._cache = InMemoryCache()

    async def get_user_complete_data(self, username: str) -> Dict[str, Any]:
        """Fetch all user data in a single batched query with caching."""
        cache_key = f"user_complete_data:{username}"
        cached_data = self._cache.get(cache_key)
        if cached_data:
            logger.debug(f"Cache hit for {username}'s complete data")
            return cached_data

        logger.info(f"Fetching complete data for user: {username}")
        query = {
            "query": BATCH_QUERY,
            "variables": {"username": username}
        }

        response = await self._call_api(query, username)
        logger.info(f"Raw API response: {json.dumps(response, indent=2)}")
        
        if response and 'data' in response:
            logger.info(f"Received valid data for user: {username}")
            logger.debug(f"Data structure: {json.dumps(response['data'], indent=2)}")
            self._cache.set(cache_key, response['data'], 'profile')
            return response['data']

        logger.error(f"Failed to fetch complete data for {username}")
        logger.error(f"Response structure: {json.dumps(response, indent=2) if response else 'No response'}")
        return {}

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def login_to_leetcode(self):
        # Open a new tab with the LeetCode login page
        import webbrowser
        webbrowser.open('https://leetcode.com/accounts/login/')

    async def get_leetcode_session_cookie(self) -> Optional[str]:
        try:
            if not self._session:
                self._session = aiohttp.ClientSession()
            async with self._session.get('https://leetcode.com') as response:
                cookies = response.cookies
                return cookies.get('leetcode_session')
        except Exception as e:
            logger.error(f"Failed to get session cookie: {str(e)}")
            return None

    async def _enforce_rate_limit(self):
        """Enforce rate limiting to prevent IP bans"""
        current_time = time()

        # Remove timestamps older than the rate limit period
        self._request_timestamps = [
            ts for ts in self._request_timestamps
            if current_time - ts < RATE_LIMIT_PERIOD
        ]

        # If we've hit the rate limit, wait until we can make another request
        if len(self._request_timestamps) >= RATE_LIMIT_REQUESTS:
            wait_time = RATE_LIMIT_PERIOD - \
                (current_time - self._request_timestamps[0])
            if wait_time > 0:
                logger.info(
                    f"Rate limit reached, waiting {wait_time:.2f} seconds")
                await sleep(wait_time)

        # Add small delay between requests
        await sleep(DELAY_BETWEEN_REQUESTS)

        # Add current request timestamp
        self._request_timestamps.append(current_time)

    async def _call_api(self, graphql_query: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Make an async GraphQL API call with rate limiting"""
        try:
            async with aiohttp.ClientSession() as session:
                if not self.session_cookie:
                    self.session_cookie = await self.get_leetcode_session_cookie()

                # Enforce rate limiting
                await self._enforce_rate_limit()

                start_time = time()
                logger.info(f"Making GraphQL request for user: {username}")
                logger.debug(f"Query: {json.dumps(graphql_query, indent=2)}")

                headers = {
                    "Content-Type": "application/json",
                    "Referer": f"https://leetcode.com/{username}/",
                    "Origin": "https://leetcode.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Cookie": f"LEETCODE_SESSION={self.session_cookie}",
                    "Accept": "*/*",
                    "Access-Control-Allow-Origin": "*"
                }

                async with session.post(
                    "https://leetcode.com/graphql",
                    json=graphql_query,
                    headers=headers
                ) as response:
                    elapsed_time = time() - start_time
                    logger.info(
                        f"Request completed in {elapsed_time:.2f}s with status: {response.status}")

                    response_json = await response.json()

                    # Log response status and headers
                    logger.info(f"Response status: {response.status}")
                    logger.info(f"Response headers: {dict(response.headers)}")
                    
                    if response.ok:
                        if not response_json:
                            logger.error("Empty JSON response received")
                            return {}
                            
                        logger.debug(f"Response data: {json.dumps(response_json, indent=2)}")
                        if 'errors' in response_json:
                            logger.error(f"GraphQL errors: {json.dumps(response_json['errors'], indent=2)}")
                        return response_json
                    else:
                        logger.error(f"Request failed with status {response.status}")
                        logger.error(f"Error response: {json.dumps(response_json, indent=2)}")
                        return {}
        except Exception as e:
            logger.error(f"API call failed: {str(e)}", exc_info=True)
            raise

    async def get_user_contest_ranking(self, username: str) -> Dict[str, Any]:
        get_user_contest_ranking_json = {
            "query": """
                    query getUserContestRanking ($username: String!) {
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
                """,
            "variables": {"username": username}
        }
        return await self._call_api(get_user_contest_ranking_json, username)

    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        get_user_profile_json = {
            "query": """
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
                """,
            "variables": {"username": username},
            "operationName": "getUserProfile"
        }
        return await self._call_api(get_user_profile_json, username)

    async def get_user_skill_stats(self, username: str) -> Dict[str, Any]:
        get_user_skill_stats_json = {
            "query": """
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
                    """,
            "variables": {"username": username}
        }
        return await self._call_api(get_user_skill_stats_json, username)

    async def get_user_profile_calendar(self, username: str, year: int) -> Dict[str, Any]:
        get_user_profile_calendar_json = {
            "query": """
                        query UserProfileCalendar($username: String!, $year: Int!) {
                            matchedUser(username: $username) {
                            userCalendar(year: $year) {
                                activeYears
                                streak
                                totalActiveDays
                                dccBadges {
                                timestamp
                                badge {
                                    name
                                    icon
                                }
                                }
                                submissionCalendar
                            }
                            }
                        }
                    """,
            "variables": {"username": username, "year": year},
            "operationName": "getUserProfile"
        }
        return await self._call_api(get_user_profile_calendar_json, username)

    async def get_user_user_profile_user_question_progress_V2(self, userSlug: str) -> Dict[str, Any]:
        get_user_user_profile_user_question_progress_V2_json = {
            "query": """
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
                    """,
            "variables": {"userSlug": userSlug},
            "operationName": "getUserProfile"
        }
        return await self._call_api(get_user_user_profile_user_question_progress_V2_json, userSlug)

    async def get_submission_details(self, username: str) -> Dict[str, Any]:
        submission_details_query = {
            "query": """
            query getSubmissionDetails($username: String!) {
                matchedUser(username: $username) {
                    # submissionCalendar
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
            """,
            "variables": {"username": username},
            "operationName": "getUserProfile"
        }
        return await self._call_api(submission_details_query, username)

    async def get_user_difficulty_stats(self, username: str) -> Dict[str, Any]:
        """
        Fetches the user's difficulty statistics from LeetCode.
        """
        user_difficulty_stats_query = {
            "query": """
                query userSessionProgress($username: String!) {
                    allQuestionsCount {
                        difficulty
                        count
                    }
                    matchedUser(username: $username) {
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
                        problemsSolvedBeatsStats {
                            difficulty
                            percentage
                        }
                    }
                }
            """,
            "variables": {"username": username},
            "operationName": "userSessionProgress"
        }
        return await self._call_api(user_difficulty_stats_query, username)

    async def get_problems_list(self, categorySlug, limit, filters) -> Dict[str, Any]:
        """
        Fetches the list of all available problems from LeetCode.

        Returns:
            Response: HTTP response containing the problems list
        """
        problems_list_query = {
            "query": """
                query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                        problemsetQuestionList: questionList(
                            categorySlug: $categorySlug
                            limit: $limit
                            skip: $skip
                            filters: $filters
                        ) {
                            total: totalNum
                            questions: data {
                                acRate
                                difficulty
                                freqBar
                                questionFrontendId
                                isFavor
                                isPaidOnly
                                status
                                title
                                titleSlug
                                topicTags {
                                    name
                                    id
                                    slug
                                }
                                hasSolution
                                hasVideoSolution
                            }
                        }
                }
            """,
            "variables": {
                "categorySlug": categorySlug,
                "limit": limit,
                "skip": 0,  # Skip is handled at pagination level
                "filters": {
                    "difficulty": filters.get("difficulty"),
                    "status": filters.get("status"),
                    "tags": filters.get("tags"),
                    "listId": filters.get("listId")
                }
            },
            "operationName": "problemsetQuestionList"
        }
        return await self._call_api(problems_list_query, "")
