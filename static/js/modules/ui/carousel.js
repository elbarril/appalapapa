/**
 * Carousel Module
 * @module ui/carousel
 * @description Carousel management with keyboard navigation and accessibility
 */

import { announceToScreenReader } from './accessibility.js';

/**
 * Enable keyboard navigation for a carousel
 * @param {HTMLElement} carouselEl - The carousel element
 * @param {bootstrap.Carousel} bsCarousel - Bootstrap carousel instance
 */
function enableCarouselKeyboardNav(carouselEl, bsCarousel) {
    carouselEl.addEventListener('keydown', function(e) {
        const items = carouselEl.querySelectorAll('.carousel-item');
        if (items.length <= 1) return; // No navigation needed for single item
        
        switch(e.key) {
            case 'ArrowLeft':
                bsCarousel.prev();
                e.preventDefault();
                break;
            case 'ArrowRight':
                bsCarousel.next();
                e.preventDefault();
                break;
            case 'Home':
                bsCarousel.to(0);
                e.preventDefault();
                break;
            case 'End':
                bsCarousel.to(items.length - 1);
                e.preventDefault();
                break;
        }
    });
}

/**
 * Update carousel indicators to reflect current slide
 * @param {HTMLElement} carouselEl - The carousel element
 * @param {number} activeIndex - The index of the active slide
 */
export function updateCarouselIndicators(carouselEl, activeIndex) {
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

/**
 * Initialize a single carousel with touch support and keyboard navigation
 * @param {HTMLElement} carouselEl - Carousel element to initialize
 * @returns {bootstrap.Carousel} - Bootstrap carousel instance
 */
export function initCarousel(carouselEl) {
    // Create Bootstrap carousel instance with touch enabled
    const carousel = new bootstrap.Carousel(carouselEl, {
        interval: false,  // No auto-slide
        touch: true,      // Enable touch/swipe
        wrap: true        // Wrap around at ends
    });
    
    // Update indicators when slide changes
    carouselEl.addEventListener('slid.bs.carousel', function(event) {
        updateCarouselIndicators(carouselEl, event.to);
        
        // Announce slide change to screen readers
        const totalSlides = carouselEl.querySelectorAll('.carousel-item').length;
        announceToScreenReader(`Sesión ${event.to + 1} de ${totalSlides}`, 'polite');
    });
    
    // Add keyboard navigation
    enableCarouselKeyboardNav(carouselEl, carousel);
    
    // Make carousel focusable for keyboard users
    if (!carouselEl.hasAttribute('tabindex')) {
        carouselEl.setAttribute('tabindex', '0');
    }
    carouselEl.setAttribute('role', 'region');
    carouselEl.setAttribute('aria-roledescription', 'carrusel');
    
    // Get patient name for accessible label
    const patientCard = carouselEl.closest('[data-patient-id]');
    const patientName = patientCard?.querySelector('.patient-name')?.textContent?.trim();
    if (patientName) {
        carouselEl.setAttribute('aria-label', `Sesiones de ${patientName}`);
    }
    
    return carousel;
}

/**
 * Initialize all carousels on the page
 */
export function initCarousels() {
    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carouselEl => initCarousel(carouselEl));
}

/**
 * Get carousel by patient ID
 * @param {number|string} patientId - Patient ID
 * @returns {HTMLElement|null} - Carousel element or null
 */
export function getCarouselByPatientId(patientId) {
    return document.getElementById(`carousel-${patientId}`);
}

/**
 * Go to specific slide in a carousel
 * @param {string|HTMLElement} carousel - Carousel ID or element
 * @param {number} index - Slide index
 */
export function goToSlide(carousel, index) {
    const carouselEl = typeof carousel === 'string' 
        ? document.getElementById(carousel) 
        : carousel;
    
    if (!carouselEl) return;
    
    const bsCarousel = bootstrap.Carousel.getInstance(carouselEl);
    if (bsCarousel) {
        bsCarousel.to(index);
    }
}
