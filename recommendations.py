import random

class ProblemRecommender:
    def __init__(self, user_data):
        self.user_data = user_data
        
    def analyze_solving_patterns(self):
        topics = self.user_data['topics']
        difficulties = {
            'Easy': self.user_data['stats']['easySolved'],
            'Medium': self.user_data['stats']['mediumSolved'],
            'Hard': self.user_data['stats']['hardSolved']
        }
        
        topic_completion = {
            name: (info['solved'] / info['total'] * 100) 
            for name, info in topics.items()
            if info['total'] > 0
        }
                
        return topic_completion, difficulties

    def get_ml_recommendations(self):
        solved = self.user_data['stats']['solvedProblems']
        easy = self.user_data['stats']['easySolved']
        med = self.user_data['stats']['mediumSolved']
        hard = self.user_data['stats']['hardSolved']
        
        score_easy = 0.5 * easy - 0.1 * solved
        score_med = 0.7 * med - 0.1 * solved
        score_hard = 0.8 * hard - 0.05 * solved
        
        scores = {'Easy': score_easy, 'Medium': score_med, 'Hard': score_hard}
        predicted_difficulty = max(scores, key=scores.get)
        
        topic_suggestions = {
            'Easy': ["Array", "String"],
            'Medium': ["Dynamic Programming", "Graph"],
            'Hard': ["Advanced Graph Algorithms", "Segment Tree"]
        }
        suggested_topic = random.choice(topic_suggestions[predicted_difficulty])

        return {
            'predicted_difficulty': predicted_difficulty,
            'ml_scores': {k: f"{v:.2f}" for k, v in scores.items()},
            'suggested_topic': suggested_topic
        }

    def get_leetcode_problem_links(self, topic, difficulty, num_problems=3):
        problem_links = {
            "Dynamic Programming": {
                "Medium": [
                    {"title": "Coin Change", "link": "https://leetcode.com/problems/coin-change/"},
                    {"title": "Longest Increasing Subsequence", "link": "https://leetcode.com/problems/longest-increasing-subsequence/"},
                    {"title": "Edit Distance", "link": "https://leetcode.com/problems/edit-distance/"}
                ]
            },
            "Graph": {
                "Medium": [
                    {"title": "Number of Islands", "link": "https://leetcode.com/problems/number-of-islands/"},
                    {"title": "Clone Graph", "link": "https://leetcode.com/problems/clone-graph/"},
                    {"title": "Course Schedule", "link": "https://leetcode.com/problems/course-schedule/"}
                ]
            },
            "Array": {
                "Easy": [
                    {"title": "Two Sum", "link": "https://leetcode.com/problems/two-sum/"},
                    {"title": "Remove Duplicates from Sorted Array", "link": "https://leetcode.com/problems/remove-duplicates-from-sorted-array/"},
                    {"title": "Best Time to Buy and Sell Stock", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"}
                ]
            },
            "String": {
                "Easy": [
                    {"title": "Valid Palindrome", "link": "https://leetcode.com/problems/valid-palindrome/"},
                    {"title": "Longest Common Prefix", "link": "https://leetcode.com/problems/longest-common-prefix/"},
                    {"title": "Reverse String", "link": "https://leetcode.com/problems/reverse-string/"}
                ]
            },
            "Advanced Graph Algorithms": {
                "Hard": [
                    {"title": "Shortest Distance from All Buildings", "link": "https://leetcode.com/problems/shortest-distance-from-all-buildings/"},
                ]
            },
            "Segment Tree": {
                "Hard": [
                    {"title": "Range Sum Query - Mutable", "link": "https://leetcode.com/problems/range-sum-query-mutable/"},
                ]
            }
        }

        if topic in problem_links and difficulty in problem_links[topic]:
            return random.sample(problem_links[topic][difficulty], min(num_problems, len(problem_links[topic][difficulty])))
        else:
            return [{"title": "No problems found", "link": "#"}] * num_problems

    def get_recommendations(self):
        topic_completion, difficulties = self.analyze_solving_patterns()
        sorted_topics = sorted(topic_completion.items(), key=lambda x: x[1])
        weak_topics = sorted_topics[:3]
        weak_categories = [(topic, f"{completion:.1f}%") for topic, completion in weak_topics]
        
        ml_result = self.get_ml_recommendations()
        suggested_difficulty = ml_result['predicted_difficulty']
        suggested_topic = ml_result['suggested_topic']

        problem_links = self.get_leetcode_problem_links(suggested_topic, suggested_difficulty)

        roadmap = {
            "Difficulty": suggested_difficulty,
            "Topic": suggested_topic,
            "Problems": problem_links
        }

        recommendations = {
            'weak_categories': weak_categories,
            'next_difficulty': suggested_difficulty,
            'ml_scores': ml_result['ml_scores'],
            'roadmap': roadmap
        }
        return recommendations
