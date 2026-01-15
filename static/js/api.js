/**
 * API Module for Therapy Session Management
 * 
 * Handles all CRUD operations via REST API without page refresh.
 */

const API_BASE = '/api/v1';

/**
 * Get CSRF token from meta tag
 * @returns {string|null} - CSRF token or null if not found
 */
function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : null;
}

/**
 * Make an API request with error handling
 * @param {string} url - API endpoint URL
 * @param {object} options - Fetch options
 * @returns {Promise<object>} - Response data
 */
async function apiRequest(url, options = {}) {
    const csrfToken = getCsrfToken();
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(csrfToken && { 'X-CSRFToken': csrfToken }),
        },
        credentials: 'same-origin',
    };

    // Merge headers properly
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {}),
        },
    };

    const response = await fetch(url, mergedOptions);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Error en la solicitud');
    }

    return data;
}

// =============================================================================
// Patient API Functions
// =============================================================================

/**
 * Get a patient by ID
 * @param {number} patientId - Patient ID
 * @returns {Promise<object>} - Patient data
 */
async function getPatient(patientId) {
    return apiRequest(`${API_BASE}/patients/${patientId}`);
}

/**
 * Update a patient
 * @param {number} patientId - Patient ID
 * @param {object} data - Patient data {name, notes}
 * @returns {Promise<object>} - Updated patient data
 */
