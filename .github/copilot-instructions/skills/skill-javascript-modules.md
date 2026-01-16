# Skill: JavaScript Modules

## Overview

This skill covers ES6 module patterns, import/export syntax, and strategies for modularizing JavaScript in the Therapy Session Management Application. The goal is to transform a monolithic 1000+ line file into maintainable, testable modules.

---

## Current State Analysis

### Current Structure
```
static/js/
├── api.js              # Monolithic file (1044 lines)
└── bootstrap.bundle.min.js  # Vendor library
```

### Issues with Monolithic JavaScript
- **Hard to maintain**: All functions in global scope
- **No encapsulation**: Any function can access/modify anything
- **Difficult testing**: Can't test modules in isolation
- **Name collisions**: Risk of overwriting global variables
- **Poor code organization**: Mixed concerns (API, UI, utilities)

---

## ES6 Module Syntax

### Named Exports

```javascript
// utils.js - Multiple named exports
export function formatDate(date) {
    // ...
}

export function formatPrice(price) {
    // ...
}

export const SPANISH_DAYS = ['Domingo', 'Lunes', 'Martes', ...];

// Import named exports
import { formatDate, formatPrice } from './utils.js';
import { formatDate, SPANISH_DAYS } from './utils.js';
```

### Default Exports

```javascript
// api-client.js - Single default export
class ApiClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    async get(endpoint) { /* ... */ }
    async post(endpoint, data) { /* ... */ }
}

export default ApiClient;

// Import default export
import ApiClient from './api-client.js';
```

### Mixed Exports

```javascript
// session-api.js
export async function getSession(id) { /* ... */ }
export async function updateSession(id, data) { /* ... */ }
export async function deleteSession(id) { /* ... */ }

// Default export for common use case
export default {
    get: getSession,
    update: updateSession,
    delete: deleteSession,
};

// Import options
import SessionApi from './session-api.js';           // Default
import { getSession } from './session-api.js';       // Named
import SessionApi, { getSession } from './session-api.js'; // Both
```

### Re-exports

```javascript
// index.js - Barrel file for cleaner imports
export { formatDate, formatPrice } from './utils.js';
export { showToast, hideToast } from './toast.js';
export { default as ApiClient } from './api-client.js';

// Consumer imports from single entry point
import { formatDate, showToast, ApiClient } from './modules/index.js';
```

---

## Proposed Module Structure

### File Organization

```
static/js/
├── main.js                 # Entry point, initializes app
├── bootstrap.bundle.min.js # Vendor (unchanged)
│
├── api/
│   ├── index.js           # Re-exports all API modules
│   ├── client.js          # Base API client (fetch wrapper)
│   ├── patients.js        # Patient CRUD operations
│   ├── sessions.js        # Session CRUD operations
│   └── dashboard.js       # Dashboard data fetching
│
├── ui/
│   ├── index.js           # Re-exports all UI modules
│   ├── toast.js           # Toast notifications
│   ├── modal.js           # Modal management
│   ├── carousel.js        # Carousel controls
│   └── forms.js           # Form utilities
│
├── utils/
│   ├── index.js           # Re-exports all utilities
│   ├── formatters.js      # Date, price formatting
│   ├── validators.js      # Input validation
│   └── dom.js             # DOM helper functions
│
└── constants/
    └── index.js           # Application constants
```

### Module Contents

#### api/client.js - Base API Client

