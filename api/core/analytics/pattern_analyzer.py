from typing import Dict, Any, List
from datetime import datetime
import json
import logging
from ..ml.pattern_recognition_model import PatternRecognitionModel

logger = logging.getLogger(__name__)

class PatternAnalyzer:
    def __init__(self, user_data: Dict[str, Any]):
        self.user_data = user_data
        self.matched_user = user_data.get("matchedUser", {})
        self.submit_stats = self.matched_user.get("submitStats", {})
        self.tag_counts = self.matched_user.get("tagProblemCounts", {})
        self.calendar = self.matched_user.get("userCalendar", {})
        self.pattern_model = PatternRecognitionModel()

    def analyze_coding_personality(self) -> Dict[str, Any]:
        """Analyze user's coding style and preferences using ML model"""
        try:
            # Get recent submissions for pattern analysis
            submissions = self.matched_user.get("recentSubmissionList", [])
            
            # Use ML model to predict patterns
            logger.info("Using ML model for pattern recognition")
            pattern_prediction = self.pattern_model.predict_pattern(submissions)
            
            if pattern_prediction["confidence_scores"]["feature_reliability"] > 0.5:
                logger.info("Using ML model predictions")
                primary_style = pattern_prediction["primary_pattern"].title()
                pattern_distribution = pattern_prediction["pattern_distribution"]
            else:
                logger.info("Falling back to heuristic analysis due to low confidence")
                style_data = self._determine_solving_style_heuristic()
                primary_style = style_data["primary_style"]
                pattern_distribution = {primary_style.lower(): 100}
            
            return {
                "problem_solving_style": {
                    "primary_style": primary_style,
                    "pattern_distribution": pattern_distribution,
                    "confidence_metrics": pattern_prediction["confidence_scores"],
                    "approach_description": self._get_style_description(primary_style)
                },
                "preferred_topics": self._analyze_preferred_topics(),
                "consistency_metrics": self._analyze_consistency()
            }
        except Exception as e:
            logger.error(f"Error in pattern analysis: {str(e)}", exc_info=True)
            return self._fallback_analysis()

    def _determine_solving_style_heuristic(self) -> Dict[str, Any]:
        """Legacy heuristic-based solving style determination"""
        submit_stats = self.matched_user.get("submitStats", {})
        total_submissions = submit_stats.get("totalSubmissionNum", [])
        ac_submissions = submit_stats.get("acSubmissionNum", [])

        # Calculate success rate
        if total_submissions and ac_submissions:
            success_rate = sum(sub["count"] for sub in ac_submissions) / \
                          sum(sub["count"] for sub in total_submissions) * 100
        else:
            success_rate = 0

        # Determine style based on success rate
        style = "Methodical" if success_rate > 70 else \
                "Experimental" if success_rate < 40 else "Balanced"

        return {
            "primary_style": style,
            "success_rate": round(success_rate, 2)
        }

    def _fallback_analysis(self) -> Dict[str, Any]:
        """Provide fallback analysis when ML model fails"""
        return {
            "problem_solving_style": {
                "primary_style": "Balanced",
                "pattern_distribution": {"balanced": 100},
                "confidence_metrics": {
                    "feature_reliability": 0.0,
                    "pattern_strength": 0.0
                },
                "approach_description": self._get_style_description("Balanced")
            },
            "preferred_topics": {"strong": [], "moderate": [], "weak": []},
            "consistency_metrics": {
                "current_streak": 0,
                "total_active_days": 0,
                "avg_submissions_per_day": 0,
                "consistency_level": "Getting Started"
            }
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
        """Get detailed description for coding style based on ML analysis"""
        descriptions = {
            "Methodical": (
                "You excel at systematic problem decomposition and thorough analysis before implementation. "
                "Your high success rate on first attempts (particularly in data structure problems) "
                "indicates strong analytical skills and careful planning. Our ML model has identified "
                "patterns showing consistent use of optimal data structures and algorithms."
            ),
            "Experimental": (
                "Your iterative approach to problem-solving shows strong learning patterns. "
                "You quickly adapt solutions based on test results and effectively use "
                "debugging insights to optimize your code. The ML analysis reveals you excel "
                "at identifying edge cases through systematic testing."
            ),
            "Efficient": (
                "You consistently produce optimized solutions with excellent time and space complexity. "
                "Our ML model has detected patterns of advanced algorithm usage and effective "
                "optimization techniques in your solutions. You show particular strength in "
                "problems requiring performance optimization."
            ),
            "Structured": (
                "Your code demonstrates clear organization and strong design principles. "
                "ML analysis shows consistent patterns of modular code structure and "
                "effective problem decomposition. You excel at maintaining code clarity "
                "even while implementing complex algorithms."
            ),
            "Balanced": (
                "You effectively combine analytical planning with practical implementation. "
                "Our ML model has identified versatile problem-solving patterns in your approach. "
                "You adapt your strategy based on problem complexity, showing strong "
                "judgment in choosing between thorough analysis and rapid prototyping."
            )
        }
        return descriptions.get(style,
            "Your coding style is evolving as you solve more problems. Our ML model "
            "needs more data to provide detailed insights into your problem-solving patterns.")

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
        """Generate personalized suggestions using ML insights"""
        try:
            suggestions = []
            submissions = self.matched_user.get("recentSubmissionList", [])
            
            # Get ML-based pattern analysis
            pattern_prediction = self.pattern_model.predict_pattern(submissions)
            primary_style = pattern_prediction["primary_pattern"].title()
            pattern_scores = pattern_prediction["pattern_distribution"]
            
            # Get consistency metrics
            consistency = self._analyze_consistency()
            consistency_metric = consistency["consistency_level"]
            
            # Consistency-based suggestions with ML context
            if consistency["current_streak"] < 7:
                if primary_style in ["Experimental", "Balanced"]:
                    message = (
                        "Your adaptive learning style would benefit from daily practice. "
                        "Try solving at least one problem daily to build momentum and "
                        "reinforce pattern recognition."
                    )
                else:
                    message = (
                        "Your methodical approach needs consistent practice. "
                        "Maintain a daily solving routine to strengthen your "
                        "systematic problem-solving skills."
                    )
                suggestions.append({
                    "type": "consistency",
                    "message": message,
                    "priority": "high"
                })
            
            # Pattern-based suggestions
            lowest_pattern = min(pattern_scores.items(), key=lambda x: x[1])
            if lowest_pattern[1] < 20:  # If any pattern score is below 20%
                suggestions.append({
                    "type": "pattern_improvement",
                    "message": self._get_pattern_improvement_suggestion(lowest_pattern[0], primary_style),
                    "priority": "medium"
                })
            
            # Topic-based suggestions with ML insights
            preferred_topics = self._analyze_preferred_topics()
            if preferred_topics["weak"]:
                weak_topics = preferred_topics["weak"][:3]
                suggestion = self._generate_topic_suggestion(weak_topics, primary_style)
                suggestions.append(suggestion)
            
            # Optimization suggestions based on code patterns
            if pattern_scores.get("efficient", 0) < 40:
                suggestions.append({
                    "type": "optimization",
                    "message": (
                        "Focus on optimizing your solutions. Our analysis shows potential "
                        "for improvement in time and space complexity. Start with your "
                        "stronger topics and gradually apply optimization techniques."
                    ),
                    "priority": "medium"
                })
            
            logger.info(f"Generated {len(suggestions)} ML-informed suggestions")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}", exc_info=True)
            return self._generate_basic_suggestions()

    def _get_pattern_improvement_suggestion(self, weak_pattern: str, primary_style: str) -> str:
        """Generate targeted suggestion for improving specific pattern."""
        improvements = {
            "methodical": (
                "To strengthen your systematic approach, start by outlining your solution "
                "before coding. Document your problem-solving steps and analyze edge cases "
                "thoroughly before implementation."
            ),
            "experimental": (
                "To improve your experimental approach, practice more with test-driven "
                "development. Start with simple test cases and gradually add complexity "
                "to build robust solutions."
            ),
            "efficient": (
                "To enhance solution efficiency, focus on analyzing time and space "
                "complexity before implementation. Study common optimization techniques "
                "and practice applying them to your solutions."
            ),
            "structured": (
                "To improve code organization, practice breaking down complex problems "
                "into smaller, manageable components. Focus on writing modular code "
                "with clear interfaces between components."
            )
        }
        return improvements.get(weak_pattern,
            "Focus on diversifying your problem-solving approach to develop a more "
            "rounded skill set.")

    def _generate_topic_suggestion(
        self,
        weak_topics: List[str],
        primary_style: str
    ) -> Dict[str, str]:
        """Generate personalized topic suggestion based on learning style."""
        topics_str = ", ".join(weak_topics)
        
        if primary_style == "Methodical":
            message = (
                f"Your systematic approach will work well for mastering {topics_str}. "
                "Start with foundational problems and progressively increase difficulty "
                "while documenting patterns you discover."
            )
        elif primary_style == "Experimental":
            message = (
                f"To improve in {topics_str}, experiment with different solution approaches. "
                "Use your strength in iterative learning to explore various implementations "
                "and learn from each attempt."
            )
        else:
            message = (
                f"Consider focusing on {topics_str} to broaden your skill set. "
                "Apply your balanced approach to systematically explore these topics "
                "while experimenting with different solutions."
            )
            
        return {
            "type": "topic_focus",
            "message": message,
            "priority": "medium"
        }

    def _generate_basic_suggestions(self) -> List[Dict[str, str]]:
        """Generate basic suggestions when ML analysis is unavailable."""
        suggestions = []
        consistency = self._analyze_consistency()
        
        if consistency["current_streak"] < 7:
            suggestions.append({
                "type": "consistency",
                "message": "Try to solve at least one problem daily to build momentum",
                "priority": "high"
            })
        
        preferred_topics = self._analyze_preferred_topics()
        if preferred_topics["weak"]:
            suggestions.append({
                "type": "topic_focus",
                "message": f"Consider focusing on {', '.join(preferred_topics['weak'][:3])} "
                         "to broaden your skill set",
                "priority": "medium"
            })
            
        return suggestions