async function updatePatient(patientId, data) {
    return apiRequest(`${API_BASE}/patients/${patientId}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
}

/**
 * Delete a patient (soft delete)
 * @param {number} patientId - Patient ID
 * @returns {Promise<object>} - Success message
 */
async function deletePatient(patientId) {
    return apiRequest(`${API_BASE}/patients/${patientId}`, {
        method: 'DELETE',
    });
}

// =============================================================================
// Session API Functions
// =============================================================================

/**
 * Get a session by ID
 * @param {number} sessionId - Session ID
 * @returns {Promise<object>} - Session data
 */
async function getSession(sessionId) {
    return apiRequest(`${API_BASE}/sessions/${sessionId}`);
}

/**
 * Update a session
 * @param {number} sessionId - Session ID
 * @param {object} data - Session data {session_date, session_price, pending, notes}
 * @returns {Promise<object>} - Updated session data
 */
async function updateSession(sessionId, data) {
    return apiRequest(`${API_BASE}/sessions/${sessionId}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
}

/**
 * Delete a session (soft delete)
 * @param {number} sessionId - Session ID
 * @returns {Promise<object>} - Success message
 */
async function deleteSession(sessionId) {
    return apiRequest(`${API_BASE}/sessions/${sessionId}`, {
        method: 'DELETE',
    });
}

/**
 * Toggle session payment status
 * @param {number} sessionId - Session ID
 * @returns {Promise<object>} - New status {message, pending}
 */
async function toggleSessionPayment(sessionId) {
    return apiRequest(`${API_BASE}/sessions/${sessionId}/toggle`, {
        method: 'POST',
    });
}

// =============================================================================
// UI Helper Functions
// =============================================================================

/**
 * Show a toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type: success, error, warning, info
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1100';
        document.body.appendChild(toastContainer);
    }

    // Map type to Bootstrap classes
    const typeClasses = {
        success: 'text-bg-success',
        error: 'text-bg-danger',
        warning: 'text-bg-warning',
        info: 'text-bg-info',
    };

    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast ${typeClasses[type] || typeClasses.info}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastEl = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
    toast.show();

    // Remove toast from DOM after it's hidden
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

/**
 * Format a date string for display in Spanish
 * @param {string} dateStr - Date in YYYY-MM-DD format
 * @returns {string} - Formatted date string in Spanish (e.g., "Lunes 15/01/2024")
 */
function formatDisplayDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr + 'T00:00:00');
    
    // Spanish day names (Monday=0 in our array, but getDay() returns 0=Sunday)
    const spanishDays = [
        'Domingo', 'Lunes', 'Martes', 'Miércoles', 
        'Jueves', 'Viernes', 'Sábado'
    ];
    
    const dayName = spanishDays[date.getDay()];
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${dayName} ${day}/${month}/${year}`;
}

/**
 * Format a price for display (matching backend format)
 * @param {number} price - Price value
 * @returns {string} - Formatted price string (e.g., "$1,234.56")
 */
function formatPrice(price) {
    const numPrice = parseFloat(price);
    return '$' + numPrice.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// =============================================================================
// Patient Actions
// =============================================================================

/**
 * Open the edit patient modal
 * @param {number} patientId - Patient ID
 * @param {string} patientName - Current patient name
 */
async function openEditPatientModal(patientId, patientName) {
    const modal = document.getElementById('editPatientModal');
    if (!modal) return;

    // Set form values
    document.getElementById('editPatientId').value = patientId;
    document.getElementById('editPatientName').value = patientName;

    // Try to get notes from API
    try {
        const patient = await getPatient(patientId);
        document.getElementById('editPatientNotes').value = patient.notes || '';
    } catch (error) {
        document.getElementById('editPatientNotes').value = '';
    }

    // Show modal
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

/**
 * Save edited patient
 */
async function saveEditPatient() {
    const patientId = document.getElementById('editPatientId').value;
    const name = document.getElementById('editPatientName').value.trim();
    const notes = document.getElementById('editPatientNotes').value.trim();

    if (!name) {
        showToast('El nombre es requerido', 'error');
        return;
    }

    try {
        await updatePatient(patientId, { name, notes });
        showToast('Paciente actualizado correctamente', 'success');

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('editPatientModal'));
        modal.hide();

        // Update the patient name in the UI
        updatePatientNameInUI(patientId, name);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Update patient name in the UI without refresh
 * @param {number} patientId - Patient ID
 * @param {string} newName - New patient name
 */
function updatePatientNameInUI(patientId, newName) {
    const patientCard = document.querySelector(`[data-patient-id="${patientId}"]`);
    if (patientCard) {
        const nameElement = patientCard.querySelector('.patient-name');
        if (nameElement) {
            nameElement.textContent = newName;
            nameElement.title = newName;
        }
    }
}

/**
 * Open the delete patient confirmation modal
 * @param {number} patientId - Patient ID
 * @param {string} patientName - Patient name
 */
function openDeletePatientModal(patientId, patientName) {
    const modal = document.getElementById('deletePatientModal');
    if (!modal) return;

    document.getElementById('deletePatientId').value = patientId;
    document.getElementById('deletePatientName').textContent = patientName;

    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

/**
 * Confirm and delete patient
 */
async function confirmDeletePatient() {
    const patientId = document.getElementById('deletePatientId').value;

    try {
        await deletePatient(patientId);
        showToast('Paciente eliminado correctamente', 'success');

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('deletePatientModal'));
        modal.hide();

        // Remove patient card from UI
        removePatientFromUI(patientId);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Remove patient card from the UI
 * @param {number} patientId - Patient ID
 */
function removePatientFromUI(patientId) {
    const patientCard = document.querySelector(`[data-patient-id="${patientId}"]`);
    if (patientCard) {
        patientCard.closest('.col').remove();
    }

    // Check if there are no more patients
    const remainingPatients = document.querySelectorAll('[data-patient-id]');
    if (remainingPatients.length === 0) {
        const gridContainer = document.querySelector('.row.row-cols-1');
        if (gridContainer) {
            gridContainer.innerHTML = `
                <div class="col-12">
                    <div class="text-center my-5">
                        <h3 class="text-muted">No hay pacientes</h3>
                    </div>
                </div>
            `;
        }
    }
}

// =============================================================================
// Session Actions
// =============================================================================

/**
 * Open the edit session modal
 * @param {number} sessionId - Session ID
 * @param {number} personId - Person ID
 */
async function openEditSessionModal(sessionId, personId) {
    const modal = document.getElementById('editSessionModal');
    if (!modal) return;

    try {
        const session = await getSession(sessionId);

        document.getElementById('editSessionId').value = sessionId;
        document.getElementById('editSessionPersonId').value = personId;
        document.getElementById('editSessionDate').value = session.session_date;
        document.getElementById('editSessionPrice').value = session.session_price;
        document.getElementById('editSessionPending').checked = session.pending;
        document.getElementById('editSessionNotes').value = session.notes || '';

        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Save edited session
 */
async function saveEditSession() {
    const sessionId = document.getElementById('editSessionId').value;
    const sessionDate = document.getElementById('editSessionDate').value;
    const sessionPrice = document.getElementById('editSessionPrice').value;
    const pending = document.getElementById('editSessionPending').checked;
    const notes = document.getElementById('editSessionNotes').value.trim();

    if (!sessionDate || !sessionPrice) {
        showToast('Fecha y precio son requeridos', 'error');
        return;
    }

    try {
        const updatedSession = await updateSession(sessionId, {
            session_date: sessionDate,
            session_price: parseFloat(sessionPrice),
            pending: pending,
            notes: notes || null,
        });

        showToast('Sesión actualizada correctamente', 'success');

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('editSessionModal'));
        modal.hide();

        // Update session in UI
        updateSessionInUI(sessionId, updatedSession);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Update session data in the UI without refresh
 * @param {number} sessionId - Session ID
 * @param {object} session - Updated session data
 */
function updateSessionInUI(sessionId, session) {
    const sessionCard = document.querySelector(`[data-session-id="${sessionId}"]`);
    if (!sessionCard) return;

    // Update carousel item's pending status data attribute
    const carouselItem = sessionCard.closest('.carousel-item');
    if (carouselItem) {
        carouselItem.dataset.sessionPending = session.pending ? 'true' : 'false';
    }

    // Update date (using .session-date class)
    const dateElement = sessionCard.querySelector('.session-date');
    if (dateElement) {
        dateElement.textContent = formatDisplayDate(session.session_date);
    }

    // Update price (using .session-price class)
    const priceElement = sessionCard.querySelector('.session-price');
    if (priceElement) {
        priceElement.textContent = formatPrice(session.session_price);
    }

    // Update status badge
    const badgeElement = sessionCard.querySelector('.session-status');
    if (badgeElement) {
        if (session.pending) {
            badgeElement.className = 'badge text-bg-warning session-status';
            badgeElement.textContent = 'PENDIENTE';
        } else {
            badgeElement.className = 'badge text-bg-success session-status';
            badgeElement.textContent = 'PAGADO';
        }
    }

    // Update toggle button and footer buttons
    updateSessionButtons(sessionId, session.pending);

    // Check if we need to remove this session from filtered view
    handleFilteredSessionUpdate(sessionId, session.pending);
}

/**
 * Toggle payment status for a session
 * @param {number} sessionId - Session ID
 */
async function togglePayment(sessionId) {
    try {
        const result = await toggleSessionPayment(sessionId);
        showToast(result.message, 'info');

        // Update UI
        const sessionCard = document.querySelector(`[data-session-id="${sessionId}"]`);
        if (sessionCard) {
            // Update carousel item's pending status data attribute
            const carouselItem = sessionCard.closest('.carousel-item');
            if (carouselItem) {
                carouselItem.dataset.sessionPending = result.pending ? 'true' : 'false';
            }

            // Update status badge
            const badgeElement = sessionCard.querySelector('.session-status');
            if (badgeElement) {
                if (result.pending) {
                    badgeElement.className = 'badge text-bg-warning session-status';
                    badgeElement.textContent = 'PENDIENTE';
                } else {
                    badgeElement.className = 'badge text-bg-success session-status';
                    badgeElement.textContent = 'PAGADO';
                }
            }

            // Update toggle button and footer buttons
            updateSessionButtons(sessionId, result.pending);

            // Check if we need to remove this session from filtered view
            handleFilteredSessionUpdate(sessionId, result.pending);
        }
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Update session buttons appearance based on pending status
 * Rebuilds the button group to match the template structure
 * @param {number} sessionId - Session ID
 * @param {boolean} pending - Whether session is pending
 */
function updateSessionButtons(sessionId, pending) {
    const sessionCard = document.querySelector(`[data-session-id="${sessionId}"]`);
    if (!sessionCard) return;

    const cardFooter = sessionCard.querySelector('.card-footer');
    if (!cardFooter) return;

    const btnGroup = cardFooter.querySelector('.btn-group');
    if (!btnGroup) return;

    // Get patient ID from the parent card
    const patientCard = sessionCard.closest('[data-patient-id]');
    const personId = patientCard ? patientCard.dataset.patientId : '';

    // Get current date from session card for aria labels
    const dateElement = sessionCard.querySelector('.session-date');
    const dateText = dateElement ? dateElement.textContent : '';

    // Rebuild button group based on pending status - 3 buttons: Edit, Delete, Toggle
    if (pending) {
        btnGroup.innerHTML = `
            <button type="button"
               class="btn btn-outline-secondary flex-fill"
               title="Editar sesión"
               aria-label="Editar sesión del ${dateText}"
               onclick="openEditSessionModal(${sessionId}, ${personId})">
                <i class="bi bi-pencil-square me-1" aria-hidden="true"></i>Editar
            </button>
            <button type="button"
               class="btn btn-outline-danger flex-fill delete-session-btn"
               title="Eliminar sesión"
               aria-label="Eliminar sesión del ${dateText}"
               onclick="openDeleteSessionModal(${sessionId}, '${dateText}')">
                <i class="bi bi-trash me-1" aria-hidden="true"></i>Eliminar
            </button>
            <button type="button"
               class="btn btn-success flex-fill toggle-payment-btn"
               title="Marcar como pagado"
               aria-label="Marcar sesión del ${dateText} como pagado"
               onclick="togglePayment(${sessionId})">
                <i class="bi bi-check-circle me-1" aria-hidden="true"></i>Pagado
            </button>
        `;
    } else {
        btnGroup.innerHTML = `
            <button type="button"
               class="btn btn-outline-secondary flex-fill"
               title="Editar sesión"
               aria-label="Editar sesión del ${dateText}"
               onclick="openEditSessionModal(${sessionId}, ${personId})">
                <i class="bi bi-pencil-square me-1" aria-hidden="true"></i>Editar
            </button>
            <button type="button"
               class="btn btn-outline-danger flex-fill delete-session-btn"
               title="Eliminar sesión"
               aria-label="Eliminar sesión del ${dateText}"
               onclick="openDeleteSessionModal(${sessionId}, '${dateText}')">
                <i class="bi bi-trash me-1" aria-hidden="true"></i>Eliminar
            </button>
            <button type="button"
               class="btn btn-outline-secondary flex-fill toggle-payment-btn"
               title="Marcar como pendiente"
               aria-label="Marcar sesión del ${dateText} como pendiente"
               onclick="togglePayment(${sessionId})">
                <i class="bi bi-clock-history me-1" aria-hidden="true"></i>Pendiente
            </button>
        `;
    }
}

/**
 * Get current filter from URL
 * @returns {string} - Current filter ('all', 'pending', 'paid')
 */
function getCurrentFilter() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('show') || 'all';
}

/**
 * Handle session removal from filtered view when payment status changes
 * @param {number} sessionId - Session ID
 * @param {boolean} pending - Whether session is now pending
 */
function handleFilteredSessionUpdate(sessionId, pending) {
    const currentFilter = getCurrentFilter();
    
    // If filter is 'all', no need to remove anything
    if (currentFilter === 'all') return;
    
    // If filtering by 'pending' and session is now paid (not pending), remove it
    // If filtering by 'paid' and session is now pending, remove it
    const shouldRemove = 
        (currentFilter === 'pending' && !pending) ||
        (currentFilter === 'paid' && pending);
    
    if (shouldRemove) {
        removeSessionFromUI(sessionId);
    }
}

/**
 * Open the delete session confirmation modal
 * @param {number} sessionId - Session ID
 * @param {string} sessionDate - Session date for display
 */
function openDeleteSessionModal(sessionId, sessionDate) {
    const modal = document.getElementById('deleteSessionModal');
    if (!modal) return;

    document.getElementById('deleteSessionId').value = sessionId;
    document.getElementById('deleteSessionDate').textContent = sessionDate;

    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

/**
 * Confirm and delete session
 */
async function confirmDeleteSession() {
    const sessionId = document.getElementById('deleteSessionId').value;

    try {
        await deleteSession(sessionId);
        showToast('Sesión eliminada correctamente', 'success');

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('deleteSessionModal'));
        modal.hide();

        // Remove session from UI
        removeSessionFromUI(sessionId);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Remove session from the UI
 * @param {number} sessionId - Session ID
 */
function removeSessionFromUI(sessionId) {
    const sessionCard = document.querySelector(`[data-session-id="${sessionId}"]`);
    if (!sessionCard) return;

    const carouselItem = sessionCard.closest('.carousel-item');
    const carousel = carouselItem?.closest('.carousel');
    const patientCard = sessionCard.closest('[data-patient-id]');

    if (!carousel) return;

    const carouselInner = carousel.querySelector('.carousel-inner');
    const allItems = carouselInner.querySelectorAll('.carousel-item');
    const currentFilter = getCurrentFilter();

    if (allItems.length <= 1) {
        // Last session in this patient's card
        if (currentFilter !== 'all') {
            // When filtering, remove the entire patient card since they have no more matching sessions
            removePatientFromUI(patientCard?.dataset?.patientId);
        } else {
            // In "all" view, show "no sessions" message
            const cardBody = carousel.closest('.card-body');
            if (cardBody) {
                cardBody.innerHTML = '<p class="text-muted text-center my-3">No hay sesiones registradas.</p>';
            }
        }
    } else {
        // More than one session - just remove this one and adjust carousel
        const wasActive = carouselItem.classList.contains('active');
        carouselItem.remove();

        // Update remaining items
        const remainingItems = carouselInner.querySelectorAll('.carousel-item');

        // If removed item was active, make first remaining item active
        if (wasActive && remainingItems.length > 0) {
            remainingItems[0].classList.add('active');
        }

        // Update carousel indicators (now at bottom with new class)
        const indicatorsContainer = carousel.querySelector('.carousel-indicators-bottom');
        if (indicatorsContainer) {
            // Update single-slide class
            if (remainingItems.length <= 1) {
                indicatorsContainer.classList.add('single-slide');
            }
            
            // Rebuild indicators
            indicatorsContainer.innerHTML = '';
            remainingItems.forEach((item, index) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.setAttribute('data-bs-target', `#${carousel.id}`);
                button.setAttribute('data-bs-slide-to', index);
                button.setAttribute('aria-label', `Sesión ${index + 1}`);
                if (remainingItems.length <= 1) {
                    button.disabled = true;
                }
                if (item.classList.contains('active')) {
                    button.classList.add('active');
                    button.setAttribute('aria-current', 'true');
                }
                indicatorsContainer.appendChild(button);
            });
        }
    }
}

