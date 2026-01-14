"""
Patient service for patient management operations.

Handles creation, update, deletion, and querying of patients.
"""

from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime
import logging
from flask import request
from collections import defaultdict

from app.extensions import db
from app.models.person import Person
from app.models.session import TherapySession
from app.models.audit_log import AuditLog
from app.utils.constants import AuditAction, ALL_FILTER, PENDING_FILTER, PAID_FILTER
from app.utils.formatters import format_date, format_price

logger = logging.getLogger(__name__)


class PatientService:
    """Service for patient (person) operations."""

    @staticmethod
    def get_all_active(order_by_name: bool = True) -> List[Person]:
        """
        Get all active patients.

        Args:
            order_by_name: Whether to order by name

        Returns:
            List of active Person objects
        """
        return Person.get_all_active(order_by_name).all()

    @staticmethod
    def get_by_id(person_id: int) -> Optional[Person]:
        """
        Get patient by ID.

        Args:
            person_id: Patient's ID

        Returns:
            Person object or None
        """
        return Person.query_active().filter_by(id=person_id).first()

    @staticmethod
    def get_for_select() -> List[Tuple[int, str]]:
        """
        Get patients formatted for select dropdown.

        Returns:
            List of tuples (id, name)
        """
        persons = Person.get_all_active().all()
        return [(p.id, p.name) for p in persons]

    @staticmethod
    def create(
        name: str, user_id: Optional[int] = None, notes: Optional[str] = None
    ) -> Tuple[bool, Optional[Person], str]:
        """
        Create a new patient.

        Args:
            name: Patient's name
            user_id: ID of user creating the patient
            notes: Optional notes

        Returns:
            Tuple of (success, person, message)
        """
        if not name or not name.strip():
            return False, None, "El nombre es requerido."

        name = name.strip()

        # Check for duplicate
        existing = Person.get_by_name(name)
        if existing:
            return False, None, "Ya existe un paciente con ese nombre."

        try:
            person = Person(name=name, notes=notes, created_by_id=user_id)
            db.session.add(person)
            db.session.commit()

            # Audit log
            AuditLog.log_create(
                table_name="persons",
                record_id=person.id,
                new_values={"name": name, "notes": notes},
                user_id=user_id,
                ip_address=request.remote_addr if request else None,
            )

            logger.info(f"Patient created: {name} (ID: {person.id})")
            return True, person, "Paciente agregado correctamente."

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating patient {name}: {str(e)}")
            return False, None, "Error al crear el paciente. Intente nuevamente."

    @staticmethod
    def update(
        person_id: int,
        name: str,
        user_id: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> Tuple[bool, Optional[Person], str]:
        """
        Update an existing patient.

        Args:
            person_id: Patient's ID
            name: New name
            user_id: ID of user updating
            notes: New notes

        Returns:
            Tuple of (success, person, message)
        """
        person = PatientService.get_by_id(person_id)
        if not person:
            return False, None, "Paciente no encontrado."

        if not name or not name.strip():
            return False, None, "El nombre es requerido."

        name = name.strip()

        # Check for duplicate (excluding current)
        existing = (
            Person.query_active()
            .filter(Person.name == name, Person.id != person_id)
            .first()
        )
        if existing:
            return False, None, "Ya existe otro paciente con ese nombre."

        try:
            old_values = {"name": person.name, "notes": person.notes}

            person.name = name
            person.notes = notes
            person.updated_by_id = user_id
            db.session.commit()

            # Audit log
            AuditLog.log_update(
                table_name="persons",
                record_id=person.id,
                old_values=old_values,
                new_values={"name": name, "notes": notes},
                user_id=user_id,
                ip_address=request.remote_addr if request else None,
            )

            logger.info(f"Patient updated: {name} (ID: {person_id})")
            return True, person, "Paciente actualizado correctamente."

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating patient {person_id}: {str(e)}")
            return False, None, "Error al actualizar el paciente. Intente nuevamente."

    @staticmethod
    def delete(
        person_id: int, user_id: Optional[int] = None, soft: bool = True
    ) -> Tuple[bool, str]:
        """
        Delete a patient.

        Args:
            person_id: Patient's ID
            user_id: ID of user deleting
            soft: Whether to soft delete (default True)

        Returns:
            Tuple of (success, message)
        """
        person = PatientService.get_by_id(person_id)
        if not person:
            return False, "Paciente no encontrado."

        try:
            old_values = person.to_dict()

            if soft:
                # Soft delete person and sessions
                person.soft_delete(user_id)
                for session in person.therapy_sessions:
                    session.soft_delete(user_id)
            else:
                # Hard delete (cascade will delete sessions)
                db.session.delete(person)

            db.session.commit()

            # Audit log
            action = AuditAction.SOFT_DELETE if soft else AuditAction.DELETE
            AuditLog.log(
                action=action,
                table_name="persons",
                record_id=person_id,
                old_values=old_values,
                user_id=user_id,
                ip_address=request.remote_addr if request else None,
            )

            logger.info(f"Patient deleted: ID {person_id} (soft={soft})")
            return True, "Paciente eliminado correctamente."

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting patient {person_id}: {str(e)}")
            return False, "Error al eliminar el paciente. Intente nuevamente."

    @staticmethod
    def restore(person_id: int, user_id: Optional[int] = None) -> Tuple[bool, str]:
        """
        Restore a soft-deleted patient.

        Args:
            person_id: Patient's ID
            user_id: ID of user restoring

        Returns:
            Tuple of (success, message)
        """
        person = Person.query.filter_by(id=person_id).first()
        if not person:
            return False, "Paciente no encontrado."

        if not person.is_deleted:
            return False, "Este paciente no está eliminado."

        try:
            person.restore()
            for session in person.therapy_sessions:
                session.restore()

            db.session.commit()

            AuditLog.log(
                action=AuditAction.RESTORE,
                table_name="persons",
                record_id=person_id,
                user_id=user_id,
                ip_address=request.remote_addr if request else None,
            )

            logger.info(f"Patient restored: ID {person_id}")
            return True, "Paciente restaurado correctamente."

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error restoring patient {person_id}: {str(e)}")
            return False, "Error al restaurar el paciente. Intente nuevamente."

    @staticmethod
    def get_dashboard_data(show_filter: str = ALL_FILTER) -> Dict[str, Any]:
        """
        Get data for the main dashboard.

        Args:
            show_filter: Filter for sessions ('all', 'pending', 'paid')

        Returns:
            Dictionary with grouped_sessions, total, filter info
        """
        # Build base query
        query = (
            db.session.query(
                Person.id,
                Person.name,
                TherapySession.id,
                TherapySession.session_date,
                TherapySession.session_price,
                TherapySession.pending,
            )
            .outerjoin(
                TherapySession,
                db.and_(
                    Person.id == TherapySession.person_id,
                    TherapySession.deleted_at.is_(None),
                ),
            )
            .filter(Person.deleted_at.is_(None))
        )

        # Apply filter
        if show_filter == PENDING_FILTER:
            query = query.filter(TherapySession.pending == True)
        elif show_filter == PAID_FILTER:
            query = query.filter(TherapySession.pending == False)

        # Order by name and date
        query = query.order_by(Person.name, TherapySession.session_date)

        # Group data
        grouped_sessions = defaultdict(list)
        total = 0

        for person_id, name, session_id, date, price, pending in query.all():
            grouped_session_key = (person_id, name)

            if date and price:
                total += 1
                session_data = (
                    session_id,
                    format_date(date) if date else "",
                    format_price(price) if price else "",
                    pending,
                )
                grouped_sessions[grouped_session_key].append(session_data)
            elif person_id not in [k[0] for k in grouped_sessions.keys()]:
                # Include patients with no sessions
                grouped_sessions[grouped_session_key] = []

        return {
            "grouped_sessions": dict(grouped_sessions),
            "total": total,
            "filter": show_filter,
        }
