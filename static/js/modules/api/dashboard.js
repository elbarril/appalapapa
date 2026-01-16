/**
 * Dashboard API Module
 * @module api/dashboard
 * @description API calls for dashboard data
 */

import { get } from './client.js';

/**
 * Session summary for dashboard
 * @typedef {Object} SessionSummary
 * @property {number} id - Session ID
 * @property {string} date - Formatted date
 * @property {string} price - Formatted price
 * @property {boolean} pending - Payment status
 */

/**
 * Patient with sessions for dashboard
 * @typedef {Object} PatientWithSessions
 * @property {number} patient_id - Patient ID
 * @property {string} patient_name - Patient name
 * @property {SessionSummary[]} sessions - Patient's sessions
 */

/**
 * Dashboard data structure
 * @typedef {Object} DashboardData
 * @property {PatientWithSessions[]} grouped_sessions - Patients with their sessions
 * @property {boolean} allow_delete - Whether delete is allowed
 */

/**
 * Get dashboard data with optional filter
 * @param {('all'|'pending'|'paid')} [filter='all'] - Filter type
 * @returns {Promise<DashboardData>} - Dashboard data
 * @example
 * // Get all sessions
 * const data = await getDashboardData();
 * 
 * // Get only pending sessions
 * const pending = await getDashboardData('pending');
 */
export async function getDashboardData(filter = 'all') {
    return get(`/dashboard?show=${filter}`);
}
