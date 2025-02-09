"""
Setup verification script for LeetCode Profile Analysis.
Run this script to verify that all components are working correctly.
"""

import sys
import logging
from flask import Flask
from core.analytics import AnalyticsManager, PatternAnalyzer, SkillAnalyzer, LearningPathAnalyzer
from GQLQuery import GQLQuery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all required modules can be imported."""
    logger.info("Testing imports...")
    modules = [
        ('Flask', Flask),
        ('AnalyticsManager', AnalyticsManager),
        ('PatternAnalyzer', PatternAnalyzer),
        ('SkillAnalyzer', SkillAnalyzer),
        ('LearningPathAnalyzer', LearningPathAnalyzer),
        ('GQLQuery', GQLQuery)
    ]
    
    for name, module in modules:
        logger.info(f"✓ Successfully imported {name}")
    
    return True

def test_leetcode_api():
    """Test connection to LeetCode API."""
    logger.info("Testing LeetCode API connection...")
    try:
        api = GQLQuery()
        logger.info("✓ Successfully initialized LeetCode API client")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize LeetCode API client: {str(e)}")
        return False

def test_analytics_system():
    """Test analytics system initialization."""
    logger.info("Testing analytics system...")
    try:
        # Create a minimal test data structure
        test_data = {
            "matchedUser": {
                "submitStats": {
                    "acSubmissionNum": [
                        {"difficulty": "All", "count": 10, "submissions": 20}
                    ]
                },
                "tagProblemCounts": {
                    "advanced": [],
                    "intermediate": [],
                    "fundamental": []
                },
                "profile": {
                    "ranking": 100000
                }
            }
        }
        
        # Initialize analytics components
        analytics = AnalyticsManager(test_data)
        pattern_analyzer = PatternAnalyzer(test_data)
        skill_analyzer = SkillAnalyzer(test_data)
        learning_path_analyzer = LearningPathAnalyzer(test_data)
        
        # Test basic analysis generation
        analytics.generate_complete_analysis()
        logger.info("✓ Successfully initialized and tested analytics system")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to test analytics system: {str(e)}")
        return False

def run_all_tests():
    """Run all setup verification tests."""
    logger.info("Starting setup verification...")
    
    tests = [
        ("Import Test", test_imports),
        ("LeetCode API Test", test_leetcode_api),
        ("Analytics System Test", test_analytics_system)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            logger.info(f"\nRunning {name}...")
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"Test failed with error: {str(e)}")
            results.append((name, False))
    
    # Print summary
    logger.info("\n" + "="*50)
    logger.info("Test Summary:")
    logger.info("="*50)
    
    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{name}: {status}")
        if not result:
            all_passed = False
    
    logger.info("="*50)
    if all_passed:
        logger.info("All tests passed! The system is ready to use.")
        return 0
    else:
        logger.error("Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
