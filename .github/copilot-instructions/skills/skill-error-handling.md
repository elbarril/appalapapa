# Skill: Error Handling

## Overview

This skill covers error handling patterns in JavaScript for the Therapy Session Management Application. Proper error handling ensures graceful degradation, user-friendly feedback, and maintainable debugging. The goal is to catch errors at appropriate levels, provide meaningful messages in Spanish, and maintain application stability.

---

## Error Types in JavaScript

### Built-in Error Types

| Error Type | When Thrown | Example |
|------------|-------------|---------|
| `Error` | Generic error | `throw new Error('Something went wrong')` |
| `TypeError` | Wrong type used | Calling method on `null` |
| `ReferenceError` | Undefined variable | Accessing undeclared variable |
| `SyntaxError` | Invalid syntax | Malformed JSON |
| `RangeError` | Out of range | Invalid array length |
| `URIError` | Invalid URI | `decodeURIComponent('%')` |
| `NetworkError` | Network failure | Fetch fails |

### Custom Error Classes

```javascript
/**
 * Base application error
 * @extends Error
 */
class AppError extends Error {
    /**
     * @param {string} message - Error message
     * @param {string} code - Error code for programmatic handling
     * @param {number} [statusCode] - HTTP status code if applicable
     */
    constructor(message, code, statusCode = null) {
        super(message);
        this.name = 'AppError';
        this.code = code;
        this.statusCode = statusCode;
        this.timestamp = new Date().toISOString();
    }
}

/**
 * API request error
 * @extends AppError
 */
class ApiError extends AppError {
    constructor(message, statusCode, responseData = null) {
        super(message, 'API_ERROR', statusCode);
        this.name = 'ApiError';
        this.responseData = responseData;
    }
}

/**
 * Validation error
 * @extends AppError
 */
class ValidationError extends AppError {
    /**
     * @param {string} message
     * @param {Object.<string, string>} fields - Field-specific errors
     */
    constructor(message, fields = {}) {
        super(message, 'VALIDATION_ERROR', 400);
        this.name = 'ValidationError';
        this.fields = fields;
    }
}

/**
 * Authentication error
 * @extends AppError
 */
class AuthError extends AppError {
    constructor(message = 'No autorizado') {
        super(message, 'AUTH_ERROR', 401);
        this.name = 'AuthError';
    }
}

/**
 * Not found error
 * @extends AppError
 */
class NotFoundError extends AppError {
    constructor(resource = 'Recurso') {
        super(`${resource} no encontrado`, 'NOT_FOUND', 404);
        this.name = 'NotFoundError';
    }
}
```

---

## Try/Catch Patterns

### Basic Pattern

```javascript
try {
    // Code that might throw
    const result = riskyOperation();
    return result;
} catch (error) {
    // Handle the error
    console.error('Operation failed:', error);
    throw error;  // Re-throw if can't handle
} finally {
    // Always runs (cleanup)
    cleanup();
}
```

### Async/Await Pattern

```javascript
/**
 * Fetch patient with error handling
 * @param {number} patientId
 * @returns {Promise<Patient>}
 */
async function getPatient(patientId) {
    try {
        const response = await fetch(`/api/v1/patients/${patientId}`);
        
        if (!response.ok) {
            // Create appropriate error based on status
            if (response.status === 404) {
                throw new NotFoundError('Paciente');
            }
            if (response.status === 401) {
                throw new AuthError();
            }
            throw new ApiError('Error al cargar paciente', response.status);
        }
        
        return await response.json();
    } catch (error) {
        // Re-throw known errors
        if (error instanceof AppError) {
            throw error;
        }
        
        // Wrap unknown errors
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new ApiError('Error de conexión. Verifique su internet.', 0);
        }
        
        throw new AppError('Error inesperado', 'UNKNOWN_ERROR');
    }
}
```

### Multiple Catch Blocks (Simulated)

