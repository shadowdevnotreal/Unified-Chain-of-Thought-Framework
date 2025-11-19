// Unified CoT Framework v3.0 - Dashboard Controller
// Intelligence Amplification Platform

// Sample data (in production, this would come from API/database)
const dashboardData = {
    agents: [
        {
            name: 'Code Perfection System',
            icon: 'fa-code',
            uses: 312,
            successRate: 98.7,
            avgDuration: '4m 23s',
            qualityScore: 9.6,
            trend: 'up'
        },
        {
            name: 'Security Auditor',
            icon: 'fa-shield-alt',
            uses: 198,
            successRate: 100.0,
            avgDuration: '2m 15s',
            qualityScore: 9.8,
            trend: 'up'
        },
        {
            name: 'Performance Optimizer',
            icon: 'fa-tachometer-alt',
            uses: 156,
            successRate: 96.2,
            avgDuration: '3m 45s',
            qualityScore: 9.3,
            trend: 'up'
        },
        {
            name: 'Test Engineer',
            icon: 'fa-vial',
            uses: 145,
            successRate: 97.9,
            avgDuration: '5m 12s',
            qualityScore: 9.4,
            trend: 'stable'
        },
        {
            name: 'Code Reviewer',
            icon: 'fa-search',
            uses: 134,
            successRate: 99.3,
            avgDuration: '2m 48s',
            qualityScore: 9.5,
            trend: 'up'
        },
        {
            name: 'Documentation Generator',
            icon: 'fa-book',
            uses: 98,
            successRate: 95.9,
            avgDuration: '3m 22s',
            qualityScore: 9.1,
            trend: 'stable'
        },
        {
            name: 'Team Architect',
            icon: 'fa-sitemap',
            uses: 87,
            successRate: 98.9,
            avgDuration: '6m 34s',
            qualityScore: 9.7,
            trend: 'up'
        },
        {
            name: 'Accessibility Auditor',
            icon: 'fa-universal-access',
            uses: 67,
            successRate: 97.0,
            avgDuration: '3m 18s',
            qualityScore: 9.2,
            trend: 'stable'
        },
        {
            name: 'Refactoring Specialist',
            icon: 'fa-wrench',
            uses: 52,
            successRate: 96.2,
            avgDuration: '7m 45s',
            qualityScore: 9.4,
            trend: 'up'
        },
        {
            name: 'Migration Specialist',
            icon: 'fa-exchange-alt',
            uses: 34,
            successRate: 94.1,
            avgDuration: '12m 23s',
            qualityScore: 9.0,
            trend: 'up'
        },
        {
            name: 'DevOps Automation',
            icon: 'fa-cogs',
            uses: 28,
            successRate: 96.4,
            avgDuration: '5m 56s',
            qualityScore: 9.3,
            trend: 'stable'
        },
        {
            name: 'Database Optimizer',
            icon: 'fa-database',
            uses: 21,
            successRate: 95.2,
            avgDuration: '4m 38s',
            qualityScore: 9.1,
            trend: 'up'
        }
    ],
    patterns: [
        {
            id: 'PLM-001',
            name: 'JWT Token Refresh Pattern',
            category: 'Authentication',
            uses: 47,
            successRate: 98.0,
            timeSaved: '23 hours'
        },
        {
            id: 'PLM-015',
            name: 'React State Management',
            category: 'Frontend',
            uses: 42,
            successRate: 95.2,
            timeSaved: '18 hours'
        },
        {
            id: 'PLM-032',
            name: 'API Rate Limiting',
            category: 'Backend',
            uses: 38,
            successRate: 97.4,
            timeSaved: '15 hours'
        },
        {
            id: 'PLM-008',
            name: 'Database Migration Zero-Downtime',
            category: 'Database',
            uses: 31,
            successRate: 93.5,
            timeSaved: '42 hours'
        },
        {
            id: 'PLM-024',
            name: 'Error Handling Middleware',
            category: 'Backend',
            uses: 29,
            successRate: 96.6,
            timeSaved: '12 hours'
        }
    ],
    insights: [
        {
            type: 'success',
            icon: 'fa-lightbulb',
            title: 'Agent Synergy Discovered',
            message: 'Performance Agent catches 3.2x more issues when paired with Code Reviewer',
            confidence: 'High'
        },
        {
            type: 'info',
            icon: 'fa-chart-line',
            title: 'Quality Improvement',
            message: 'cot++ usage increased quality scores by 23% on complex refactoring tasks',
            confidence: 'High'
        },
        {
            type: 'success',
            icon: 'fa-clock',
            title: 'Time Savings',
            message: 'Your pattern library saves approximately 12.3 hours per week',
            confidence: 'Medium'
        },
        {
            type: 'warning',
            icon: 'fa-exclamation-triangle',
            title: 'Optimization Opportunity',
            message: 'Consider using cot+ instead of cot++ for routine code reviews (30% faster, similar results)',
            confidence: 'Medium'
        }
    ],
    recentActivity: [
        {
            agent: 'Code Perfection System',
            task: 'Refactor authentication module',
            intensity: 'cot++',
            status: 'completed',
            duration: '18m 34s',
            quality: 9.8,
            timestamp: '5 minutes ago'
        },
        {
            agent: 'Security Auditor',
            task: 'Audit OAuth2 implementation',
            intensity: 'cot+',
            status: 'completed',
            duration: '3m 12s',
            quality: 9.9,
            timestamp: '12 minutes ago'
        },
        {
            agent: 'Performance Optimizer',
            task: 'Optimize database queries',
            intensity: 'cot+',
            status: 'in_progress',
            duration: '2m 45s',
            quality: null,
            timestamp: '2 minutes ago'
        },
        {
            agent: 'Test Engineer',
            task: 'Generate integration tests',
            intensity: 'cot',
            status: 'completed',
            duration: '4m 56s',
            quality: 9.2,
            timestamp: '23 minutes ago'
        },
        {
            agent: 'Documentation Generator',
            task: 'Create API documentation',
            intensity: 'cot',
            status: 'completed',
            duration: '3m 18s',
            quality: 9.1,
            timestamp: '35 minutes ago'
        }
    ]
};

