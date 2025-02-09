from flask import Flask, render_template, request
from GQLQuery import GQLQuery
from recommendations import ProblemRecommender
from data_formatter import format_user_profile
import asyncio
from asgiref.sync import async_to_sync
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
leetcode_api = GQLQuery()

def get_user_data(username):
    """Helper function to run async code in sync context"""
    async def fetch_data():
        try:
            data = await leetcode_api.get_user_complete_data(username)
            logger.debug(f"Raw API response: {data}")
            # The response from get_user_complete_data needs to match format_user_profile expectations
            return {
                "matchedUser": data["matchedUser"],
                "userContestRanking": data["userContestRanking"],
                "allQuestionsCount": data["allQuestionsCount"]
            }
        except Exception as e:
            logger.error(f"Error fetching data: {e}", exc_info=True)
            return None
    
    # Run async function in sync context
    return async_to_sync(fetch_data)()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        logger.info(f"Processing request for username: {username}")
        
        # Get complete user data and format it
        user_data = get_user_data(username)
        
        if user_data is None:
            logger.error(f"Failed to fetch data for user: {username}")
            return render_template('index.html', error="Failed to fetch user data. Please check the username and try again.")
        
        logger.debug(f"User data before formatting: {user_data}")    
        formatted_data = format_user_profile(user_data)
        logger.debug(f"Formatted user data: {formatted_data}")
        
        if formatted_data is None:
            logger.error(f"Failed to format data for user: {username}")
            return render_template('index.html', error="Failed to process user data. Please try again later.")
            
        # Generate recommendations
        recommender = ProblemRecommender(formatted_data)
        recommendations = recommender.get_recommendations()
        
        return render_template('results.html', 
                             username=username,
                             stats=formatted_data,
                             recommendations=recommendations)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
