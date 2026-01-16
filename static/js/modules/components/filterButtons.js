/**
 * Filter Buttons Component Module
 * @module components/filterButtons
 * @description Dashboard filter buttons with accessibility support
 */

import { getDashboardData } from '../api/dashboard.js';
import { showToast } from '../ui/toast.js';
import { announceToScreenReader } from '../ui/accessibility.js';
import { renderPatientsList } from './dashboardRenderer.js';

/**
 * Filter labels for screen reader announcements
 * @type {Object<string, string>}
 */
const FILTER_LABELS = {
    all: 'Todas',
    pending: 'Pendientes',
    paid: 'Pagadas'
};

/**
 * Initialize filter buttons with proper ARIA attributes
 */
export function initFilterButtons() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        const isActive = btn.classList.contains('active');
        btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
        
        // Add click handler if not already present
        if (!btn.dataset.filterInitialized) {
            btn.addEventListener('click', function() {
                const filter = this.dataset.filter;
                if (filter) {
                    applyFilter(filter);
                }
            });
            btn.dataset.filterInitialized = 'true';
        }
    });
}

/**
 * Get current filter from URL
 * @returns {string} - Current filter ('all', 'pending', 'paid')
 */
export function getCurrentFilter() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('show') || 'all';
}

/**
 * Apply filter and refresh the patient list
 * @param {('all'|'pending'|'paid')} filter - Filter to apply
 */
export async function applyFilter(filter) {
    try {
        // Update URL without reload
        const url = new URL(window.location);
        url.searchParams.set('show', filter);
        window.history.pushState({}, '', url);
        
        // Update active filter button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-pressed', 'false');
            if (btn.dataset.filter === filter) {
                btn.classList.add('active');
                btn.setAttribute('aria-pressed', 'true');
            }
        });
        
        // Fetch and render data
        const data = await getDashboardData(filter);
        renderPatientsList(data);
        
        // Announce filter change to screen readers
        const count = data.grouped_sessions ? data.grouped_sessions.length : 0;
        announceToScreenReader(
            `Filtro cambiado a ${FILTER_LABELS[filter] || filter}. Mostrando ${count} pacientes.`
        );
    } catch (error) {
        showToast(error.message || 'Error al cargar los datos', 'error');
    }
}

// Make applyFilter globally available for backward compatibility
window.applyFilter = applyFilter;
