from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from .pattern_analyzer import PatternAnalyzer
from .skill_analyzer import SkillAnalyzer
from .learning_path_analyzer import LearningPathAnalyzer

logger = logging.getLogger(__name__)

class AnalyticsManager:
    def __init__(self, user_data: Dict[str, Any]):
        """Initialize the analytics manager with user data."""
        self.user_data = user_data
        self.pattern_analyzer = PatternAnalyzer(user_data)
        self.skill_analyzer = SkillAnalyzer(user_data)
        self.learning_path_analyzer = LearningPathAnalyzer(user_data)
        self._analysis_cache: Dict[str, Any] = {}
        self._last_analysis_time: Optional[datetime] = None

    def generate_complete_analysis(self) -> Dict[str, Any]:
        """Generate a complete analysis of the user's LeetCode profile."""
        try:
            logger.info("Starting complete analysis generation")
            
            # Check if we have a recent cached analysis
            if self._is_cache_valid():
                logger.info("Returning cached analysis")
                return self._analysis_cache

            # Generate individual analyses
            pattern_analysis = self.pattern_analyzer.get_complete_analysis()
            skill_analysis = self.skill_analyzer.get_complete_skill_analysis()
            learning_path = self.learning_path_analyzer.generate_learning_path()

            # Compile comprehensive analysis
            analysis = self._compile_analysis(
                pattern_analysis,
                skill_analysis,
                learning_path
            )

            # Cache the results
            self._cache_analysis(analysis)
            
            logger.info("Complete analysis generated successfully")
            logger.debug(f"Generated analysis structure: {analysis}")
            if not isinstance(analysis, dict) or 'detailed_analysis' not in analysis:
                logger.error("Analysis data structure is invalid")
                return self._generate_fallback_analysis()
            return analysis

        except Exception as e:
            logger.error(f"Error generating complete analysis: {str(e)}", exc_info=True)
            return self._generate_fallback_analysis()

    def _compile_analysis(
        self,
        pattern_analysis: Dict[str, Any],
        skill_analysis: Dict[str, Any],
        learning_path: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compile individual analyses into a comprehensive report."""
        return {
            "summary": self._generate_summary(pattern_analysis, skill_analysis),
            "detailed_analysis": {
                "coding_patterns": pattern_analysis,
                "skill_assessment": skill_analysis,
                "learning_path": learning_path,
                "weak_topics": skill_analysis.get("detailed_analysis", {}).get("weak_topics", [])
            },
            "recommendations": self._generate_recommendations(
                pattern_analysis,
                skill_analysis,
                learning_path
            ),
            "personalized_insights": self._generate_personalized_insights(
                pattern_analysis,
                skill_analysis
            ),
            "next_steps": self._generate_next_steps(learning_path),
            "analysis_timestamp": datetime.now().isoformat()
        }

    def _generate_summary(
        self,
        pattern_analysis: Dict[str, Any],
        skill_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a high-level summary of the analysis."""
        coding_personality = pattern_analysis.get("coding_personality", {})
        overall_rating = skill_analysis.get("overall_rating", {})

        return {
            "coding_style": coding_personality.get("problem_solving_style", {}).get("primary_style", "Developing"),
            "skill_level": overall_rating.get("level", "Beginner"),
            "overall_score": overall_rating.get("score", 0),
            "key_strengths": self._identify_key_strengths(pattern_analysis, skill_analysis),
            "priority_areas": self._identify_priority_areas(pattern_analysis, skill_analysis)
        }

    def _generate_recommendations(
        self,
        pattern_analysis: Dict[str, Any],
        skill_analysis: Dict[str, Any],
        learning_path: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate personalized recommendations."""
        return {
            "immediate_focus": self._get_immediate_focus_areas(
                pattern_analysis,
                skill_analysis
            ),
            "study_plan": learning_path.get("recommended_path", {}),
            "practice_strategy": self._generate_practice_strategy(
                pattern_analysis,
                skill_analysis
            )
        }

    def _generate_personalized_insights(
        self,
        pattern_analysis: Dict[str, Any],
        skill_analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Generate personalized insights based on the analysis."""
        insights = []
        
        # Pattern-based insights
        coding_personality = pattern_analysis.get("coding_personality", {})
        if coding_personality:
            insights.append({
                "type": "coding_style",
                "insight": coding_personality.get("approach_description", ""),
                "impact": "This affects how you approach problem-solving"
            })

        # Skill-based insights
        skill_details = skill_analysis.get("detailed_analysis", {})
        contest_perf = skill_details.get("contest_performance", {})
        if contest_perf:
            insights.append({
                "type": "contest_performance",
                "insight": contest_perf.get("ranking_trend", {}).get("description", ""),
                "impact": "This influences your competitive programming growth"
            })

        return insights

    def _generate_next_steps(self, learning_path: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate concrete next steps from the learning path."""
        next_steps = []
        
        # Add immediate actions from the learning path
        recommended_path = learning_path.get("recommended_path", {})
        weekly_focus = recommended_path.get("weekly_focus", [])
        
        if weekly_focus:
            next_week = weekly_focus[0]
            next_steps.append({
                "action": f"Focus on {next_week['focus_topic']}",
                "timeframe": "This week",
                "difficulty": next_week['difficulty'],
                "target": f"{next_week['problems_per_day']} problems per day"
            })

        return next_steps

    def _identify_key_strengths(
        self,
        pattern_analysis: Dict[str, Any],
        skill_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify key strengths from the analysis."""
        strengths = []
        
        # Add topic-based strengths
        topics = pattern_analysis.get("skill_analysis", {}).get("preferred_topics", {})
        strong_topics = topics.get("strong", [])
        if strong_topics:
            strengths.extend(strong_topics[:3])  # Top 3 strong topics

        # Add performance-based strengths
        skill_details = skill_analysis.get("detailed_analysis", {})
        problem_mastery = skill_details.get("problem_mastery", {})
        mastery_levels = problem_mastery.get("mastery_levels", {})
        
        for difficulty, level in mastery_levels.items():
            if level in ["Master", "Advanced"]:
                strengths.append(f"{difficulty} Problem Solving")

        return strengths[:5]  # Return top 5 strengths

    def _identify_priority_areas(
        self,
        pattern_analysis: Dict[str, Any],
        skill_analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Identify priority areas for improvement."""
        priorities = []
        
        # Add consistency-based priorities
        consistency = pattern_analysis.get("coding_personality", {}).get("consistency_metrics", {})
        if consistency.get("consistency_level") in ["Getting Started", "Building Consistency"]:
            priorities.append({
                "area": "Consistency",
                "reason": "Regular practice is key to improvement",
                "priority": "high"
            })

        # Add skill-based priorities
        skill_details = skill_analysis.get("detailed_analysis", {})
        problem_mastery = skill_details.get("problem_mastery", {})
        
        for difficulty, stats in problem_mastery.get("difficulty_stats", {}).items():
            if stats.get("success_rate", 0) < 40:
                priorities.append({
                    "area": f"{difficulty} Problems",
                    "reason": "Low success rate needs improvement",
                    "priority": "medium"
                })

        return priorities

    def _get_immediate_focus_areas(
        self,
        pattern_analysis: Dict[str, Any],
        skill_analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Determine immediate focus areas based on analysis."""
        focus_areas = []
        
        # Add pattern-based focus areas
        pattern_suggestions = pattern_analysis.get("development_suggestions", [])
        for suggestion in pattern_suggestions:
            if suggestion.get("priority") == "high":
                focus_areas.append({
                    "area": suggestion.get("type"),
                    "action": suggestion.get("message"),
                    "urgency": "High"
                })

        # Add skill-based focus areas
        skill_recommendations = skill_analysis.get("recommendations", [])
        for recommendation in skill_recommendations:
            if recommendation.get("priority") == "high":
                focus_areas.append({
                    "area": recommendation.get("type"),
                    "action": recommendation.get("message"),
                    "urgency": "High"
                })

        return focus_areas

    def _generate_practice_strategy(
        self,
        pattern_analysis: Dict[str, Any],
        skill_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a practice strategy based on analysis."""
        coding_personality = pattern_analysis.get("coding_personality", {})
        skill_level = skill_analysis.get("overall_rating", {}).get("level", "Beginner")
        
        return {
            "practice_style": self._adapt_to_coding_personality(coding_personality),
            "difficulty_distribution": self._get_difficulty_distribution(skill_level),
            "time_allocation": self._suggest_time_allocation(coding_personality)
        }

    def _adapt_to_coding_personality(self, personality: Dict[str, Any]) -> Dict[str, str]:
        """Adapt practice recommendations to coding personality."""
        style = personality.get("problem_solving_style", {}).get("primary_style", "Balanced")
        
        strategies = {
            "Methodical": {
                "approach": "Start with thorough problem analysis",
                "suggestion": "Focus on understanding patterns before implementation"
            },
            "Experimental": {
                "approach": "Use a test-driven approach",
                "suggestion": "Start with simple cases and progressively add complexity"
            },
            "Balanced": {
                "approach": "Combine analysis with practical implementation",
                "suggestion": "Alternate between planning and coding phases"
            }
        }
        
        return strategies.get(style, strategies["Balanced"])

    def _get_difficulty_distribution(self, skill_level: str) -> Dict[str, int]:
        """Get recommended problem difficulty distribution."""
        distributions = {
            "Beginner": {"Easy": 70, "Medium": 30, "Hard": 0},
            "Intermediate": {"Easy": 30, "Medium": 60, "Hard": 10},
            "Advanced": {"Easy": 10, "Medium": 50, "Hard": 40},
            "Expert": {"Easy": 5, "Medium": 35, "Hard": 60}
        }
        return distributions.get(skill_level, distributions["Beginner"])

    def _suggest_time_allocation(self, personality: Dict[str, Any]) -> Dict[str, int]:
        """Suggest time allocation for different activities."""
        consistency = personality.get("consistency_metrics", {}).get("consistency_level", "Getting Started")
        
        if consistency == "Highly Consistent":
            return {
                "problem_solving": 60,
                "concept_review": 20,
                "pattern_recognition": 20
            }
        else:
            return {
                "problem_solving": 40,
                "concept_review": 40,
                "pattern_recognition": 20
            }

    def _is_cache_valid(self) -> bool:
        """Check if cached analysis is still valid (less than 1 hour old)."""
        if not self._last_analysis_time:
            return False
            
        age = datetime.now() - self._last_analysis_time
        return age.total_seconds() < 3600  # Cache valid for 1 hour

    def _cache_analysis(self, analysis: Dict[str, Any]) -> None:
        """Cache the analysis results."""
        self._analysis_cache = analysis
        self._last_analysis_time = datetime.now()

    def _generate_fallback_analysis(self) -> Dict[str, Any]:
        """Generate a basic analysis when full analysis fails."""
        return {
            "summary": {
                "message": "Basic analysis generated due to error in detailed analysis",
                "coding_style": "Not available",
                "skill_level": "Not available"
            },
            "recommendations": {
                "message": "Please try again later for detailed recommendations",
                "general_advice": "Continue practicing regularly"
            },
            "analysis_timestamp": datetime.now().isoformat()
        }
