# Skill: JSDoc Documentation

## Overview

JSDoc is a documentation standard for JavaScript that enables type checking, IDE autocompletion, and generates API documentation. This skill covers JSDoc syntax, type annotations, and best practices for the Therapy Session Management Application.

---

## Basic Syntax

### Comment Structure

```javascript
/**
 * Single-line description.
 */

/**
 * Multi-line description that explains
 * what this function or class does in detail.
 */

/**
 * Description with tags.
 * @param {string} name - The name parameter
 * @returns {boolean} - Whether operation succeeded
 */
```

### Placement

```javascript
/**
 * Documentation goes BEFORE the element it describes.
 */
function myFunction() { }

/**
 * Class documentation.
 */
class MyClass {
    /**
     * Property documentation.
     * @type {string}
     */
    myProperty;
    
    /**
     * Method documentation.
     */
    myMethod() { }
}
```

---

## Type Annotations

### Primitive Types

```javascript
/**
 * @param {string} name - Text value
 * @param {number} age - Numeric value
 * @param {boolean} active - True/false value
 * @param {null} empty - Null value
 * @param {undefined} missing - Undefined value
 * @param {symbol} id - Symbol value
 * @param {bigint} largeNum - BigInt value
 */
```

### Complex Types

```javascript
/**
 * @param {object} config - Generic object
 * @param {Object} data - Same as object
 * @param {Array} items - Generic array
 * @param {Function} callback - Any function
 * @param {Date} timestamp - Date object
 * @param {RegExp} pattern - Regular expression
 * @param {Error} err - Error object
 * @param {Promise} result - Promise object
 */
```

### Typed Arrays

```javascript
/**
 * @param {string[]} names - Array of strings
 * @param {number[]} scores - Array of numbers
 * @param {Array<string>} tags - Alternative syntax
 * @param {Array<number|string>} mixed - Mixed array
 */
```

### Union Types

```javascript
/**
 * @param {string|number} id - String or number
 * @param {string|null} name - String or null
 * @param {boolean|undefined} flag - Boolean or undefined
 */
```

### Nullable Types

```javascript
/**
 * @param {?string} name - String or null
 * @param {!string} required - Never null (non-nullable)
 */
```

### Optional Parameters

```javascript
/**
 * @param {string} name - Required parameter
 * @param {number} [age] - Optional parameter
 * @param {string} [city='Unknown'] - Optional with default
 */
function createUser(name, age, city = 'Unknown') { }
```

---

## Object Types

### Inline Object Type

```javascript
/**
 * @param {{name: string, age: number}} user - User object
 * @param {{id: number, title: string, done?: boolean}} task - Task with optional done
 */
```

### Named Object Type with @typedef

```javascript
/**
 * Patient data object
 * @typedef {Object} Patient
 * @property {number} id - Unique identifier
 * @property {string} name - Patient name
 * @property {string} [notes] - Optional notes
 * @property {boolean} deleted - Soft delete flag
 * @property {Date} createdAt - Creation timestamp
 */

/**
 * Get patient by ID
 * @param {number} id - Patient ID
 * @returns {Promise<Patient>} - Patient data
 */
async function getPatient(id) { }
```

### Nested Object Types

```javascript
/**
 * Session with patient info
 * @typedef {Object} SessionWithPatient
 * @property {number} id - Session ID
 * @property {string} session_date - Date string (YYYY-MM-DD)
 * @property {number} session_price - Price amount
 * @property {boolean} pending - Payment pending status
 * @property {Patient} patient - Associated patient
 */
```

---

## Function Types

### Function Parameters

```javascript
/**
 * @param {function} callback - Generic callback
 * @param {function(string): void} logger - Function taking string, returning nothing
 * @param {function(number, number): number} calculator - Two numbers in, one out
 * @param {(error: Error|null, result?: any) => void} nodeCallback - Node-style callback
 */
```

### @callback for Reusable Function Types

```javascript
/**
 * API response handler callback
 * @callback ApiCallback
 * @param {Error|null} error - Error if failed
 * @param {Object} [data] - Response data if successful
 * @returns {void}
 */

/**
 * Fetch data with callback
 * @param {string} url - API URL
 * @param {ApiCallback} callback - Response handler
 */
function fetchData(url, callback) { }
```

---

## Common JSDoc Tags

### Function Documentation

```javascript
/**
 * Short description of what the function does.
 * 
 * Longer description with more details about behavior,
 * edge cases, or usage examples.
 * 
 * @param {string} name - Description of name parameter
 * @param {number} [age=0] - Optional age with default
 * @returns {Object} Description of return value
 * @throws {Error} When name is empty
 * @example
 * // Basic usage
 * const user = createUser('John', 25);
 * 
 * @example
 * // Without age
 * const user = createUser('Jane');
 * 
 * @see {@link updateUser} for updating users
 * @since 1.0.0
 * @deprecated Use createUserV2 instead
 */
function createUser(name, age = 0) {
    if (!name) throw new Error('Name required');
    return { name, age };
}
```

