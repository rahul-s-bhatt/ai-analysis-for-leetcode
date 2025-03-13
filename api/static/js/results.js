// Chart configuration and initialization
let analysisData, statsData;

// Log raw data for debugging
console.log('Raw analysis:', analysisDataRaw);
console.log('Raw stats:', statsDataRaw);

try {
    // Parse data
    analysisData = JSON.parse(analysisDataRaw);
    statsData = JSON.parse(statsDataRaw);
    
    // Log parsed data
    console.log('Parsed analysis data:', analysisData);
    console.log('Parsed stats data:', statsData);
    
    if (!analysisData || !statsData) {
        throw new Error('Missing data');
    }
} catch (error) {
    console.error('Error parsing data:', error);
    // Set defaults to prevent undefined errors
    analysisData = {
        detailed_analysis: { skill_assessment: { detailed_analysis: {} } },
        recommendations: {},
        summary: {}
    };
    statsData = { stats: {} };
}

// ML Helper Functions
function getMLConfidenceData(metricName) {
    const mlMetrics = {
        'Coding Style': {
            confidence: analysisData.coding_personality?.problem_solving_style?.confidence_metrics?.pattern_strength * 100 || 0,
            samples: analysisData.coding_personality?.problem_solving_style?.confidence_metrics?.sample_size || 0
        },
        'Skill Level': {
            confidence: analysisData.code_quality_metrics?.solution_efficiency?.metrics?.optimization_ratio * 100 || 0,
            samples: analysisData.detailed_analysis?.skill_assessment?.detailed_analysis?.total_submissions || 0
        },
        'Overall Score': {
            confidence: analysisData.learning_insights?.learning_patterns?.consistency_score * 100 || 0,
            samples: analysisData.detailed_analysis?.skill_assessment?.detailed_analysis?.assessed_problems?.length || 0
        }
    };
    return mlMetrics[metricName] || { confidence: 0, samples: 0 };
}

function enhanceChartWithML(chart, type) {
    const mlInsights = analysisData.learning_insights?.ml_predictions?.[type] || {};
    if (Object.keys(mlInsights).length > 0) {
        chart.options.plugins.annotation = {
            annotations: {
                mlPrediction: {
                    type: 'line',
                    borderColor: 'rgba(236, 72, 153, 0.5)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    label: {
                        content: 'ML Prediction',
                        enabled: true,
                        position: 'end'
                    },
                    scaleID: 'y',
                    value: mlInsights.predicted_value || 0
                }
            }
        };
        chart.update();
    }
}