```javascript
/**
 * Base API Client
 * @module api/client
 */

const API_BASE = '/api/v1';

/**
 * Get CSRF token from meta tag
 * @returns {string|null}
 */
function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : null;
}

/**
 * Make an API request with error handling
 * @param {string} endpoint - API endpoint (without base URL)
 * @param {RequestInit} options - Fetch options
 * @returns {Promise<any>} - Response data
 * @throws {Error} - If request fails
 */
export async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const csrfToken = getCsrfToken();
    
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...(csrfToken && { 'X-CSRFToken': csrfToken }),
            ...options.headers,
        },
        credentials: 'same-origin',
        ...options,
    };

    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Error en la solicitud');
    }

    return data;
}

/**
 * GET request helper
 * @param {string} endpoint
 * @returns {Promise<any>}
 */
export function get(endpoint) {
    return apiRequest(endpoint, { method: 'GET' });
}

/**
 * POST request helper
 * @param {string} endpoint
 * @param {object} data
 * @returns {Promise<any>}
 */
export function post(endpoint, data) {
    return apiRequest(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

/**
 * PUT request helper
 * @param {string} endpoint
 * @param {object} data
 * @returns {Promise<any>}
 */
export function put(endpoint, data) {
    return apiRequest(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
}

/**
 * DELETE request helper
 * @param {string} endpoint
 * @returns {Promise<any>}
 */
export function del(endpoint) {
    return apiRequest(endpoint, { method: 'DELETE' });
}

export default { apiRequest, get, post, put, del };
```

#### api/patients.js - Patient API Module

```javascript
/**
 * Patient API Module
 * @module api/patients
 */

import { get, put, del } from './client.js';

/**
 * Get a patient by ID
 * @param {number} patientId
 * @returns {Promise<object>}
 */
export async function getPatient(patientId) {
    return get(`/patients/${patientId}`);
}

/**
 * Update a patient
 * @param {number} patientId
 * @param {object} data - { name, notes }
 * @returns {Promise<object>}
 */
export async function updatePatient(patientId, data) {
    return put(`/patients/${patientId}`, data);
}

/**
 * Delete a patient (soft delete)
 * @param {number} patientId
 * @returns {Promise<object>}
 */
export async function deletePatient(patientId) {
    return del(`/patients/${patientId}`);
}

export default { getPatient, updatePatient, deletePatient };
```

#### api/sessions.js - Session API Module

```javascript
/**
 * Session API Module
 * @module api/sessions
 */

import { get, put, del, post } from './client.js';

/**
 * Get a session by ID
 * @param {number} sessionId
 * @returns {Promise<object>}
 */
export async function getSession(sessionId) {
    return get(`/sessions/${sessionId}`);
}

/**
 * Update a session
 * @param {number} sessionId
 * @param {object} data - { session_date, session_price, pending, notes }
 * @returns {Promise<object>}
 */
export async function updateSession(sessionId, data) {
    return put(`/sessions/${sessionId}`, data);
}

/**
 * Delete a session (soft delete)
 * @param {number} sessionId
 * @returns {Promise<object>}
 */
export async function deleteSession(sessionId) {
    return del(`/sessions/${sessionId}`);
}

/**
 * Toggle session payment status
 * @param {number} sessionId
 * @returns {Promise<object>}
 */
export async function togglePayment(sessionId) {
    return post(`/sessions/${sessionId}/toggle-payment`, {});
}

export default { getSession, updateSession, deleteSession, togglePayment };
```

#### api/index.js - API Barrel File

```javascript
/**
 * API Module Exports
 * @module api
 */

// Re-export all API functions
export * from './client.js';
export * from './patients.js';
export * from './sessions.js';
export * from './dashboard.js';

// Named module exports for namespaced usage
export { default as PatientApi } from './patients.js';
export { default as SessionApi } from './sessions.js';
export { default as DashboardApi } from './dashboard.js';
```

#### ui/toast.js - Toast Notifications

