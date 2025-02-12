# LeetCode Analysis System

An advanced analytics tool that provides deep insights into your LeetCode profile, helping you understand your coding patterns, track progress, and optimize your learning path.

[![Security Scan](https://github.com/yourusername/ai-analysis-for-leetcode/actions/workflows/security.yml/badge.svg)](https://github.com/yourusername/ai-analysis-for-leetcode/actions/workflows/security.yml)
[![Dependency Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/yourusername/ai-analysis-for-leetcode/pulls?q=is%3Apr+author%3Aapp%2Fdependabot)
[![Security Policy](https://img.shields.io/badge/security-policy-brightgreen.svg)](SECURITY.md)

## Architecture Overview

The system is built with a modern, scalable architecture:

- Flask-based REST API with async support
- Redis caching layer
- Prometheus metrics and Grafana dashboards
- Kubernetes deployment with high availability
- Automated CI/CD pipeline

## Prerequisites

- Docker
- Kubernetes cluster (v1.21+)
- kubectl
- GitHub account (for CI/CD)

## Local Development

1. Set up the virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the application:
```bash
python -m flask --app api.app run --debug
```

## Docker Build

Build the container:
```bash
docker build -t leetcode-analysis-api .
```

Run locally:
```bash
docker run -p 8080:8080 leetcode-analysis-api
```

## Kubernetes Deployment

1. Create the namespace:
```bash
kubectl apply -f k8s/base/namespace.yaml
```

2. Deploy Redis:
```bash
kubectl apply -f k8s/base/redis-deployment.yaml
```

3. Deploy the API:
```bash
kubectl apply -f k8s/base/api-deployment.yaml
```

4. Deploy monitoring:
```bash
kubectl apply -f k8s/monitoring/prometheus.yaml
kubectl apply -f k8s/monitoring/grafana.yaml
```

## Monitoring

Access monitoring dashboards:

- Prometheus: `http://localhost:9090` (after port-forward)
- Grafana: `http://localhost:3000` (after port-forward)

Default Grafana credentials:
- Username: admin
- Password: admin123

## CI/CD Pipeline

The system uses GitHub Actions for:
- Automated testing
- Security scanning
- Container building
- Kubernetes deployment

Pipeline workflow is defined in `.github/workflows/main.yml`

## Security

Security measures implemented:
- Container security scanning
- Dependency vulnerability checks
- RBAC for Kubernetes resources
- Network policies
- Regular security updates

## Health Checks

The API provides health check endpoints:
- `/health` - Basic application health
- `/metrics` - Prometheus metrics

## API Documentation

### Endpoints

#### GET /api/analysis/{username}
Get analysis for a specific LeetCode user.

Response:
```json
{
    "analysis": {
        "coding_patterns": {...},
        "skill_assessment": {...},
        "recommendations": {...}
    }
}
```

#### POST /
Web interface for user analysis.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

Please review our [Security Policy](SECURITY.md) before contributing.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