```javascript
async function handlePatientAction(patientId) {
    try {
        const patient = await getPatient(patientId);
        await updatePatient(patientId, newData);
        showToast('Paciente actualizado', 'success');
    } catch (error) {
        // Handle different error types
        if (error instanceof NotFoundError) {
            showToast('El paciente no existe', 'error');
            redirectToDashboard();
        } else if (error instanceof AuthError) {
            showToast('Sesión expirada. Inicie sesión nuevamente.', 'error');
            redirectToLogin();
        } else if (error instanceof ValidationError) {
            showFormErrors(error.fields);
        } else if (error instanceof ApiError) {
            showToast(error.message, 'error');
        } else {
            // Unknown error - log for debugging
            console.error('Unexpected error:', error);
            showToast('Error inesperado. Intente nuevamente.', 'error');
        }
    }
}
```

---

## API Error Handling

### Centralized API Client

```javascript
/**
 * API client with built-in error handling
 */
const api = {
    /**
     * Make an API request with standardized error handling
     * @param {string} endpoint
     * @param {RequestInit} options
     * @returns {Promise<any>}
     * @throws {ApiError}
     */
    async request(endpoint, options = {}) {
        const url = `/api/v1${endpoint}`;
        
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                    ...options.headers,
                },
                credentials: 'same-origin',
                ...options,
            });
            
            // Parse response
            let data;
            try {
                data = await response.json();
            } catch {
                data = null;
            }
            
            // Handle HTTP errors
            if (!response.ok) {
                throw this.createError(response.status, data);
            }
            
            return data;
        } catch (error) {
            // Network errors
            if (error.name === 'TypeError') {
                throw new ApiError(
                    'No se pudo conectar con el servidor. Verifique su conexión.',
                    0
                );
            }
            
            // Re-throw API errors
            if (error instanceof ApiError) {
                throw error;
            }
            
            // Wrap unknown errors
            throw new ApiError('Error inesperado', 500, { originalError: error.message });
        }
    },
    
    /**
     * Create appropriate error from response
     * @param {number} status
     * @param {object|null} data
     * @returns {ApiError}
     */
    createError(status, data) {
        const messages = {
            400: data?.error || 'Datos inválidos',
            401: 'Sesión expirada. Inicie sesión nuevamente.',
            403: 'No tiene permiso para realizar esta acción',
            404: data?.error || 'Recurso no encontrado',
            409: data?.error || 'Conflicto con datos existentes',
            422: data?.error || 'Error de validación',
            429: 'Demasiadas solicitudes. Espere un momento.',
            500: 'Error del servidor. Intente más tarde.',
            502: 'Servidor no disponible. Intente más tarde.',
            503: 'Servicio temporalmente no disponible',
        };
        
        const message = messages[status] || `Error del servidor (${status})`;
        return new ApiError(message, status, data);
    },
    
    // Convenience methods
    get: (endpoint) => api.request(endpoint, { method: 'GET' }),
    post: (endpoint, data) => api.request(endpoint, { method: 'POST', body: JSON.stringify(data) }),
    put: (endpoint, data) => api.request(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (endpoint) => api.request(endpoint, { method: 'DELETE' }),
};
```

### Error Response Handling

```javascript
/**
 * Handle API response and extract error message
 * @param {Response} response
 * @returns {Promise<string>}
 */
async function getErrorMessage(response) {
    try {
        const data = await response.json();
        
        // Handle different error response formats
        if (data.error) return data.error;
        if (data.message) return data.message;
        if (data.errors) {
            // Flask-WTF validation errors
            const firstError = Object.values(data.errors)[0];
            return Array.isArray(firstError) ? firstError[0] : firstError;
        }
        
        return 'Error desconocido';
    } catch {
        return `Error del servidor (${response.status})`;
    }
}
```

---

## UI Error Handling

### Toast Notifications for Errors

```javascript
/**
 * Show error toast with appropriate styling
 * @param {Error} error
 */
function showErrorToast(error) {
    let message = 'Error inesperado';
    let type = 'error';
    
    if (error instanceof ValidationError) {
        message = error.message;
        type = 'warning';
    } else if (error instanceof NotFoundError) {
        message = error.message;
    } else if (error instanceof AuthError) {
        message = error.message;
        // Also redirect to login
        setTimeout(() => redirectToLogin(), 2000);
    } else if (error instanceof ApiError) {
        message = error.message;
    } else if (error.message) {
        message = error.message;
    }
    
    showToast(message, type);
}
```

### Form Error Display