// Chart.js Global Configuration
Chart.defaults.color = '#CBD5E1';
Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(0, 0, 0, 0.95)';
Chart.defaults.plugins.tooltip.titleFont = { family: "'Plus Jakarta Sans', sans-serif" };
Chart.defaults.plugins.tooltip.bodyFont = { family: "'Plus Jakarta Sans', sans-serif" };

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Interactive Components
    const initializeInteractiveComponents = () => {
        // Progress Bar
        const progressBar = document.getElementById('progress-bar');
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progressBar.style.width = scrolled + '%';
        });

        // Initialize Tooltips
        tippy('[data-tippy-content]', {
            theme: 'ml-insight',
            placement: 'top',
            animation: 'shift-away',
            duration: [200, 150],
            onShow(instance) {
                // Add ML confidence data for tooltips
                if (instance.reference.classList.contains('stat-card')) {
                    const metricName = instance.reference.querySelector('h5').textContent;
                    const confidenceData = getMLConfidenceData(metricName);
                    instance.setContent(`
                        ${instance.props.content}
                        <div class="metric-details">
                            <div>Confidence: ${confidenceData.confidence}%</div>
                            <div>Based on ${confidenceData.samples} samples</div>
                        </div>
                    `);
                }
            }
        });

        // Add intersection observers for animations
        const observerOptions = {
            threshold: 0.2,
            rootMargin: '0px 0px -50px 0px'
        };

        const animateOnScroll = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    animateOnScroll.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.chart-container, .stat-card, .glass-card').forEach(el => {
            animateOnScroll.observe(el);
        });
    };


    // Scroll to Top Button
    const scrollTopBtn = document.getElementById('scroll-top');
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Helper function to show/hide no-data message
    const showNoDataMessage = (containerId) => {
        const container = document.getElementById(containerId);
        if (container) {
            const noDataMessage = container.querySelector('.no-data-message');
            if (noDataMessage) {
                noDataMessage.style.display = 'block';
            }
        }
    };

    try {
        // Show/hide no-data messages based on data availability
        console.log('Checking data availability');
        if (!analysisData?.detailed_analysis?.skill_assessment?.detailed_analysis?.skill_progression?.length) {
            showNoDataMessage('skillTimelineChart');
        }
        if (!Object.keys(analysisData?.detailed_analysis?.skill_assessment?.detailed_analysis?.topic_mastery || {}).length) {
            showNoDataMessage('topicMatrixChart');
        }
        if (!Object.keys(analysisData?.detailed_analysis?.skill_assessment?.detailed_analysis?.solving_patterns || {}).length) {
            showNoDataMessage('patternRadarChart');
        }
        if (!Object.Keys(analysisData?.detailed_analysis?.skill_assessment?.detailed_analysis?.learning_velocity || {}).length) {
            showNoDataMessage('velocityChart');
        }
        if (!analysisData?.code_quality_metrics?.complexity_metrics?.patterns) {
            showNoDataMessage('complexityChart');
        }

        // Initialize ML charts and visualizations
        const initializeMLCharts = () => {
            const weakTopicsChart = new Chart(document.getElementById('weakTopicsChart').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: analysisData.detailed_analysis?.skill_assessment?.detailed_analysis?.weak_topics?.map(t => t.name) || [],
                    datasets: [
                        {
                            label: 'Solved Problems',
                            data: analysisData.detailed_analysis?.skill_assessment?.detailed_analysis?.weak_topics?.map(t => t.solved) || [],
                            backgroundColor: 'rgba(16, 185, 129, 0.7)',
                            borderColor: 'rgba(16, 185, 129, 1)',
                            borderWidth: 2
                        },
                        {
                            label: 'ML Predicted Difficulty',
                            data: analysisData.detailed_analysis?.skill_assessment?.ml_insights?.topic_difficulty?.values || [],
                            type: 'line',
                            borderColor: 'rgba(99, 102, 241, 0.8)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            fill: false,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                afterBody: function(context) {
                                    const idx = context[0].dataIndex;
                                    const topic = analysisData.detailed_analysis?.skill_assessment?.detailed_analysis?.weak_topics?.[idx];
                                    if (topic) {
                                        const mlConfidence = analysisData.detailed_analysis?.skill_assessment?.ml_insights?.confidence_scores?.[topic.name];
                                        return mlConfidence ? `ML Confidence: ${(mlConfidence * 100).toFixed(1)}%` : '';
                                    }
                                    return '';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        },
                        x: {
                            grid: { display: false }
                        }
                    }
                }
            });

            // Add ML insights to existing charts
            enhanceChartWithML(skillTimelineChart, 'skill_progression');
            enhanceChartWithML(topicMatrixChart, 'topic_mastery');
            enhanceChartWithML(patternRadarChart, 'solving_patterns');
        };

        // Initialize all charts
        initializeCharts();
        initializeMLCharts();

        // Add intersection observer for fade-in animations
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in');
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.1 }
        );

        document.querySelectorAll('.glass-card').forEach(card => {
            observer.observe(card);
        });

    } catch (error) {
        console.error('Error initializing charts:', error);
    }
});

