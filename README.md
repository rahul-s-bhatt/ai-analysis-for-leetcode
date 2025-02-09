# AI-Powered LeetCode Profile Analyzer

An advanced analytics tool that provides deep insights into your LeetCode profile, helping you understand your coding patterns, track progress, and optimize your learning path.

## 🚀 Features

- **Profile Analysis**: Comprehensive analysis of your LeetCode profile using AI
- **Learning Path**: Personalized recommendations for skill improvement
- **Pattern Recognition**: Identify coding patterns in your solutions
- **Skill Assessment**: Detailed breakdown of your technical strengths
- **Contest Performance**: Analysis of your competition statistics

## 🛠 Tech Stack

- Python 3.11.5
- Flask for API and Web Interface
- GraphQL for LeetCode API Integration
- Async Processing for Performance
- Docker Support

## 📋 Prerequisites

- Python 3.11.5
- Docker (optional)

## 🔧 Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-analysis-for-leetcode.git
cd ai-analysis-for-leetcode
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Unix/macOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Docker Setup

1. Build the Docker image:
```bash
docker build -t leetcode-analyzer .
```

2. Run the container:
```bash
docker run -p 3000:3000 leetcode-analyzer
```

## 🚀 Usage

### Running Locally

1. Start the Flask application:
```bash
python api/app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Enter a LeetCode username to analyze

### API Endpoints

1. Web Interface:
- `GET /`: Home page with input form
- `POST /`: Submit username for analysis

2. API:
- `GET /api/analysis/<username>`: Get JSON analysis for a specific user

## 📊 Features in Detail

### Profile Analysis
- Submission history analysis
- Problem-solving patterns
- Language preferences
- Time complexity patterns

### Learning Path Generation
- Personalized problem recommendations
- Skill gap analysis
- Progress tracking
- Difficulty progression suggestions

### Pattern Recognition
- Common solution patterns
- Algorithmic preferences
- Time/space complexity trends
- Language-specific patterns

## 🔐 Security

The application uses:
- Rate limiting for API requests
- Error handling for failed requests
- Secure session management
- Input validation

## 🌐 Deployment

The application is Vercel-compatible and can be deployed directly using the included configuration files:
- `vercel.json`: Vercel deployment configuration
- `Dockerfile`: Container configuration
- `requirements.txt`: Python dependencies

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📝 License

This project is licensed under the terms of the LICENSE file included in the repository.

## 🔍 Issues and Support

For issues, feature requests, or support, please file an issue in the GitHub repository issue tracker.
