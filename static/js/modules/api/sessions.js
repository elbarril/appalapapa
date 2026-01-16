/**
 * Sessions API Module
 * @module api/sessions
 * @description API calls for therapy session management
 */

import { get, post, put, del } from './client.js';

/**
 * Session data structure
 * @typedef {Object} Session
 * @property {number} id - Session ID
 * @property {number} person_id - Patient ID
 * @property {string} session_date - Session date (YYYY-MM-DD)
 * @property {number} session_price - Session price
 * @property {boolean} pending - Whether payment is pending
 * @property {string|null} notes - Session notes
 */

/**
 * Get a session by ID
 * @param {number} sessionId - Session ID
 * @returns {Promise<Session>} - Session data
 * @example
 * const session = await getSession(1);
 * console.log(session.session_date, session.pending);
 */
export async function getSession(sessionId) {
    return get(`/sessions/${sessionId}`);
}

/**
 * Update a session
 * @param {number} sessionId - Session ID
 * @param {Object} data - Session data to update
 * @param {string} data.session_date - Session date (YYYY-MM-DD)
 * @param {number} data.session_price - Session price
 * @param {boolean} data.pending - Payment status
 * @param {string} [data.notes] - Session notes (optional)
 * @returns {Promise<Session>} - Updated session data
 * @example
 * const updated = await updateSession(1, {
 *     session_date: '2024-01-15',
 *     session_price: 100,
 *     pending: false,
 *     notes: 'Session completed'
 * });
 */
export async function updateSession(sessionId, data) {
    return put(`/sessions/${sessionId}`, data);
}

/**
 * Delete a session (soft delete)
 * @param {number} sessionId - Session ID
 * @returns {Promise<{message: string}>} - Success message
 * @example
 * await deleteSession(1);
 */
export async function deleteSession(sessionId) {
    return del(`/sessions/${sessionId}`);
}

/**
 * Toggle session payment status
 * @param {number} sessionId - Session ID
 * @returns {Promise<{message: string, pending: boolean}>} - New status
 * @example
 * const result = await toggleSessionPayment(1);
 * console.log(result.pending ? 'Now pending' : 'Now paid');
 */
export async function toggleSessionPayment(sessionId) {
    return post(`/sessions/${sessionId}/toggle`, {});
}
