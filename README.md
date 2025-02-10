# AI-Powered LeetCode Profile Analyzer

An advanced analytics tool that provides deep insights into your LeetCode profile, helping you understand your coding patterns, track progress, and optimize your learning path.

[![Security Scan](https://github.com/yourusername/ai-analysis-for-leetcode/actions/workflows/security.yml/badge.svg)](https://github.com/yourusername/ai-analysis-for-leetcode/actions/workflows/security.yml)
[![Dependency Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/yourusername/ai-analysis-for-leetcode/pulls?q=is%3Apr+author%3Aapp%2Fdependabot)
[![Security Policy](https://img.shields.io/badge/security-policy-brightgreen.svg)](SECURITY.md)

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

We take security seriously. Our security measures include:

- **Automated Security Scanning**: Weekly automated security scans using GitHub Actions
- **Dependency Management**: Automated dependency updates via Dependabot
- **Code Analysis**: 
  - CodeQL security scanning
  - Bandit for Python security checks
  - Safety for dependency vulnerability checks
- **API Security**:
  - Rate limiting for API requests
  - Input validation and sanitization
  - Secure session management
  - Error handling for failed requests

For reporting security issues or viewing our security policy, please see our [Security Policy](SECURITY.md).

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

Please review our [Security Policy](SECURITY.md) before contributing.

## 📝 License

This project is licensed under the terms of the LICENSE file included in the repository.

## 🔍 Issues and Support

For issues, feature requests, or support, please file an issue in the GitHub repository issue tracker.
