/**
 * Chart.js Integration Utilities for Student Performance Prediction
 * Department of Computer Science & Engineering (AIML), JSS University, Noida
 */

function initDepartmentRiskChart(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    fetch('/api/charts/department-risk')
        .then(response => response.json())
        .then(data => {
            new Chart(canvas, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: data.colors,
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { boxWidth: 14, font: { size: 12 } }
                        }
                    },
                    cutout: '65%'
                }
            });
        })
        .catch(err => console.error("Error loading risk chart:", err));
}

function initStudentHistoryChart(canvasId, studentId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    fetch(`/api/charts/student-metrics/${studentId}`)
        .then(response => response.json())
        .then(data => {
            new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: data.cycles,
                    datasets: [
                        {
                            label: 'Attendance %',
                            data: data.attendance,
                            backgroundColor: 'rgba(54, 162, 235, 0.7)',
                            borderColor: 'rgb(54, 162, 235)',
                            borderWidth: 1
                        },
                        {
                            label: 'Internal Marks (out of 30)',
                            data: data.internals,
                            backgroundColor: 'rgba(255, 159, 64, 0.7)',
                            borderColor: 'rgb(255, 159, 64)',
                            borderWidth: 1
                        },
                        {
                            label: 'Assignments (out of 25)',
                            data: data.assignments,
                            backgroundColor: 'rgba(75, 192, 192, 0.7)',
                            borderColor: 'rgb(75, 192, 192)',
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: { font: { size: 11 } }
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: { boxWidth: 12, font: { size: 11 } }
                        }
                    }
                }
            });
        })
        .catch(err => console.error("Error loading student history chart:", err));
}

function updateUnreadNotificationBadge() {
    fetch('/api/notifications/unread-count')
        .then(res => res.json())
        .then(data => {
            const badge = document.getElementById('notif-badge');
            if (badge) {
                if (data.unread_count > 0) {
                    badge.textContent = data.unread_count;
                    badge.style.display = 'inline-block';
                } else {
                    badge.style.display = 'none';
                }
            }
        })
        .catch(e => {});
}

document.addEventListener('DOMContentLoaded', () => {
    updateUnreadNotificationBadge();
});
