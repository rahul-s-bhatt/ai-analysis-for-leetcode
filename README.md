# LeetCode AI Insights

This project is an innovative web application designed to transform your LeetCode practice into a data-driven journey. By integrating advanced AI, it provides deep insights into your LeetCode performance, helping you understand your problem-solving patterns, identify weaknesses, and track your progress. The project delivers personalized recommendations to optimize your study path, aiming to significantly enhance your coding skills and problem-solving abilities.

## Authors

- [Rahul S. Bhatt]

## Features

### Iteration 1

- Clean, modern user interface
- Basic profile statistics visualization
- Problem-solving distribution by difficulty
- Profile performance overview
- Responsive design for all devices


## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualization**: Plotly.js
- **API Integration**: LeetCode GraphQL API

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd leetcode-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Visit the homepage
2. Enter a LeetCode username
3. View detailed profile analysis and statistics

## Project Structure

```
leetcode-analyzer/
├── app.py              # Main Flask application
├── Config.py           # Configuration settings
├── GQLQuery.py         # LeetCode API integration
├── requirements.txt    # Project dependencies
├── static/
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
└── templates/         # HTML templates
    ├── base.html
    ├── index.html
    ├── profile.html
    └── error.html
```

## Color Palette

- Primary Yellow: `#F4B400`
- Primary Blue: `#1D3557`
- Secondary Blue: `#457B9D`
- Neutral Blue: `#2E598A`
- Problem Difficulty Colors:
  - Easy: `#00B8A3`
  - Medium: `#FFC01E`
  - Hard: `#FF375F`

## Roadmap

### Iteration 1 (Current)
- Basic profile analysis
- Problem-solving statistics
- Simple visualizations

### Iteration 2 (Planned)
- Basic AI integration
- Enhanced data visualization
- Performance trends analysis

### Iteration 3 (Future)
- Advanced AI features
- Detailed skill analysis
- Personalized recommendations

## Contributing

Feel free to open issues and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](LICENSE)