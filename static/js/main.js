// Grenada Athletics - Main JavaScript

// Global variables
let athletes = [];
let events = [];
let competitions = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Grenada Athletics app initialized');
    
    // Load initial data
    loadAthletes();
    loadEvents();
    loadCompetitions();
    
    // Set up form handlers
    setupFormHandlers();
});

// API Functions
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showAlert('An error occurred. Please try again.', 'danger');
        throw error;
    }
}

// Athletes Functions
async function loadAthletes() {
    try {
        const data = await apiCall('/athletes/api');
        athletes = data;
        renderAthletes();
    } catch (error) {
        console.error('Failed to load athletes:', error);
    }
}

function renderAthletes() {
    const container = document.getElementById('athletesGrid');
    if (!container) return;
    
    if (athletes.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="empty-state">
                    <i class="fas fa-users empty-icon"></i>
                    <h3>No Athletes Yet</h3>
                    <p>Start by adding your first athlete to the system.</p>
                    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addAthleteModal">
                        <i class="fas fa-plus me-2"></i>Add First Athlete
                    </button>
                </div>
            </div>
        `;
        return;
    }
    
    container.innerHTML = athletes.map(athlete => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="athlete-card">
                <div class="athlete-header">
                    <div class="athlete-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <div class="athlete-info">
                        <h5 class="athlete-name">${athlete.name}</h5>
                        <p class="athlete-sport">${athlete.sport}</p>
                    </div>
                </div>
                <div class="athlete-details">
                    <div class="detail-item">
                        <i class="fas fa-birthday-cake me-2"></i>
                        <span>Age: ${athlete.age}</span>
                    </div>
                    ${athlete.personal_best ? `
                    <div class="detail-item">
                        <i class="fas fa-trophy me-2"></i>
                        <span>PB: ${athlete.personal_best}</span>
                    </div>
                    ` : ''}
                    ${athlete.achievements ? `
                    <div class="detail-item">
                        <i class="fas fa-medal me-2"></i>
                        <span>${athlete.achievements.length > 50 ? athlete.achievements.substring(0, 50) + '...' : athlete.achievements}</span>
                    </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

async function addAthlete() {
    const form = document.getElementById('addAthleteForm');
    const formData = new FormData(form);
    
    const athleteData = {
        name: document.getElementById('athleteName').value,
        age: parseInt(document.getElementById('athleteAge').value),
        sport: document.getElementById('athleteSport').value,
        personal_best: document.getElementById('athletePB').value,
        achievements: document.getElementById('athleteAchievements').value
    };
    
    try {
        const result = await apiCall('/athletes/api', {
            method: 'POST',
            body: JSON.stringify(athleteData)
        });
        
        showAlert('Athlete added successfully!', 'success');
        form.reset();
        bootstrap.Modal.getInstance(document.getElementById('addAthleteModal')).hide();
        loadAthletes();
    } catch (error) {
        console.error('Failed to add athlete:', error);
    }
}

// Events Functions
async function loadEvents() {
    try {
        const data = await apiCall('/events/api');
        events = data;
        renderEvents();
    } catch (error) {
        console.error('Failed to load events:', error);
    }
}

function renderEvents() {
    const container = document.getElementById('eventsList');
    if (!container) return;
    
    if (events.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="empty-state">
                    <i class="fas fa-calendar empty-icon"></i>
                    <h3>No Events Yet</h3>
                    <p>Start by adding your first event to the system.</p>
                    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addEventModal">
                        <i class="fas fa-plus me-2"></i>Add First Event
                    </button>
                </div>
            </div>
        `;
        return;
    }
    
    container.innerHTML = events.map(event => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="event-card">
                <div class="event-header">
                    <div class="event-type-badge">${event.event_type}</div>
                    <h5 class="event-name">${event.name}</h5>
                </div>
                <div class="event-details">
                    ${event.date ? `
                    <div class="detail-item">
                        <i class="fas fa-calendar me-2"></i>
                        <span>${new Date(event.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</span>
                    </div>
                    ` : ''}
                    ${event.description ? `
                    <div class="detail-item">
                        <i class="fas fa-info-circle me-2"></i>
                        <span>${event.description.length > 100 ? event.description.substring(0, 100) + '...' : event.description}</span>
                    </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

async function addEvent() {
    const athleteData = {
        name: document.getElementById('eventName').value,
        event_type: document.getElementById('eventType').value,
        date: document.getElementById('eventDate').value,
        description: document.getElementById('eventDescription').value
    };
    
    try {
        const result = await apiCall('/events/api', {
            method: 'POST',
            body: JSON.stringify(athleteData)
        });
        
        showAlert('Event added successfully!', 'success');
        document.getElementById('addEventForm').reset();
        bootstrap.Modal.getInstance(document.getElementById('addEventModal')).hide();
        loadEvents();
    } catch (error) {
        console.error('Failed to add event:', error);
    }
}

// Competitions Functions
async function loadCompetitions() {
    try {
        const data = await apiCall('/competitions/api');
        competitions = data;
        renderCompetitions();
    } catch (error) {
        console.error('Failed to load competitions:', error);
    }
}

function renderCompetitions() {
    const container = document.getElementById('competitionsList');
    if (!container) return;
    
    if (competitions.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="empty-state">
                    <i class="fas fa-trophy empty-icon"></i>
                    <h3>No Competitions Yet</h3>
                    <p>Start by adding your first competition to the system.</p>
                    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addCompetitionModal">
                        <i class="fas fa-plus me-2"></i>Add First Competition
                    </button>
                </div>
            </div>
        `;
        return;
    }
    
    container.innerHTML = competitions.map(competition => {
        const startDate = new Date(competition.start_date);
        const endDate = competition.end_date ? new Date(competition.end_date) : null;
        const today = new Date();
        
        let status = 'Upcoming';
        let statusClass = 'bg-warning';
        
        if (endDate && endDate < today) {
            status = 'Completed';
            statusClass = 'bg-secondary';
        } else if (startDate <= today) {
            status = 'Ongoing';
            statusClass = 'bg-success';
        }
        
        return `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="competition-card">
                    <div class="competition-header">
                        <div class="competition-status">
                            <span class="badge ${statusClass}">${status}</span>
                        </div>
                        <h5 class="competition-name">${competition.name}</h5>
                    </div>
                    <div class="competition-details">
                        <div class="detail-item">
                            <i class="fas fa-map-marker-alt me-2"></i>
                            <span>${competition.location}</span>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-calendar me-2"></i>
                            <span>${startDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}${endDate ? ' - ' + endDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : ''}</span>
                        </div>
                        ${competition.description ? `
                        <div class="detail-item">
                            <i class="fas fa-info-circle me-2"></i>
                            <span>${competition.description.length > 100 ? competition.description.substring(0, 100) + '...' : competition.description}</span>
                        </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

async function addCompetition() {
    const competitionData = {
        name: document.getElementById('competitionName').value,
        location: document.getElementById('competitionLocation').value,
        start_date: document.getElementById('competitionStartDate').value,
        end_date: document.getElementById('competitionEndDate').value || null,
        description: document.getElementById('competitionDescription').value
    };
    
    try {
        const result = await apiCall('/competitions/api', {
            method: 'POST',
            body: JSON.stringify(competitionData)
        });
        
        showAlert('Competition added successfully!', 'success');
        document.getElementById('addCompetitionForm').reset();
        bootstrap.Modal.getInstance(document.getElementById('addCompetitionModal')).hide();
        loadCompetitions();
    } catch (error) {
        console.error('Failed to add competition:', error);
    }
}

// Utility Functions
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main content
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alertDiv, main.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

function setupFormHandlers() {
    // Add form validation and submission handlers here if needed
    console.log('Form handlers set up');
}

// Export functions for global access
window.addAthlete = addAthlete;
window.addEvent = addEvent;
window.addCompetition = addCompetition;




