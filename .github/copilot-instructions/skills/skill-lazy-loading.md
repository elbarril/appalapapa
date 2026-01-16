# Skill: Lazy Loading

> **Scope:** Lazy loading strategies for images, components, routes, and data in Flask/Jinja2 web applications to improve initial load performance.

---

## 1. Image Lazy Loading

### Native Lazy Loading

```html
<!-- Native browser lazy loading - simplest approach -->
<img 
    src="{{ url_for('static', filename='images/patient-photo.jpg') }}"
    alt="Foto del paciente"
    loading="lazy"
    decoding="async"
    width="200"
    height="200"
>
```

### Lazy Loading with Placeholder

```html
<!-- templates/macros/_images.html -->

{% macro lazy_image(
    src,
    alt,
    width,
    height,
    class_name='',
    placeholder='blur'
) %}
{#
    Lazy loaded image with placeholder.
    
    Parameters:
        src (str): Image path relative to static/images/
        alt (str): Alt text for accessibility
        width (int): Image width in pixels
        height (int): Image height in pixels
        class_name (str): Additional CSS classes
        placeholder (str): 'blur' | 'skeleton' | 'color'
#}
{% set aspect = (height / width * 100)|round(2) %}

<div class="lazy-image-wrapper lazy-image--{{ placeholder }}" 
     style="aspect-ratio: {{ width }}/{{ height }}">
    
    {% if placeholder == 'blur' %}
    {# Low-quality placeholder (generate with script) #}
    <img 
        src="{{ url_for('static', filename='images/placeholders/' + src|replace('.', '-tiny.')) }}"
        alt=""
        class="lazy-image__placeholder"
        aria-hidden="true">
    {% endif %}
    
    <img 
        src="{{ url_for('static', filename='images/' + src) }}"
        alt="{{ alt }}"
        width="{{ width }}"
        height="{{ height }}"
        loading="lazy"
        decoding="async"
        class="lazy-image__main {{ class_name }}"
        onload="this.parentElement.classList.add('loaded')">
</div>
{% endmacro %}
```

```css
/* static/css/components/_lazy-images.css */

.lazy-image-wrapper {
    position: relative;
    overflow: hidden;
    background-color: var(--bg-skeleton);
}

/* Blur placeholder */
.lazy-image--blur .lazy-image__placeholder {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: blur(20px);
    transform: scale(1.1);
    transition: opacity 0.3s ease;
}

.lazy-image--blur.loaded .lazy-image__placeholder {
    opacity: 0;
}

/* Skeleton placeholder */
.lazy-image--skeleton::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
        90deg,
        var(--bg-skeleton) 25%,
        var(--bg-skeleton-highlight) 50%,
        var(--bg-skeleton) 75%
    );
    background-size: 200% 100%;
    animation: skeleton-loading 1.5s infinite;
}

.lazy-image--skeleton.loaded::before {
    display: none;
}

/* Main image */
.lazy-image__main {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.lazy-image-wrapper.loaded .lazy-image__main {
    opacity: 1;
}

@keyframes skeleton-loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
```

### Intersection Observer for Custom Lazy Loading