// =============================================================================
// Initialize Event Listeners
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Edit patient form submission
    const editPatientForm = document.getElementById('editPatientForm');
    if (editPatientForm) {
        editPatientForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveEditPatient();
        });
    }

    // Delete patient confirmation
    const confirmDeletePatientBtn = document.getElementById('confirmDeletePatientBtn');
    if (confirmDeletePatientBtn) {
        confirmDeletePatientBtn.addEventListener('click', confirmDeletePatient);
    }

    // Edit session form submission
    const editSessionForm = document.getElementById('editSessionForm');
    if (editSessionForm) {
        editSessionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveEditSession();
        });
    }

    // Delete session confirmation
    const confirmDeleteSessionBtn = document.getElementById('confirmDeleteSessionBtn');
    if (confirmDeleteSessionBtn) {
        confirmDeleteSessionBtn.addEventListener('click', confirmDeleteSession);
    }

    // Initialize all carousels with touch support enabled
    initializeCarousels();
});

/**
 * Initialize all carousels with proper touch support
 * This ensures swipe/touch works immediately without requiring a click first
 * Also adds event listeners for indicator updates on slide
 */
function initializeCarousels() {
    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carouselEl => {
        // Create Bootstrap carousel instance with touch enabled
        const carousel = new bootstrap.Carousel(carouselEl, {
            interval: false,  // No auto-slide
            touch: true,      // Enable touch/swipe
            wrap: true        // Wrap around at ends
        });
        
        // Update indicators when slide changes
        carouselEl.addEventListener('slid.bs.carousel', function(event) {
            updateCarouselIndicators(carouselEl, event.to);
        });
    });
}