### Async Functions

```javascript
/**
 * Fetch patient data from API
 * @async
 * @param {number} patientId - Patient ID
 * @returns {Promise<Patient>} Patient data
 * @throws {Error} If patient not found (404)
 */
async function getPatient(patientId) {
    const response = await fetch(`/api/v1/patients/${patientId}`);
    if (!response.ok) throw new Error('Patient not found');
    return response.json();
}
```

### Class Documentation

```javascript
/**
 * API client for making HTTP requests
 * @class
 * @classdesc Handles all API communication with error handling and CSRF protection.
 * 
 * @example
 * const api = new ApiClient('/api/v1');
 * const patient = await api.get('/patients/1');
 */
class ApiClient {
    /**
     * Create an API client
     * @constructor
     * @param {string} baseUrl - Base URL for all requests
     */
    constructor(baseUrl) {
        /**
         * Base URL for API requests
         * @type {string}
         * @private
         */
        this.baseUrl = baseUrl;
    }
    
    /**
     * Make a GET request
     * @param {string} endpoint - API endpoint
     * @returns {Promise<any>} Response data
     */
    async get(endpoint) { }
}
```

### Module Documentation

```javascript
/**
 * Patient API Module
 * 
 * Provides functions for patient CRUD operations.
 * All functions return promises and handle errors.
 * 
 * @module api/patients
 * @see module:api/client
 * @example
 * import { getPatient, updatePatient } from './api/patients.js';
 * 
 * const patient = await getPatient(123);
 * await updatePatient(123, { name: 'New Name' });
 */
```

---

## Project-Specific Type Definitions

### types.js - Shared Type Definitions

```javascript
/**
 * Shared Type Definitions
 * @module types
 */

// =============================================================================
// API Response Types
// =============================================================================

/**
 * Standard API response wrapper
 * @typedef {Object} ApiResponse
 * @property {boolean} success - Whether request succeeded
 * @property {string} [message] - Success/error message
 * @property {any} [data] - Response payload
 * @property {string} [error] - Error message if failed
 */

/**
 * Paginated response
 * @typedef {Object} PaginatedResponse
 * @property {Array} items - Page items
 * @property {number} page - Current page number
 * @property {number} per_page - Items per page
 * @property {number} total - Total items
 * @property {number} pages - Total pages
 */

// =============================================================================
// Entity Types
// =============================================================================

/**
 * Patient entity
 * @typedef {Object} Patient
 * @property {number} id - Unique identifier
 * @property {string} name - Patient full name
 * @property {string} [notes] - Optional notes
 * @property {boolean} deleted - Soft delete flag
 * @property {string} created_at - ISO timestamp
 * @property {string} updated_at - ISO timestamp
 * @property {number} user_id - Owner user ID
 */

/**
 * Therapy session entity
 * @typedef {Object} Session
 * @property {number} id - Unique identifier
 * @property {string} session_date - Date (YYYY-MM-DD)
 * @property {number} session_price - Price amount
 * @property {boolean} pending - Payment pending status
 * @property {string} [notes] - Optional notes
 * @property {number} person_id - Associated patient ID
 * @property {boolean} deleted - Soft delete flag
 */

/**
 * Session with formatted display data
 * @typedef {Object} SessionDisplay
 * @property {number} id - Session ID
 * @property {string} formatted_date - Formatted date (e.g., "Lunes 15/01/2026")
 * @property {string} formatted_price - Formatted price (e.g., "$150.00")
 * @property {boolean} pending - Payment status
 * @property {string} status_label - "PENDIENTE" or "PAGADO"
 * @property {string} status_class - CSS class for styling
 */

/**
 * User entity
 * @typedef {Object} User
 * @property {number} id - Unique identifier
 * @property {string} email - Email address
 * @property {string} role - User role (admin|therapist|viewer)
 * @property {boolean} active - Account active status
 */

// =============================================================================
// Form Data Types
// =============================================================================

/**
 * Patient form data
 * @typedef {Object} PatientFormData
 * @property {string} name - Patient name (required)
 * @property {string} [notes] - Optional notes
 */

/**
 * Session form data
 * @typedef {Object} SessionFormData
 * @property {string} session_date - Date (YYYY-MM-DD)
 * @property {number} session_price - Price amount
 * @property {boolean} [pending=true] - Payment status
 * @property {string} [notes] - Optional notes
 */

// =============================================================================
// UI Types
// =============================================================================

/**
 * Toast notification options
 * @typedef {Object} ToastOptions
 * @property {'success'|'error'|'warning'|'info'} type - Toast type
 * @property {number} [duration=3000] - Display duration in ms
 * @property {boolean} [dismissible=true] - Can be dismissed
 */

/**
 * Modal configuration
 * @typedef {Object} ModalConfig
 * @property {string} title - Modal title
 * @property {string} content - Modal body content (HTML)
 * @property {string} [size='md'] - Modal size (sm|md|lg|xl)
 * @property {boolean} [closable=true] - Show close button
 * @property {ModalButton[]} [buttons] - Footer buttons
 */

/**
 * Modal button configuration
 * @typedef {Object} ModalButton
 * @property {string} label - Button text
 * @property {string} [className='btn-secondary'] - CSS class
 * @property {function} [onClick] - Click handler
 * @property {boolean} [dismiss=false] - Close modal on click
 */

// =============================================================================
// Event Types
// =============================================================================

/**
 * Custom event detail for patient updates
 * @typedef {Object} PatientUpdateEvent
 * @property {number} patientId - Updated patient ID
 * @property {Patient} patient - Updated patient data
 * @property {'create'|'update'|'delete'} action - Action performed
 */

/**
 * Custom event detail for session updates
 * @typedef {Object} SessionUpdateEvent
 * @property {number} sessionId - Updated session ID
 * @property {Session} session - Updated session data
 * @property {'create'|'update'|'delete'|'toggle-payment'} action - Action performed
 */
```