```javascript
/**
 * Toast Notification Module
 * @module ui/toast
 */

import { TOAST_DURATION } from '../constants/index.js';

/**
 * Show a toast notification
 * @param {string} message - Message to display
 * @param {'success'|'error'|'warning'|'info'} type - Toast type
 * @param {number} duration - Duration in ms (default: 3000)
 */
export function showToast(message, type = 'info', duration = TOAST_DURATION) {
    const container = getToastContainer();
    const toast = createToastElement(message, type);
    
    container.appendChild(toast);
    
    // Trigger animation
    requestAnimationFrame(() => {
        toast.classList.add('toast--visible');
    });
    
    // Auto-dismiss
    setTimeout(() => hideToast(toast), duration);
    
    return toast;
}

/**
 * Hide a toast notification
 * @param {HTMLElement} toast - Toast element to hide
 */
export function hideToast(toast) {
    toast.classList.remove('toast--visible');
    toast.addEventListener('transitionend', () => toast.remove(), { once: true });
}

/**
 * Get or create toast container
 * @returns {HTMLElement}
 */
function getToastContainer() {
    let container = document.getElementById('toast-container');
    
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        container.setAttribute('aria-live', 'polite');
        container.setAttribute('aria-atomic', 'true');
        document.body.appendChild(container);
    }
    
    return container;
}

/**
 * Create a toast element
 * @param {string} message
 * @param {string} type
 * @returns {HTMLElement}
 */
function createToastElement(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast toast--${type}`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <span class="toast__message">${message}</span>
        <button class="toast__close" aria-label="Cerrar">×</button>
    `;
    
    toast.querySelector('.toast__close').addEventListener('click', () => hideToast(toast));
    
    return toast;
}

export default { showToast, hideToast };
```

#### utils/formatters.js - Formatting Utilities

```javascript
/**
 * Formatting Utilities
 * @module utils/formatters
 */

import { SPANISH_DAYS } from '../constants/index.js';

/**
 * Format a date for display in Spanish
 * @param {string} dateString - ISO date string (YYYY-MM-DD)
 * @returns {string} - Formatted date (e.g., "Lunes 15/01/2026")
 */
export function formatDisplayDate(dateString) {
    const [year, month, day] = dateString.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    const dayOfWeek = SPANISH_DAYS[date.getDay()];
    
    const formattedDay = String(day).padStart(2, '0');
    const formattedMonth = String(month).padStart(2, '0');
    
    return `${dayOfWeek} ${formattedDay}/${formattedMonth}/${year}`;
}

/**
 * Format a price for display
 * @param {number} price - Price value
 * @returns {string} - Formatted price (e.g., "$150.00")
 */
export function formatPrice(price) {
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 2,
    }).format(price);
}

/**
 * Format a date for input fields
 * @param {Date|string} date
 * @returns {string} - ISO format (YYYY-MM-DD)
 */
export function formatDateForInput(date) {
    if (typeof date === 'string') {
        return date.split('T')[0];
    }
    return date.toISOString().split('T')[0];
}

export default { formatDisplayDate, formatPrice, formatDateForInput };
```

#### constants/index.js - Application Constants

```javascript
/**
 * Application Constants
 * @module constants
 */

// Spanish day names (Sunday = 0)
export const SPANISH_DAYS = [
    'Domingo', 'Lunes', 'Martes', 'Miércoles',
    'Jueves', 'Viernes', 'Sábado'
];

// Spanish month names
export const SPANISH_MONTHS = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];

// Toast notification duration (ms)
export const TOAST_DURATION = 3000;

// Payment status
export const PAYMENT_STATUS = {
    PENDING: true,
    PAID: false,
};

// Filter options
export const FILTER_OPTIONS = {
    ALL: 'all',
    PENDING: 'pending',
    PAID: 'paid',
};

// API endpoints
export const ENDPOINTS = {
    PATIENTS: '/patients',
    SESSIONS: '/sessions',
    DASHBOARD: '/dashboard',
};

export default {
    SPANISH_DAYS,
    SPANISH_MONTHS,
    TOAST_DURATION,
    PAYMENT_STATUS,
    FILTER_OPTIONS,
    ENDPOINTS,
};
```

---

## Entry Point Pattern

### main.js - Application Entry Point

