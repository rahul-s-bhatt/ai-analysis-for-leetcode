# Installation Guide

This guide walks you through setting up the AI Analysis for LeetCode project in your local environment.

## Prerequisites

- Python 3.8 or higher
- Docker (optional, for containerized deployment)
- Git

## Local Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/ai-analysis-for-leetcode.git
cd ai-analysis-for-leetcode
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configuration**
- Copy `.env.example` to `.env`
- Update environment variables with your settings

## Docker Installation

1. **Build the Docker Image**
```bash
docker build -t ai-leetcode-analyzer .
```

2. **Run the Container**
```bash
docker run -p 5000:5000 ai-leetcode-analyzer
```

## Verification

1. **Run Tests**
```bash
python test_setup.py
```

2. **Start the Application**
```bash
python api/app.py
```

3. **Access the Application**
- Open your browser and navigate to `http://localhost:5000`
- You should see the application dashboard

## Troubleshooting

### Common Issues

1. **Port Conflicts**
- If port 5000 is already in use, modify the port in `api/app.py` or use Docker port mapping

2. **Dependencies Issues**
- Ensure your Python version is compatible
- Try upgrading pip: `pip install --upgrade pip`
- Install dependencies one by one if bulk installation fails

### Getting Help

If you encounter any issues:
1. Check the [Issues](https://github.com/yourusername/ai-analysis-for-leetcode/issues) page
2. Create a new issue with detailed error information
3. Review the logs in the `logs` directory

## Next Steps

- Review the [API Documentation](API-Documentation)
- Explore the [Architecture Overview](Architecture)
- Learn how to [Contribute](Contributing) to the project