from flask import Flask, render_template, request, jsonify
from GQLQuery import GQLQuery
from core.analytics import AnalyticsManager
from data_formatter import format_user_profile
import json
import asyncio
from asgiref.sync import async_to_sync
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
leetcode_api = GQLQuery()

def analyze_user_data(username):
    """Helper function to fetch and analyze user data"""
    async def fetch_and_analyze():
        try:
            async with leetcode_api:  # Using context manager to handle session
                data = await leetcode_api.get_user_complete_data(username)
                logger.debug(f"Raw API response: {data}")
                if not data:
                    return None

                # Initialize analytics manager with the complete data
                analytics_manager = AnalyticsManager(data)
                analysis = analytics_manager.generate_complete_analysis()

                return {
                    "user_data": {
                        "matchedUser": data.get("matchedUser"),
                        "userContestRanking": data.get("userContestRanking"),
                        "allQuestionsCount": data.get("allQuestionsCount")
                    },
                    "analysis": analysis
                }
        except Exception as e:
            logger.error(f"Error analyzing data: {e}", exc_info=True)
            return None

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(fetch_and_analyze())
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Event loop error: {e}", exc_info=True)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        logger.info(f"Processing request for username: {username}")
        
        # Get and analyze user data
        result = analyze_user_data(username)
        
        if result is None:
            logger.error(f"Failed to fetch/analyze data for user: {username}")
            return render_template('index.html', 
                error="Failed to analyze user data. Please check the username and try again.")
        
        user_data = result["user_data"]
        analysis = result["analysis"]
        
        # Format base profile data
        formatted_data = format_user_profile(user_data)
        if formatted_data is None:
            logger.error(f"Failed to format data for user: {username}")
            return render_template('index.html', 
                error="Failed to process user data. Please try again later.")
        
        # Convert analysis to dict to ensure proper JSON serialization
        analysis_dict = json.loads(json.dumps(analysis))
        logger.debug(f"Analysis data being passed to template: {analysis_dict}")
        return render_template('results.html',
                             username=username,
                             stats=formatted_data,
                             analysis=analysis_dict)
    
    return render_template('index.html')

@app.route('/api/analysis/<username>')
def get_analysis(username):
    """API endpoint to get just the analysis"""
    result = analyze_user_data(username)
    if result is None:
        return jsonify({"error": "Failed to analyze user data"}), 400
    return jsonify(result["analysis"])

if __name__ == '__main__':
    app.run(debug=True)
