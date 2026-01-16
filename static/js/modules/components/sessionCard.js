/**
 * Session Card Component Module
 * @module components/sessionCard
 * @description Session card UI component with edit/delete/toggle functionality
 */

import { getSession, updateSession, deleteSession, toggleSessionPayment } from '../api/sessions.js';
import { showToast } from '../ui/toast.js';
import { openModal, closeModal } from '../ui/modal.js';
import { validateSessionForm } from '../utils/validators.js';
import { formatDisplayDate, formatPrice } from '../utils/formatters.js';
import { escapeHtml } from '../utils/helpers.js';
import { announceToScreenReader } from '../ui/accessibility.js';

/**
 * Get current filter from URL
 * @returns {string} - Current filter ('all', 'pending', 'paid')
 */
function getCurrentFilter() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('show') || 'all';
}

/**
 * Open the edit session modal
 * @param {number} sessionId - Session ID
 * @param {number} personId - Person ID
 */
export async function openEditSessionModal(sessionId, personId) {
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

        openModal('editSessionModal');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Save edited session
 * @returns {Promise<void>}
 */
export async function saveEditSession() {
    const sessionId = document.getElementById('editSessionId').value;
    const sessionDate = document.getElementById('editSessionDate').value;
    const sessionPrice = document.getElementById('editSessionPrice').value;
    const pending = document.getElementById('editSessionPending').checked;
    const notes = document.getElementById('editSessionNotes').value.trim();

    // Validate
    const validation = validateSessionForm({
        session_date: sessionDate,
        session_price: sessionPrice,
        notes: notes
    });
    if (!validation.valid) {
        showToast(validation.message, 'error');
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
        closeModal('editSessionModal');

        // Update session in UI
        updateSessionInUI(sessionId, updatedSession);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Update session data in the UI without refresh
 * @param {number|string} sessionId - Session ID
 * @param {Object} session - Updated session data
 */
export function updateSessionInUI(sessionId, session) {
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
    updateSessionBadge(sessionCard, session.pending);

    // Update toggle button and footer buttons
    updateSessionButtons(sessionId, session.pending);

    // Check if we need to remove this session from filtered view
    handleFilteredSessionUpdate(sessionId, session.pending);
}

/**
 * Update session badge based on pending status
 * @param {HTMLElement} sessionCard - Session card element
 * @param {boolean} pending - Whether session is pending
 */
function updateSessionBadge(sessionCard, pending) {
    const badgeElement = sessionCard.querySelector('.session-status');
    if (badgeElement) {
        if (pending) {
            badgeElement.className = 'badge text-bg-warning session-status';
            badgeElement.textContent = 'PENDIENTE';
        } else {
            badgeElement.className = 'badge text-bg-success session-status';
            badgeElement.textContent = 'PAGADO';
        }
    }
}

/**
 * Toggle payment status for a session
 * @param {number} sessionId - Session ID
 */
export async function togglePayment(sessionId) {
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
            updateSessionBadge(sessionCard, result.pending);

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
 * @param {number|string} sessionId - Session ID
 * @param {boolean} pending - Whether session is pending
 */
export function updateSessionButtons(sessionId, pending) {
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
               aria-label="Editar sesión del ${escapeHtml(dateText)}"
               onclick="openEditSessionModal(${sessionId}, ${personId})">
                <i class="bi bi-pencil-square me-1" aria-hidden="true"></i>Editar
            </button>
            <button type="button"
               class="btn btn-outline-danger flex-fill delete-session-btn"
               title="Eliminar sesión"
               aria-label="Eliminar sesión del ${escapeHtml(dateText)}"
               onclick="openDeleteSessionModal(${sessionId}, '${escapeHtml(dateText)}')">
                <i class="bi bi-trash me-1" aria-hidden="true"></i>Eliminar
            </button>
            <button type="button"
               class="btn btn-success flex-fill toggle-payment-btn"
               title="Marcar como pagado"
               aria-label="Marcar sesión del ${escapeHtml(dateText)} como pagado"
               onclick="togglePayment(${sessionId})">
                <i class="bi bi-check-circle me-1" aria-hidden="true"></i>Pagado
            </button>
        `;
    } else {
        btnGroup.innerHTML = `
            <button type="button"
               class="btn btn-outline-secondary flex-fill"
               title="Editar sesión"
               aria-label="Editar sesión del ${escapeHtml(dateText)}"
               onclick="openEditSessionModal(${sessionId}, ${personId})">
                <i class="bi bi-pencil-square me-1" aria-hidden="true"></i>Editar
            </button>
            <button type="button"
               class="btn btn-outline-danger flex-fill delete-session-btn"
               title="Eliminar sesión"
               aria-label="Eliminar sesión del ${escapeHtml(dateText)}"
               onclick="openDeleteSessionModal(${sessionId}, '${escapeHtml(dateText)}')">
                <i class="bi bi-trash me-1" aria-hidden="true"></i>Eliminar
            </button>
            <button type="button"
               class="btn btn-outline-secondary flex-fill toggle-payment-btn"
               title="Marcar como pendiente"
               aria-label="Marcar sesión del ${escapeHtml(dateText)} como pendiente"
               onclick="togglePayment(${sessionId})">
                <i class="bi bi-clock-history me-1" aria-hidden="true"></i>Pendiente
            </button>
        `;
    }
}

/**
 * Handle session removal from filtered view when payment status changes
 * @param {number|string} sessionId - Session ID
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
export function openDeleteSessionModal(sessionId, sessionDate) {
    const modal = document.getElementById('deleteSessionModal');
    if (!modal) return;

    document.getElementById('deleteSessionId').value = sessionId;
    document.getElementById('deleteSessionDate').textContent = sessionDate;

    openModal('deleteSessionModal');
}

/**
 * Confirm and delete session
 * @returns {Promise<void>}
 */
export async function confirmDeleteSession() {
    const sessionId = document.getElementById('deleteSessionId').value;

    try {
        await deleteSession(sessionId);
        showToast('Sesión eliminada correctamente', 'success');

        // Close modal
        closeModal('deleteSessionModal');

        // Remove session from UI
        removeSessionFromUI(sessionId);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Remove session from the UI
 * @param {number|string} sessionId - Session ID
 */
export function removeSessionFromUI(sessionId) {
    const sessionCard = document.querySelector(`[data-session-id="${sessionId}"]`);
    if (!sessionCard) return;

    const carouselItem = sessionCard.closest('.carousel-item');
    const carousel = carouselItem?.closest('.carousel');
    const patientCard = sessionCard.closest('[data-patient-id]');

    if (!carousel) return;

    const carouselInner = carousel.querySelector('.carousel-inner');
    const allItems = carouselInner.querySelectorAll('.carousel-item');
    const currentFilter = getCurrentFilter();

    // Import dynamically to avoid circular dependency
    import('./patientCard.js').then(({ removePatientFromUI }) => {
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
            handleCarouselItemRemoval(carouselItem, carousel, carouselInner, allItems);
        }
    });
}

/**
 * Handle carousel item removal and indicator updates
 * @param {HTMLElement} carouselItem - Carousel item to remove
 * @param {HTMLElement} carousel - Carousel container
 * @param {HTMLElement} carouselInner - Carousel inner container
 * @param {NodeListOf<Element>} allItems - All carousel items
 */
function handleCarouselItemRemoval(carouselItem, carousel, carouselInner, allItems) {
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

/**
 * Initialize session card event listeners
 */
export function initSessionCard() {
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
}

// Make functions globally available for backward compatibility with onclick handlers
window.openEditSessionModal = openEditSessionModal;
window.openDeleteSessionModal = openDeleteSessionModal;
window.saveEditSession = saveEditSession;
window.confirmDeleteSession = confirmDeleteSession;
window.togglePayment = togglePayment;