---

## Documentation Examples

### API Function Documentation

```javascript
/**
 * Toggle the payment status of a therapy session.
 * 
 * Changes a pending session to paid, or a paid session to pending.
 * Updates the UI automatically after successful toggle.
 * 
 * @async
 * @param {number} sessionId - The ID of the session to toggle
 * @returns {Promise<Session>} The updated session data
 * @throws {Error} If session not found (404)
 * @throws {Error} If user not authorized (403)
 * @fires SessionUpdateEvent
 * 
 * @example
 * // Toggle payment and update UI
 * try {
 *     const session = await toggleSessionPayment(123);
 *     console.log(`Session is now ${session.pending ? 'pending' : 'paid'}`);
 * } catch (error) {
 *     showToast(error.message, 'error');
 * }
 */
async function toggleSessionPayment(sessionId) {
    const response = await apiRequest(`/sessions/${sessionId}/toggle-payment`, {
        method: 'POST',
    });
    
    document.dispatchEvent(new CustomEvent('session-update', {
        detail: { sessionId, session: response, action: 'toggle-payment' }
    }));
    
    return response;
}
```

### UI Component Documentation

```javascript
/**
 * Show a toast notification to the user.
 * 
 * Creates and displays a toast message with automatic dismissal.
 * Supports different types for visual distinction (success, error, etc.).
 * Uses ARIA live regions for screen reader accessibility.
 * 
 * @param {string} message - The message to display
 * @param {'success'|'error'|'warning'|'info'} [type='info'] - Toast type for styling
 * @param {number} [duration=3000] - Duration in milliseconds before auto-dismiss
 * @returns {HTMLElement} The created toast element
 * 
 * @example
 * // Success message
 * showToast('Paciente guardado exitosamente', 'success');
 * 
 * @example
 * // Error with longer duration
 * showToast('Error al conectar con el servidor', 'error', 5000);
 * 
 * @example
 * // Get reference to dismiss programmatically
 * const toast = showToast('Procesando...', 'info', 0);
 * // Later...
 * hideToast(toast);
 */
function showToast(message, type = 'info', duration = 3000) { }
```

### Event Handler Documentation

```javascript
/**
 * Handle click events on session action buttons.
 * 
 * Delegates click events to appropriate handlers based on
 * the data-action attribute of the clicked element.
 * 
 * @param {MouseEvent} event - The click event
 * @listens document#click
 * @private
 * 
 * @example
 * // HTML structure expected:
 * // <button data-action="toggle-payment" data-session-id="123">
 * //   Marcar Pagado
 * // </button>
 */
function handleSessionClick(event) {
    const button = event.target.closest('[data-action]');
    if (!button) return;
    
    const action = button.dataset.action;
    const sessionId = parseInt(button.dataset.sessionId, 10);
    
    // ... handle action
}
```

---

## Tag Reference

### Common Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `@param` | Function parameter | `@param {string} name - User name` |
| `@returns` | Return value | `@returns {boolean} Success status` |
| `@throws` | Possible exceptions | `@throws {Error} If invalid` |
| `@async` | Async function | `@async` |
| `@type` | Variable type | `@type {string}` |
| `@typedef` | Custom type | `@typedef {Object} User` |
| `@property` | Object property | `@property {number} id` |
| `@callback` | Callback type | `@callback Handler` |

### Documentation Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `@description` | Full description | `@description Does X` |
| `@example` | Usage example | `@example func()` |
| `@see` | Related reference | `@see {@link other}` |
| `@since` | Version added | `@since 1.0.0` |
| `@deprecated` | Marked obsolete | `@deprecated Use X` |
| `@todo` | Work to be done | `@todo Add validation` |

