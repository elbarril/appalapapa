/**
 * Toast Notifications Module
 * @module ui/toast
 * @description Toast notification system with accessibility support
 */

import { escapeHtml } from '../utils/helpers.js';

/** @type {HTMLElement|null} Toast container element */
let toastContainer = null;

/**
 * Toast type to Bootstrap class mapping
 * @type {Object<string, string>}
 */
const TYPE_CLASSES = {
    success: 'text-bg-success',
    error: 'text-bg-danger',
    warning: 'text-bg-warning',
    info: 'text-bg-info',
};

/**
 * Initialize toast container
 * Creates the container element if it doesn't exist
 */
export function initToast() {
    toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1100';
        // ARIA live region for screen reader announcements
        toastContainer.setAttribute('aria-live', 'polite');
        toastContainer.setAttribute('aria-atomic', 'false');
        document.body.appendChild(toastContainer);
    }
}

/**
 * Show a toast notification
 * @param {string} message - Message to display
 * @param {('success'|'error'|'warning'|'info')} [type='info'] - Notification type
 * @param {number} [duration=4000] - Duration in milliseconds
 * @example
 * showToast('Paciente guardado', 'success');
 * showToast('Error al guardar', 'error');
 */
export function showToast(message, type = 'info', duration = 4000) {
    if (!toastContainer) {
        initToast();
    }

    // Use 'alert' role for errors (assertive), 'status' for others (polite)
    const role = type === 'error' ? 'alert' : 'status';
    const ariaLive = type === 'error' ? 'assertive' : 'polite';

    const toastId = `toast-${Date.now()}`;
    const toastHTML = `
        <div id="${toastId}" 
             class="toast ${TYPE_CLASSES[type] || TYPE_CLASSES.info}" 
             role="${role}" 
             aria-live="${ariaLive}" 
             aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${escapeHtml(message)}
                </div>
                <button type="button" 
                        class="btn-close btn-close-white me-2 m-auto" 
                        data-bs-dismiss="toast" 
                        aria-label="Cerrar notificación">
                </button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastEl = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastEl, { delay: duration });
    toast.show();

    // Remove toast from DOM after it's hidden
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

/**
 * Clear all visible toasts
 */
export function clearAllToasts() {
    if (!toastContainer) return;
    
    const toasts = toastContainer.querySelectorAll('.toast');
    toasts.forEach(toastEl => {
        const toast = bootstrap.Toast.getInstance(toastEl);
        if (toast) {
            toast.hide();
        }
    });
}

// Make showToast globally available for backward compatibility
// This allows onclick handlers in templates to still work
window.showToast = showToast;
