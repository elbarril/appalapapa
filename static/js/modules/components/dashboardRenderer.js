/**
 * Dashboard Renderer Module
 * @module components/dashboardRenderer
 * @description Renders patient cards and sessions carousel for the dashboard
 */

import { escapeHtml } from '../utils/helpers.js';
import { initCarousels } from '../ui/carousel.js';

/**
 * Render the patients list from dashboard data
 * @param {Object} data - Dashboard data from API
 * @param {Array} data.grouped_sessions - Array of patients with their sessions
 * @param {boolean} data.allow_delete - Whether delete is allowed for the user
 */
export function renderPatientsList(data) {
    const container = document.querySelector('.patients-grid-container');
    if (!container) return;
    
    const { grouped_sessions, allow_delete } = data;
    
    if (!grouped_sessions || grouped_sessions.length === 0) {
        container.innerHTML = `
            <div class="text-center my-5 py-5">
                <i class="bi bi-people display-1 text-body-secondary mb-3" aria-hidden="true"></i>
                <h3 class="text-body-secondary">No hay pacientes</h3>
                <p class="text-body-secondary mb-4">Comienza agregando tu primer paciente.</p>
                <a href="/patients/add" class="btn btn-primary">
                    <i class="bi bi-person-plus me-1" aria-hidden="true"></i>
                    Agregar Paciente
                </a>
            </div>
        `;
        return;
    }
    
    let html = '<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4">';
    
    grouped_sessions.forEach((patient, index) => {
        const patientId = patient.patient_id;
        const patientName = patient.patient_name;
        const sessions = patient.sessions;
        const escapedName = escapeHtml(patientName);
        
        html += `
            <div class="col">
                <div class="card h-100 patient-card fade-in" data-patient-id="${patientId}" style="animation-delay: ${index * 0.05}s">
                    <!-- Patient header -->
                    <div class="card-header">
                        <h5 class="mb-2 patient-name" title="${patientName}">
                            <i class="bi bi-person-fill me-1 text-mlc-teal" aria-hidden="true"></i>
                            ${patientName}
                        </h5>
                        <div class="btn-group btn-group-sm w-100" role="group" aria-label="Acciones de paciente">
                            <button type="button"
                               class="btn btn-outline-secondary flex-fill" 
                               title="Editar paciente" 
                               aria-label="Editar paciente ${patientName}"
                               onclick="openEditPatientModal(${patientId}, '${escapedName}')">
                                <i class="bi bi-pencil me-1" aria-hidden="true"></i>Editar
                            </button>
                            ${allow_delete ? `
                                <button type="button"
                                   class="btn btn-outline-danger flex-fill" 
                                   title="Eliminar paciente" 
                                   aria-label="Eliminar paciente ${patientName}"
                                   onclick="openDeletePatientModal(${patientId}, '${escapedName}')">
                                    <i class="bi bi-trash me-1" aria-hidden="true"></i>Eliminar
                                </button>
                            ` : ''}
                        </div>
                    </div>

                    <!-- Patient body with sessions carousel -->
                    <div class="card-body p-2">
                        ${renderSessionsCarousel(patientId, sessions)}
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
    
    // Re-initialize carousels
    initCarousels();
}

/**
 * Render sessions carousel for a patient
 * @param {number} patientId - Patient ID
 * @param {Array} sessions - Sessions array
 * @returns {string} - HTML string for the carousel
 */
export function renderSessionsCarousel(patientId, sessions) {
    if (!sessions || sessions.length === 0) {
        return `
            <p class="text-body-secondary text-center my-3">
                <i class="bi bi-calendar-x me-1" aria-hidden="true"></i>
                No hay sesiones registradas.
            </p>
        `;
    }
    
    const singleSlide = sessions.length <= 1 ? 'single-slide' : '';
    
    let carouselItems = '';
    let indicators = '';
    
    sessions.forEach((session, index) => {
        const isFirst = index === 0;
        const sessionId = session.id;
        const sessionDate = session.date;
        const sessionPrice = session.price;
        const pending = session.pending;
        const escapedDate = escapeHtml(sessionDate);
        
        const badgeClass = pending ? 'text-bg-warning' : 'text-bg-success';
        const badgeText = pending ? 'PENDIENTE' : 'PAGADO';
        
        carouselItems += `
            <div class="carousel-item ${isFirst ? 'active' : ''}" data-session-pending="${pending ? 'true' : 'false'}">
                <div class="card mx-auto session-card" data-session-id="${sessionId}">
                    <div class="card-header d-flex justify-content-between align-items-center py-2">
                        <small class="text-body-secondary session-date">${sessionDate}</small>
                        <span class="badge ${badgeClass} session-status">${badgeText}</span>
                    </div>

                    <div class="card-body py-2">
                        <p class="card-text mb-0 session-price">${sessionPrice}</p>
                    </div>

                    <div class="card-footer py-2">
                        <div class="btn-group btn-group-sm w-100" role="group" aria-label="Acciones de sesión">
                            <button type="button"
                               class="btn btn-outline-secondary flex-fill"
                               title="Editar sesión"
                               aria-label="Editar sesión del ${sessionDate}"
                               onclick="openEditSessionModal(${sessionId}, ${patientId})">
                                <i class="bi bi-pencil-square me-1" aria-hidden="true"></i>Editar
                            </button>
                            <button type="button"
                               class="btn btn-outline-danger flex-fill delete-session-btn"
                               title="Eliminar sesión"
                               aria-label="Eliminar sesión del ${sessionDate}"
                               onclick="openDeleteSessionModal(${sessionId}, '${escapedDate}')">
                                <i class="bi bi-trash me-1" aria-hidden="true"></i>Eliminar
                            </button>
                            ${pending ? `
                                <button type="button"
                                   class="btn btn-success flex-fill toggle-payment-btn"
                                   title="Marcar como pagado"
                                   aria-label="Marcar sesión del ${sessionDate} como pagado"
                                   onclick="togglePayment(${sessionId})">
                                    <i class="bi bi-check-circle me-1" aria-hidden="true"></i>Pagado
                                </button>
                            ` : `
                                <button type="button"
                                   class="btn btn-outline-secondary flex-fill toggle-payment-btn"
                                   title="Marcar como pendiente"
                                   aria-label="Marcar sesión del ${sessionDate} como pendiente"
                                   onclick="togglePayment(${sessionId})">
                                    <i class="bi bi-clock-history me-1" aria-hidden="true"></i>Pendiente
                                </button>
                            `}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        indicators += `
            <button type="button" 
                    data-bs-target="#carousel-${patientId}" 
                    data-bs-slide-to="${index}" 
                    ${isFirst ? 'class="active" aria-current="true"' : ''}
                    aria-label="Sesión ${index + 1}"
                    ${sessions.length <= 1 ? 'disabled' : ''}>
            </button>
        `;
    });
    
    return `
        <div id="carousel-${patientId}" class="carousel slide" data-bs-ride="false" data-bs-touch="true">
            <div class="carousel-inner">
                ${carouselItems}
            </div>
            <div class="carousel-indicators-bottom ${singleSlide}">
                ${indicators}
            </div>
        </div>
    `;
}
