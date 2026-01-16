/**
 * Accessibility Module
 * @module ui/accessibility
 * @description Accessibility utilities including screen reader announcements
 */

/** @type {HTMLElement|null} Screen reader announcer element */
let announcer = null;

/**
 * Initialize the screen reader announcer element
 */
function initAnnouncer() {
    if (announcer) return;
    
    announcer = document.createElement('div');
    announcer.id = 'sr-announcer';
    announcer.className = 'visually-hidden';
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('aria-atomic', 'true');
    announcer.setAttribute('role', 'status');
    document.body.appendChild(announcer);
}

/**
 * Announce a message to screen readers using an ARIA live region
 * @param {string} message - Message to announce
 * @param {('polite'|'assertive')} [priority='polite'] - Announcement priority
 * @example
 * announceToScreenReader('Sesión guardada correctamente');
 * announceToScreenReader('Error: El nombre es requerido', 'assertive');
 */
export function announceToScreenReader(message, priority = 'polite') {
    if (!announcer) {
        initAnnouncer();
    }
    
    // Update the live region priority if needed
    announcer.setAttribute('aria-live', priority);
    announcer.setAttribute('role', priority === 'assertive' ? 'alert' : 'status');
    
    // Clear and set message (the delay ensures screen readers catch the change)
    announcer.textContent = '';
    setTimeout(() => {
        announcer.textContent = message;
    }, 100);
}

/**
 * Set up focus visible polyfill behavior
 * Adds 'focus-visible' class for keyboard focus only
 */
export function initFocusVisible() {
    // Only keyboard focus should show focus outline
    document.addEventListener('mousedown', () => {
        document.body.classList.add('using-mouse');
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            document.body.classList.remove('using-mouse');
        }
    });
}

/**
 * Check if an element is visible to screen readers
 * @param {HTMLElement} element - Element to check
 * @returns {boolean} - True if visible to screen readers
 */
export function isVisibleToScreenReader(element) {
    if (!element) return false;
    
    const style = window.getComputedStyle(element);
    
    // Check if element is hidden
    if (style.display === 'none') return false;
    if (style.visibility === 'hidden') return false;
    if (element.getAttribute('aria-hidden') === 'true') return false;
    
    return true;
}

/**
 * Make an element accessible with proper ARIA attributes
 * @param {HTMLElement} element - Element to make accessible
 * @param {Object} options - Accessibility options
 * @param {string} [options.role] - ARIA role
 * @param {string} [options.label] - ARIA label
 * @param {string} [options.describedBy] - ID of describing element
 */
export function makeAccessible(element, options = {}) {
    if (options.role) {
        element.setAttribute('role', options.role);
    }
    if (options.label) {
        element.setAttribute('aria-label', options.label);
    }
    if (options.describedBy) {
        element.setAttribute('aria-describedby', options.describedBy);
    }
}

/**
 * Initialize accessibility features
 */
export function initAccessibility() {
    initAnnouncer();
    initFocusVisible();
}