```javascript
/**
 * Display validation errors on form fields
 * @param {HTMLFormElement} form
 * @param {Object.<string, string>} errors - Field name to error message
 */
function showFormErrors(form, errors) {
    // Clear previous errors
    clearFormErrors(form);
    
    Object.entries(errors).forEach(([field, message]) => {
        const input = form.querySelector(`[name="${field}"]`);
        
        if (input) {
            // Mark input as invalid
            input.classList.add('is-invalid');
            input.setAttribute('aria-invalid', 'true');
            
            // Create error message element
            const errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            errorDiv.id = `${field}-error`;
            errorDiv.textContent = message;
            
            // Associate error with input
            input.setAttribute('aria-describedby', errorDiv.id);
            
            // Insert after input
            input.parentNode.insertBefore(errorDiv, input.nextSibling);
        }
    });
    
    // Focus first invalid field
    const firstInvalid = form.querySelector('.is-invalid');
    if (firstInvalid) {
        firstInvalid.focus();
    }
}

/**
 * Clear all form errors
 * @param {HTMLFormElement} form
 */
function clearFormErrors(form) {
    form.querySelectorAll('.is-invalid').forEach(input => {
        input.classList.remove('is-invalid');
        input.removeAttribute('aria-invalid');
        input.removeAttribute('aria-describedby');
    });
    
    form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
}
```

### Loading State with Error Recovery

```javascript
/**
 * Execute async action with loading state and error handling
 * @param {HTMLElement} button
 * @param {Function} action
 */
async function withLoadingState(button, action) {
    const originalContent = button.innerHTML;
    const originalDisabled = button.disabled;
    
    try {
        // Set loading state
        button.disabled = true;
        button.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            <span class="visually-hidden">Cargando...</span>
        `;
        
        // Execute action
        await action();
        
    } catch (error) {
        // Show error
        showErrorToast(error);
        throw error;  // Re-throw for caller to handle
        
    } finally {
        // Restore button state
        button.disabled = originalDisabled;
        button.innerHTML = originalContent;
    }
}

// Usage
deleteButton.addEventListener('click', async () => {
    await withLoadingState(deleteButton, async () => {
        await deletePatient(patientId);
        removePatientFromUI(patientId);
        showToast('Paciente eliminado', 'success');
    });
});
```

---

## Error Boundaries

### Global Error Handler

```javascript
/**
 * Global unhandled error handler
 */
window.addEventListener('error', (event) => {
    console.error('Unhandled error:', event.error);
    
    // Log to monitoring service
    logErrorToService({
        type: 'unhandled',
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        stack: event.error?.stack,
    });
    
    // Show user-friendly message
    showToast('Ocurrió un error inesperado', 'error');
});

/**
 * Global unhandled promise rejection handler
 */
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    
    // Log to monitoring service
    logErrorToService({
        type: 'unhandledrejection',
        message: event.reason?.message || String(event.reason),
        stack: event.reason?.stack,
    });
    
    // Prevent default browser handling
    event.preventDefault();
    
    // Show user-friendly message
    showToast('Error de conexión o servidor', 'error');
});
```

### Component-Level Error Boundary

```javascript
/**
 * Wrap a component function with error boundary
 * @param {Function} componentFn
 * @param {HTMLElement} container
 * @param {Function} fallbackFn
 */
