# JavaScript Module Documentation

This document describes the JavaScript module architecture and API for the Therapy Session Management Application.

## Architecture Overview

The JavaScript is organized as ES6 modules with `main.js` as the entry point:

```
static/js/
├── main.js                 # Entry point (ES6 module)
└── modules/
    ├── api/                # API communication
    │   ├── client.js       # Base HTTP client
    │   ├── patients.js     # Patient API endpoints
    │   ├── sessions.js     # Session API endpoints
    │   └── dashboard.js    # Dashboard data loading
    ├── ui/                 # UI utilities
    │   ├── toast.js        # Toast notifications
    │   ├── modal.js        # Modal management
    │   ├── carousel.js     # Carousel controls
    │   └── accessibility.js # A11y utilities
    ├── components/         # Page components
    │   ├── patientCard.js  # Patient card logic
    │   ├── sessionCard.js  # Session card logic
    │   ├── filterButtons.js # Filter button handling
    │   └── dashboardRenderer.js # Dashboard rendering
    └── utils/              # Utilities
        ├── formatters.js   # Date/price formatting
        ├── validators.js   # Input validation
        └── helpers.js      # General helpers
```

---

## API Module (`modules/api/`)

### client.js

Base HTTP client for all API requests.

#### `ApiError`

Custom error class for API failures.

```javascript
class ApiError extends Error {
    constructor(message, status, data = null)
}
```

**Properties:**
- `message` (string): Error message
- `status` (number): HTTP status code
- `data` (Object|null): Response data

#### `getCsrfToken()`

Get CSRF token from meta tag.

```javascript
const token = getCsrfToken();
// Returns: string | null
```

#### `apiRequest(endpoint, options)`

Make an API request with error handling.

```javascript
// GET request
const data = await apiRequest('/patients/1');

// POST request
const result = await apiRequest('/patients', {
    method: 'POST',
    body: JSON.stringify({ name: 'John' })
});
```

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `endpoint` | string | - | API endpoint (relative to /api/v1/) |
| `options` | Object | `{}` | Fetch options |
| `options.method` | string | `'GET'` | HTTP method |
| `options.body` | Object | - | Request body (will be JSON stringified) |
| `options.headers` | Object | - | Additional headers |

**Returns:** `Promise<Object>` - Response data

**Throws:** `ApiError` if request fails

#### Helper Functions

```javascript
// GET request
const data = await get('/patients/1');

// POST request
const result = await post('/patients', { name: 'John' });

// PUT request
await put('/patients/1', { name: 'Updated' });

// DELETE request
await del('/patients/1');
```

---

### patients.js

Patient-specific API endpoints.

#### `getPatient(patientId)`

Fetch a patient by ID.

```javascript
const patient = await getPatient(1);
```

#### `updatePatient(patientId, data)`

Update patient information.

```javascript
await updatePatient(1, { name: 'New Name', notes: 'Updated notes' });
```

#### `deletePatient(patientId)`

Soft delete a patient.

```javascript
await deletePatient(1);
```

---

### sessions.js

Session-specific API endpoints.

#### `getSession(sessionId)`

Fetch a session by ID.

```javascript
const session = await getSession(1);
```

#### `togglePaymentStatus(sessionId)`

Toggle session payment status.

```javascript
const result = await togglePaymentStatus(1);
// Returns: { pending: false, message: 'Sesión marcada como pagada' }
```

#### `deleteSession(sessionId)`

Delete a session.

```javascript
await deleteSession(1);
```

---

## UI Module (`modules/ui/`)

### toast.js

Toast notification system with accessibility support.

#### `showToast(message, type, duration)`

Display a toast notification.

```javascript
import { showToast } from './modules/ui/toast.js';

showToast('Paciente guardado', 'success');
showToast('Error al guardar', 'error');
showToast('Atención requerida', 'warning', 6000);
```

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `message` | string | - | Message to display |
| `type` | string | `'info'` | `'success'`, `'error'`, `'warning'`, `'info'` |
| `duration` | number | `4000` | Duration in milliseconds |

**Accessibility:** Uses ARIA live regions. Errors use `role="alert"` (assertive), others use `role="status"` (polite).

#### `clearAllToasts()`

Clear all visible toasts.

```javascript
clearAllToasts();
```

---

### modal.js

Bootstrap modal management utilities.

#### `openModal(modalId)`

Open a modal by ID.

```javascript
openModal('editPatientModal');
```

#### `closeModal(modalId)`

Close a modal by ID.

```javascript
closeModal('editPatientModal');
```

#### `getModalInstance(modalId)`

Get Bootstrap modal instance.

```javascript
const modal = getModalInstance('editPatientModal');
modal.hide();
```

---

### carousel.js

Carousel control utilities.

#### `goToSlide(carouselId, index)`

Navigate carousel to specific slide.

```javascript
goToSlide('carousel-1', 0); // Go to first slide
```

#### `getCurrentSlide(carouselId)`

Get current active slide index.

```javascript
const index = getCurrentSlide('carousel-1');
```

---

## Utils Module (`modules/utils/`)

### formatters.js

Date and price formatting utilities for Spanish locale.

#### `formatDisplayDate(dateStr)`

Format a date string for display in Spanish.

```javascript
formatDisplayDate('2024-01-15');
// Returns: "Lunes 15/01/2024"
```

#### `formatDateLong(dateStr)`

Format date with month name.

```javascript
formatDateLong('2024-01-15');
// Returns: "15 de Enero, 2024"
```

#### `formatPrice(amount)`

Format a number as currency.

```javascript
formatPrice(100);
// Returns: "$100.00"
```

---

### validators.js

Input validation utilities.

#### `validateEmail(email)`

Validate email format.

```javascript
validateEmail('test@example.com'); // true
validateEmail('invalid'); // false
```

#### `validateRequired(value)`

Check if value is not empty.

```javascript
validateRequired('hello'); // true
validateRequired(''); // false
```

#### `validatePrice(price)`

Validate price is a positive number.

```javascript
validatePrice(100); // true
validatePrice(-50); // false
```

---

### helpers.js

General helper functions.

#### `escapeHtml(text)`

Escape HTML special characters.

```javascript
escapeHtml('<script>alert("xss")</script>');
// Returns: "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;"
```

#### `debounce(func, wait)`

Create a debounced function.

```javascript
const debouncedSearch = debounce(searchPatients, 300);
input.addEventListener('input', debouncedSearch);
```

---

## Global Exports

For backward compatibility with `onclick` handlers in templates, some functions are exposed globally:

```javascript
// Available on window object
window.showToast
window.togglePayment
window.openEditSessionModal
window.openDeleteSessionModal
window.openEditPatientModal
window.openDeletePatientModal
```

---

## Error Handling

All API calls should be wrapped in try-catch:

```javascript
import { showToast } from './modules/ui/toast.js';
import { updatePatient } from './modules/api/patients.js';

async function handleUpdate(patientId, data) {
    try {
        await updatePatient(patientId, data);
        showToast('Paciente actualizado', 'success');
    } catch (error) {
        console.error('Update failed:', error);
        showToast(error.message || 'Error al actualizar', 'error');
    }
}
```

---

## Adding New Modules

1. Create file in appropriate directory
2. Use ES6 module syntax (`export`/`import`)
3. Add JSDoc documentation for all functions
4. Export from the module's index if needed
5. Update this documentation

---

*Last Updated: January 15, 2026*
