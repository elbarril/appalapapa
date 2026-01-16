/**
 * Base API Client Module
 * @module api/client
 * @description Handles all HTTP requests to the backend API with error handling
 */

/**
 * API base URL
 * @constant {string}
 */
const API_BASE = '/api/v1';

/**
 * Custom API Error class with additional context
 */
export class ApiError extends Error {
    /**
     * Create an API Error
     * @param {string} message - Error message
     * @param {number} status - HTTP status code
     * @param {Object|null} data - Response data if available
     */
    constructor(message, status, data = null) {
        super(message);
        this.name = 'ApiError';
        this.status = status;
        this.data = data;
    }
}

/**
 * Get CSRF token from meta tag
 * @returns {string|null} - CSRF token or null if not found
 */
export function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : null;
}

/**
 * Make an API request with error handling
 * @param {string} endpoint - API endpoint (relative to base URL)
 * @param {Object} [options={}] - Fetch options
 * @param {string} [options.method='GET'] - HTTP method
 * @param {Object} [options.body] - Request body (will be JSON stringified)
 * @param {Object} [options.headers] - Additional headers
 * @returns {Promise<Object>} - Response data
 * @throws {ApiError} If request fails
 * @example
 * // GET request
 * const data = await apiRequest('/patients/1');
 * 
 * // POST request
 * const result = await apiRequest('/patients', {
 *     method: 'POST',
 *     body: JSON.stringify({ name: 'John' })
 * });
 */
export async function apiRequest(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
    const csrfToken = getCsrfToken();
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(csrfToken && { 'X-CSRFToken': csrfToken }),
        },
        credentials: 'same-origin',
    };

    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {}),
        },
    };

    try {
        const response = await fetch(url, mergedOptions);
        
        // Handle empty responses
        const text = await response.text();
        const data = text ? JSON.parse(text) : {};

        if (!response.ok) {
            throw new ApiError(
                data.error || data.message || 'Error en la solicitud',
                response.status,
                data
            );
        }

        return data;
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        if (error instanceof SyntaxError) {
            throw new ApiError('Error al procesar la respuesta del servidor', 500, null);
        }
        throw new ApiError('Error de conexión', 0, null);
    }
}

/**
 * HTTP GET request helper
 * @param {string} endpoint - API endpoint
 * @returns {Promise<Object>} - Response data
 */
export function get(endpoint) {
    return apiRequest(endpoint, { method: 'GET' });
}

/**
 * HTTP POST request helper
 * @param {string} endpoint - API endpoint
 * @param {Object} data - Request body
 * @returns {Promise<Object>} - Response data
 */
export function post(endpoint, data) {
    return apiRequest(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

/**
 * HTTP PUT request helper
 * @param {string} endpoint - API endpoint
 * @param {Object} data - Request body
 * @returns {Promise<Object>} - Response data
 */
export function put(endpoint, data) {
    return apiRequest(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
}

/**
 * HTTP DELETE request helper
 * @param {string} endpoint - API endpoint
 * @returns {Promise<Object>} - Response data
 */
export function del(endpoint) {
    return apiRequest(endpoint, { method: 'DELETE' });
}

/**
 * Initialize API client (called on app startup)
 */
export function initApi() {
    console.log('API client initialized');
}
