# Contributing Guidelines

Thank you for your interest in contributing to AI Analysis for LeetCode! This document outlines the process and guidelines for contributing to the project.

## Code of Conduct

Please note that this project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Report unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork the Repository**
   - Fork the repository on GitHub
   - Clone your fork locally
   ```bash
   git clone https://github.com/your-username/ai-analysis-for-leetcode.git
   ```

2. **Set Up Development Environment**
   - Follow the [Installation Guide](Installation-Guide)
   - Set up pre-commit hooks
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Development Workflow

### 1. Creating Issues

Before starting work:
- Check existing issues and pull requests
- Create a new issue describing the bug or feature
- Wait for issue to be approved/discussed

### 2. Branching Strategy

- Main branch: `main` (stable)
- Development branch: `dev`
- Feature branches: `feature/your-feature-name`
- Bug fix branches: `fix/issue-description`

```bash
# Create a new branch
git checkout -b feature/your-feature-name
```

### 3. Coding Standards

#### Python Code Style
- Follow PEP 8 guidelines
- Use type hints
- Maximum line length: 88 characters
- Use meaningful variable names
- Document classes and functions

Example:
```python
from typing import List, Optional

def analyze_pattern(
    submissions: List[dict],
    timeframe: Optional[str] = None
) -> dict:
    """
    Analyze problem-solving patterns from submissions.

    Args:
        submissions: List of submission dictionaries
        timeframe: Optional timeframe filter

    Returns:
        Dictionary containing pattern analysis results
    """
    # Implementation
```

#### Documentation
- Keep documentation up to date
- Add docstrings to all public functions
- Update README.md when adding features
- Include example usage where appropriate

### 4. Testing

#### Writing Tests
- Write tests for new features
- Update tests for bug fixes
- Maintain test coverage above 80%

```python
def test_pattern_analysis():
    """Test the pattern analysis functionality."""
    submissions = [
        {"problem": "Two Sum", "status": "Accepted"}
    ]
    result = analyze_pattern(submissions)
    assert "patterns" in result
    assert len(result["patterns"]) > 0
```

#### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=api
```

### 5. Submitting Changes

1. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add pattern analysis for dynamic programming"
   ```
   
   Commit Message Format:
   - feat: New feature
   - fix: Bug fix
   - docs: Documentation changes
   - test: Adding/updating tests
   - refactor: Code refactoring
   - style: Formatting changes
   - chore: Maintenance tasks

2. **Push Changes**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Open a pull request on GitHub
   - Link related issues
   - Provide clear description of changes
   - Add test results and coverage report
   - Request review from maintainers

### 6. Review Process

- Automated checks must pass
- At least one maintainer approval required
- Address review comments promptly
- Keep pull request focused and small

## Project Structure

```
ai-analysis-for-leetcode/
├── api/                  # Main application code
│   ├── core/            # Core functionality
│   │   ├── analytics/   # Analysis modules
│   │   └── utils/       # Utility functions
│   └── templates/       # HTML templates
├── docs/                # Documentation
├── tests/              # Test files
└── requirements.txt    # Dependencies
```

## Common Tasks

### Adding New Analytics Feature
1. Create new module in `api/core/analytics/`
2. Add unit tests in `tests/`
3. Update API documentation
4. Add example usage

### Fixing Bugs
1. Add failing test case
2. Fix the bug
3. Ensure all tests pass
4. Update documentation if needed

## Getting Help

- Check existing [documentation](https://github.com/yourusername/ai-analysis-for-leetcode/wiki)
- Open an issue for questions
- Join project discussions
- Contact maintainers

## Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to AI Analysis for LeetCode!