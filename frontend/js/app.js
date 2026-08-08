// Main JavaScript file for AI Grievance System

const API_BASE_URL = 'http://localhost:5001';

// API Helper Functions
const api = {
    // Auth endpoints
    async register(userData) {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        return await response.json();
    },

    async login(credentials) {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });
        return await response.json();
    },

    async getProfile() {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/auth/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return await response.json();
    },

    // Petition endpoints
    async submitPetition(formData) {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/petitions/submit`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        return await response.json();
    },

    async getPetitions(filters = {}) {
        const token = getToken();
        const queryParams = new URLSearchParams(filters).toString();
        const response = await fetch(`${API_BASE_URL}/petitions/list?${queryParams}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return await response.json();
    },

    async getPetition(id) {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/petitions/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return await response.json();
    },

    async updatePetitionStatus(id, statusData) {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/petitions/${id}/status`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(statusData)
        });
        return await response.json();
    },

    async trackPetition(petitionId) {
        const response = await fetch(`${API_BASE_URL}/petitions/track/${petitionId}`);
        return await response.json();
    },

    // Department endpoints
    async getDepartments() {
        const response = await fetch(`${API_BASE_URL}/departments/list`);
        return await response.json();
    },

    // Analytics endpoints
    async getDashboardStats() {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/analytics/dashboard`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return await response.json();
    },

    async getTrends() {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/analytics/trends`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return await response.json();
    },

    // Notifications endpoints
    async getNotifications() {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/notifications/list`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return await response.json();
    },

    async markNotificationRead(id) {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/notifications/${id}/read`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return await response.json();
    }
};

// Token Management
function saveToken(token) {
    localStorage.setItem('token', token);
}

function getToken() {
    return localStorage.getItem('token');
}

function removeToken() {
    localStorage.removeItem('token');
}

function saveUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function removeUser() {
    localStorage.removeItem('user');
}

function isLoggedIn() {
    return !!getToken();
}

function logout() {
    removeToken();
    removeUser();
    window.location.href = 'index.html';
}

// UI Helper Functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showLoading(element) {
    element.innerHTML = `
        <div class="spinner-container">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getPriorityBadgeClass(priority) {
    const classes = {
        'high': 'badge-priority-high',
        'medium': 'badge-priority-medium',
        'low': 'badge-priority-low'
    };
    return classes[priority] || 'bg-secondary';
}

function getStatusBadgeClass(status) {
    const classes = {
        'submitted': 'badge-status-submitted',
        'in_review': 'badge-status-in_review',
        'in_progress': 'badge-status-in_progress',
        'resolved': 'badge-status-resolved',
        'rejected': 'badge-status-rejected'
    };
    return classes[status] || 'bg-secondary';
}

function formatStatus(status) {
    return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Check authentication on protected pages
function checkAuth() {
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Update navbar based on auth status
function updateNavbar() {
    const user = getUser();
    const navbarNav = document.querySelector('#navbarNav .navbar-nav');

    if (user && navbarNav) {
        navbarNav.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="dashboard.html">Dashboard</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="submit-petition.html">Submit Petition</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="track-petition.html">Track</a>
            </li>
            ${user.role === 'admin' || user.role === 'officer' ? `
            <li class="nav-item">
                <a class="nav-link" href="admin-dashboard.html">Admin</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="analytics.html">Analytics</a>
            </li>
            ` : ''}
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                    ${user.name}
                </a>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" onclick="logout()">Logout</a></li>
                </ul>
            </li>
        `;
    }
}

// Initialize navbar on page load
document.addEventListener('DOMContentLoaded', function () {
    updateNavbar();
});
