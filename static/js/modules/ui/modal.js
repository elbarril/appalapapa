/**
 * Modal Management Module
 * @module ui/modal
 * @description Modal dialog management with focus trapping and accessibility
 */

/**
 * Get all focusable elements within a container
 * @param {HTMLElement} container - Container element
 * @returns {NodeListOf<Element>} - Focusable elements
 */
function getFocusableElements(container) {
    return container.querySelectorAll(
        'button:not([disabled]), ' +
        '[href], ' +
        'input:not([disabled]):not([type="hidden"]), ' +
        'select:not([disabled]), ' +
        'textarea:not([disabled]), ' +
        '[tabindex]:not([tabindex="-1"]):not([disabled])'
    );
}

/**
 * Trap focus within a modal
 * @param {HTMLElement} modal - Modal element
 * @param {KeyboardEvent} event - Keyboard event
 */
function trapFocusInModal(modal, event) {
    const focusableElements = getFocusableElements(modal);
    if (focusableElements.length === 0) return;
    
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    if (event.shiftKey) {
        // Shift + Tab
        if (document.activeElement === firstFocusable) {
            lastFocusable.focus();
            event.preventDefault();
        }
    } else {
        // Tab
        if (document.activeElement === lastFocusable) {
            firstFocusable.focus();
            event.preventDefault();
        }
    }
}

/**
 * Initialize focus management for a single modal
 * @param {HTMLElement} modal - Modal element to initialize
 */
function initModalFocus(modal) {
    let triggerElement = null;
    
    // Store trigger element when modal opens
    modal.addEventListener('show.bs.modal', function() {
        triggerElement = document.activeElement;
    });
    
    // Focus first focusable element when modal is shown
    modal.addEventListener('shown.bs.modal', function() {
        const focusableElements = getFocusableElements(modal);
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }
    });
    
    // Return focus to trigger element when modal closes
    modal.addEventListener('hidden.bs.modal', function() {
        if (triggerElement && document.body.contains(triggerElement)) {
            triggerElement.focus();
        }
    });
    
    // Trap focus within modal
    modal.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            trapFocusInModal(modal, e);
        }
    });
}

/**
 * Initialize focus management for all modals on the page
 */
export function initModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => initModalFocus(modal));
}

/**
 * Open a modal by ID
 * @param {string} modalId - Modal element ID
 * @returns {bootstrap.Modal|null} - Bootstrap Modal instance or null
 * @example
 * openModal('editPatientModal');
 */
export function openModal(modalId) {
    const modalEl = document.getElementById(modalId);
    if (!modalEl) {
        console.error(`Modal not found: ${modalId}`);
        return null;
    }
    
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
    return modal;
}

/**
 * Close a modal by ID
 * @param {string} modalId - Modal element ID
 * @example
 * closeModal('editPatientModal');
 */
export function closeModal(modalId) {
    const modalEl = document.getElementById(modalId);
    if (!modalEl) return;
    
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) {
        modal.hide();
    }
}

/**
 * Get Bootstrap Modal instance for an element
 * @param {string} modalId - Modal element ID
 * @returns {bootstrap.Modal|null} - Bootstrap Modal instance or null
 */
export function getModalInstance(modalId) {
    const modalEl = document.getElementById(modalId);
    if (!modalEl) return null;
    return bootstrap.Modal.getInstance(modalEl);
}

// Make modal functions globally available for backward compatibility
window.openModal = openModal;
window.closeModal = closeModal;