```javascript
/**
 * Main Application Entry Point
 * @module main
 */

// Import modules
import { showToast } from './ui/toast.js';
import { formatDisplayDate, formatPrice } from './utils/formatters.js';
import { PatientApi, SessionApi, DashboardApi } from './api/index.js';
import { initializeModals } from './ui/modal.js';
import { initializeCarousels } from './ui/carousel.js';

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);

/**
 * Initialize the application
 */
function initApp() {
    console.log('App initialized');
    
    // Initialize UI components
    initializeModals();
    initializeCarousels();
    
    // Set up global event listeners
    setupEventListeners();
    
    // Expose necessary functions to global scope (for inline handlers)
    exposeGlobalFunctions();
}

/**
 * Set up event listeners using event delegation
 */
function setupEventListeners() {
    // Delegate all click events
    document.addEventListener('click', handleClick);
    
    // Delegate form submissions
    document.addEventListener('submit', handleSubmit);
}

/**
 * Handle delegated click events
 * @param {Event} event
 */
function handleClick(event) {
    const target = event.target.closest('[data-action]');
    if (!target) return;
    
    const action = target.dataset.action;
    const handlers = {
        'toggle-payment': () => handleTogglePayment(target),
        'edit-patient': () => handleEditPatient(target),
        'delete-patient': () => handleDeletePatient(target),
        'edit-session': () => handleEditSession(target),
        'delete-session': () => handleDeleteSession(target),
    };
    
    if (handlers[action]) {
        event.preventDefault();
        handlers[action]();
    }
}

/**
 * Expose functions to global scope for inline onclick handlers
 * (Temporary during migration, will be removed after full refactor)
 */
function exposeGlobalFunctions() {
    window.showToast = showToast;
    window.formatDisplayDate = formatDisplayDate;
    window.formatPrice = formatPrice;
    window.togglePayment = handleTogglePayment;
    // ... other functions needed by inline handlers
}
```

---

## HTML Script Loading

### Using type="module"

```html
<!-- In base.html -->
<head>
    <!-- ... -->
</head>
<body>
    <!-- Content -->
    
    <!-- Vendor scripts (non-module) -->
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    
    <!-- Application modules -->
    <script type="module" src="{{ url_for('static', filename='js/main.js') }}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
```

### Module Script Behavior

| Feature | Regular Script | Module Script |
|---------|----------------|---------------|
| Scope | Global | Module (private) |
| Strict mode | Optional | Always on |
| Top-level `this` | `window` | `undefined` |
| Loading | Synchronous | Deferred by default |
| Same file twice | Executes twice | Executes once |
| CORS | Not required | Required for cross-origin |

---

## Migration Strategy

### Phase 1: Create Module Structure
1. Create folder structure (`api/`, `ui/`, `utils/`, `constants/`)
2. Create empty module files with JSDoc headers
3. Don't modify `api.js` yet

### Phase 2: Extract Utilities
1. Move `formatDisplayDate`, `formatPrice` to `utils/formatters.js`
2. Move constants to `constants/index.js`
3. Test utilities in isolation

### Phase 3: Extract API Client
1. Move `apiRequest` and CRUD functions to `api/client.js`
2. Create `api/patients.js` and `api/sessions.js`
3. Update imports

### Phase 4: Extract UI Components
1. Move `showToast` to `ui/toast.js`
2. Move modal functions to `ui/modal.js`
3. Move carousel functions to `ui/carousel.js`

### Phase 5: Create Entry Point
1. Create `main.js` with initialization
2. Set up event delegation
3. Expose necessary globals temporarily

### Phase 6: Update Templates
1. Change script tags to use `type="module"`
2. Update inline handlers to use data attributes
3. Remove global function calls gradually

### Phase 7: Cleanup
1. Remove deprecated `api.js`
2. Remove global function exposures
3. Final testing

---

## Import/Export Patterns

### Pattern: Namespace Import

```javascript
// Import all as namespace
import * as PatientApi from './api/patients.js';

// Usage
PatientApi.getPatient(123);
PatientApi.updatePatient(123, data);
```

### Pattern: Selective Import

