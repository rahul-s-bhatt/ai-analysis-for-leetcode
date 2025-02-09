class ProblemRecommender:
    def __init__(self, user_data):
        self.user_data = user_data
        
    def analyze_solving_patterns(self):
        # Get topic stats from formatted data
        topics = self.user_data['topics']
        difficulties = {
            'Easy': self.user_data['stats']['easySolved'],
            'Medium': self.user_data['stats']['mediumSolved'],
            'Hard': self.user_data['stats']['hardSolved']
        }
        
        # Calculate topic completion rates
        topic_completion = {
            name: (info['solved'] / info['total'] * 100) 
            for name, info in topics.items()
            if info['total'] > 0
        }
                
        return topic_completion, difficulties

    def get_ml_recommendations(self):
        # Extract features from user stats
        solved = self.user_data['stats']['solvedProblems']
        easy = self.user_data['stats']['easySolved']
        med = self.user_data['stats']['mediumSolved']
        hard = self.user_data['stats']['hardSolved']
        
        # Use dummy coefficients as a stand-in for a trained ML model
        # (Replace these with real model predictions as needed)
        score_easy = 0.5 * easy - 0.1 * solved
        score_med = 0.7 * med - 0.1 * solved
        score_hard = 0.8 * hard - 0.05 * solved
        
        scores = {'Easy': score_easy, 'Medium': score_med, 'Hard': score_hard}
        predicted_difficulty = max(scores, key=scores.get)
        
        return {
            'predicted_difficulty': predicted_difficulty,
            'ml_scores': {k: f"{v:.2f}" for k, v in scores.items()}
        }
    
    def get_recommendations(self):
        topic_completion, difficulties = self.analyze_solving_patterns()
        
        recommendations = {
            'weak_categories': [],
            'next_difficulty': None,
            'suggested_problems': []
        }
        
        # Find categories with lowest completion rates
        sorted_topics = sorted(topic_completion.items(), key=lambda x: x[1])
        recommendations['weak_categories'] = [(topic, f"{completion:.1f}%") 
                                           for topic, completion in sorted_topics[:3]]
        
        # Suggest next difficulty level
        total_solved = self.user_data['stats']['solvedProblems']
        if total_solved < 50:
            recommendations['next_difficulty'] = 'Easy'
        elif difficulties['Easy'] > 30 and difficulties['Medium'] < 20:
            recommendations['next_difficulty'] = 'Medium'
        elif difficulties['Medium'] > 50 and difficulties['Hard'] < 10:
            recommendations['next_difficulty'] = 'Hard'
        
        # Get ML-driven recommendation
        ml_result = self.get_ml_recommendations()
        recommendations['next_difficulty'] = ml_result['predicted_difficulty']
        recommendations['ml_scores'] = ml_result['ml_scores']
        
        return recommendations