```javascript
// static/js/modules/ui/lazyLoader.js

/**
 * Advanced lazy loading with Intersection Observer.
 * @module ui/lazyLoader
 */

/**
 * Initialize lazy loading for images
 * @param {Object} options - Configuration options
 * @param {string} options.selector - CSS selector for lazy images
 * @param {string} options.rootMargin - Margin around viewport
 * @param {number} options.threshold - Visibility threshold (0-1)
 */
export function initLazyImages(options = {}) {
    const {
        selector = '[data-lazy-src]',
        rootMargin = '50px 0px',
        threshold = 0.01
    } = options;
    
    const images = document.querySelectorAll(selector);
    
    if (!images.length) return;
    
    // Use native lazy loading if available and no custom behavior needed
    if ('loading' in HTMLImageElement.prototype && !options.forceObserver) {
        images.forEach(img => {
            img.src = img.dataset.lazySrc;
            if (img.dataset.lazySrcset) {
                img.srcset = img.dataset.lazySrcset;
            }
            img.loading = 'lazy';
        });
        return;
    }
    
    // Fallback to Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadImage(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { rootMargin, threshold });
    
    images.forEach(img => observer.observe(img));
}

/**
 * Load a lazy image
 * @param {HTMLImageElement} img - Image element to load
 */
function loadImage(img) {
    const src = img.dataset.lazySrc;
    const srcset = img.dataset.lazySrcset;
    
    // Preload image
    const tempImg = new Image();
    
    tempImg.onload = () => {
        img.src = src;
        if (srcset) img.srcset = srcset;
        img.classList.add('loaded');
        img.removeAttribute('data-lazy-src');
        img.removeAttribute('data-lazy-srcset');
    };
    
    tempImg.onerror = () => {
        img.classList.add('error');
        console.warn(`Failed to load image: ${src}`);
    };
    
    tempImg.src = src;
}

/**
 * Lazy load background images
 * @param {string} selector - CSS selector for elements with lazy backgrounds
 */
export function initLazyBackgrounds(selector = '[data-lazy-bg]') {
    const elements = document.querySelectorAll(selector);
    
    if (!elements.length) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.style.backgroundImage = `url('${el.dataset.lazyBg}')`;
                el.classList.add('bg-loaded');
                el.removeAttribute('data-lazy-bg');
                observer.unobserve(el);
            }
        });
    }, { rootMargin: '100px 0px' });
    
    elements.forEach(el => observer.observe(el));
}
```

---

## 2. Component Lazy Loading

### Dynamic Import for Components

```javascript
// static/js/main.js

/**
 * Lazy load components based on presence in DOM
 */
async function initComponents() {
    const componentMap = {
        // Modal component
        '[data-modal]': {
            loader: () => import('./modules/ui/modal.js'),
            init: (mod) => mod.initModals()
        },
        
        // Toast notifications
        '[data-toast-container]': {
            loader: () => import('./modules/ui/toast.js'),
            init: (mod) => mod.initToasts()
        },
        
        // Session carousel
        '.session-carousel': {
            loader: () => import('./modules/ui/carousel.js'),
            init: (mod) => mod.initCarousels()
        },
        
        // Charts (heavy dependency)
        '[data-chart]': {
            loader: () => import('./modules/components/charts.js'),
            init: (mod) => mod.initCharts()
        },
        
        // Date picker
        'input[type="date"]': {
            loader: () => import('./modules/ui/datePicker.js'),
            init: (mod) => mod.initDatePickers()
        },
        
        // Rich text editor
        '[data-rich-editor]': {
            loader: () => import('./modules/ui/richEditor.js'),
            init: (mod) => mod.initEditors()
        }
    };
    
    // Load components that are present in the DOM
    const loadPromises = [];
    
    for (const [selector, config] of Object.entries(componentMap)) {
        if (document.querySelector(selector)) {
            loadPromises.push(
                config.loader()
                    .then(config.init)
                    .catch(err => console.error(`Failed to load ${selector}:`, err))
            );
        }
    }
    
    await Promise.all(loadPromises);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initComponents);
```

### Lazy Load on Interaction

```javascript
// static/js/modules/ui/lazyComponent.js

/**
 * Load component on user interaction.
 * @module ui/lazyComponent
 */

/**
 * Load a component when user interacts with trigger element
 * @param {string} triggerSelector - CSS selector for trigger elements
 * @param {Function} loader - Dynamic import function
 * @param {string} [event='click'] - Event to listen for
 */
export function loadOnInteraction(triggerSelector, loader, event = 'click') {
    const triggers = document.querySelectorAll(triggerSelector);
    
    if (!triggers.length) return;
    
    let loaded = false;
    let modulePromise = null;
    
    // Preload on hover for faster perceived load
    const preload = () => {
        if (!modulePromise) {
            modulePromise = loader();
        }
    };
    
    const handleInteraction = async (e) => {
        if (loaded) return;
        
        // Show loading state
        const trigger = e.currentTarget;
        trigger.classList.add('loading');
        
        try {
            const module = await (modulePromise || loader());
            loaded = true;
            
            // Initialize module
            if (module.init) {
                module.init();
            }
            
            // Re-trigger the original event
            if (event === 'click') {
                trigger.click();
            }
        } catch (err) {
            console.error('Failed to load component:', err);
        } finally {
            trigger.classList.remove('loading');
        }
    };
    
    triggers.forEach(trigger => {
        // Preload on hover
        trigger.addEventListener('mouseenter', preload, { once: true });
        trigger.addEventListener('focus', preload, { once: true });
        
        // Load on interaction
        trigger.addEventListener(event, handleInteraction, { once: true });
    });
}

// Usage example
// loadOnInteraction('[data-open-modal]', () => import('./modal.js'));
```

