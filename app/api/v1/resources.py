"""
REST API v1 Resources.

JSON API endpoints for patients, sessions, and authentication.
"""

from flask import jsonify, request, current_app
from flask_login import login_required, current_user

from app.api.v1 import api_v1_bp
from app.services.patient_service import PatientService
from app.services.session_service import SessionService
from app.extensions import limiter


# =============================================================================
# Health Check
# =============================================================================


@api_v1_bp.route("/health")
def health():
    """API health check endpoint."""
    return jsonify({"status": "ok", "version": "v1"})


# =============================================================================
# Patients API
# =============================================================================


@api_v1_bp.route("/patients")
@login_required
def list_patients():
    """
    List all patients.

    Returns:
        JSON array of patients
    """
    patients = PatientService.get_all_active()
    return jsonify(
        {"patients": [p.to_dict() for p in patients], "count": len(patients)}
    )


@api_v1_bp.route("/patients/<int:patient_id>")
@login_required
def get_patient(patient_id):
    """
    Get a single patient.

    Args:
        patient_id: Patient ID

    Returns:
        JSON patient object or 404
    """
    patient = PatientService.get_by_id(patient_id)
    if not patient:
        return jsonify({"error": "Paciente no encontrado"}), 404

    return jsonify(patient.to_dict())


@api_v1_bp.route("/patients", methods=["POST"])
@login_required
@limiter.limit("30 per minute")
def create_patient():
    """
    Create a new patient.

    Request body:
        - name: Patient name (required)
        - notes: Optional notes

    Returns:
        JSON patient object or error
    """
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "El nombre es requerido"}), 400

    success, patient, message = PatientService.create(
        name=data["name"], user_id=current_user.id, notes=data.get("notes")
    )

    if success:
        return jsonify(patient.to_dict()), 201
    else:
        return jsonify({"error": message}), 400


@api_v1_bp.route("/patients/<int:patient_id>", methods=["DELETE"])
@login_required
def delete_patient(patient_id):
    """
    Delete a patient (soft delete).

    Args:
        patient_id: Patient ID

    Returns:
        Success message or error
    """
    success, message = PatientService.delete(
        person_id=patient_id, user_id=current_user.id, soft=True
    )

    if success:
        return jsonify({"message": message})
    else:
        return jsonify({"error": message}), 400


# =============================================================================
# Sessions API
# =============================================================================


@api_v1_bp.route("/patients/<int:patient_id>/sessions")
@login_required
def list_sessions(patient_id):
    """
    List sessions for a patient.

    Args:
        patient_id: Patient ID

    Returns:
        JSON array of sessions
    """
    from app.models.session import TherapySession

    sessions = TherapySession.get_by_person(patient_id).all()
    return jsonify(
        {"sessions": [s.to_dict() for s in sessions], "count": len(sessions)}
    )


@api_v1_bp.route("/sessions", methods=["POST"])
@login_required
@limiter.limit("30 per minute")
def create_session():
    """
    Create a new session.

    Request body:
        - person_id: Patient ID (required)
        - session_date: Date YYYY-MM-DD (required)
        - session_price: Price (required)
        - pending: Payment status (default true)
        - notes: Optional notes

    Returns:
        JSON session object or error
    """
    from datetime import datetime

    data = request.get_json()

    required_fields = ["person_id", "session_date", "session_price"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} es requerido"}), 400

    try:
        session_date = datetime.strptime(data["session_date"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    success, session, message = SessionService.create(
        person_id=data["person_id"],
        session_date=session_date,
        session_price=float(data["session_price"]),
        user_id=current_user.id,
        pending=data.get("pending", True),
        notes=data.get("notes"),
    )

    if success:
        return jsonify(session.to_dict()), 201
    else:
        return jsonify({"error": message}), 400


@api_v1_bp.route("/sessions/<int:session_id>/toggle", methods=["POST"])
@login_required
def toggle_session(session_id):
    """
    Toggle session payment status.

    Args:
        session_id: Session ID

    Returns:
        Updated session or error
    """
    success, new_status, message = SessionService.toggle_payment_status(
        session_id=session_id, user_id=current_user.id
    )

    if success:
        return jsonify({"message": message, "pending": new_status})
    else:
        return jsonify({"error": message}), 400


@api_v1_bp.route("/sessions/<int:session_id>", methods=["DELETE"])
@login_required
def delete_session(session_id):
    """
    Delete a session (soft delete).

    Args:
        session_id: Session ID

    Returns:
        Success message or error
    """
    success, message = SessionService.delete(
        session_id=session_id, user_id=current_user.id, soft=True
    )

    if success:
        return jsonify({"message": message})
    else:
        return jsonify({"error": message}), 400


# =============================================================================
# Statistics API
# =============================================================================


@api_v1_bp.route("/stats")
@login_required
def get_stats():
    """
    Get dashboard statistics.

    Returns:
        JSON with totals and counts
    """
    totals = SessionService.calculate_totals()
    patients = PatientService.get_all_active()

    return jsonify(
        {
            "patients_count": len(patients),
            "pending_total": totals["pending_total"],
            "paid_total": totals["paid_total"],
            "grand_total": totals["grand_total"],
        }
    )
