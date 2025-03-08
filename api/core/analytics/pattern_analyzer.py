from typing import Dict, Any, List
from datetime import datetime
import json

class PatternAnalyzer:
    def __init__(self, user_data: Dict[str, Any]):
        self.user_data = user_data
        self.matched_user = user_data.get("matchedUser", {})
        self.submit_stats = self.matched_user.get("submitStats", {})
        self.tag_counts = self.matched_user.get("tagProblemCounts", {})
        self.calendar = self.matched_user.get("userCalendar", {})

    def analyze_coding_personality(self) -> Dict[str, Any]:
        """Analyze user's coding style and preferences"""
        return {
            "problem_solving_style": self._determine_solving_style(),
            "preferred_topics": self._analyze_preferred_topics(),
            "consistency_metrics": self._analyze_consistency()
        }

    def _determine_solving_style(self) -> Dict[str, Any]:
        """Determine user's problem-solving approach"""
        submit_stats = self.matched_user.get("submitStats", {})
        total_submissions = submit_stats.get("totalSubmissionNum", [])
        ac_submissions = submit_stats.get("acSubmissionNum", [])

        # Calculate success rate
        if total_submissions and ac_submissions:
            success_rate = sum(sub["count"] for sub in ac_submissions) / \
                          sum(sub["count"] for sub in total_submissions) * 100
        else:
            success_rate = 0

        # Determine style based on success rate and submission patterns
        style = "Methodical" if success_rate > 70 else \
                "Experimental" if success_rate < 40 else "Balanced"

        return {
            "primary_style": style,
            "success_rate": round(success_rate, 2),
            "approach_description": self._get_style_description(style)
        }

    def _analyze_preferred_topics(self) -> Dict[str, List[str]]:
        """Analyze user's topic preferences"""
        topic_preferences: Dict[str, List[str]] = {"strong": [], "moderate": [], "weak": []}
        for level in ["advanced", "intermediate", "fundamental"]:
            topics = self.tag_counts.get(level, [])
            for topic in topics:
                solved = topic.get("problemsSolved", 0)
                if solved > 10:
                    topic_preferences["strong"].append(topic["tagName"])
                elif solved > 5:
                    topic_preferences["moderate"].append(topic["tagName"])
                else:
                    topic_preferences["weak"].append(topic["tagName"])

        return topic_preferences

    def _analyze_consistency(self) -> Dict[str, Any]:
        """Analyze user's solving consistency"""
        calendar_data = self.calendar
        streak = calendar_data.get("streak", 0)
        total_active_days = calendar_data.get("totalActiveDays", 0)
        
        # Convert submission calendar string to dict if it exists
        submission_calendar = {}
        if calendar_data.get("submissionCalendar"):
            try:
                submission_calendar = json.loads(calendar_data["submissionCalendar"])
            except json.JSONDecodeError:
                submission_calendar = {}

        # Calculate average submissions per active day
        avg_submissions = len(submission_calendar) / total_active_days if total_active_days > 0 else 0

        return {
            "current_streak": streak,
            "total_active_days": total_active_days,
            "avg_submissions_per_day": round(avg_submissions, 2),
            "consistency_level": self._get_consistency_level(streak, total_active_days)
        }

    def _get_style_description(self, style: str) -> str:
        """Get description for coding style"""
        descriptions = {
            "Methodical": "You take a careful, systematic approach to problem-solving, "
                        "often achieving high success rates on first attempts.",
            "Experimental": "You learn through experimentation, trying different approaches "
                          "until finding the optimal solution.",
            "Balanced": "You maintain a good balance between careful planning and "
                       "practical experimentation."
        }
        return descriptions.get(style, "Your coding style is evolving")

    def _get_consistency_level(self, streak: int, total_days: int) -> str:
        """Determine consistency level"""
        if streak >= 30:
            return "Highly Consistent"
        elif streak >= 14:
            return "Moderately Consistent"
        elif streak >= 7:
            return "Building Consistency"
        else:
            return "Getting Started"

    def get_complete_analysis(self) -> Dict[str, Any]:
        """Get complete pattern analysis"""
        return {
            "coding_personality": self.analyze_coding_personality(),
            "skill_analysis": {
                "preferred_topics": self._analyze_preferred_topics(),
                "consistency": self._analyze_consistency()
            },
            "development_suggestions": self._generate_suggestions()
        }

    def _generate_suggestions(self) -> List[Dict[str, str]]:
        """Generate personalized suggestions based on patterns"""
        suggestions = []
        consistency = self._analyze_consistency()
        
        # Consistency-based suggestions
        if consistency["current_streak"] < 7:
            suggestions.append({
                "type": "consistency",
                "message": "Try to solve at least one problem daily to build momentum",
                "priority": "high"
            })
        
        # Topic-based suggestions
        preferred_topics = self._analyze_preferred_topics()
        if preferred_topics["weak"]:
            suggestions.append({
                "type": "topic_focus",
                "message": f"Consider focusing on {', '.join(preferred_topics['weak'][:3])} "
                         "to broaden your skill set",
                "priority": "medium"
            })

        return suggestions
