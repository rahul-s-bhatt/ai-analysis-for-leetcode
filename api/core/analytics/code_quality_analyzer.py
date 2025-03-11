from typing import Dict, Any, List
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

class CodeQualityAnalyzer:
    def __init__(self, user_data: Dict[str, Any]):
        """Initialize the code quality analyzer with user data."""
        self.user_data = user_data
        self.submissions = user_data.get("matchedUser", {}).get("recentSubmissionList", [])
        if not self.submissions:
            logger.warning("No submissions found in user data")

    def analyze_code_quality(self) -> Dict[str, Any]:
        """Analyze code quality across submissions."""
        try:
            logger.info("Starting code quality analysis")
            
            # Analyze complexity
            logger.debug("Analyzing code complexity")
            complexity_metrics = self._analyze_complexity()
            
            # Analyze optimization patterns
            logger.debug("Analyzing optimization patterns")
            optimization_patterns = self._analyze_optimization_patterns()
            
            # Analyze code style
            logger.debug("Analyzing code style")
            code_style = self._analyze_code_style()
            
            # Analyze solution efficiency
            logger.debug("Analyzing solution efficiency")
            solution_efficiency = self._analyze_solution_efficiency()
            
            result = {
                "complexity_metrics": complexity_metrics,
                "optimization_patterns": optimization_patterns,
                "code_style": code_style,
                "solution_efficiency": solution_efficiency
            }
            
            logger.info("Code quality analysis completed successfully")
            logger.debug(f"Analysis result: {result}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in analyze_code_quality: {str(e)}", exc_info=True)
            return {
                "complexity_metrics": {},
                "optimization_patterns": {
                    "identified_patterns": {"efficient_data_structures": {}},
                    "optimization_score": 0,
                    "recommendations": []
                },
                "code_style": {},
                "solution_efficiency": {
                    "metrics": {
                        "runtime_percentile": 0,
                        "memory_percentile": 0,
                        "optimization_ratio": 0
                    },
                    "overall_efficiency": 0,
                    "areas_for_improvement": []
                }
            }

    def _analyze_complexity(self) -> Dict[str, Any]:
        """Analyze time and space complexity patterns."""
        complexities = {
            "time": self._categorize_time_complexity(),
            "space": self._categorize_space_complexity()
        }

        # Calculate improvement trends
        complexity_trend = self._calculate_complexity_trend()
        
        return {
            "patterns": complexities,
            "trend": complexity_trend,
            "recommendations": self._generate_complexity_recommendations(complexities)
        }

    def _categorize_time_complexity(self) -> Dict[str, int]:
        """Categorize solutions by time complexity."""
        complexity_counts = {
            "O(1)": 0,
            "O(log n)": 0,
            "O(n)": 0,
            "O(n log n)": 0,
            "O(n²)": 0,
            "O(2ⁿ)": 0
        }

        for submission in self.submissions:
            if submission.get("statusDisplay") == "Accepted":
                runtime = submission.get("runtime", "")
                memory = submission.get("memory", "")
                
                # Estimate complexity based on runtime and input size
                estimated_complexity = self._estimate_complexity(runtime, memory)
                if estimated_complexity in complexity_counts:
                    complexity_counts[estimated_complexity] += 1

        return complexity_counts

    def _analyze_optimization_patterns(self) -> Dict[str, Any]:
        """Analyze optimization patterns in solutions."""
        patterns = {
            "efficient_data_structures": self._check_data_structure_usage(),
            "algorithm_optimization": self._analyze_algorithm_choices(),
            "memory_optimization": self._analyze_memory_usage()
        }

        return {
            "identified_patterns": patterns,
            "optimization_score": self._calculate_optimization_score(patterns),
            "recommendations": self._generate_optimization_recommendations(patterns)
        }

    def _check_data_structure_usage(self) -> Dict[str, float]:
        """Analyze the efficiency of data structure usage."""
        ds_usage = {
            "hash_tables": 0,
            "trees": 0,
            "heaps": 0,
            "arrays": 0,
            "linked_lists": 0
        }

        for submission in self.submissions:
            code = submission.get("code", "")
            if code:
                # Check for data structure usage patterns
                if "HashMap" in code or "dict" in code:
                    ds_usage["hash_tables"] += 1
                if "TreeMap" in code or "TreeSet" in code:
                    ds_usage["trees"] += 1
                if "PriorityQueue" in code or "heap" in code:
                    ds_usage["heaps"] += 1
                if "[]" in code or "List" in code:
                    ds_usage["arrays"] += 1
                if "LinkedList" in code or "next" in code:
                    ds_usage["linked_lists"] += 1

        total = sum(ds_usage.values()) or 1
        return {k: round(v/total * 100, 2) for k, v in ds_usage.items()}

    def _analyze_algorithm_choices(self) -> Dict[str, Any]:
        """Analyze algorithm selection patterns."""
        patterns = {
            "divide_and_conquer": 0,
            "dynamic_programming": 0,
            "greedy": 0,
            "brute_force": 0
        }

        total_submissions = len([s for s in self.submissions if s.get("statusDisplay") == "Accepted"]) or 1

        for submission in self.submissions:
            code = submission.get("code", "")
            if code:
                # Identify algorithm patterns
                if "memo" in code or "dp" in code:
                    patterns["dynamic_programming"] += 1
                elif "mid = " in code and "return" in code and ("left" in code or "right" in code):
                    patterns["divide_and_conquer"] += 1
                elif len(re.findall(r"for.*for", code)) > 1:
                    patterns["brute_force"] += 1
                else:
                    patterns["greedy"] += 1

        return {
            "patterns": {k: round(v/total_submissions * 100, 2) for k, v in patterns.items()},
            "preferred_approach": max(patterns.items(), key=lambda x: x[1])[0]
        }

    def _analyze_solution_efficiency(self) -> Dict[str, Any]:
        """Analyze the overall efficiency of solutions."""
        efficiency_metrics = {
            "runtime_percentile": self._calculate_runtime_percentile(),
            "memory_percentile": self._calculate_memory_percentile(),
            "optimization_ratio": self._calculate_optimization_ratio()
        }

        return {
            "metrics": efficiency_metrics,
            "overall_efficiency": sum(efficiency_metrics.values()) / len(efficiency_metrics),
            "areas_for_improvement": self._identify_efficiency_improvements(efficiency_metrics)
        }

    def _calculate_runtime_percentile(self) -> float:
        """Calculate the average runtime percentile across solutions."""
        runtime_beats = [
            float(s.get("runtimePercentile", 0))
            for s in self.submissions
            if s.get("statusDisplay") == "Accepted" and s.get("runtimePercentile")
        ]
        return round(sum(runtime_beats) / len(runtime_beats), 2) if runtime_beats else 0

    def _calculate_memory_percentile(self) -> float:
        """Calculate the average memory usage percentile across solutions."""
        memory_beats = [
            float(s.get("memoryPercentile", 0))
            for s in self.submissions
            if s.get("statusDisplay") == "Accepted" and s.get("memoryPercentile")
        ]
        return round(sum(memory_beats) / len(memory_beats), 2) if memory_beats else 0

    def _calculate_optimization_ratio(self) -> float:
        """Calculate the ratio of optimized solutions to total solutions."""
        optimized = len([
            s for s in self.submissions
            if s.get("statusDisplay") == "Accepted" 
            and (float(s.get("runtimePercentile", 0)) > 70 or float(s.get("memoryPercentile", 0)) > 70)
        ])
        total = len([s for s in self.submissions if s.get("statusDisplay") == "Accepted"]) or 1
        return round(optimized / total * 100, 2)

    def _identify_efficiency_improvements(self, metrics: Dict[str, float]) -> List[Dict[str, str]]:
        """Identify specific areas for efficiency improvement."""
        improvements = []

        if metrics["runtime_percentile"] < 50:
            improvements.append({
                "area": "Time Complexity",
                "suggestion": "Focus on optimizing algorithmic complexity and reducing unnecessary iterations"
            })

        if metrics["memory_percentile"] < 50:
            improvements.append({
                "area": "Space Complexity",
                "suggestion": "Look for opportunities to optimize memory usage and reduce unnecessary data structure overhead"
            })

        if metrics["optimization_ratio"] < 40:
            improvements.append({
                "area": "Solution Optimization",
                "suggestion": "Practice identifying and implementing more efficient algorithms and data structures"
            })

        return improvements

    def _estimate_complexity(self, runtime: str, memory: str) -> str:
        """Estimate time complexity based on runtime and memory usage patterns."""
        try:
            runtime_ms = float(runtime.replace("ms", ""))
            if runtime_ms < 1:
                return "O(1)"
            elif runtime_ms < 10:
                return "O(log n)"
            elif runtime_ms < 50:
                return "O(n)"
            elif runtime_ms < 200:
                return "O(n log n)"
            elif runtime_ms < 1000:
                return "O(n²)"
            else:
                return "O(2ⁿ)"
        except:
            return "O(n)"  # Default to linear if unable to determine

    def _calculate_complexity_trend(self) -> Dict[str, str]:
        """Calculate trends in solution complexity over time."""
        recent_submissions = sorted(
            [s for s in self.submissions if s.get("statusDisplay") == "Accepted"],
            key=lambda x: x.get("timestamp", 0)
        )[-10:]  # Look at last 10 accepted submissions

        if not recent_submissions:
            return {"trend": "Not enough data", "description": "Need more submissions to analyze trends"}

        # Calculate average runtime percentile for first and second half
        mid = len(recent_submissions) // 2
        first_half = sum(float(s.get("runtimePercentile", 0)) for s in recent_submissions[:mid]) / mid
        second_half = sum(float(s.get("runtimePercentile", 0)) for s in recent_submissions[mid:]) / (len(recent_submissions) - mid)

        if second_half - first_half > 10:
            return {
                "trend": "Improving",
                "description": "Your solutions are becoming more efficient over time"
            }
        elif first_half - second_half > 10:
            return {
                "trend": "Declining",
                "description": "Recent solutions could be more optimized"
            }
        else:
            return {
                "trend": "Stable",
                "description": "Maintaining consistent solution efficiency"
            }