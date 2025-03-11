from typing import Dict, Any, List
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import logging

logger = logging.getLogger(__name__)

class PatternRecognitionModel:
    """Machine learning model for recognizing coding patterns and strategies."""
    
    def __init__(self):
        """Initialize the pattern recognition model."""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.feature_names = [
            'avg_time_to_solve',
            'success_rate',
            'code_length',
            'submission_count',
            'optimized_solutions_ratio',
            'data_structure_variety',
            'algorithm_complexity',
            'refactoring_frequency'
        ]

    def extract_features(self, submission_data: List[Dict[str, Any]]) -> np.ndarray:
        """Extract features from submission data."""
        try:
            if not submission_data:
                logger.warning("No submission data provided for feature extraction")
                return np.zeros((1, len(self.feature_names)))

            features = []
            total_submissions = len(submission_data)
            
            # Calculate average time to solve
            solve_times = [
                s.get('runtime', 0) for s in submission_data 
                if s.get('statusDisplay') == 'Accepted'
            ]
            avg_time = np.mean(solve_times) if solve_times else 0
            
            # Calculate success rate
            accepted_count = sum(1 for s in submission_data if s.get('statusDisplay') == 'Accepted')
            success_rate = accepted_count / total_submissions if total_submissions > 0 else 0
            
            # Analyze code patterns
            code_lengths = [len(s.get('code', '')) for s in submission_data]
            avg_code_length = np.mean(code_lengths) if code_lengths else 0
            
            # Calculate optimization metrics
            runtime_percentiles = [
                float(s.get('runtimePercentile', 0)) 
                for s in submission_data 
                if s.get('statusDisplay') == 'Accepted'
            ]
            optimized_ratio = sum(1 for p in runtime_percentiles if p > 75) / len(runtime_percentiles) if runtime_percentiles else 0
            
            # Analyze data structure usage
            data_structures = set()
            for sub in submission_data:
                code = sub.get('code', '').lower()
                for ds in ['array', 'list', 'tree', 'graph', 'hash', 'heap', 'stack', 'queue']:
                    if ds in code:
                        data_structures.add(ds)
            ds_variety = len(data_structures) / 8  # Normalize by total possible

            # Estimate algorithm complexity
            complexities = []
            for sub in submission_data:
                runtime = float(sub.get('runtime', 0))
                if runtime < 100:
                    complexities.append(1)  # O(n) or better
                elif runtime < 500:
                    complexities.append(2)  # O(n log n)
                else:
                    complexities.append(3)  # O(n²) or worse
            avg_complexity = np.mean(complexities) if complexities else 0
            
            # Calculate refactoring frequency
            submissions_by_problem = {}
            for sub in submission_data:
                prob_id = sub.get('problemId')
                if prob_id:
                    submissions_by_problem[prob_id] = submissions_by_problem.get(prob_id, 0) + 1
            refactor_ratio = sum(1 for count in submissions_by_problem.values() if count > 1) / len(submissions_by_problem) if submissions_by_problem else 0

            features = [
                avg_time,
                success_rate,
                avg_code_length,
                total_submissions,
                optimized_ratio,
                ds_variety,
                avg_complexity,
                refactor_ratio
            ]

            return np.array(features).reshape(1, -1)

        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}", exc_info=True)
            return np.zeros((1, len(self.feature_names)))

    def predict_pattern(self, submission_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict coding patterns from submission data."""
        try:
            features = self.extract_features(submission_data)
            
            # For now, use rule-based predictions until model is trained
            # TODO: Replace with actual model predictions once trained
            pattern_scores = {
                "methodical": features[0][1] * 0.3 + features[0][4] * 0.7,  # Success rate and optimization
                "experimental": features[0][7] * 0.6 + features[0][5] * 0.4,  # Refactoring and DS variety
                "structured": features[0][2] * 0.4 + features[0][6] * 0.6,  # Code length and complexity
                "efficient": features[0][0] * 0.5 + features[0][4] * 0.5,  # Time and optimization
            }
            
            # Normalize scores
            total = sum(pattern_scores.values())
            if total > 0:
                pattern_scores = {k: round(v/total * 100, 2) for k, v in pattern_scores.items()}
            
            primary_pattern = max(pattern_scores.items(), key=lambda x: x[1])[0]
            
            return {
                "primary_pattern": primary_pattern,
                "pattern_distribution": pattern_scores,
                "confidence_scores": {
                    "feature_reliability": min(len(submission_data) / 50, 1.0),  # Scale with data amount
                    "pattern_strength": max(pattern_scores.values()) / 100
                }
            }

        except Exception as e:
            logger.error(f"Error predicting pattern: {str(e)}", exc_info=True)
            return {
                "primary_pattern": "unknown",
                "pattern_distribution": {},
                "confidence_scores": {
                    "feature_reliability": 0.0,
                    "pattern_strength": 0.0
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