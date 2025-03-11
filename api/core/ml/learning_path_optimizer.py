from typing import Dict, Any, List
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class LearningPathOptimizer:
    """Machine learning model for optimizing personalized learning paths."""
    
    def __init__(self):
        """Initialize the learning path optimizer."""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            random_state=42
        )
        self.topic_prerequisites = {
            "Dynamic Programming": ["Arrays", "Recursion"],
            "Graph Algorithms": ["Arrays", "Queue", "HashTable"],
            "Tree Algorithms": ["Recursion", "Queue"],
            "Advanced Data Structures": ["Arrays", "LinkedList", "Tree"],
            "System Design": ["Object-Oriented Design", "Arrays", "HashTable"]
        }
        self.difficulty_progression = {
            "Beginner": {"Easy": 0.7, "Medium": 0.3, "Hard": 0.0},
            "Intermediate": {"Easy": 0.3, "Medium": 0.6, "Hard": 0.1},
            "Advanced": {"Easy": 0.1, "Medium": 0.5, "Hard": 0.4},
            "Elite": {"Easy": 0.1, "Medium": 0.3, "Hard": 0.6}
        }

    def analyze_learning_patterns(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user's learning patterns and preferences."""
        try:
            submissions = user_data.get("matchedUser", {}).get("recentSubmissionList", [])
            if not submissions:
                return self._get_default_patterns()

            # Analyze submission timing patterns
            submission_times = [
                datetime.fromtimestamp(sub.get("timestamp", 0))
                for sub in submissions
            ]
            
            # Time of day preference
            hours = [t.hour for t in submission_times]
            peak_hours = self._find_peak_hours(hours)
            
            # Session duration analysis
            sessions = self._identify_sessions(submission_times)
            avg_session_length = np.mean([s["duration"].total_seconds()/3600 for s in sessions]) if sessions else 2.0
            
            # Problem selection patterns
            problem_sequences = self._analyze_problem_sequences(submissions)
            
            # Learning speed
            learning_speed = self._calculate_learning_speed(submissions)
            
            return {
                "peak_hours": peak_hours,
                "avg_session_length": round(avg_session_length, 2),
                "problem_patterns": problem_sequences,
                "learning_speed": learning_speed
            }
        
        except Exception as e:
            logger.error(f"Error analyzing learning patterns: {str(e)}", exc_info=True)
            return self._get_default_patterns()

    def generate_learning_path(
        self,
        user_data: Dict[str, Any],
        current_skill: Dict[str, Any],
        target_areas: List[str]
    ) -> Dict[str, Any]:
        """Generate personalized learning path."""
        try:
            # Analyze learning patterns
            patterns = self.analyze_learning_patterns(user_data)
            
            # Get current skill level and preferences
            skill_level = current_skill.get("skill_level", "Beginner")
            learning_speed = patterns.get("learning_speed", "moderate")
            
            # Adjust difficulty distribution based on skill level
            difficulty_dist = self.difficulty_progression.get(skill_level, self.difficulty_progression["Beginner"])
            
            # Generate weekly focus areas
            weekly_plan = self._generate_weekly_plan(
                target_areas,
                difficulty_dist,
                patterns,
                learning_speed
            )
            
            # Generate daily schedule
            daily_schedule = self._generate_daily_schedule(
                patterns.get("peak_hours", [(9, 12)]),
                patterns.get("avg_session_length", 2.0)
            )
            
            return {
                "weekly_plan": weekly_plan,
                "daily_schedule": daily_schedule,
                "estimated_completion_time": self._estimate_completion_time(
                    weekly_plan,
                    learning_speed
                ),
                "prerequisite_map": self._generate_prerequisite_map(target_areas),
                "adaptivity_metrics": {
                    "skill_alignment": self._calculate_skill_alignment(weekly_plan, skill_level),
                    "preference_matching": self._calculate_preference_matching(patterns, weekly_plan)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating learning path: {str(e)}", exc_info=True)
            return self._get_default_learning_path()

    def _find_peak_hours(self, hours: List[int]) -> List[tuple]:
        """Find peak activity hours."""
        if not hours:
            return [(9, 12)]  # Default morning hours
            
        hour_counts = np.bincount(hours, minlength=24)
        peaks = []
        current_peak = []
        
        for hour in range(24):
            if hour_counts[hour] > np.mean(hour_counts):
                if not current_peak:
                    current_peak = [hour]
                elif hour - current_peak[-1] == 1:
                    current_peak.append(hour)
                else:
                    if len(current_peak) >= 2:
                        peaks.append((current_peak[0], current_peak[-1]))
                    current_peak = [hour]
        
        if len(current_peak) >= 2:
            peaks.append((current_peak[0], current_peak[-1]))
            
        return peaks if peaks else [(9, 12)]

    def _identify_sessions(self, timestamps: List[datetime]) -> List[Dict[str, Any]]:
        """Identify distinct study sessions."""
        if not timestamps:
            return []
            
        sessions = []
        current_session = {
            "start": timestamps[0],
            "end": timestamps[0],
            "duration": timedelta(0)
        }
        
        for t in timestamps[1:]:
            if (t - current_session["end"]) > timedelta(hours=2):
                current_session["duration"] = current_session["end"] - current_session["start"]
                sessions.append(current_session)
                current_session = {"start": t, "end": t, "duration": timedelta(0)}
            else:
                current_session["end"] = t
        
        current_session["duration"] = current_session["end"] - current_session["start"]
        sessions.append(current_session)
        
        return sessions

    def _analyze_problem_sequences(self, submissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in problem selection."""
        sequences = {
            "difficulty_transitions": {
                "up": 0,
                "down": 0,
                "same": 0
            },
            "topic_transitions": {},
            "preferred_difficulty": "unknown"
        }
        
        if len(submissions) < 2:
            return sequences
            
        # Analyze difficulty transitions
        for i in range(len(submissions)-1):
            curr_diff = submissions[i].get("difficulty")
            next_diff = submissions[i+1].get("difficulty")
            
            if curr_diff and next_diff:
                diff_levels = {"Easy": 1, "Medium": 2, "Hard": 3}
                curr_level = diff_levels.get(curr_diff, 0)
                next_level = diff_levels.get(next_diff, 0)
                
                if next_level > curr_level:
                    sequences["difficulty_transitions"]["up"] += 1
                elif next_level < curr_level:
                    sequences["difficulty_transitions"]["down"] += 1
                else:
                    sequences["difficulty_transitions"]["same"] += 1
        
        # Determine preferred difficulty
        diff_counts = {}
        for sub in submissions:
            diff = sub.get("difficulty")
            if diff:
                diff_counts[diff] = diff_counts.get(diff, 0) + 1
        
        if diff_counts:
            sequences["preferred_difficulty"] = max(diff_counts.items(), key=lambda x: x[1])[0]
        
        return sequences

    def _calculate_learning_speed(self, submissions: List[Dict[str, Any]]) -> str:
        """Calculate user's learning speed based on submission history."""
        if not submissions:
            return "moderate"
            
        # Calculate success rate over time
        accepted_timestamps = {}
        for sub in submissions:
            if sub.get("statusDisplay") == "Accepted":
                problem_id = sub.get("problemId")
                if problem_id not in accepted_timestamps:
                    accepted_timestamps[problem_id] = datetime.fromtimestamp(sub.get("timestamp", 0))
        
        if not accepted_timestamps:
            return "moderate"
            
        # Calculate problems solved per day
        date_range = (max(accepted_timestamps.values()) - min(accepted_timestamps.values())).days + 1
        problems_per_day = len(accepted_timestamps) / max(date_range, 1)
        
        if problems_per_day > 3:
            return "fast"
        elif problems_per_day > 1:
            return "moderate"
        else:
            return "steady"

    def _generate_weekly_plan(
        self,
        target_areas: List[str],
        difficulty_dist: Dict[str, float],
        patterns: Dict[str, Any],
        learning_speed: str
    ) -> List[Dict[str, Any]]:
        """Generate weekly study plan."""
        problems_per_day = {
            "fast": 5,
            "moderate": 3,
            "steady": 2
        }.get(learning_speed, 3)
        
        weekly_plan = []
        for i, topic in enumerate(target_areas):
            # Adjust difficulty distribution based on topic
            topic_difficulty = difficulty_dist.copy()
            if topic in ["Dynamic Programming", "System Design"]:
                topic_difficulty["Hard"] = min(topic_difficulty["Hard"] + 0.1, 1.0)
                topic_difficulty["Easy"] = max(topic_difficulty["Easy"] - 0.1, 0.0)
            
            weekly_plan.append({
                "week": i + 1,
                "focus_topic": topic,
                "difficulty_distribution": topic_difficulty,
                "problems_per_day": problems_per_day,
                "prerequisites": self.topic_prerequisites.get(topic, []),
                "estimated_time": self._estimate_topic_time(topic, problems_per_day)
            })
            
        return weekly_plan

    def _generate_daily_schedule(
        self,
        peak_hours: List[tuple],
        session_length: float
    ) -> List[Dict[str, Any]]:
        """Generate daily study schedule."""
        schedule = []
        for start_hour, end_hour in peak_hours:
            duration = min(session_length, end_hour - start_hour)
            schedule.append({
                "start_time": f"{start_hour:02d}:00",
                "duration_hours": duration,
                "recommended_breaks": self._calculate_breaks(duration)
            })
        return schedule

    def _estimate_completion_time(
        self,
        weekly_plan: List[Dict[str, Any]],
        learning_speed: str
    ) -> Dict[str, Any]:
        """Estimate time to complete the learning path."""
        speed_factors = {
            "fast": 0.8,
            "moderate": 1.0,
            "steady": 1.2
        }
        
        total_weeks = len(weekly_plan)
        base_hours = sum(week["estimated_time"] for week in weekly_plan)
        adjusted_hours = base_hours * speed_factors.get(learning_speed, 1.0)
        
        return {
            "weeks": total_weeks,
            "estimated_hours": round(adjusted_hours, 1),
            "confidence_level": "high" if learning_speed != "steady" else "medium"
        }

    def _generate_prerequisite_map(self, topics: List[str]) -> Dict[str, List[str]]:
        """Generate prerequisite map for topics."""
        prereq_map = {}
        for topic in topics:
            if topic in self.topic_prerequisites:
                prereq_map[topic] = self.topic_prerequisites[topic]
        return prereq_map

    def _calculate_skill_alignment(
        self,
        weekly_plan: List[Dict[str, Any]],
        skill_level: str
    ) -> float:
        """Calculate how well the plan aligns with user's skill level."""
        target_difficulty = self.difficulty_progression.get(skill_level, {})
        if not target_difficulty:
            return 0.5
            
        alignment_scores = []
        for week in weekly_plan:
            week_diff = week["difficulty_distribution"]
            score = sum(
                abs(week_diff.get(diff, 0) - target_diff)
                for diff, target_diff in target_difficulty.items()
            )
            alignment_scores.append(1 - (score / 2))  # Normalize to 0-1
            
        return round(np.mean(alignment_scores), 2)

    def _calculate_preference_matching(
        self,
        patterns: Dict[str, Any],
        weekly_plan: List[Dict[str, Any]]
    ) -> float:
        """Calculate how well the plan matches user preferences."""
        matches = []
        
        # Time preference matching
        if patterns.get("peak_hours"):
            matches.append(1.0)  # Plan uses identified peak hours
            
        # Session length matching
        target_length = patterns.get("avg_session_length", 2.0)
        actual_lengths = [
            sum(s["duration_hours"] for s in self._generate_daily_schedule(
                patterns.get("peak_hours", [(9, 12)]),
                target_length
            ))
        ]
        if actual_lengths:
            length_match = 1 - min(abs(target_length - np.mean(actual_lengths)) / target_length, 1)
            matches.append(length_match)
            
        # Difficulty preference matching
        preferred_diff = patterns.get("problem_patterns", {}).get("preferred_difficulty")
        if preferred_diff and weekly_plan:
            diff_matches = []
            for week in weekly_plan:
                if preferred_diff in week["difficulty_distribution"]:
                    diff_matches.append(week["difficulty_distribution"][preferred_diff])
            if diff_matches:
                matches.append(np.mean(diff_matches))
        
        return round(np.mean(matches) if matches else 0.5, 2)

    def _calculate_breaks(self, duration: float) -> List[int]:
        """Calculate recommended break minutes based on session duration."""
        if duration <= 1:
            return [30]
        elif duration <= 2:
            return [30, 90]
        else:
            breaks = []
            current = 45
            while current < duration * 60:
                breaks.append(current)
                current += 45
            return breaks

    def _estimate_topic_time(self, topic: str, problems_per_day: int) -> float:
        """Estimate time needed for a topic in hours."""
        base_hours = 7 * problems_per_day  # One week base
        
        # Adjust for topic complexity
        topic_multipliers = {
            "Dynamic Programming": 1.5,
            "System Design": 1.3,
            "Graph Algorithms": 1.4,
            "Tree Algorithms": 1.2,
            "Advanced Data Structures": 1.3
        }
        
        return base_hours * topic_multipliers.get(topic, 1.0)

    def _get_default_patterns(self) -> Dict[str, Any]:
        """Return default learning patterns."""
        return {
            "peak_hours": [(9, 12), (14, 17)],
            "avg_session_length": 2.0,
            "problem_patterns": {
                "difficulty_transitions": {"up": 0, "down": 0, "same": 0},
                "topic_transitions": {},
                "preferred_difficulty": "Medium"
            },
            "learning_speed": "moderate"
        }

    def _get_default_learning_path(self) -> Dict[str, Any]:
        """Return default learning path."""
        return {
            "weekly_plan": [
                {
                    "week": 1,
                    "focus_topic": "Arrays",
                    "difficulty_distribution": {"Easy": 0.7, "Medium": 0.3, "Hard": 0.0},
                    "problems_per_day": 3,
                    "prerequisites": [],
                    "estimated_time": 21
                }
            ],
            "daily_schedule": [
                {
                    "start_time": "09:00",
                    "duration_hours": 2.0,
                    "recommended_breaks": [45, 90]
                }
            ],
            "estimated_completion_time": {
                "weeks": 1,
                "estimated_hours": 21,
                "confidence_level": "medium"
            },
            "prerequisite_map": {},
            "adaptivity_metrics": {
                "skill_alignment": 0.5,
                "preference_matching": 0.5
            }
        }

    def save_model(self, path: str) -> None:
        """Save the trained model to disk."""
        try:
            joblib.dump(self.model, path)
            logger.info(f"Model saved successfully to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}", exc_info=True)

    def load_model(self, path: str) -> None:
        """Load a trained model from disk."""
        try:
            self.model = joblib.load(path)
            logger.info(f"Model loaded successfully from {path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}", exc_info=True)