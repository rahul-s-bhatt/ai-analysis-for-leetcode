from typing import Dict, Any, List
from datetime import datetime

class SkillAnalyzer:
    def __init__(self, user_data: Dict[str, Any]):
        self.user_data = user_data
        self.matched_user = user_data.get("matchedUser", {})
        self.contest_data = user_data.get("userContestRanking", {})
        self.contest_history = user_data.get("userContestRankingHistory", [])
        self.tag_counts = self.matched_user.get("tagProblemCounts", {})

    def analyze_skill_level(self) -> Dict[str, Any]:
        """Analyze overall skill level based on multiple factors"""
        contest_performance = self._analyze_contest_performance()
        problem_mastery = self._analyze_problem_mastery()
        relative_standing = self._analyze_relative_standing()

        return {
            "overall_rating": self._calculate_overall_rating(
                contest_performance,
                problem_mastery,
                relative_standing
            ),
            "contest_performance": contest_performance,
            "problem_mastery": problem_mastery,
            "relative_standing": relative_standing
        }

    def _analyze_contest_performance(self) -> Dict[str, Any]:
        """Analyze user's performance in contests"""
        rating = self.contest_data.get("rating", 0)
        attended_contests = self.contest_data.get("attendedContestsCount", 0)
        global_ranking = self.contest_data.get("globalRanking", 0)
        top_percentage = self.contest_data.get("topPercentage", 100)

        # Calculate rating level
        rating_level = "Elite" if rating > 2000 else \
                      "Advanced" if rating > 1600 else \
                      "Intermediate" if rating > 1200 else \
                      "Beginner"

        return {
            "rating": rating,
            "rating_level": rating_level,
            "contests_participated": attended_contests,
            "global_ranking": global_ranking,
            "percentile": round(100 - top_percentage, 2) if top_percentage else 0,
            "ranking_trend": self._analyze_ranking_trend()
        }

    def _analyze_problem_mastery(self) -> Dict[str, Any]:
        """Analyze mastery across problem types"""
        submit_stats = self.matched_user.get("submitStats", {})
        ac_submissions = submit_stats.get("acSubmissionNum", [])
        
        # Calculate difficulty-wise mastery
        difficulty_stats = {}
        for submission in ac_submissions:
            difficulty = submission.get("difficulty", "All")
            if difficulty != "All":
                count = submission.get("count", 0)
                total = submission.get("submissions", 0)
                success_rate = (count / total * 100) if total > 0 else 0
                difficulty_stats[difficulty] = {
                    "solved": count,
                    "total_attempts": total,
                    "success_rate": round(success_rate, 2)
                }

        # Calculate mastery levels
        mastery_levels = self._calculate_mastery_levels(difficulty_stats)

        return {
            "difficulty_stats": difficulty_stats,
            "mastery_levels": mastery_levels,
            "total_solved": sum(stat.get("solved", 0) for stat in difficulty_stats.values())
        }

    def _analyze_relative_standing(self) -> Dict[str, Any]:
        """Analyze user's standing relative to others"""
        beats_stats = self.matched_user.get("problemsSolvedBeatsStats", [])
        
        percentiles = {}
        for stat in beats_stats:
            difficulty = stat.get("difficulty", "")
            percentage = stat.get("percentage", 0)
            if difficulty:
                percentiles[difficulty] = round(percentage, 2)

        return {
            "percentiles": percentiles,
            "overall_standing": self._calculate_overall_standing(percentiles)
        }

    def _analyze_ranking_trend(self) -> Dict[str, str]:
        """Analyze trend in contest rankings"""
        if not self.contest_history:
            return {"trend": "Not enough data", "description": "Participate in contests to see your trend"}

        recent_contests = sorted(
            self.contest_history,
            key=lambda x: x.get("contest", {}).get("startTime", ""),
            reverse=True
        )[:5]  # Look at last 5 contests

        ratings = [contest.get("rating", 0) for contest in recent_contests]
        if not ratings:
            return {"trend": "No data", "description": "No recent contest data available"}

        # Calculate trend
        if len(ratings) >= 2:
            trend = "Improving" if ratings[0] > ratings[-1] else \
                   "Declining" if ratings[0] < ratings[-1] else "Stable"
        else:
            trend = "Not enough data"

        descriptions = {
            "Improving": "Your contest performance is on an upward trend",
            "Declining": "Your recent contest performance shows room for improvement",
            "Stable": "Your contest performance has been consistent",
            "Not enough data": "Participate in more contests to establish a trend"
        }

        return {
            "trend": trend,
            "description": descriptions[trend]
        }

    def _calculate_mastery_levels(self, difficulty_stats: Dict[str, Dict]) -> Dict[str, str]:
        """Calculate mastery level for each difficulty"""
        mastery_levels = {}
        
        for difficulty, stats in difficulty_stats.items():
            success_rate = stats["success_rate"]
            solved_count = stats["solved"]
            
            if solved_count > 50 and success_rate > 80:
                level = "Master"
            elif solved_count > 30 and success_rate > 60:
                level = "Advanced"
            elif solved_count > 10 and success_rate > 40:
                level = "Intermediate"
            else:
                level = "Beginner"
                
            mastery_levels[difficulty] = level
            
        return mastery_levels

    def _calculate_overall_standing(self, percentiles: Dict[str, float]) -> Dict[str, Any]:
        """Calculate overall standing based on percentiles"""
        if not percentiles:
            return {
                "level": "Unranked",
                "description": "Not enough data to determine standing"
            }

        avg_percentile = sum(percentiles.values()) / len(percentiles)
        
        if avg_percentile > 90:
            level = "Top Performer"
            description = "You're among the top performers in the community"
        elif avg_percentile > 70:
            level = "Advanced"
            description = "You're performing well above average"
        elif avg_percentile > 50:
            level = "Competent"
            description = "You're performing above average"
        else:
            level = "Developing"
            description = "You're making progress and have room to grow"

        return {
            "level": level,
            "description": description,
            "average_percentile": round(avg_percentile, 2)
        }

    def _calculate_overall_rating(self, contest_perf: Dict, problem_mastery: Dict, relative_standing: Dict) -> Dict[str, Any]:
        """Calculate overall rating considering all factors"""
        # Weights for different components
        weights = {
            "contest": 0.3,
            "problem_solving": 0.4,
            "relative_standing": 0.3
        }

        # Calculate contest score (0-100)
        contest_score = min(100, (contest_perf.get("rating", 0) / 3000) * 100)

        # Calculate problem solving score
        total_solved = problem_mastery.get("total_solved", 0)
        problem_score = min(100, (total_solved / 500) * 100)  # Assuming 500 problems is excellent

        # Get relative standing score
        standing_score = relative_standing.get("percentiles", {}).get("All", 50)

        # Calculate weighted average
        final_score = (
            weights["contest"] * contest_score +
            weights["problem_solving"] * problem_score +
            weights["relative_standing"] * standing_score
        )

        # Determine level
        level = "Elite" if final_score > 90 else \
                "Advanced" if final_score > 70 else \
                "Intermediate" if final_score > 50 else \
                "Beginner"

        return {
            "score": round(final_score, 2),
            "level": level,
            "component_scores": {
                "contest_performance": round(contest_score, 2),
                "problem_solving": round(problem_score, 2),
                "community_standing": round(standing_score, 2)
            }
        }
    
    def get_complete_skill_analysis(self) -> Dict[str, Any]:
        """Get complete skill analysis report"""
        skill_analysis = self.analyze_skill_level()
        weak_topics = self.analyze_topic_performance()
        
        return {
            "overall_rating": skill_analysis["overall_rating"],
            "detailed_analysis": {
                "contest_performance": skill_analysis["contest_performance"],
                "problem_mastery": skill_analysis["problem_mastery"],
                "relative_standing": skill_analysis["relative_standing"],
                "weak_topics": weak_topics,
                "skill_progression": self._generate_skill_progression(),
                "topic_mastery": self._generate_topic_mastery_scores(),
                "solving_patterns": self._analyze_solving_patterns(),
                "learning_velocity": self._calculate_learning_velocity()
            },
            "recommendations": self._generate_skill_recommendations(skill_analysis)
        }
    
    def analyze_topic_performance(self) -> List[Dict[str, Any]]:
        """Analyze performance across different topics/tags and identify weakest areas"""
        # Combine topics across all difficulty levels
        all_topics = self._combine_topic_stats()
        
        # Calculate completion rates and sort by performance
        topic_stats = []
        for tag_name, stats in all_topics.items():
            completion_rate = round((stats["solved"] / stats["total"] * 100), 2) if stats["total"] > 0 else 0
            topic_stats.append({
                "name": tag_name,
                "solved": stats["solved"],
                "total": stats["total"],
                "completion_rate": completion_rate,
                "recommendation": self._generate_topic_recommendation(tag_name, completion_rate)
            })
        
        # Sort by completion rate and return bottom 3
        return sorted(topic_stats, key=lambda x: x["completion_rate"])[:3]

    def _combine_topic_stats(self) -> Dict[str, Dict[str, int]]:
        """Combine topic statistics across all difficulty levels"""
        all_topics = {}
        
        for level in ["fundamental", "intermediate", "advanced"]:
            for topic in self.tag_counts.get(level, []):
                tag_name = topic["tagName"]
                if tag_name not in all_topics:
                    all_topics[tag_name] = {
                        "solved": topic["problemsSolved"],
                        "total": topic["problemsSolved"]  # Using solved as base for total
                    }
                else:
                    all_topics[tag_name]["solved"] += topic["problemsSolved"]
                    all_topics[tag_name]["total"] += topic["problemsSolved"]

        # Add buffer to total problems to account for unlocked/unavailable problems
        for stats in all_topics.values():
            stats["total"] = max(stats["total"] + 5, int(stats["total"] * 1.2))

        return all_topics

    def _generate_topic_recommendation(self, tag_name: str, completion_rate: float) -> str:
        """Generate personalized recommendation for a topic"""
        if completion_rate < 20:
            return f"Focus on building fundamentals in {tag_name}. Start with easier problems to build confidence."
        elif completion_rate < 40:
            return f"Continue practicing {tag_name} problems. Try mixing easy and medium difficulty problems."
        else:
            return f"While {tag_name} needs improvement, you're making progress. Focus on medium and hard problems."

    def _generate_skill_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate personalized skill improvement recommendations"""
        recommendations = []
        
        # Contest-based recommendations
        contest_perf = analysis["contest_performance"]
        if contest_perf["contests_participated"] < 5:
            recommendations.append({
                "type": "contest",
                "message": "Participate in more contests to improve your competitive programming skills",
                "priority": "high"
            })

        # Problem mastery recommendations
        problem_mastery = analysis["problem_mastery"]
        for difficulty, level in problem_mastery["mastery_levels"].items():
            if level in ["Beginner", "Intermediate"]:
                recommendations.append({
                    "type": "mastery",
                    "message": f"Focus on improving your {difficulty} problem-solving skills",
                    "priority": "medium"
                })

        return recommendations

    def _generate_skill_progression(self) -> List[Dict[str, Any]]:
        """Generate skill progression timeline data"""
        submissions = self.matched_user.get("recentSubmissionList", [])
        if not submissions:
            return []

        # Sort submissions by timestamp
        sorted_submissions = sorted(
            submissions,
            key=lambda x: x.get("timestamp", 0)
        )

        # Calculate cumulative score over time
        progression = []
        total_solved = 0
        running_difficulty_score = 0

        for submission in sorted_submissions:
            if submission.get("statusDisplay") == "Accepted":
                total_solved += 1
                # Weight by difficulty
                difficulty = submission.get("difficulty", "")
                difficulty_score = {
                    "Easy": 1,
                    "Medium": 2,
                    "Hard": 4
                }.get(difficulty, 1)
                
                running_difficulty_score += difficulty_score

                # Calculate weighted score
                score = (running_difficulty_score / total_solved) * (total_solved ** 0.5)
                
                progression.append({
                    "date": datetime.fromtimestamp(submission.get("timestamp", 0)).strftime("%Y-%m-%d"),
                    "score": round(score, 2),
                    "total_solved": total_solved,
                    "difficulty": difficulty
                })

        # Return last 30 data points for better visualization
        return progression[-30:] if len(progression) > 30 else progression

    def _generate_topic_mastery_scores(self) -> Dict[str, float]:
        """Generate topic mastery scores for visualization"""
        topic_stats = self._combine_topic_stats()
        topic_scores = {}
        
        for topic, stats in topic_stats.items():
            # Calculate base completion score
            completion_rate = (stats["solved"] / stats["total"]) if stats["total"] > 0 else 0
            
            # Calculate success rate from submissions if available
            success_rate = 0
            topic_submissions = [s for s in self.matched_user.get("recentSubmissionList", [])
                               if topic in s.get("topicTags", [])]
            if topic_submissions:
                successful = len([s for s in topic_submissions if s.get("statusDisplay") == "Accepted"])
                success_rate = successful / len(topic_submissions)
            
            # Calculate final score combining completion and success rate
            final_score = (completion_rate * 0.7 + success_rate * 0.3) * 100
            topic_scores[topic] = round(min(final_score, 100), 2)
        
        # Return top 8 topics for better visualization
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_topics[:8])

    def _analyze_solving_patterns(self) -> Dict[str, float]:
        """Analyze problem-solving patterns and approaches"""
        submissions = self.matched_user.get("recentSubmissionList", [])
        if not submissions:
            return {}

        patterns = {
            "First Try Success": 0,  # Problems solved on first attempt
            "Analytical": 0,         # Quick solutions with optimal approach
            "Iterative": 0,         # Multiple attempts with improvement
            "Persistent": 0         # Eventually solved after many attempts
        }

        # Group submissions by problem ID to analyze attempt patterns
        problem_attempts = {}
        for sub in submissions:
            prob_id = sub.get("problemId")
            if prob_id:
                if prob_id not in problem_attempts:
                    problem_attempts[prob_id] = []
                problem_attempts[prob_id].append(sub)

        total_problems = len(problem_attempts)
        if total_problems == 0:
            return patterns
    
    def _calculate_learning_velocity(self) -> Dict[str, int]:
        """Calculate learning velocity (problems solved over time)"""
        submissions = self.matched_user.get("recentSubmissionList", [])
        if not submissions:
            return {}

        # Group accepted submissions by date
        daily_solved = {}
        for sub in submissions:
            if sub.get("statusDisplay") == "Accepted":
                date = datetime.fromtimestamp(sub.get("timestamp", 0)).strftime("%Y-%m-%d")
                if date not in daily_solved:
                    daily_solved[date] = set()  # Use set to avoid counting same problem twice
                daily_solved[date].add(sub.get("problemId"))

        # Convert to daily counts and get last 7 days
        velocity_data = {}
        dates = sorted(daily_solved.keys())[-7:]  # Last 7 days
        for date in dates:
            velocity_data[date] = len(daily_solved[date])

        return velocity_data

        # Analyze patterns for each problem
        for attempts in problem_attempts.values():
            attempts = sorted(attempts, key=lambda x: x.get("timestamp", 0))
            success = any(a.get("statusDisplay") == "Accepted" for a in attempts)
            
            if success:
                if len(attempts) == 1:
                    patterns["First Try Success"] += 1
                elif len(attempts) <= 3:
                    patterns["Analytical"] += 1
                elif len(attempts) <= 5:
                    patterns["Iterative"] += 1
                else:
                    patterns["Persistent"] += 1

        # Convert to percentages
        for key in patterns:
            patterns[key] = round((patterns[key] / total_problems) * 100, 2)

        return patterns
