"""
Session management routes.

Handles creating, editing, deleting, and payment tracking of therapy sessions.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.services.patient_service import PatientService
from app.services.session_service import SessionService
from app.utils.constants import FlashCategory
from app.validators.forms import (
    DeleteSessionForm,
    EditSessionForm,
    SessionForm,
    TogglePaymentForm,
)

sessions_bp = Blueprint("sessions", __name__)


@sessions_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_session():
    """Add a new therapy session."""
    form = SessionForm()

    # Populate patient choices
    form.person_id.choices = PatientService.get_for_select()

    if not form.person_id.choices:
        flash("Primero debes agregar un paciente.", FlashCategory.WARNING)
        return redirect(url_for("patients.add_person"))

    if form.validate_on_submit():
        success, session, message = SessionService.create(
            person_id=form.person_id.data,
            session_date=form.session_date.data,
            session_price=float(form.session_price.data),
            user_id=current_user.id,
            pending=form.pending.data if hasattr(form, "pending") else True,
            notes=form.notes.data if hasattr(form, "notes") else None,
        )

        if success:
            flash(message, FlashCategory.SUCCESS)
            return redirect(url_for("patients.index"))
        else:
            flash(message, FlashCategory.ERROR)

    return render_template("sessions/form_session.html", form=form)


@sessions_bp.route("/<int:person_id>/<int:session_id>/edit", methods=["GET", "POST"])
@login_required
def update_session(person_id, session_id):
    """Edit an existing therapy session."""
    session_data = SessionService.get_session_with_person(session_id, person_id)

    if not session_data:
        flash("Sesión no encontrada.", FlashCategory.ERROR)
        return redirect(url_for("patients.index"))

    form = EditSessionForm()

    if request.method == "GET":
        # Pre-populate form
        form.session_date.data = session_data["date"]
        form.session_price.data = session_data["price"]
        if hasattr(form, "pending"):
            form.pending.data = session_data["pending"]
        if hasattr(form, "notes"):
            form.notes.data = session_data.get("notes")

    if form.validate_on_submit():
        success, session, message = SessionService.update(
            session_id=session_id,
            session_date=form.session_date.data,
            session_price=float(form.session_price.data),
            user_id=current_user.id,
            pending=form.pending.data if hasattr(form, "pending") else None,
            notes=form.notes.data if hasattr(form, "notes") else None,
        )

        if success:
            flash(message, FlashCategory.SUCCESS)
            return redirect(url_for("patients.index"))
        else:
            flash(message, FlashCategory.ERROR)

    return render_template(
        "sessions/form_edit.html",
        form=form,
        id=session_id,
        person_id=person_id,
        name=session_data["name"],
        date=session_data["date"],
        price=session_data["price"],
    )


@sessions_bp.route("/<int:session_id>/remove")
@login_required
def remove_session(session_id):
    """Delete a therapy session."""
    success, message = SessionService.delete(
        session_id=session_id,
        user_id=current_user.id,
        soft=True,  # Use soft delete by default
    )

    if success:
        flash(message, FlashCategory.SUCCESS)
    else:
        flash(message, FlashCategory.ERROR)

    return redirect(url_for("patients.index"))


@sessions_bp.route("/<int:session_id>/toggle")
@login_required
def toggle_pending(session_id):
    """Toggle payment status of a session."""
    success, new_status, message = SessionService.toggle_payment_status(session_id=session_id, user_id=current_user.id)

    if success:
        # Use info category for toggle since it's not an error
        flash(message, FlashCategory.INFO)
    else:
        flash(message, FlashCategory.ERROR)

    return redirect(url_for("patients.index"))
