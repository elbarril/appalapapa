/**
 * Patients API Module
 * @module api/patients
 * @description API calls for patient (person) management
 */

import { get, put, del } from './client.js';

/**
 * Patient data structure
 * @typedef {Object} Patient
 * @property {number} id - Patient ID
 * @property {string} name - Patient name
 * @property {string|null} notes - Patient notes
 * @property {string} created_at - Creation timestamp
 */

/**
 * Get a patient by ID
 * @param {number} patientId - Patient ID
 * @returns {Promise<Patient>} - Patient data
 * @example
 * const patient = await getPatient(1);
 * console.log(patient.name);
 */
export async function getPatient(patientId) {
    return get(`/patients/${patientId}`);
}

/**
 * Update a patient
 * @param {number} patientId - Patient ID
 * @param {Object} data - Patient data to update
 * @param {string} data.name - Patient name (required)
 * @param {string} [data.notes] - Patient notes (optional)
 * @returns {Promise<Patient>} - Updated patient data
 * @example
 * const updated = await updatePatient(1, { name: 'John Doe', notes: 'Regular patient' });
 */
export async function updatePatient(patientId, data) {
    return put(`/patients/${patientId}`, data);
}

/**
 * Delete a patient (soft delete)
 * @param {number} patientId - Patient ID
 * @returns {Promise<{message: string}>} - Success message
 * @example
 * await deletePatient(1);
 */
export async function deletePatient(patientId) {
    return del(`/patients/${patientId}`);
}