### Scope Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `@private` | Private member | `@private` |
| `@protected` | Protected member | `@protected` |
| `@public` | Public member | `@public` |
| `@readonly` | Cannot be modified | `@readonly` |
| `@const` | Constant value | `@const` |

### Class Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `@class` | Class definition | `@class` |
| `@constructor` | Constructor | `@constructor` |
| `@extends` | Parent class | `@extends BaseClass` |
| `@implements` | Interface | `@implements IHandler` |
| `@abstract` | Abstract class | `@abstract` |
| `@static` | Static member | `@static` |

### Module Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `@module` | Module name | `@module api/client` |
| `@exports` | Exported member | `@exports getPatient` |
| `@requires` | Dependency | `@requires module:utils` |

---

## IDE Integration

### VS Code Support

VS Code automatically reads JSDoc for:
- **Hover documentation**: Shows docs when hovering over symbols
- **IntelliSense**: Autocomplete with type info
- **Parameter hints**: Shows param types while typing
- **Type checking**: With `// @ts-check` or `jsconfig.json`

### Enable Type Checking

```javascript
// @ts-check
// Add at top of file for TypeScript-like checking

/**
 * @param {string} name
 */
function greet(name) {
    console.log(name.toUpperCase());
    console.log(name.foo); // Error: Property 'foo' does not exist
}
```

### jsconfig.json for Project-Wide Checking

```json
{
    "compilerOptions": {
        "checkJs": true,
        "strict": true,
        "target": "ES2020",
        "module": "ES2020",
        "moduleResolution": "node"
    },
    "include": ["static/js/**/*"],
    "exclude": ["static/js/bootstrap.bundle.min.js"]
}
```

---

## Documentation Generation

### Using JSDoc CLI

```bash
# Install JSDoc
npm install -g jsdoc

# Generate documentation
jsdoc static/js/ -r -d docs/js

# With configuration file
jsdoc -c jsdoc.json
```

### jsdoc.json Configuration

```json
{
    "source": {
        "include": ["static/js/"],
        "exclude": ["static/js/bootstrap.bundle.min.js"],
        "includePattern": ".+\\.js$"
    },
    "opts": {
        "destination": "./docs/js/",
        "recurse": true
    },
    "plugins": ["plugins/markdown"],
    "templates": {
        "cleverLinks": true,
        "monospaceLinks": true
    }
}
```

---

## Best Practices

### DO ✅

```javascript
/**
 * ✅ Use complete sentences for descriptions
 * ✅ Document all public functions
 * ✅ Include @example for complex functions
 * ✅ Use @typedef for reusable types
 * ✅ Document edge cases with @throws
 */

/**
 * Calculate the total price of all pending sessions.
 * 
 * Sums the session_price of all sessions where pending is true.
 * Returns 0 if no pending sessions exist.
 * 
 * @param {Session[]} sessions - Array of session objects
 * @returns {number} Total price of pending sessions
 * 
 * @example
 * const total = calculatePendingTotal(sessions);
 * console.log(`Total pendiente: ${formatPrice(total)}`);
 */
function calculatePendingTotal(sessions) {
    return sessions
        .filter(s => s.pending)
        .reduce((sum, s) => sum + s.session_price, 0);
}
```

### DON'T ❌

```javascript
/**
 * ❌ Obvious or redundant documentation
 */
function getName() {
    return this.name;  // Gets the name - DUH!
}

/**
 * ❌ Outdated documentation (worse than none)
 * @param {string} id - User ID  // Actually expects number now!
 */
function getUser(id) { }

/**
 * ❌ Undocumented parameters
 * @param name  // Missing type and description
 */
function createUser(name, age, email) { }  // age and email not documented!
```

---

## Checklist for JSDoc

### Coverage
- [ ] All exported functions documented
- [ ] All public class methods documented
- [ ] All module files have `@module` tag
- [ ] Complex types defined with `@typedef`

### Quality
- [ ] Descriptions explain "why" not just "what"
- [ ] Parameters include types and descriptions
- [ ] Return values documented with types
- [ ] Error cases documented with `@throws`

### Examples
- [ ] Complex functions have `@example`
- [ ] Examples are runnable code
- [ ] Edge cases shown in examples

### Maintenance
- [ ] Documentation matches implementation
- [ ] Deprecated items marked with `@deprecated`
- [ ] New features marked with `@since`

---

## Related Skills

- [skill-javascript-modules.md](./skill-javascript-modules.md) - Module patterns
- [skill-error-handling.md](./skill-error-handling.md) - Documenting errors
- [skill-documentation.md](./skill-documentation.md) - General documentation

---

*Last Updated: January 15, 2026*
