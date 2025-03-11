from typing import Dict, Any, List
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SkillAssessmentModel:
    """Machine learning model for accurate skill level assessment."""
    
    def __init__(self):
        """Initialize the skill assessment model."""
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.feature_names = [
            'problem_solving_rate',
            'contest_rating',
            'avg_difficulty_score',
            'consistency_score',
            'efficiency_score',
            'topic_mastery_score',
            'problem_diversity',
            'learning_velocity'
        ]

    def extract_features(self, user_data: Dict[str, Any]) -> np.ndarray:
        """Extract features from user's LeetCode data."""
        try:
            features = []
            
            # Problem solving rate
            solved_problems = user_data.get("matchedUser", {}).get("submitStats", {}).get("acSubmissionNum", [])
            total_solved = sum(item.get("count", 0) for item in solved_problems if item.get("difficulty") != "All")
            total_submissions = sum(item.get("submissions", 0) for item in solved_problems if item.get("difficulty") != "All")
            solving_rate = total_solved / total_submissions if total_submissions > 0 else 0
            features.append(solving_rate)
            
            # Contest rating
            contest_rating = user_data.get("userContestRanking", {}).get("rating", 0)
            normalized_rating = min(contest_rating / 3000, 1.0)  # Normalize to 0-1
            features.append(normalized_rating)
            
            # Average difficulty score
            difficulty_weights = {"Easy": 1, "Medium": 2, "Hard": 4}
            difficulty_counts = {
                item.get("difficulty"): item.get("count", 0)
                for item in solved_problems
                if item.get("difficulty") in difficulty_weights
            }
            weighted_sum = sum(count * difficulty_weights[diff] for diff, count in difficulty_counts.items())
            total_count = sum(difficulty_counts.values()) or 1
            avg_difficulty = weighted_sum / total_count
            normalized_difficulty = min(avg_difficulty / 4, 1.0)  # Normalize by max weight
            features.append(normalized_difficulty)
            
            # Consistency score
            recent_submissions = user_data.get("matchedUser", {}).get("recentSubmissionList", [])
            if recent_submissions:
                # Analyze submission frequency over last 30 days
                submission_dates = [
                    datetime.fromtimestamp(sub.get("timestamp", 0)).date()
                    for sub in recent_submissions
                ]
                unique_dates = len(set(submission_dates))
                consistency = unique_dates / 30  # Normalize by 30 days
            else:
                consistency = 0
            features.append(consistency)
            
            # Efficiency score
            if recent_submissions:
                runtime_percentiles = [
                    float(sub.get("runtimePercentile", 0))
                    for sub in recent_submissions
                    if sub.get("statusDisplay") == "Accepted"
                ]
                efficiency = np.mean(runtime_percentiles) / 100 if runtime_percentiles else 0
            else:
                efficiency = 0
            features.append(efficiency)
            
            # Topic mastery score
            tag_problems = user_data.get("matchedUser", {}).get("tagProblemCounts", {})
            topic_scores = []
            for level in ["fundamental", "intermediate", "advanced"]:
                for topic in tag_problems.get(level, []):
                    solved = topic.get("problemsSolved", 0)
                    total = max(topic.get("problemsCount", 0), 1)
                    topic_scores.append(solved / total)
            topic_mastery = np.mean(topic_scores) if topic_scores else 0
            features.append(topic_mastery)
            
            # Problem diversity
            if solved_problems:
                solved_by_type = {
                    item.get("difficulty"): item.get("count", 0)
                    for item in solved_problems
                    if item.get("difficulty") != "All"
                }
                total = sum(solved_by_type.values()) or 1
                diversity_scores = [-((count/total) * np.log2(count/total)) 
                                  for count in solved_by_type.values()]
                diversity = sum(diversity_scores) / len(diversity_scores) if diversity_scores else 0
            else:
                diversity = 0
            features.append(diversity)
            
            # Learning velocity
            if recent_submissions:
                timestamps = sorted(sub.get("timestamp", 0) for sub in recent_submissions)
                if len(timestamps) >= 2:
                    time_span = timestamps[-1] - timestamps[0]
                    problems_per_day = len(timestamps) / (time_span / 86400) if time_span > 0 else 0
                    velocity = min(problems_per_day / 10, 1.0)  # Normalize by 10 problems per day
                else:
                    velocity = 0
            else:
                velocity = 0
            features.append(velocity)

            return np.array(features).reshape(1, -1)

        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}", exc_info=True)
            return np.zeros((1, len(self.feature_names)))

    def predict_skill_level(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict user's skill level and provide detailed assessment."""
        try:
            features = self.extract_features(user_data)
            
            # For now, use weighted feature combination until model is trained
            # TODO: Replace with actual model predictions once trained
            feature_weights = [0.15, 0.20, 0.15, 0.10, 0.15, 0.10, 0.05, 0.10]
            skill_score = np.dot(features[0], feature_weights)
            
            # Determine skill level based on score
            if skill_score > 0.8:
                level = "Elite"
            elif skill_score > 0.6:
                level = "Advanced"
            elif skill_score > 0.4:
                level = "Intermediate"
            else:
                level = "Beginner"
            
            # Calculate confidence metrics
            data_confidence = min(len(user_data.get("matchedUser", {}).get("recentSubmissionList", [])) / 100, 1.0)
            prediction_stability = np.mean([
                features[0][1],  # Contest rating stability
                features[0][3],  # Consistency score
                data_confidence
            ])
            
            return {
                "skill_level": level,
                "overall_score": round(skill_score * 100, 2),
                "component_scores": {
                    "problem_solving": round(features[0][0] * 100, 2),
                    "contest_performance": round(features[0][1] * 100, 2),
                    "problem_difficulty": round(features[0][2] * 100, 2),
                    "consistency": round(features[0][3] * 100, 2),
                    "code_efficiency": round(features[0][4] * 100, 2),
                    "topic_coverage": round(features[0][5] * 100, 2),
                    "approach_diversity": round(features[0][6] * 100, 2),
                    "learning_rate": round(features[0][7] * 100, 2)
                },
                "confidence_metrics": {
                    "data_confidence": round(data_confidence * 100, 2),
                    "prediction_stability": round(prediction_stability * 100, 2)
                }
            }

        except Exception as e:
            logger.error(f"Error predicting skill level: {str(e)}", exc_info=True)
            return {
                "skill_level": "Unknown",
                "overall_score": 0,
                "component_scores": {name: 0 for name in self.feature_names},
                "confidence_metrics": {
                    "data_confidence": 0,
                    "prediction_stability": 0
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