### Lazy Load Heavy Features

```javascript
// static/js/modules/components/dashboardRenderer.js

/**
 * Dashboard with lazy-loaded charts and reports
 */

let chartsLoaded = false;
let pdfLoaded = false;

/**
 * Load chart library on demand
 * @returns {Promise<Object>} Chart module
 */
async function loadCharts() {
    if (!chartsLoaded) {
        // Load Chart.js dynamically
        const { Chart } = await import('https://cdn.jsdelivr.net/npm/chart.js@4/+esm');
        chartsLoaded = true;
        return Chart;
    }
}

/**
 * Initialize dashboard with lazy-loaded components
 */
export async function initDashboard() {
    // Core dashboard - load immediately
    renderPatientList();
    renderSessionsSummary();
    
    // Charts - load when visible
    const chartSection = document.querySelector('#statistics-section');
    if (chartSection) {
        const observer = new IntersectionObserver(async (entries) => {
            if (entries[0].isIntersecting) {
                observer.disconnect();
                const Chart = await loadCharts();
                renderCharts(Chart);
            }
        });
        observer.observe(chartSection);
    }
    
    // PDF export - load on button click
    const exportBtn = document.querySelector('#export-pdf');
    if (exportBtn) {
        exportBtn.addEventListener('click', async () => {
            exportBtn.disabled = true;
            exportBtn.textContent = 'Generando...';
            
            if (!pdfLoaded) {
                await import('./pdfExporter.js');
                pdfLoaded = true;
            }
            
            window.exportToPdf();
            exportBtn.disabled = false;
            exportBtn.textContent = 'Exportar PDF';
        });
    }
}
```

---

## 3. Route-Based Lazy Loading

### Flask Route Optimization

```python
# app/routes/patients.py

from flask import Blueprint, render_template, jsonify, request

bp = Blueprint('patients', __name__)


@bp.route('/patients')
def list_patients():
    """
    Initial page load - minimal data for fast render.
    Additional data loaded via API.
    """
    # Only fetch what's needed for initial render
    return render_template('patients/list.html')


@bp.route('/api/v1/patients')
def get_patients():
    """
    API endpoint for lazy-loaded patient data.
    Called after initial page render.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    patients = PatientService.get_paginated(
        user_id=current_user.id,
        page=page,
        per_page=per_page
    )
    
    return jsonify({
        'patients': [p.to_dict() for p in patients.items],
        'total': patients.total,
        'pages': patients.pages,
        'current_page': patients.page
    })


@bp.route('/api/v1/patients/<int:id>/sessions')
def get_patient_sessions(id):
    """
    Lazy load sessions when patient card is expanded.
    """
    sessions = SessionService.get_by_patient(
        patient_id=id,
        user_id=current_user.id,
        limit=10
    )
    
    return jsonify({
        'sessions': [s.to_dict() for s in sessions]
    })
```

### Client-Side Route Loading

