/**
 * Main Application Entry Point
 * @module main
 * @description Initializes all JavaScript modules for the Therapy Session Management App
 * @version 2.8.0
 */

// API Modules
import { initApi } from './modules/api/client.js';

// UI Modules
import { initToast, showToast } from './modules/ui/toast.js';
import { initModals, openModal, closeModal } from './modules/ui/modal.js';
import { initCarousels } from './modules/ui/carousel.js';
import { initAccessibility, announceToScreenReader } from './modules/ui/accessibility.js';

// Component Modules
import { initPatientCard, openEditPatientModal, openDeletePatientModal } from './modules/components/patientCard.js';
import { initSessionCard, openEditSessionModal, openDeleteSessionModal, togglePayment } from './modules/components/sessionCard.js';
import { initFilterButtons, applyFilter } from './modules/components/filterButtons.js';
import { renderPatientsList, renderSessionsCarousel } from './modules/components/dashboardRenderer.js';

// Utility Modules
import { formatDisplayDate, formatPrice } from './modules/utils/formatters.js';
import { escapeHtml } from './modules/utils/helpers.js';

/**
 * Global error handler for uncaught errors
 */
window.addEventListener('error', (event) => {
    console.error('Uncaught error:', event.error);
    showToast('Ha ocurrido un error inesperado', 'error');
});

/**
 * Global promise rejection handler
 */
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    // Don't show toast for every rejection to avoid spam
});

/**
 * Initialize application when DOM is ready
 */
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Initialize core modules
        initApi();
        initToast();
        initAccessibility();
        
        // Initialize UI components
        initModals();
        initCarousels();
        
        // Initialize page-specific components based on page content
        const isDashboard = document.querySelector('.patients-grid-container') || 
                           document.querySelector('.patients-container') ||
                           document.querySelector('[data-patient-id]');
        
        if (isDashboard) {
            initPatientCard();
            initSessionCard();
            initFilterButtons();
        }
        
        console.log('Application initialized successfully');
    } catch (error) {
        console.error('Failed to initialize application:', error);
    }
});

// Re-export commonly used functions for global access
// This ensures backward compatibility with onclick handlers in templates
export { 
    showToast, 
    openModal, 
    closeModal,
    formatDisplayDate,
    formatPrice,
    escapeHtml,
    announceToScreenReader,
    applyFilter,
    openEditPatientModal,
    openDeletePatientModal,
    openEditSessionModal,
    openDeleteSessionModal,
    togglePayment,
    renderPatientsList,
    renderSessionsCarousel,
    initCarousels
};
