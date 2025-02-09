import logging
import json

logger = logging.getLogger(__name__)

def format_solved_problems_data(data):
    try:
        logger.debug("Formatting solved problems data")
        stats = data["matchedUser"]["submitStats"]["acSubmissionNum"]
        total_questions = data.get("allQuestionsCount", [])
        
        return {
            "solvedProblems": stats[0]["count"],
            "easySolved": stats[1]["count"],
            "mediumSolved": stats[2]["count"],
            "hardSolved": stats[3]["count"],
            "totalQuestions": {
                item["difficulty"]: item["count"] 
                for item in total_questions
            }
        }
    except (KeyError, IndexError) as e:
        logger.error(f"Error formatting solved problems: {e}", exc_info=True)
        return {
            "solvedProblems": 0,
            "easySolved": 0,
            "mediumSolved": 0,
            "hardSolved": 0,
            "totalQuestions": {}
        }

def format_topic_tags_data(data):
    try:
        logger.debug("Formatting topic tags data")
        tag_counts = data["matchedUser"]["tagProblemCounts"]
        all_tags = {}
        
        for level in ["advanced", "intermediate", "fundamental"]:
            for tag in tag_counts[level]:
                all_tags[tag["tagName"]] = {
                    "solved": tag["problemsSolved"],
                    "total": 0,  # No total field available; using default 0
                    "level": level
                }
        return all_tags
    except KeyError as e:
        logger.error(f"Error formatting topic tags: {e}", exc_info=True)
        return {}

def format_recent_submissions(data):
    try:
        logger.debug("Formatting recent submissions data")
        # 'recentSubmissionList' is removed from query; return empty list
        return []
    except KeyError as e:
        logger.error(f"Error formatting submissions: {e}", exc_info=True)
        logger.debug(f"Data received: {data}")
        return []

def format_user_profile(data):
    try:
        logger.debug("Starting to format user profile")
        logger.debug(f"Input data structure: {json.dumps(data, indent=2)}")
        
        if not data:
            logger.error("No data provided")
            return None
            
        if "matchedUser" not in data:
            logger.error("No matchedUser in data")
            logger.debug(f"Available keys: {data.keys()}")
            return None
            
        profile = data["matchedUser"]
        contest_data = data.get("userContestRanking", {})
        
        # Validate required nested structures
        if "submitStats" not in profile:
            logger.error("No submitStats in profile")
            return None
            
        if "tagProblemCounts" not in profile:
            logger.error("No tagProblemCounts in profile")
            return None

        formatted = {
            "username": profile.get("username", ""),
            "profile": {
                "realName": profile.get("profile", {}).get("realName", ""),
                "ranking": profile.get("profile", {}).get("ranking", 0),
                "reputation": profile.get("profile", {}).get("reputation", 0),
                "company": profile.get("profile", {}).get("company", ""),
                "school": profile.get("profile", {}).get("school", ""),
                "starRating": profile.get("profile", {}).get("starRating", 0),
            },
            "stats": format_solved_problems_data(data),
            "topics": format_topic_tags_data(data),
            "contest": {
                "rating": contest_data.get("rating", 0),
                "attended": contest_data.get("attendedContestsCount", 0),
                "ranking": contest_data.get("globalRanking", 0),
                "topPercentage": contest_data.get("topPercentage", 100)
            },
            "calendar": {
                "streak": profile.get("userCalendar", {}).get("streak", 0),
                "totalActiveDays": profile.get("userCalendar", {}).get("totalActiveDays", 0),
            },
            "recentSubmissions": format_recent_submissions(data)
        }
        
        logger.debug(f"Formatted profile: {json.dumps(formatted, indent=2)}")
        return formatted
        
    except Exception as e:
        logger.error(f"Error formatting user profile: {e}", exc_info=True)
        logger.debug(f"Data that caused error: {json.dumps(data, indent=2)}")
        return None