```javascript
// static/js/modules/api/patients.js

/**
 * Patient data API with lazy loading support.
 * @module api/patients
 */

const cache = new Map();

/**
 * Fetch patients with pagination
 * @param {Object} options - Fetch options
 * @param {number} options.page - Page number
 * @param {number} options.perPage - Items per page
 * @returns {Promise<Object>} Paginated patients
 */
export async function fetchPatients({ page = 1, perPage = 20 } = {}) {
    const cacheKey = `patients-${page}-${perPage}`;
    
    if (cache.has(cacheKey)) {
        return cache.get(cacheKey);
    }
    
    const response = await fetch(`/api/v1/patients?page=${page}&per_page=${perPage}`);
    
    if (!response.ok) {
        throw new Error('Failed to fetch patients');
    }
    
    const data = await response.json();
    cache.set(cacheKey, data);
    
    return data;
}

/**
 * Lazy load patient sessions when needed
 * @param {number} patientId - Patient ID
 * @returns {Promise<Array>} Patient sessions
 */
export async function fetchPatientSessions(patientId) {
    const cacheKey = `sessions-${patientId}`;
    
    if (cache.has(cacheKey)) {
        return cache.get(cacheKey);
    }
    
    const response = await fetch(`/api/v1/patients/${patientId}/sessions`);
    
    if (!response.ok) {
        throw new Error('Failed to fetch sessions');
    }
    
    const data = await response.json();
    cache.set(cacheKey, data.sessions);
    
    return data.sessions;
}

/**
 * Clear cache (after mutations)
 */
export function clearCache() {
    cache.clear();
}
```

---

## 4. Data Lazy Loading

### Infinite Scroll

```javascript
// static/js/modules/ui/infiniteScroll.js

/**
 * Infinite scroll implementation.
 * @module ui/infiniteScroll
 */

/**
 * Initialize infinite scroll for a container
 * @param {Object} options - Configuration
 * @param {string} options.container - Container selector
 * @param {string} options.sentinel - Sentinel element selector
 * @param {Function} options.loadMore - Function to load more items
 * @param {number} options.threshold - Pixels before sentinel to trigger load
 */
export function initInfiniteScroll(options) {
    const {
        container,
        sentinel,
        loadMore,
        threshold = 200
    } = options;
    
    const containerEl = document.querySelector(container);
    const sentinelEl = document.querySelector(sentinel);
    
    if (!containerEl || !sentinelEl) return;
    
    let loading = false;
    let hasMore = true;
    
    const observer = new IntersectionObserver(async (entries) => {
        const entry = entries[0];
        
        if (entry.isIntersecting && !loading && hasMore) {
            loading = true;
            sentinelEl.classList.add('loading');
            
            try {
                const result = await loadMore();
                hasMore = result.hasMore;
                
                if (!hasMore) {
                    sentinelEl.textContent = 'No hay más elementos';
                    observer.disconnect();
                }
            } catch (err) {
                console.error('Failed to load more:', err);
            } finally {
                loading = false;
                sentinelEl.classList.remove('loading');
            }
        }
    }, {
        root: null,
        rootMargin: `${threshold}px`,
        threshold: 0
    });
    
    observer.observe(sentinelEl);
    
    // Return cleanup function
    return () => observer.disconnect();
}

// Usage
// initInfiniteScroll({
//     container: '#patient-list',
//     sentinel: '#load-more-sentinel',
//     loadMore: async () => {
//         const data = await fetchPatients({ page: currentPage++ });
//         renderPatients(data.patients);
//         return { hasMore: currentPage < data.pages };
//     }
// });
```

### Load on Expand/Reveal

```javascript
// static/js/modules/components/patientCard.js

/**
 * Patient card with lazy-loaded details.
 * @module components/patientCard
 */

import { fetchPatientSessions } from '../api/patients.js';

/**
 * Initialize expandable patient cards
 */
export function initPatientCards() {
    document.addEventListener('click', async (e) => {
        const expandBtn = e.target.closest('[data-expand-patient]');
        if (!expandBtn) return;
        
        const card = expandBtn.closest('.patient-card');
        const detailsSection = card.querySelector('.patient-details');
        const patientId = card.dataset.patientId;
        
        // Toggle expansion
        if (card.classList.contains('expanded')) {
            card.classList.remove('expanded');
            return;
        }
        
        // Load data if not already loaded
        if (!detailsSection.dataset.loaded) {
            expandBtn.classList.add('loading');
            
            try {
                const sessions = await fetchPatientSessions(patientId);
                renderSessionsList(detailsSection, sessions);
                detailsSection.dataset.loaded = 'true';
            } catch (err) {
                detailsSection.innerHTML = `
                    <p class="text-danger">Error al cargar sesiones</p>
                `;
            } finally {
                expandBtn.classList.remove('loading');
            }
        }
        
        card.classList.add('expanded');
    });
}

/**
 * Render sessions list in detail section
 * @param {HTMLElement} container - Container element
 * @param {Array} sessions - Session data
 */
function renderSessionsList(container, sessions) {
    if (!sessions.length) {
        container.innerHTML = '<p class="text-muted">Sin sesiones registradas</p>';
        return;
    }
    
    container.innerHTML = `
        <ul class="session-list">
            ${sessions.map(s => `
                <li class="session-item">
                    <span class="session-date">${s.date}</span>
                    <span class="session-status badge badge--${s.paid ? 'success' : 'warning'}">
                        ${s.paid ? 'Pagada' : 'Pendiente'}
                    </span>
                </li>
            `).join('')}
        </ul>
    `;
}
```