/**
 * Update carousel indicators to reflect current slide
 * @param {HTMLElement} carouselEl - The carousel element
 * @param {number} activeIndex - The index of the active slide
 */
function updateCarouselIndicators(carouselEl, activeIndex) {
    const indicators = carouselEl.querySelectorAll('.carousel-indicators-bottom button');
    indicators.forEach((button, index) => {
        if (index === activeIndex) {
            button.classList.add('active');
            button.setAttribute('aria-current', 'true');
        } else {
            button.classList.remove('active');
            button.removeAttribute('aria-current');
        }
    });
}

// =============================================================================
// Dashboard API Functions
// =============================================================================

/**
 * Get dashboard data with optional filter
 * @param {string} filter - Filter type ('all', 'pending', 'paid')
 * @returns {Promise<object>} - Dashboard data
 */
async function getDashboardData(filter = 'all') {
    return apiRequest(`${API_BASE}/dashboard?show=${filter}`);
}

/**
 * Apply filter and refresh the patient list
 * @param {string} filter - Filter to apply ('all', 'pending', 'paid')
 */
async function applyFilter(filter) {
    try {
        // Update URL without reload
        const url = new URL(window.location);
        url.searchParams.set('show', filter);
        window.history.pushState({}, '', url);
        
        // Update active filter button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.filter === filter) {
                btn.classList.add('active');
            }
        });
        
        // Fetch and render data
        const data = await getDashboardData(filter);
        renderPatientsList(data);
    } catch (error) {
        showToast(error.message || 'Error al cargar los datos', 'error');
    }
}