```javascript
// Import only what you need
import { getPatient, updatePatient } from './api/patients.js';

// Usage
getPatient(123);
updatePatient(123, data);
```

### Pattern: Default + Named

```javascript
// Module exports both
export function getPatient(id) { /* ... */ }
export function updatePatient(id, data) { /* ... */ }
export default { getPatient, updatePatient };

// Consumer can choose style
import PatientApi from './api/patients.js';  // Object
import { getPatient } from './api/patients.js';  // Function
```

---

## Circular Dependency Prevention

### Problem

```javascript
// a.js
import { bFunction } from './b.js';
export function aFunction() { /* uses bFunction */ }

// b.js
import { aFunction } from './a.js';  // Circular!
export function bFunction() { /* uses aFunction */ }
```

### Solutions

```javascript
// Solution 1: Extract shared code to third module
// shared.js
export function sharedFunction() { /* ... */ }

// a.js
import { sharedFunction } from './shared.js';

// b.js
import { sharedFunction } from './shared.js';
```

```javascript
// Solution 2: Dependency injection
// b.js
export function bFunction(aFunction) {
    return function() {
        // Uses injected aFunction
    };
}

// main.js
import { aFunction } from './a.js';
import { bFunction } from './b.js';
const b = bFunction(aFunction);
```

---

## Testing Modules

### Test File Structure

```javascript
// tests/utils/formatters.test.js
import { formatDisplayDate, formatPrice } from '../../static/js/utils/formatters.js';

describe('formatDisplayDate', () => {
    test('formats date with Spanish day name', () => {
        expect(formatDisplayDate('2026-01-15')).toBe('Miércoles 15/01/2026');
    });
    
    test('handles edge cases', () => {
        expect(formatDisplayDate('2026-01-01')).toBe('Jueves 01/01/2026');
    });
});

describe('formatPrice', () => {
    test('formats price with currency symbol', () => {
        expect(formatPrice(150)).toContain('150');
    });
});
```

### Mocking Modules

```javascript
// Mock the API client
jest.mock('../../static/js/api/client.js', () => ({
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    del: jest.fn(),
}));

import { getPatient } from '../../static/js/api/patients.js';
import { get } from '../../static/js/api/client.js';

test('getPatient calls correct endpoint', async () => {
    get.mockResolvedValue({ id: 1, name: 'Test' });
    
    const result = await getPatient(1);
    
    expect(get).toHaveBeenCalledWith('/patients/1');
    expect(result.name).toBe('Test');
});
```

---

## Browser Compatibility

### Native ES Modules Support

| Browser | Version | Year |
|---------|---------|------|
| Chrome | 61+ | 2017 |
| Firefox | 60+ | 2018 |
| Safari | 11+ | 2017 |
| Edge | 16+ | 2017 |

### Fallback for Older Browsers

```html
<!-- Modern browsers use module -->
<script type="module" src="main.js"></script>

<!-- Fallback for older browsers -->
<script nomodule src="main-legacy.js"></script>
```

---

## Checklist for JavaScript Modules

### Structure
- [ ] Logical folder organization (api/, ui/, utils/)
- [ ] Each module has single responsibility
- [ ] Barrel files (index.js) for clean imports
- [ ] No circular dependencies

### Exports
- [ ] Consistent export style (named vs default)
- [ ] JSDoc on all exported functions
- [ ] Constants in dedicated module

### Imports
- [ ] Explicit imports (not `import *` unless needed)
- [ ] Relative paths for local modules
- [ ] No unused imports

### Migration
- [ ] Global exposure limited to transition period
- [ ] Event delegation over inline handlers
- [ ] Tests for each module

---

## Related Skills

- [skill-jsdoc-documentation.md](./skill-jsdoc-documentation.md) - Documenting modules
- [skill-event-delegation.md](./skill-event-delegation.md) - Event handling patterns
- [skill-error-handling.md](./skill-error-handling.md) - Error handling in modules

---

*Last Updated: January 15, 2026*
