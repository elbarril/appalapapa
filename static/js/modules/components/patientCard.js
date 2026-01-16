/**
 * Patient Card Component Module
 * @module components/patientCard
 * @description Patient card UI component with edit/delete functionality
 */

import { getPatient, updatePatient, deletePatient } from '../api/patients.js';
import { showToast } from '../ui/toast.js';
import { openModal, closeModal, getModalInstance } from '../ui/modal.js';
import { validatePatientForm } from '../utils/validators.js';
import { escapeHtml } from '../utils/helpers.js';

/**
 * Open the edit patient modal
 * @param {number} patientId - Patient ID
 * @param {string} patientName - Current patient name
 */
export async function openEditPatientModal(patientId, patientName) {
    const modal = document.getElementById('editPatientModal');
    if (!modal) return;

    // Set form values
    document.getElementById('editPatientId').value = patientId;
    document.getElementById('editPatientName').value = patientName;

    // Try to get notes from API
    try {
        const patient = await getPatient(patientId);
        document.getElementById('editPatientNotes').value = patient.notes || '';
    } catch (error) {
        document.getElementById('editPatientNotes').value = '';
    }

    // Show modal
    openModal('editPatientModal');
}

/**
 * Save edited patient
 * @returns {Promise<void>}
 */
export async function saveEditPatient() {
    const patientId = document.getElementById('editPatientId').value;
    const name = document.getElementById('editPatientName').value.trim();
    const notes = document.getElementById('editPatientNotes').value.trim();

    // Validate
    const validation = validatePatientForm({ name, notes });
    if (!validation.valid) {
        showToast(validation.message, 'error');
        return;
    }

    try {
        await updatePatient(patientId, { name, notes });
        showToast('Paciente actualizado correctamente', 'success');

        // Close modal
        closeModal('editPatientModal');

        // Update the patient name in the UI
        updatePatientNameInUI(patientId, name);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Update patient name in the UI without refresh
 * @param {number|string} patientId - Patient ID
 * @param {string} newName - New patient name
 */
export function updatePatientNameInUI(patientId, newName) {
    const patientCard = document.querySelector(`[data-patient-id="${patientId}"]`);
    if (patientCard) {
        const nameElement = patientCard.querySelector('.patient-name');
        if (nameElement) {
            nameElement.textContent = newName;
            nameElement.title = newName;
        }
    }
}

/**
 * Open the delete patient confirmation modal
 * @param {number} patientId - Patient ID
 * @param {string} patientName - Patient name
 */
export function openDeletePatientModal(patientId, patientName) {
    const modal = document.getElementById('deletePatientModal');
    if (!modal) return;

    document.getElementById('deletePatientId').value = patientId;
    document.getElementById('deletePatientName').textContent = patientName;

    openModal('deletePatientModal');
}

/**
 * Confirm and delete patient
 * @returns {Promise<void>}
 */
export async function confirmDeletePatient() {
    const patientId = document.getElementById('deletePatientId').value;

    try {
        await deletePatient(patientId);
        showToast('Paciente eliminado correctamente', 'success');

        // Close modal
        closeModal('deletePatientModal');

        // Remove patient card from UI
        removePatientFromUI(patientId);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Remove patient card from the UI
 * @param {number|string} patientId - Patient ID
 */
export function removePatientFromUI(patientId) {
    const patientCard = document.querySelector(`[data-patient-id="${patientId}"]`);
    if (patientCard) {
        patientCard.closest('.col').remove();
    }

    // Check if there are no more patients
    const remainingPatients = document.querySelectorAll('[data-patient-id]');
    if (remainingPatients.length === 0) {
        const gridContainer = document.querySelector('.row.row-cols-1');
        if (gridContainer) {
            gridContainer.innerHTML = `
                <div class="col-12">
                    <div class="text-center my-5">
                        <h3 class="text-muted">No hay pacientes</h3>
                    </div>
                </div>
            `;
        }
    }
}

/**
 * Initialize patient card event listeners
 */
export function initPatientCard() {
    // Edit patient form submission
    const editPatientForm = document.getElementById('editPatientForm');
    if (editPatientForm) {
        editPatientForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveEditPatient();
        });
    }

    // Delete patient confirmation
    const confirmDeletePatientBtn = document.getElementById('confirmDeletePatientBtn');
    if (confirmDeletePatientBtn) {
        confirmDeletePatientBtn.addEventListener('click', confirmDeletePatient);
    }
}

// Make functions globally available for backward compatibility with onclick handlers
window.openEditPatientModal = openEditPatientModal;
window.openDeletePatientModal = openDeletePatientModal;
window.saveEditPatient = saveEditPatient;
window.confirmDeletePatient = confirmDeletePatient;