/**
 * Render the patients list from dashboard data
 * @param {object} data - Dashboard data from API
 */
function renderPatientsList(data) {
    const container = document.querySelector('.patients-grid-container');
    if (!container) return;
    
    const { grouped_sessions, allow_delete } = data;
    
    if (!grouped_sessions || grouped_sessions.length === 0) {
        container.innerHTML = `
            <div class="text-center my-5 py-5">
                <i class="bi bi-people display-1 text-body-secondary mb-3" aria-hidden="true"></i>
                <h3 class="text-body-secondary">No hay pacientes</h3>
                <p class="text-body-secondary mb-4">Comienza agregando tu primer paciente.</p>
                <a href="/patients/add" class="btn btn-primary">
                    <i class="bi bi-person-plus me-1" aria-hidden="true"></i>
                    Agregar Paciente
                </a>
            </div>
        `;
        return;
    }
    
    let html = '<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4">';
    
    grouped_sessions.forEach((patient, index) => {
        const patientId = patient.patient_id;
        const patientName = patient.patient_name;
        const sessions = patient.sessions;
        const escapedName = escapeHtml(patientName);
        
        html += `
            <div class="col">
                <div class="card h-100 patient-card fade-in" data-patient-id="${patientId}" style="animation-delay: ${index * 0.05}s">
                    <!-- Patient header -->
                    <div class="card-header">
                        <h5 class="mb-2 patient-name" title="${patientName}">
                            <i class="bi bi-person-fill me-1 text-mlc-teal" aria-hidden="true"></i>
                            ${patientName}
                        </h5>
                        <div class="btn-group btn-group-sm w-100" role="group" aria-label="Acciones de paciente">
                            <button type="button"
                               class="btn btn-outline-secondary flex-fill" 
                               title="Editar paciente" 
                               aria-label="Editar paciente ${patientName}"
                               onclick="openEditPatientModal(${patientId}, '${escapedName}')">
                                <i class="bi bi-pencil me-1" aria-hidden="true"></i>Editar
                            </button>
                            ${allow_delete ? `
                                <button type="button"
                                   class="btn btn-outline-danger flex-fill" 
                                   title="Eliminar paciente" 
                                   aria-label="Eliminar paciente ${patientName}"
                                   onclick="openDeletePatientModal(${patientId}, '${escapedName}')">
                                    <i class="bi bi-trash me-1" aria-hidden="true"></i>Eliminar
                                </button>
                            ` : ''}
                        </div>
                    </div>

                    <!-- Patient body with sessions carousel -->
                    <div class="card-body p-2">
                        ${renderSessionsCarousel(patientId, sessions)}
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
    
    // Re-initialize carousels
    initializeCarousels();
}

/**
 * Render sessions carousel for a patient
 * @param {number} patientId - Patient ID
 * @param {Array} sessions - Sessions array
 * @returns {string} - HTML string
 */
function renderSessionsCarousel(patientId, sessions) {
    if (!sessions || sessions.length === 0) {
        return `
            <p class="text-body-secondary text-center my-3">
                <i class="bi bi-calendar-x me-1" aria-hidden="true"></i>
                No hay sesiones registradas.
            </p>
        `;
    }
    
    const singleSlide = sessions.length <= 1 ? 'single-slide' : '';
    
    let carouselItems = '';
    let indicators = '';
    
    sessions.forEach((session, index) => {
        const isFirst = index === 0;
        const sessionId = session.id;
        const sessionDate = session.date;
        const sessionPrice = session.price;
        const pending = session.pending;
        const escapedDate = escapeHtml(sessionDate);
        
        const badgeClass = pending ? 'text-bg-warning' : 'text-bg-success';
        const badgeText = pending ? 'PENDIENTE' : 'PAGADO';
        
        carouselItems += `
            <div class="carousel-item ${isFirst ? 'active' : ''}" data-session-pending="${pending ? 'true' : 'false'}">
                <div class="card mx-auto session-card" data-session-id="${sessionId}">
                    <div class="card-header d-flex justify-content-between align-items-center py-2">
                        <small class="text-body-secondary session-date">${sessionDate}</small>
                        <span class="badge ${badgeClass} session-status">${badgeText}</span>
                    </div>

                    <div class="card-body py-2">
                        <p class="card-text mb-0 session-price">${sessionPrice}</p>
                    </div>

                    <div class="card-footer py-2">
                        <div class="btn-group btn-group-sm w-100" role="group" aria-label="Acciones de sesión">
                            <button type="button"
                               class="btn btn-outline-secondary flex-fill"
                               title="Editar sesión"
                               aria-label="Editar sesión del ${sessionDate}"
                               onclick="openEditSessionModal(${sessionId}, ${patientId})">
                                <i class="bi bi-pencil-square me-1" aria-hidden="true"></i>Editar
                            </button>
                            <button type="button"
                               class="btn btn-outline-danger flex-fill delete-session-btn"
                               title="Eliminar sesión"
                               aria-label="Eliminar sesión del ${sessionDate}"
                               onclick="openDeleteSessionModal(${sessionId}, '${escapedDate}')">
                                <i class="bi bi-trash me-1" aria-hidden="true"></i>Eliminar
                            </button>
                            ${pending ? `
                                <button type="button"
                                   class="btn btn-success flex-fill toggle-payment-btn"
                                   title="Marcar como pagado"
                                   aria-label="Marcar sesión del ${sessionDate} como pagado"
                                   onclick="togglePayment(${sessionId})">
                                    <i class="bi bi-check-circle me-1" aria-hidden="true"></i>Pagado
                                </button>
                            ` : `
                                <button type="button"
                                   class="btn btn-outline-secondary flex-fill toggle-payment-btn"
                                   title="Marcar como pendiente"
                                   aria-label="Marcar sesión del ${sessionDate} como pendiente"
                                   onclick="togglePayment(${sessionId})">
                                    <i class="bi bi-clock-history me-1" aria-hidden="true"></i>Pendiente
                                </button>
                            `}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        indicators += `
            <button type="button" 
                    data-bs-target="#carousel-${patientId}" 
                    data-bs-slide-to="${index}" 
                    ${isFirst ? 'class="active" aria-current="true"' : ''}
                    aria-label="Sesión ${index + 1}"
                    ${sessions.length <= 1 ? 'disabled' : ''}>
            </button>
        `;
    });
    
    return `
        <div id="carousel-${patientId}" class="carousel slide" data-bs-ride="false" data-bs-touch="true">
            <div class="carousel-inner">
                ${carouselItems}
            </div>
            <div class="carousel-indicators-bottom ${singleSlide}">
                ${indicators}
            </div>
        </div>
    `;
}

/**
 * Escape HTML to prevent XSS
 * @param {string} str - String to escape
 * @returns {string} - Escaped string
 */
function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}
