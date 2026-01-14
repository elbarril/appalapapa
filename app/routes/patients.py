"""
Patient management routes.

Handles listing, creating, editing, and deleting patients.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.validators.forms import PersonForm, DeletePersonForm
from app.services.patient_service import PatientService
from app.utils.constants import FlashCategory, FILTERS, ALLOW_DELETE, ALL_FILTER

patients_bp = Blueprint("patients", __name__)


@patients_bp.route("/")
@login_required
def index():
    """
    Main dashboard showing all patients and their sessions.
    """
    show_filter = request.args.get("show", ALL_FILTER)

    data = PatientService.get_dashboard_data(show_filter)

    return render_template(
        "patients/list.html",
        grouped_sessions=data["grouped_sessions"],
        filters=FILTERS,
        allow_delete=ALLOW_DELETE,
        show=show_filter,
    )


@patients_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_person():
    """Add a new patient."""
    form = PersonForm()

    if form.validate_on_submit():
        success, person, message = PatientService.create(
            name=form.name.data,
            user_id=current_user.id,
            notes=form.notes.data if hasattr(form, "notes") else None,
        )

        if success:
            flash(message, FlashCategory.SUCCESS)
            return redirect(url_for("sessions.add_session"))
        else:
            flash(message, FlashCategory.ERROR)

    return render_template("patients/form_person.html", form=form)


@patients_bp.route("/<int:person_id>/edit", methods=["GET", "POST"])
@login_required
def edit_person(person_id):
    """Edit an existing patient."""
    person = PatientService.get_by_id(person_id)
    if not person:
        flash("Paciente no encontrado.", FlashCategory.ERROR)
        return redirect(url_for("patients.index"))

    form = PersonForm(obj=person)

    if form.validate_on_submit():
        success, person, message = PatientService.update(
            person_id=person_id,
            name=form.name.data,
            user_id=current_user.id,
            notes=form.notes.data if hasattr(form, "notes") else None,
        )

        if success:
            flash(message, FlashCategory.SUCCESS)
            return redirect(url_for("patients.index"))
        else:
            flash(message, FlashCategory.ERROR)

    return render_template(
        "patients/form_person.html", form=form, person=person, editing=True
    )


@patients_bp.route("/<int:person_id>/delete", methods=["GET", "POST"])
@login_required
def remove_person(person_id):
    """Delete a patient (with confirmation)."""
    if not ALLOW_DELETE:
        flash("La eliminación de pacientes está deshabilitada.", FlashCategory.ERROR)
        return redirect(url_for("patients.index"))

    person = PatientService.get_by_id(person_id)
    if not person:
        flash("Paciente no encontrado.", FlashCategory.ERROR)
        return redirect(url_for("patients.index"))

    form = DeletePersonForm()

    if request.method == "POST":
        # For legacy support, also check without form validation
        success, message = PatientService.delete(
            person_id=person_id,
            user_id=current_user.id,
            soft=True,  # Use soft delete by default
        )

        if success:
            flash(message, FlashCategory.SUCCESS)
        else:
            flash(message, FlashCategory.ERROR)

        return redirect(url_for("patients.index"))

    return render_template(
        "patients/delete_person.html", form=form, person_id=person_id, name=person.name
    )