---

## 5. Lazy Loading Patterns

### Skeleton Loading States

```html
<!-- templates/macros/_skeletons.html -->

{% macro patient_card_skeleton() %}
<div class="patient-card patient-card--skeleton" aria-hidden="true">
    <div class="patient-card__header">
        <div class="skeleton skeleton--circle" style="width: 48px; height: 48px;"></div>
        <div class="skeleton skeleton--text" style="width: 60%;"></div>
    </div>
    <div class="patient-card__body">
        <div class="skeleton skeleton--text" style="width: 80%;"></div>
        <div class="skeleton skeleton--text" style="width: 40%;"></div>
    </div>
    <div class="patient-card__footer">
        <div class="skeleton skeleton--button"></div>
        <div class="skeleton skeleton--button"></div>
    </div>
</div>
{% endmacro %}

{% macro session_row_skeleton() %}
<tr class="skeleton-row" aria-hidden="true">
    <td><div class="skeleton skeleton--text" style="width: 100px;"></div></td>
    <td><div class="skeleton skeleton--text" style="width: 150px;"></div></td>
    <td><div class="skeleton skeleton--badge"></div></td>
    <td><div class="skeleton skeleton--text" style="width: 80px;"></div></td>
</tr>
{% endmacro %}
```

```css
/* static/css/components/_skeletons.css */

.skeleton {
    background: linear-gradient(
        90deg,
        var(--skeleton-base) 25%,
        var(--skeleton-highlight) 50%,
        var(--skeleton-base) 75%
    );
    background-size: 200% 100%;
    animation: skeleton-pulse 1.5s ease-in-out infinite;
    border-radius: var(--radius-sm);
}

.skeleton--text {
    height: 1em;
    margin: 0.25em 0;
}

.skeleton--circle {
    border-radius: 50%;
}

.skeleton--button {
    width: 80px;
    height: 36px;
    border-radius: var(--radius-md);
}

.skeleton--badge {
    width: 60px;
    height: 24px;
    border-radius: var(--radius-full);
}

@keyframes skeleton-pulse {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* Theme variables */
:root {
    --skeleton-base: #e0e0e0;
    --skeleton-highlight: #f5f5f5;
}

[data-bs-theme="dark"] {
    --skeleton-base: #2d3235;
    --skeleton-highlight: #3d4245;
}
```

### Progressive Loading

