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
        
        return recommendations