function initializeCharts() {
    // Weak Topics Chart
    const weakTopics = analysisData.detailed_analysis?.skill_assessment?.detailed_analysis?.weak_topics;
    if (weakTopics?.length > 0) {
        const weakTopicsCtx = document.getElementById('weakTopicsChart').getContext('2d');
        new Chart(weakTopicsCtx, {
            type: 'bar',
            data: {
                labels: weakTopics.map(topic => topic.name),
                datasets: [
                    {
                        label: 'Solved Problems',
                        data: weakTopics.map(topic => topic.solved),
                        backgroundColor: 'rgba(16, 185, 129, 0.7)',
                        borderColor: 'rgba(16, 185, 129, 1)',
                        borderWidth: 2
                    },
                    {
                        label: 'Total Problems',
                        data: weakTopics.map(topic => topic.total),
                        backgroundColor: 'rgba(236, 72, 153, 0.7)',
                        borderColor: 'rgba(236, 72, 153, 1)',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Difficulty Distribution Chart
    const practiceStrategy = analysisData?.recommendations?.practice_strategy || {};
    if (practiceStrategy?.difficulty_distribution && Object.keys(practiceStrategy.difficulty_distribution).length > 0) {
        const diffCtx = document.getElementById('difficultyChart').getContext('2d');
        new Chart(diffCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(practiceStrategy.difficulty_distribution),
                datasets: [{
                    data: Object.values(practiceStrategy.difficulty_distribution),
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.7)',
                        'rgba(245, 158, 11, 0.7)',
                        'rgba(236, 72, 153, 0.7)'
                    ],
                    borderColor: [
                        '#10B981',
                        '#F59E0B',
                        '#EC4899'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }

    // Time Allocation Chart
    if (practiceStrategy?.time_allocation) {
        const timeCtx = document.getElementById('timeAllocationChart').getContext('2d');
        new Chart(timeCtx, {
            type: 'polarArea',
            data: {
                labels: Object.keys(practiceStrategy.time_allocation),
                datasets: [{
                    data: Object.values(practiceStrategy.time_allocation),
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.7)',
                        'rgba(111, 66, 193, 0.7)',
                        'rgba(32, 201, 151, 0.7)'
                    ],
                    borderColor: [
                        '#6366F1',
                        '#6F42C1',
                        '#20C997'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }

    // Skill Timeline Chart
    const skillData = analysisData?.detailed_analysis?.skill_assessment?.detailed_analysis?.skill_progression || [];
    if (skillData && skillData.length > 0) {
        const skillCtx = document.getElementById('skillTimelineChart').getContext('2d');
        new Chart(skillCtx, {
            type: 'line',
            data: {
                labels: skillData.map(entry => entry.date),
                datasets: [{
                    label: 'Skill Progress',
                    data: skillData.map(entry => entry.score),
                    borderColor: '#6366F1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(30, 41, 59, 0.9)',
                        titleColor: '#F8FAFC',
                        bodyColor: '#CBD5E1'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Topic Matrix Chart
    const topicMastery = analysisData.detailed_analysis?.skill_assessment?.detailed_analysis?.topic_mastery || {};
    if (Object.keys(topicMastery).length > 0) {
        const matrixCtx = document.getElementById('topicMatrixChart').getContext('2d');
        new Chart(matrixCtx, {
            type: 'radar',
            data: {
                labels: Object.keys(topicMastery),
                datasets: [{
                    label: 'Topic Mastery',
                    data: Object.values(topicMastery),
                    backgroundColor: 'rgba(236, 72, 153, 0.2)',
                    borderColor: '#EC4899',
                    borderWidth: 2,
                    pointBackgroundColor: '#EC4899'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        ticks: {
                            display: false
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }

    // Pattern Radar Chart
    const patterns = analysisData.detailed_analysis?.skill_assessment?.detailed_analysis?.solving_patterns || {};
    if (Object.keys(patterns).length > 0) {
        const patternCtx = document.getElementById('patternRadarChart').getContext('2d');
        new Chart(patternCtx, {
            type: 'polarArea',
            data: {
                labels: Object.keys(patterns),
                datasets: [{
                    data: Object.values(patterns),
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.7)',
                        'rgba(236, 72, 153, 0.7)',
                        'rgba(16, 185, 129, 0.7)',
                        'rgba(245, 158, 11, 0.7)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }

    // Learning Velocity Chart
    const velocityData = analysisData.detailed_analysis?.skill_assessment?.detailed_analysis?.learning_velocity || {};
    if (Object.keys(velocityData).length > 0) {
        const velocityCtx = document.getElementById('velocityChart').getContext('2d');
        new Chart(velocityCtx, {
            type: 'line',
            data: {
                labels: Object.keys(velocityData),
                datasets: [{
                    label: 'Problems Solved',
                    data: Object.values(velocityData),
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });

        // Initialize Complexity Distribution Chart
        const complexityMetrics = analysisData.code_quality_metrics?.complexity_metrics;
        if (complexityMetrics?.patterns?.time) {
            const complexityCtx = document.getElementById('complexityChart').getContext('2d');
            new Chart(complexityCtx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(complexityMetrics.patterns.time),
                    datasets: [{
                        data: Object.values(complexityMetrics.patterns.time),
                        backgroundColor: [
                            'rgba(16, 185, 129, 0.7)',  // O(1)
                            'rgba(59, 130, 246, 0.7)',  // O(log n)
                            'rgba(99, 102, 241, 0.7)',  // O(n)
                            'rgba(236, 72, 153, 0.7)',  // O(n log n)
                            'rgba(245, 158, 11, 0.7)',  // O(n²)
                            'rgba(239, 68, 68, 0.7)'    // O(2ⁿ)
                        ],
                        borderColor: [
                            '#10B981',
                            '#3B82F6',
                            '#6366F1',
                            '#EC4899',
                            '#F59E0B',
                            '#EF4444'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                font: {
                                    family: "'Plus Jakarta Sans', sans-serif"
                                }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw || 0;
                                    return `${label}: ${value} solutions`;
                                }
                            }
                        }
                    }
                }
            });

            // Create container for ML visualizations
            const mlVisualsContainer = document.createElement('div');
            mlVisualsContainer.className = 'ml-visualizations';
            
            // Add pattern distribution chart
            const patternChartContainer = document.createElement('div');
            patternChartContainer.className = 'pattern-chart-container';
            const patternCanvas = document.createElement('canvas');
            patternCanvas.id = 'mlPatternChart';
            patternChartContainer.appendChild(patternCanvas);
            mlVisualsContainer.appendChild(patternChartContainer);
            
            // Add learning progress chart
            const progressChartContainer = document.createElement('div');
            progressChartContainer.className = 'progress-chart-container';
            const progressCanvas = document.createElement('canvas');
            progressCanvas.id = 'mlProgressChart';
            progressChartContainer.appendChild(progressCanvas);
            mlVisualsContainer.appendChild(progressChartContainer);
            
            // Add ML insights panel
            const mlInsightsEl = document.createElement('div');
            mlInsightsEl.className = 'ml-insights-panel mt-4';
            
            // Add confidence scores visualization
            const confidenceScores = analysisData.code_quality_metrics?.solution_efficiency?.metrics || {};
            
            // Initialize ML charts
            const mlPatterns = analysisData.coding_personality?.problem_solving_style?.pattern_distribution;
            if (mlPatterns) {
                new Chart(patternCanvas.getContext('2d'), {
                    type: 'radar',
                    data: {
                        labels: Object.keys(mlPatterns).map(key => key.charAt(0).toUpperCase() + key.slice(1)),
                        datasets: [{
                            label: 'Pattern Distribution',
                            data: Object.values(mlPatterns),
                            backgroundColor: 'rgba(99, 102, 241, 0.2)',
                            borderColor: 'rgba(99, 102, 241, 1)',
                            borderWidth: 2,
                            pointBackgroundColor: 'rgba(99, 102, 241, 1)',
                            pointRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            r: {
                                beginAtZero: true,
                                max: 100,
                                ticks: { stepSize: 20 },
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                pointLabels: {
                                    font: {
                                        family: "'Plus Jakarta Sans', sans-serif",
                                        size: 12
                                    }
                                }
                            }
                        },
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return `Confidence: ${context.raw}%`;
                                    }
                                }
                            }
                        }
                    }
                });
            }

            // Initialize learning progress chart
            const learningData = analysisData.detailed_analysis?.skill_assessment?.ml_insights?.learning_rate || {};
            if (Object.keys(learningData).length > 0) {
                new Chart(progressCanvas.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: Object.keys(learningData),
                        datasets: [{
                            label: 'Learning Rate',
                            data: Object.values(learningData),
                            borderColor: '#EC4899',
                            backgroundColor: 'rgba(236, 72, 153, 0.1)',
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255, 255, 255, 0.1)' }
                            },
                            x: { grid: { display: false } }
                        },
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                mode: 'index',
                                intersect: false,
                                callbacks: {
                                    label: function(context) {
                                        return `Learning Rate: ${context.raw.toFixed(2)}`;
                                    }
                                }
                            }
                        }
                    }
                });
            }
            const confidenceHtml = `
                <div class="confidence-metrics">
                    <h5>ML Model Confidence</h5>
                    <div class="confidence-grid">
                        <div class="confidence-item">
                            <div class="confidence-bar" style="--confidence: ${confidenceScores.runtime_percentile || 0}%">
                                <span class="confidence-label">Runtime Analysis</span>
                                <span class="confidence-value">${confidenceScores.runtime_percentile || 0}%</span>
                            </div>
                        </div>
                        <div class="confidence-item">
                            <div class="confidence-bar" style="--confidence: ${confidenceScores.memory_percentile || 0}%">
                                <span class="confidence-label">Memory Usage</span>
                                <span class="confidence-value">${confidenceScores.memory_percentile || 0}%</span>
                            </div>
                        </div>
                        <div class="confidence-item">
                            <div class="confidence-bar" style="--confidence: ${confidenceScores.optimization_ratio || 0}%">
                                <span class="confidence-label">Code Optimization</span>
                                <span class="confidence-value">${confidenceScores.optimization_ratio || 0}%</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
    
            // Add trend analysis with interactive tooltip
            const trend = complexityMetrics?.trend || {};
            const trendHtml = `
                <div class="trend-analysis mt-4">
                    <h5>Complexity Trend Analysis</h5>
                    <div class="trend-indicator" data-tippy-content="Based on your last ${complexityMetrics?.patterns?.time_window || '30'} submissions">
                        <span class="badge-custom ${trend.trend?.toLowerCase()} pulse">
                            ${trend.trend || 'No Data'}: ${trend.description || 'Insufficient data for trend analysis'}
                        </span>
                    </div>
                </div>
            `;
    
            mlInsightsEl.innerHTML = confidenceHtml + trendHtml;
            document.getElementById('complexityChart').parentNode.appendChild(mlInsightsEl);
    
            // Initialize tooltips for ML insights
            tippy('[data-tippy-content]', {
                theme: 'dark',
                animation: 'shift-away',
                interactive: true
            });
    
            // Add interactive events for confidence bars
            document.querySelectorAll('.confidence-bar').forEach(bar => {
                bar.addEventListener('mouseenter', (e) => {
                    const value = e.currentTarget.style.getPropertyValue('--confidence');
                    const label = e.currentTarget.querySelector('.confidence-label').textContent;
                    
                    tippy(e.currentTarget, {
                        content: `${label}: ${value}`,
                        theme: 'dark',
                        animation: 'shift-away',
                        placement: 'right'
                    });
                });
            });
        }
    }

    // Helper function to create trend badge class
    function getTrendClass(trend) {
        switch(trend.toLowerCase()) {
            case 'improving':
                return 'success';
            case 'declining':
                return 'danger';
            default:
                return 'warning';
        }
    }
}