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

// Chart.js Global Configuration
Chart.defaults.color = '#CBD5E1';
Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Progress Bar
    const progressBar = document.getElementById('progress-bar');
    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    });

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

        // Initialize all charts
        initializeCharts();

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

            // Add trend indicator
            const trendEl = document.createElement('div');
            trendEl.className = 'trend-indicator mt-3 text-center';
            trendEl.innerHTML = `
                <span class="badge-custom ${complexityMetrics.trend.trend.toLowerCase()}">
                    ${complexityMetrics.trend.trend}: ${complexityMetrics.trend.description}
                </span>
            `;
            document.getElementById('complexityChart').parentNode.appendChild(trendEl);
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