from typing import Dict, Any, List
from datetime import datetime, timedelta
import json
import logging
from ..ml.learning_path_optimizer import LearningPathOptimizer

logger = logging.getLogger(__name__)

class LearningPathAnalyzer:
    def __init__(self, user_data: Dict[str, Any]):
        self.user_data = user_data
        self.matched_user = user_data.get("matchedUser", {})
        self.tag_counts = self.matched_user.get("tagProblemCounts", {})
        self.submit_stats = self.matched_user.get("submitStats", {})
        self.path_optimizer = LearningPathOptimizer()

    def generate_learning_path(self) -> Dict[str, Any]:
        """Generate a personalized learning path using ML optimization"""
        try:
            logger.info("Generating ML-optimized learning path")
            
            # Get basic assessments
            current_level = self._assess_current_level()
            skill_gaps = self._identify_skill_gaps()
            learning_velocity = self._calculate_learning_velocity()

            # Use ML optimizer for path generation
            target_areas = [gap["topic"] for gap in skill_gaps["critical_areas"]]
            target_areas.extend(gap["topic"] for gap in skill_gaps["improvement_areas"])
            
            optimized_path = self.path_optimizer.generate_learning_path(
                self.user_data,
                current_level,
                target_areas
            )
            
            if optimized_path.get("adaptivity_metrics", {}).get("skill_alignment", 0) > 0.6:
                logger.info("Using ML-optimized learning path")
                recommended_path = {
                    "daily_target": optimized_path["daily_schedule"][0]["recommended_problems"]
                                  if optimized_path.get("daily_schedule") else 3,
                    "weekly_focus": optimized_path.get("weekly_plan", []),
                    "preparation_strategy": {
                        "focus": "ML-Optimized",
                        "approach": "Personalized based on your learning patterns",
                        "practice_distribution": self._generate_practice_distribution(
                            current_level["overall_level"],
                            optimized_path
                        )
                    }
                }
                timeline = {
                    "estimated_completion_weeks": optimized_path["estimated_completion_time"]["weeks"],
                    "milestones": self._generate_milestones(optimized_path["estimated_completion_time"]["weeks"]),
                    "critical_path": self._generate_optimized_critical_path(
                        skill_gaps["critical_areas"],
                        optimized_path
                    )
                }
            else:
                logger.info("Falling back to heuristic path generation")
                recommended_path = self._create_study_plan(
                    current_level,
                    skill_gaps,
                    learning_velocity
                )
                timeline = self._generate_timeline(
                    current_level,
                    skill_gaps,
                    learning_velocity
                )

            return {
                "current_status": current_level,
                "skill_gaps": skill_gaps,
                "recommended_path": recommended_path,
                "estimated_timeline": timeline,
                "learning_insights": {
                    "peak_hours": optimized_path.get("daily_schedule", []),
                    "learning_patterns": self.path_optimizer.analyze_learning_patterns(self.user_data),
                    "adaptivity_metrics": optimized_path.get("adaptivity_metrics", {})
                }
            }

        except Exception as e:
            logger.error(f"Error generating learning path: {str(e)}", exc_info=True)
            return self._fallback_learning_path(
                current_level=self._assess_current_level(),
                skill_gaps=self._identify_skill_gaps(),
                learning_velocity=self._calculate_learning_velocity()
            )

    def _generate_practice_distribution(
        self,
        overall_level: str,
        optimized_path: Dict[str, Any]
    ) -> Dict[str, int]:
        """Generate practice distribution based on ML insights"""
        try:
            if "weekly_plan" in optimized_path:
                # Calculate distribution from ML recommendations
                total_problems = sum(week.get("problems_per_day", 0) * 7
                                  for week in optimized_path["weekly_plan"])
                if total_problems == 0:
                    raise ValueError("No problems found in weekly plan")
                    
                difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
                for week in optimized_path["weekly_plan"]:
                    diff = week.get("difficulty", "Medium")
                    count = week.get("problems_per_day", 0) * 7
                    if "-" in diff:  # Handle ranges like "Medium-Hard"
                        parts = diff.split("-")
                        difficulty_counts[parts[0].strip()] += count * 0.5
                        difficulty_counts[parts[1].strip()] += count * 0.5
                    else:
                        difficulty_counts[diff] += count
                
                return {
                    diff: round((count / total_problems) * 100)
                    for diff, count in difficulty_counts.items()
                }
            else:
                raise ValueError("No weekly plan in optimized path")
                
        except Exception as e:
            logger.error(f"Error generating practice distribution: {str(e)}")
            # Fall back to default distribution
            return self._generate_preparation_strategy(overall_level)["practice_distribution"]

    def _generate_optimized_critical_path(
        self,
        critical_areas: List[Dict[str, Any]],
        optimized_path: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate critical path using ML optimization insights"""
        try:
            prerequisite_map = optimized_path.get("prerequisite_map", {})
            critical_path = []
            
            for idx, area in enumerate(critical_areas):
                topic = area["topic"]
                prerequisites = prerequisite_map.get(topic, [])
                
                step = {
                    "step": idx + 1,
                    "topic": topic,
                    "min_problems": self._calculate_min_problems(topic, optimized_path),
                    "estimated_days": self._estimate_topic_days(topic, optimized_path),
                    "prerequisites": prerequisites
                }
                critical_path.append(step)
            
            return critical_path
            
        except Exception as e:
            logger.error(f"Error generating optimized critical path: {str(e)}")
            return self._generate_critical_path(critical_areas)

    def _fallback_learning_path(
        self,
        current_level: Dict[str, Any],
        skill_gaps: Dict[str, Any],
        learning_velocity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate fallback learning path when ML optimization fails"""
        return {
            "current_status": current_level,
            "skill_gaps": skill_gaps,
            "recommended_path": self._create_study_plan(
                current_level,
                skill_gaps,
                learning_velocity
            ),
            "estimated_timeline": self._generate_timeline(
                current_level,
                skill_gaps,
                learning_velocity
            ),
            "learning_insights": {
                "peak_hours": [],
                "learning_patterns": {},
                "adaptivity_metrics": {
                    "skill_alignment": 0,
                    "preference_matching": 0
                }
            }
        }

    def _calculate_min_problems(
        self,
        topic: str,
        optimized_path: Dict[str, Any]
    ) -> int:
        """Calculate minimum problems needed for a topic based on ML insights"""
        try:
            for week in optimized_path.get("weekly_plan", []):
                if week["focus_topic"] == topic:
                    return week["problems_per_day"] * 7
            return 10  # Default fallback
        except Exception:
            return 10

    def _estimate_topic_days(
        self,
        topic: str,
        optimized_path: Dict[str, Any]
    ) -> int:
        """Estimate days needed for a topic based on ML insights"""
        try:
            learning_patterns = self.path_optimizer.analyze_learning_patterns(self.user_data)
            base_days = 7
            
            if learning_patterns.get("learning_speed") == "fast":
                base_days = 5
            elif learning_patterns.get("learning_speed") == "steady":
                base_days = 10
                
            # Adjust based on topic complexity in prerequisite map
            prereq_map = optimized_path.get("prerequisite_map", {})
            if topic in prereq_map:
                base_days += len(prereq_map[topic]) * 2
                
            return base_days
        except Exception:
            return 7  # Default fallback

    def _assess_current_level(self) -> Dict[str, Any]:
        """Assess user's current skill level"""
        ac_submissions = self.submit_stats.get("acSubmissionNum", [])
        difficulty_counts = {
            sub.get("difficulty"): sub.get("count", 0)
            for sub in ac_submissions if sub.get("difficulty") != "All"
        }

        # Calculate proficiency levels
        easy_proficiency = self._calculate_proficiency_level(
            difficulty_counts.get("Easy", 0), target=100)
        medium_proficiency = self._calculate_proficiency_level(
            difficulty_counts.get("Medium", 0), target=150)
        hard_proficiency = self._calculate_proficiency_level(
            difficulty_counts.get("Hard", 0), target=50)

        return {
            "difficulty_counts": difficulty_counts,
            "proficiency_levels": {
                "Easy": easy_proficiency,
                "Medium": medium_proficiency,
                "Hard": hard_proficiency
            },
            "overall_level": self._determine_overall_level(
                easy_proficiency,
                medium_proficiency,
                hard_proficiency
            )
        }

    def _identify_skill_gaps(self) -> Dict[str, Any]:
        """Identify areas where the user needs improvement"""
        topic_gaps = []
        advanced_topics = self.tag_counts.get("advanced", [])
        intermediate_topics = self.tag_counts.get("intermediate", [])
        
        # Analyze advanced topics
        for topic in advanced_topics:
            solved = topic.get("problemsSolved", 0)
            if solved < 5:  # Consider it a gap if less than 5 problems solved
                topic_gaps.append({
                    "topic": topic["tagName"],
                    "level": "Advanced",
                    "solved": solved,
                    "priority": "high" if solved == 0 else "medium"
                })

        # Analyze intermediate topics
        for topic in intermediate_topics:
            solved = topic.get("problemsSolved", 0)
            if solved < 10:  # Consider it a gap if less than 10 problems solved
                topic_gaps.append({
                    "topic": topic["tagName"],
                    "level": "Intermediate",
                    "solved": solved,
                    "priority": "medium" if solved < 5 else "low"
                })

        return {
            "topic_gaps": topic_gaps,
            "critical_areas": [gap for gap in topic_gaps if gap["priority"] == "high"],
            "improvement_areas": [gap for gap in topic_gaps if gap["priority"] == "medium"]
        }

    def _calculate_learning_velocity(self) -> Dict[str, Any]:
        """Calculate user's learning speed and patterns"""
        calendar_data = self.matched_user.get("userCalendar", {})
        submission_calendar = calendar_data.get("submissionCalendar", "{}")
        
        try:
            submissions_by_date = json.loads(submission_calendar)
        except json.JSONDecodeError:
            submissions_by_date = {}

        if not submissions_by_date:
            return {
                "problems_per_day": 0,
                "consistency_score": 0,
                "learning_speed": "Not enough data"
            }

        # Calculate average problems per day
        active_days = len(submissions_by_date)
        total_submissions = sum(int(count) for count in submissions_by_date.values())
        problems_per_day = total_submissions / active_days if active_days > 0 else 0

        # Calculate consistency score (0-100)
        consistency_score = self._calculate_consistency_score(submissions_by_date)

        return {
            "problems_per_day": round(problems_per_day, 2),
            "consistency_score": consistency_score,
            "learning_speed": self._determine_learning_speed(
                problems_per_day,
                consistency_score
            )
        }

    def _create_study_plan(
        self,
        current_level: Dict[str, Any],
        skill_gaps: Dict[str, Any],
        learning_velocity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a personalized study plan"""
        problems_per_day = learning_velocity["problems_per_day"]
        consistency = learning_velocity["consistency_score"]

        # Adjust daily target based on current velocity and consistency
        if consistency < 30:
            suggested_daily = 1
        elif consistency < 60:
            suggested_daily = min(problems_per_day + 1, 3)
        else:
            suggested_daily = min(problems_per_day + 2, 5)

        # Create weekly focus areas
        weekly_focus = self._generate_weekly_focus(
            current_level,
            skill_gaps,
            suggested_daily
        )

        return {
            "daily_target": suggested_daily,
            "weekly_focus": weekly_focus,
            "preparation_strategy": self._generate_preparation_strategy(
                current_level["overall_level"]
            )
        }

    def _generate_timeline(
        self,
        current_level: Dict[str, Any],
        skill_gaps: Dict[str, Any],
        learning_velocity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate estimated timeline for improvement"""
        problems_per_day = learning_velocity["problems_per_day"]
        critical_gaps = len(skill_gaps["critical_areas"])
        improvement_areas = len(skill_gaps["improvement_areas"])

        # Estimate weeks needed for each gap type
        critical_weeks = self._estimate_weeks_needed(
            critical_gaps,
            problems_per_day,
            difficulty_factor=1.5
        )
        improvement_weeks = self._estimate_weeks_needed(
            improvement_areas,
            problems_per_day,
            difficulty_factor=1.2
        )

        total_weeks = critical_weeks + improvement_weeks

        return {
            "estimated_completion_weeks": total_weeks,
            "milestones": self._generate_milestones(total_weeks),
            "critical_path": self._generate_critical_path(skill_gaps["critical_areas"])
        }

    def _calculate_proficiency_level(self, solved: int, target: int) -> float:
        """Calculate proficiency level as a percentage of target"""
        return min(100, (solved / target) * 100)

    def _determine_overall_level(
        self,
        easy_prof: float,
        medium_prof: float,
        hard_prof: float
    ) -> str:
        """Determine overall level based on proficiency scores"""
        weighted_score = (
            0.2 * easy_prof +
            0.5 * medium_prof +
            0.3 * hard_prof
        )

        if weighted_score >= 80:
            return "Expert"
        elif weighted_score >= 60:
            return "Advanced"
        elif weighted_score >= 40:
            return "Intermediate"
        else:
            return "Beginner"

    def _calculate_consistency_score(self, submissions_by_date: Dict[str, str]) -> int:
        """Calculate consistency score (0-100) based on submission patterns"""
        if not submissions_by_date:
            return 0

        # Convert timestamps to dates and sort
        dates = sorted([
            datetime.fromtimestamp(int(ts)).date()
            for ts in submissions_by_date.keys()
        ])

        if not dates:
            return 0

        # Calculate gaps between submissions
        gaps = []
        for i in range(1, len(dates)):
            gap = (dates[i] - dates[i-1]).days
            gaps.append(gap)

        if not gaps:
            return 100  # Only one submission

        # Calculate consistency score
        avg_gap = sum(gaps) / len(gaps)
        consistency = 100 * (1 / (1 + avg_gap))  # Higher gaps = lower score

        return round(consistency)

    def _determine_learning_speed(
        self,
        problems_per_day: float,
        consistency_score: int
    ) -> str:
        """Determine learning speed category"""
        if problems_per_day >= 3 and consistency_score >= 70:
            return "Fast"
        elif problems_per_day >= 1.5 and consistency_score >= 50:
            return "Moderate"
        else:
            return "Steady"

    def _generate_weekly_focus(
        self,
        current_level: Dict[str, Any],
        skill_gaps: Dict[str, Any],
        daily_target: int
    ) -> List[Dict[str, Any]]:
        """Generate weekly focus areas"""
        # Declare weekly_plan with the correct type annotation
        weekly_plan: List[str] = []
        critical_areas = skill_gaps["critical_areas"]
        improvement_areas = skill_gaps["improvement_areas"]

        # First weeks focus on critical areas
        for gap in critical_areas[:4]:  # Up to 4 weeks for critical areas
            weekly_plan.append({
                "week": len(weekly_plan) + 1,
                "focus_topic": gap["topic"],
                "difficulty": "Medium",
                "problems_per_day": daily_target,
                "type": "Critical Improvement"
            })

        # Later weeks focus on improvement areas
        for gap in improvement_areas[:4]:  # Up to 4 more weeks for improvement
            weekly_plan.append({
                "week": len(weekly_plan) + 1,
                "focus_topic": gap["topic"],
                "difficulty": "Medium to Hard",
                "problems_per_day": daily_target,
                "type": "Skill Enhancement"
            })

        return weekly_plan

    def _generate_preparation_strategy(self, overall_level: str) -> Dict[str, Any]:
        """Generate preparation strategy based on overall level"""
        strategies = {
            "Beginner": {
                "focus": "Fundamentals",
                "approach": "Start with easy problems, focus on basic algorithms",
                "practice_distribution": {
                    "Easy": 70,
                    "Medium": 30,
                    "Hard": 0
                }
            },
            "Intermediate": {
                "focus": "Pattern Recognition",
                "approach": "Balance medium problems with some hard ones",
                "practice_distribution": {
                    "Easy": 30,
                    "Medium": 60,
                    "Hard": 10
                }
            },
            "Advanced": {
                "focus": "Advanced Techniques",
                "approach": "Focus on hard problems and contest preparation",
                "practice_distribution": {
                    "Easy": 10,
                    "Medium": 50,
                    "Hard": 40
                }
            },
            "Expert": {
                "focus": "Mastery",
                "approach": "Focus on hardest problems and optimization",
                "practice_distribution": {
                    "Easy": 5,
                    "Medium": 35,
                    "Hard": 60
                }
            }
        }

        return strategies.get(overall_level, strategies["Beginner"])

    def _estimate_weeks_needed(
        self,
        num_gaps: int,
        problems_per_day: float,
        difficulty_factor: float
    ) -> int:
        """Estimate weeks needed to address gaps"""
        if problems_per_day == 0:
            return num_gaps * 2  # Default estimation

        problems_needed = num_gaps * 10  # Assume 10 problems per gap
        days_needed = (problems_needed * difficulty_factor) / problems_per_day
        return max(1, round(days_needed / 7))

    def _generate_milestones(self, total_weeks: int) -> List[Dict[str, Any]]:
        """Generate milestone targets"""
        milestones = []
        current_date = datetime.now()

        for week in range(1, total_weeks + 1):
            target_date = current_date + timedelta(weeks=week)
            milestone_type = "Critical" if week <= total_weeks/2 else "Enhancement"
            
            milestones.append({
                "week": week,
                "target_date": target_date.strftime("%Y-%m-%d"),
                "type": milestone_type,
                "expected_improvement": f"{min(100, week * 15)}%"
            })

        return milestones

    def _generate_critical_path(self, critical_areas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate ordered list of critical topics to focus on"""
        return [
            {
                "step": idx + 1,
                "topic": area["topic"],
                "min_problems": 10,
                "estimated_days": 7
            }
            for idx, area in enumerate(critical_areas)
        ]