function withErrorBoundary(componentFn, container, fallbackFn) {
    return async function(...args) {
        try {
            await componentFn.apply(this, args);
        } catch (error) {
            console.error('Component error:', error);
            
            // Render fallback UI
            if (fallbackFn) {
                container.innerHTML = fallbackFn(error);
            } else {
                container.innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        <h4 class="alert-heading">Error al cargar</h4>
                        <p>${error.message || 'Error desconocido'}</p>
                        <button class="btn btn-outline-danger btn-sm" onclick="location.reload()">
                            Reintentar
                        </button>
                    </div>
                `;
            }
        }
    };
}

// Usage
const loadDashboard = withErrorBoundary(
    async () => {
        const data = await api.get('/dashboard');
        renderDashboard(data);
    },
    document.getElementById('dashboard'),
    (error) => `
        <div class="text-center py-5">
            <i class="bi bi-exclamation-triangle text-warning fs-1"></i>
            <p class="mt-3">No se pudo cargar el dashboard</p>
            <button class="btn btn-primary" onclick="loadDashboard()">Reintentar</button>
        </div>
    `
);
```

---

## Graceful Degradation

### Fallback Content

```javascript
/**
 * Load data with fallback to cached version
 * @param {string} endpoint
 * @param {string} cacheKey
 * @returns {Promise<any>}
 */
async function loadWithFallback(endpoint, cacheKey) {
    try {
        const data = await api.get(endpoint);
        
        // Cache successful response
        localStorage.setItem(cacheKey, JSON.stringify({
            data,
            timestamp: Date.now(),
        }));
        
        return data;
    } catch (error) {
        console.warn('API failed, trying cache:', error);
        
        // Try cached data
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const { data, timestamp } = JSON.parse(cached);
            const age = Date.now() - timestamp;
            
            // Show warning if cache is old (> 1 hour)
            if (age > 3600000) {
                showToast('Mostrando datos guardados. Algunos datos pueden estar desactualizados.', 'warning');
            }
            
            return data;
        }
        
        // No cache available, re-throw
        throw error;
    }
}
```

### Progressive Feature Loading

```javascript
/**
 * Initialize app with progressive feature loading
 */
async function initApp() {
    // Core features - must work
    try {
        await initNavigation();
        await initAuthentication();
    } catch (error) {
        // Critical failure - show error page
        showCriticalError(error);
        return;
    }
    
    // Enhanced features - graceful degradation
    const features = [
        { name: 'dashboard', init: initDashboard },
        { name: 'notifications', init: initNotifications },
        { name: 'analytics', init: initAnalytics },
    ];
    
    for (const feature of features) {
        try {
            await feature.init();
        } catch (error) {
            console.warn(`Feature ${feature.name} failed to load:`, error);
            // Continue with other features
        }
    }
}
```

### Retry Logic

```javascript
/**
 * Retry an async operation with exponential backoff
 * @param {Function} operation
 * @param {number} maxRetries
 * @param {number} baseDelay - Base delay in ms
 * @returns {Promise<any>}
 */
async function withRetry(operation, maxRetries = 3, baseDelay = 1000) {
    let lastError;
    
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            return await operation();
        } catch (error) {
            lastError = error;
            
            // Don't retry client errors (4xx)
            if (error instanceof ApiError && error.statusCode >= 400 && error.statusCode < 500) {
                throw error;
            }
            
            // Calculate delay with exponential backoff
            const delay = baseDelay * Math.pow(2, attempt);
            console.log(`Attempt ${attempt + 1} failed, retrying in ${delay}ms...`);
            
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
    
    throw lastError;
}

// Usage
const patient = await withRetry(() => api.get(`/patients/${id}`));
```

---

## Error Logging

### Log to Console (Development)

```javascript
/**
 * Enhanced error logging for development
 * @param {Error} error
 * @param {object} context
 */
function logError(error, context = {}) {
    console.group('🔴 Error');
    console.error('Message:', error.message);
    console.error('Type:', error.name);
    
    if (error instanceof AppError) {
        console.error('Code:', error.code);
        console.error('Status:', error.statusCode);
    }
    
    if (error.stack) {
        console.error('Stack:', error.stack);
    }
    
    if (Object.keys(context).length > 0) {
        console.error('Context:', context);
    }
    
    console.groupEnd();
}
```

### Log to Monitoring Service (Production)

```javascript
/**
 * Log error to external monitoring service
 * @param {object} errorData
 */
async function logErrorToService(errorData) {
    // Skip in development
    if (window.location.hostname === 'localhost') {
        return;
    }
    
    try {
        await fetch('/api/v1/errors', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...errorData,
                url: window.location.href,
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString(),
            }),
        });
    } catch {
        // Silently fail - don't cause more errors
        console.warn('Failed to log error to service');
    }
}
```

---

## Error Messages in Spanish

### Message Catalog

```javascript
/**
 * User-facing error messages in Spanish
 */
const ERROR_MESSAGES = {
    // Network errors
    NETWORK_ERROR: 'Error de conexión. Verifique su internet.',
    TIMEOUT: 'La solicitud tardó demasiado. Intente nuevamente.',
    SERVER_UNAVAILABLE: 'Servidor no disponible. Intente más tarde.',
    
    // Authentication
    UNAUTHORIZED: 'Sesión expirada. Inicie sesión nuevamente.',
    FORBIDDEN: 'No tiene permiso para realizar esta acción.',
    
    // Validation
    INVALID_DATA: 'Los datos ingresados no son válidos.',
    REQUIRED_FIELD: 'Este campo es obligatorio.',
    INVALID_EMAIL: 'Ingrese un correo electrónico válido.',
    INVALID_DATE: 'Ingrese una fecha válida.',
    INVALID_PRICE: 'Ingrese un precio válido.',
    
    // Resources
    NOT_FOUND: 'El recurso solicitado no existe.',
    PATIENT_NOT_FOUND: 'El paciente no existe o fue eliminado.',
    SESSION_NOT_FOUND: 'La sesión no existe o fue eliminada.',
    
    // Actions
    DELETE_FAILED: 'No se pudo eliminar. Intente nuevamente.',
    SAVE_FAILED: 'No se pudo guardar. Intente nuevamente.',
    UPDATE_FAILED: 'No se pudo actualizar. Intente nuevamente.',
    
    // Generic
    UNKNOWN_ERROR: 'Error inesperado. Intente nuevamente.',
    TRY_AGAIN: 'Por favor intente nuevamente.',
};

/**
 * Get localized error message
 * @param {string} code
 * @param {object} params - Replacement parameters
 * @returns {string}
 */
function getErrorMessage(code, params = {}) {
    let message = ERROR_MESSAGES[code] || ERROR_MESSAGES.UNKNOWN_ERROR;
    
    // Replace placeholders
    Object.entries(params).forEach(([key, value]) => {
        message = message.replace(`{${key}}`, value);
    });
    
    return message;
}
```

---

## Testing Error Handling

### Unit Tests

```javascript
describe('API Error Handling', () => {
    test('throws NotFoundError on 404', async () => {
        fetch.mockResolvedValueOnce({
            ok: false,
            status: 404,
            json: () => Promise.resolve({ error: 'Not found' }),
        });
        
        await expect(api.get('/patients/999')).rejects.toThrow(ApiError);
        await expect(api.get('/patients/999')).rejects.toMatchObject({
            statusCode: 404,
        });
    });
    
    test('throws network error on fetch failure', async () => {
        fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'));
        
        await expect(api.get('/patients')).rejects.toMatchObject({
            message: expect.stringContaining('conexión'),
        });
    });
});
```

### Integration Tests

```javascript
describe('Form Error Display', () => {
    test('shows validation errors on fields', () => {
        const form = document.createElement('form');
        form.innerHTML = `
            <input name="email" type="email">
            <input name="name" type="text">
        `;
        
        showFormErrors(form, {
            email: 'Correo inválido',
            name: 'Nombre requerido',
        });
        
        expect(form.querySelector('[name="email"]').classList.contains('is-invalid')).toBe(true);
        expect(form.querySelector('#email-error').textContent).toBe('Correo inválido');
    });
});
```

---

## Checklist for Error Handling

### Error Types
- [ ] Custom error classes for different scenarios
- [ ] Consistent error codes
- [ ] HTTP status code mapping

### Try/Catch
- [ ] All async operations wrapped
- [ ] Errors caught at appropriate level
- [ ] Errors re-thrown when can't handle

### User Feedback
- [ ] All errors shown to user
- [ ] Messages in Spanish
- [ ] Appropriate toast types (error/warning)
- [ ] Form errors displayed inline

### Recovery
- [ ] Retry logic for transient failures
- [ ] Fallback content available
- [ ] Loading states reset on error

### Logging
- [ ] Errors logged to console (dev)
- [ ] Errors sent to monitoring (prod)
- [ ] Context included in logs

### Testing
- [ ] Error scenarios tested
- [ ] Edge cases covered
- [ ] UI error display tested

---

## Related Skills

- [skill-javascript-modules.md](./skill-javascript-modules.md) - Organizing error handling
- [skill-jsdoc-documentation.md](./skill-jsdoc-documentation.md) - Documenting errors
- [skill-event-delegation.md](./skill-event-delegation.md) - Error handling in handlers

---

*Last Updated: January 15, 2026*