// Initialize Charts
function initializeCharts() {
    // Agent Usage Chart
    const agentUsageCtx = document.getElementById('agentUsageChart').getContext('2d');
    const agentLabels = dashboardData.agents.slice(0, 8).map(a => a.name.split(' ')[0]);
    const agentData = dashboardData.agents.slice(0, 8).map(a => a.uses);

    new Chart(agentUsageCtx, {
        type: 'bar',
        data: {
            labels: agentLabels,
            datasets: [{
                label: 'Total Uses',
                data: agentData,
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(118, 75, 162, 0.8)',
                    'rgba(237, 100, 166, 0.8)',
                    'rgba(255, 154, 158, 0.8)',
                    'rgba(250, 208, 196, 0.8)',
                    'rgba(162, 155, 254, 0.8)',
                    'rgba(116, 185, 255, 0.8)',
                    'rgba(86, 204, 242, 0.8)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(118, 75, 162, 1)',
                    'rgba(237, 100, 166, 1)',
                    'rgba(255, 154, 158, 1)',
                    'rgba(250, 208, 196, 1)',
                    'rgba(162, 155, 254, 1)',
                    'rgba(116, 185, 255, 1)',
                    'rgba(86, 204, 242, 1)'
                ],
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
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

    // Quality Trend Chart
    const qualityTrendCtx = document.getElementById('qualityTrendChart').getContext('2d');
    const qualityLabels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
    const qualityData = [8.2, 8.6, 9.0, 9.3];

    new Chart(qualityTrendCtx, {
        type: 'line',
        data: {
            labels: qualityLabels,
            datasets: [{
                label: 'Average Quality Score',
                data: qualityData,
                borderColor: 'rgba(102, 126, 234, 1)',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 6,
                pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 },
                    callbacks: {
                        label: function(context) {
                            return 'Quality Score: ' + context.parsed.y.toFixed(1) + '/10';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 7,
                    max: 10,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
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

// Populate Agent Performance Table
function populateAgentTable() {
    const tbody = document.getElementById('agentTableBody');
    tbody.innerHTML = '';

    dashboardData.agents.forEach(agent => {
        const row = document.createElement('tr');
        row.className = 'border-b border-gray-100 hover:bg-gray-50 transition';

        const trendIcon = agent.trend === 'up'
            ? '<i class="fas fa-arrow-up text-green-500"></i>'
            : agent.trend === 'down'
            ? '<i class="fas fa-arrow-down text-red-500"></i>'
            : '<i class="fas fa-minus text-gray-400"></i>';

        row.innerHTML = `
            <td class="py-4 px-4">
                <div class="flex items-center space-x-3">
                    <i class="fas ${agent.icon} text-purple-600 text-lg"></i>
                    <span class="font-medium text-gray-800">${agent.name}</span>
                </div>
            </td>
            <td class="text-center py-4 px-4 font-semibold text-gray-700">${agent.uses}</td>
            <td class="text-center py-4 px-4">
                <span class="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                    ${agent.successRate}%
                </span>
            </td>
            <td class="text-center py-4 px-4 text-gray-700">${agent.avgDuration}</td>
            <td class="text-center py-4 px-4">
                <div class="flex items-center justify-center space-x-2">
                    <span class="font-bold text-gray-800">${agent.qualityScore}</span>
                    <span class="text-gray-400 text-sm">/10</span>
                </div>
            </td>
            <td class="text-center py-4 px-4">${trendIcon}</td>
        `;

        tbody.appendChild(row);
    });
}

// Populate Top Patterns
function populatePatterns() {
    const container = document.getElementById('topPatterns');
    container.innerHTML = '';

    dashboardData.patterns.forEach((pattern, index) => {
        const patternDiv = document.createElement('div');
        patternDiv.className = 'flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition';

        patternDiv.innerHTML = `
            <div class="flex items-center space-x-3">
                <span class="flex items-center justify-center w-8 h-8 bg-purple-600 text-white rounded-full font-bold text-sm">
                    ${index + 1}
                </span>
                <div>
                    <p class="font-semibold text-gray-800">${pattern.name}</p>
                    <p class="text-sm text-gray-500">${pattern.category} • ${pattern.uses} uses</p>
                </div>
            </div>
            <div class="text-right">
                <p class="text-sm font-semibold text-green-600">${pattern.successRate}% success</p>
                <p class="text-xs text-gray-500">${pattern.timeSaved} saved</p>
            </div>
        `;

        container.appendChild(patternDiv);
    });
}

// Populate Smart Insights
function populateInsights() {
    const container = document.getElementById('smartInsights');
    container.innerHTML = '';

    dashboardData.insights.forEach(insight => {
        const insightDiv = document.createElement('div');

        const bgColor = insight.type === 'success' ? 'bg-green-50 border-green-200' :
                       insight.type === 'warning' ? 'bg-yellow-50 border-yellow-200' :
                       'bg-blue-50 border-blue-200';

        const iconColor = insight.type === 'success' ? 'text-green-600' :
                         insight.type === 'warning' ? 'text-yellow-600' :
                         'text-blue-600';

        insightDiv.className = `p-4 ${bgColor} border-l-4 rounded`;

        insightDiv.innerHTML = `
            <div class="flex items-start space-x-3">
                <i class="fas ${insight.icon} ${iconColor} text-xl mt-1"></i>
                <div class="flex-1">
                    <p class="font-semibold text-gray-800 mb-1">${insight.title}</p>
                    <p class="text-sm text-gray-600 mb-2">${insight.message}</p>
                    <span class="inline-block px-2 py-1 bg-white rounded text-xs font-semibold text-gray-600">
                        Confidence: ${insight.confidence}
                    </span>
                </div>
            </div>
        `;

        container.appendChild(insightDiv);
    });
}

// Populate Recent Activity
function populateRecentActivity() {
    const container = document.getElementById('recentActivity');
    container.innerHTML = '';

    dashboardData.recentActivity.forEach(activity => {
        const activityDiv = document.createElement('div');
        activityDiv.className = 'flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-purple-300 transition';

        const statusBadge = activity.status === 'completed'
            ? '<span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-semibold"><i class="fas fa-check mr-1"></i>Completed</span>'
            : '<span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold"><i class="fas fa-spinner fa-spin mr-1"></i>In Progress</span>';

        const intensityColor = activity.intensity === 'cot++' ? 'text-red-600' :
                              activity.intensity === 'cot+' ? 'text-purple-600' :
                              'text-blue-600';

        const qualityBadge = activity.quality
            ? `<span class="font-bold text-gray-800">${activity.quality}/10</span>`
            : '<span class="text-gray-400">-</span>';

        activityDiv.innerHTML = `
            <div class="flex-1">
                <div class="flex items-center space-x-2 mb-2">
                    <span class="font-semibold text-gray-800">${activity.agent}</span>
                    <span class="text-gray-400">•</span>
                    <span class="${intensityColor} font-mono text-sm font-semibold">${activity.intensity}</span>
                </div>
                <p class="text-sm text-gray-600">${activity.task}</p>
            </div>
            <div class="flex items-center space-x-6">
                <div class="text-center">
                    <p class="text-xs text-gray-500 mb-1">Duration</p>
                    <p class="font-semibold text-gray-700">${activity.duration}</p>
                </div>
                <div class="text-center">
                    <p class="text-xs text-gray-500 mb-1">Quality</p>
                    ${qualityBadge}
                </div>
                <div class="text-center min-w-[120px]">
                    ${statusBadge}
                </div>
                <div class="text-right min-w-[100px]">
                    <p class="text-xs text-gray-500">${activity.timestamp}</p>
                </div>
            </div>
        `;

        container.appendChild(activityDiv);
    });
}

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Unified CoT Framework v3.0 Dashboard Initialized');

    initializeCharts();
    populateAgentTable();
    populatePatterns();
    populateInsights();
    populateRecentActivity();

    // Refresh button functionality
    const refreshBtn = document.querySelector('button');
    refreshBtn.addEventListener('click', function() {
        refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Refreshing...';

        setTimeout(() => {
            // Simulate data refresh
            populateAgentTable();
            populatePatterns();
            populateInsights();
            populateRecentActivity();

            refreshBtn.innerHTML = '<i class="fas fa-sync-alt mr-2"></i>Refresh';

            // Show success notification
            showNotification('Dashboard refreshed successfully!', 'success');
        }, 1000);
    });
});

// Utility function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-6 py-4 rounded-lg shadow-lg transition-opacity duration-300 z-50`;

    const bgColor = type === 'success' ? 'bg-green-500' :
                   type === 'error' ? 'bg-red-500' :
                   'bg-blue-500';

    notification.classList.add(bgColor);
    notification.innerHTML = `
        <div class="flex items-center space-x-3 text-white">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'} text-xl"></i>
            <span class="font-semibold">${message}</span>
        </div>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Export for potential use in other modules
window.CoTDashboard = {
    data: dashboardData,
    refresh: function() {
        populateAgentTable();
        populatePatterns();
        populateInsights();
        populateRecentActivity();
    }
};
