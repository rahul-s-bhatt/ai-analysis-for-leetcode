# Weakest Topics Feature Implementation Plan

## Overview
Add functionality to identify and display a user's three weakest topics in LeetCode, along with relevant statistics and visualizations.

## Backend Implementation

### 1. Analytics Component Updates
Extend `SkillAnalyzer` class with new methods:
```python
def analyze_topic_performance(self):
    """Analyze performance across different topics/tags"""
    # Get topic problem counts from user data
    tag_counts = self.matched_user.get("tagProblemCounts", {})
    
    # Combine all difficulty levels
    all_topics = {}
    for level in ["fundamental", "intermediate", "advanced"]:
        for topic in tag_counts.get(level, []):
            tag_name = topic["tagName"]
            if tag_name not in all_topics:
                all_topics[tag_name] = {
                    "solved": topic["problemsSolved"],
                    "total": 0  # Will be populated from problems list
                }
            else:
                all_topics[tag_name]["solved"] += topic["problemsSolved"]
    
    # Get total problems per topic from problems list API
    # Calculate completion rates and sort
    topic_stats = self._calculate_topic_stats(all_topics)
    
    # Return top 3 weakest topics
    return sorted(topic_stats, key=lambda x: x["completion_rate"])[:3]
```

### 2. API Route Updates
Add new endpoint in `app.py`:
```python
@app.route("/api/user/<username>/weak-topics")
async def get_weak_topics(username):
    """Get user's weakest topics with statistics"""
    user_data = await gql_query.get_user_complete_data(username)
    analyzer = SkillAnalyzer(user_data)
    weak_topics = analyzer.analyze_topic_performance()
    return jsonify(weak_topics)
```

## Frontend Implementation

### 1. UI Component
Add new card section in results.html after the "Priority Areas" section:

```html
<!-- Weakest Topics Analysis -->
<div class="card stat-card">
    <div class="card-header">
        <h3>Areas for Improvement</h3>
    </div>
    <div class="card-body">
        <div id="weakTopicsChart" class="chart-container"></div>
        <div class="mt-4">
            {% for topic in analysis.weak_topics %}
            <div class="recommendation-item priority-high mb-3">
                <h5>{{ topic.name }}</h5>
                <p>Solved: {{ topic.solved }}/{{ topic.total }} ({{ topic.completion_rate }}%)</p>
                <p>{{ topic.recommendation }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
```

### 2. Chart Implementation
Add new chart initialization in the JavaScript section:

```javascript
// Weak Topics Chart
if (analysisData.weak_topics) {
    const weakTopicsCtx = document.getElementById('weakTopicsChart').getContext('2d');
    new Chart(weakTopicsCtx, {
        type: 'bar',
        data: {
            labels: analysisData.weak_topics.map(topic => topic.name),
            datasets: [
                {
                    label: 'Solved Problems',
                    data: analysisData.weak_topics.map(topic => topic.solved),
                    backgroundColor: '#28a745'
                },
                {
                    label: 'Total Problems',
                    data: analysisData.weak_topics.map(topic => topic.total),
                    backgroundColor: '#dc3545'
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Problems'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Topics'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Progress in Challenging Topics'
                }
            }
        }
    });
}
```

## Testing Plan

1. Unit Tests:
- Test topic performance analysis logic
- Verify correct calculation of completion rates
- Test sorting and selection of weakest topics

2. Integration Tests:
- Verify API endpoint returns correct data
- Test data flow from backend to frontend
- Validate chart rendering with different data scenarios

3. Manual Testing:
- Verify UI appearance and responsiveness
- Check chart interactivity
- Validate recommendations display

## Implementation Steps

1. Backend Development:
- [ ] Implement topic performance analysis methods
- [ ] Add new API endpoint
- [ ] Write unit tests
- [ ] Update existing analytics pipelines

2. Frontend Development:
- [ ] Add new UI card component
- [ ] Implement chart visualization
- [ ] Style improvements section
- [ ] Add responsive design adjustments

3. Testing & Deployment:
- [ ] Run unit and integration tests
- [ ] Perform manual testing
- [ ] Update documentation
- [ ] Deploy changes

## Next Steps

After reviewing this plan, we should:
1. Proceed with backend implementation first
2. Update the frontend in parallel
3. Integrate and test the complete feature
4. Deploy the changes