```javascript
// static/js/modules/ui/progressiveLoader.js

/**
 * Progressive loading - load content in priority order.
 * @module ui/progressiveLoader
 */

/**
 * Load content progressively based on priority
 * @param {Array} tasks - Array of loading tasks
 */
export async function loadProgressively(tasks) {
    // Group by priority
    const priorityGroups = {};
    
    tasks.forEach(task => {
        const priority = task.priority || 'low';
        if (!priorityGroups[priority]) {
            priorityGroups[priority] = [];
        }
        priorityGroups[priority].push(task);
    });
    
    // Load in priority order
    const priorities = ['critical', 'high', 'medium', 'low'];
    
    for (const priority of priorities) {
        const group = priorityGroups[priority];
        if (!group) continue;
        
        if (priority === 'critical') {
            // Load critical items sequentially
            for (const task of group) {
                await executeTask(task);
            }
        } else {
            // Load non-critical items in parallel
            await Promise.all(group.map(executeTask));
        }
        
        // Yield to main thread between priority groups
        await new Promise(r => setTimeout(r, 0));
    }
}

async function executeTask(task) {
    try {
        const module = await task.loader();
        if (task.init) {
            task.init(module);
        }
    } catch (err) {
        console.error(`Failed to load: ${task.name}`, err);
    }
}

// Usage
loadProgressively([
    {
        name: 'theme',
        priority: 'critical',
        loader: () => import('./modules/ui/theme.js'),
        init: (mod) => mod.initTheme()
    },
    {
        name: 'navigation',
        priority: 'critical',
        loader: () => import('./modules/ui/navigation.js'),
        init: (mod) => mod.initNav()
    },
    {
        name: 'forms',
        priority: 'high',
        loader: () => import('./modules/utils/validators.js'),
        init: (mod) => mod.initForms()
    },
    {
        name: 'charts',
        priority: 'low',
        loader: () => import('./modules/components/charts.js'),
        init: (mod) => mod.initCharts()
    }
]);
```

---

## 6. Lazy Loading Best Practices

### Do's and Don'ts

| ✅ Do | ❌ Don't |
|-------|---------|
| Lazy load below-fold images | Lazy load hero/above-fold images |
| Use native `loading="lazy"` | Over-complicate with JS when native works |
| Show skeleton/placeholder | Show empty space or spinner only |
| Preload on hover for interactions | Wait until click to start loading |
| Cache loaded data | Re-fetch on every interaction |
| Set explicit dimensions | Cause layout shift during load |
| Lazy load heavy libraries | Lazy load tiny utilities |

### Loading Priority Guide

| Priority | Load When | Examples |
|----------|-----------|----------|
| **Critical** | Immediately | Theme, navigation, core layout |
| **High** | DOM ready | Form validation, primary content |
| **Medium** | User interaction likely | Modals, dropdowns, tooltips |
| **Low** | User scrolls/expands | Charts, analytics, below-fold content |
| **Deferred** | Explicit action | PDF export, heavy reports |

### Performance Tips

```javascript
// 1. Preload likely-needed resources
const preloadLink = document.createElement('link');
preloadLink.rel = 'modulepreload';
preloadLink.href = '/static/js/modules/ui/modal.js';
document.head.appendChild(preloadLink);

// 2. Use Intersection Observer for efficient detection
// Instead of scroll event listeners

// 3. Batch DOM updates
const fragment = document.createDocumentFragment();
items.forEach(item => fragment.appendChild(createItemElement(item)));
container.appendChild(fragment);

// 4. Cancel unnecessary loads
const controller = new AbortController();
fetch(url, { signal: controller.signal });
// Later: controller.abort();

// 5. Implement request deduplication
const pending = new Map();

async function dedupedFetch(url) {
    if (pending.has(url)) {
        return pending.get(url);
    }
    
    const promise = fetch(url).then(r => r.json());
    pending.set(url, promise);
    
    try {
        return await promise;
    } finally {
        pending.delete(url);
    }
}
```

---

## 7. Lazy Loading Checklist

### Images
- [ ] Use `loading="lazy"` on below-fold images
- [ ] Set `width` and `height` attributes
- [ ] Use `decoding="async"`
- [ ] Implement blur-up or skeleton placeholders
- [ ] Lazy load background images with Intersection Observer

### Components
- [ ] Dynamic import heavy components
- [ ] Load on interaction for modals/dialogs
- [ ] Preload on hover for better UX
- [ ] Show loading states during load

### Data
- [ ] Paginate large lists
- [ ] Implement infinite scroll where appropriate
- [ ] Load details on expand/reveal
- [ ] Cache fetched data

### Routes
- [ ] Minimal data for initial render
- [ ] API endpoints for additional data
- [ ] Code split by route

---

## Related Skills

- [Web Performance](skill-web-performance.md)
- [Asset Optimization](skill-asset-optimization.md)
- [JavaScript Modules](skill-javascript-modules.md)
- [Component Design](skill-component-design.md)
