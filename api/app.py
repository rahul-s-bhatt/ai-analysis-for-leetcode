from flask import Flask, render_template, request, jsonify
from GQLQuery import GQLQuery
from core.analytics import AnalyticsManager
from data_formatter import format_user_profile
import json
import asyncio
from asgiref.sync import async_to_sync
import logging
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['endpoint'])
ERROR_COUNT = Counter('http_request_errors_total', 'Total HTTP request errors', ['endpoint', 'error_type'])

app = Flask(__name__, static_folder='static', static_url_path='/static')
leetcode_api = GQLQuery()

def track_request_latency(endpoint):
    """Decorator to track request latency"""
    def decorator(f):
        def wrapped(*args, **kwargs):
            start_time = time.time()
            try:
                response = f(*args, **kwargs)
                REQUEST_COUNT.labels(
                    method=request.method,
                    endpoint=endpoint,
                    status=response[1] if isinstance(response, tuple) else 200
                ).inc()
                return response
            except Exception as e:
                ERROR_COUNT.labels(
                    endpoint=endpoint,
                    error_type=type(e).__name__
                ).inc()
                raise
            finally:
                REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.time() - start_time)
        wrapped.__name__ = f.__name__
        return wrapped
    return decorator

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
            ERROR_COUNT.labels(
                endpoint='/api/analysis',
                error_type=type(e).__name__
            ).inc()
            # Create analytics manager to get fallback analysis
            analytics_manager = AnalyticsManager({})
            return {
                "user_data": {},
                "analysis": analytics_manager._generate_fallback_analysis()
            }

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(fetch_and_analyze())
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Event loop error: {e}", exc_info=True)
        ERROR_COUNT.labels(
            endpoint='/api/analysis',
            error_type=type(e).__name__
        ).inc()
        # Return fallback analysis for event loop errors
        analytics_manager = AnalyticsManager({})
        return {
            "user_data": {},
            "analysis": analytics_manager._generate_fallback_analysis()
        }

@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes probes"""
    try:
        # Basic application health check
        return jsonify({
            "status": "healthy",
            "timestamp": time.time()
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/metrics')
def metrics():
    """Endpoint for Prometheus metrics"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/', methods=['GET', 'POST'])
@track_request_latency('index')
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
@track_request_latency('api_analysis')
def get_analysis(username):
    """API endpoint to get just the analysis"""
    result = analyze_user_data(username)
    if result is None:
        return jsonify({"error": "Failed to analyze user data"}), 400
    return jsonify(result["analysis"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
