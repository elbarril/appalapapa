"""
Therapy session service for session management operations.

Handles creation, update, deletion, and payment tracking of sessions.
"""
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, date, timedelta
import logging
from flask import request

from app.extensions import db
from app.models.person import Person
from app.models.session import TherapySession
from app.models.audit_log import AuditLog
from app.utils.constants import AuditAction

logger = logging.getLogger(__name__)


class SessionService:
    """Service for therapy session operations."""
    
    @staticmethod
    def get_by_id(session_id: int) -> Optional[TherapySession]:
        """
        Get session by ID.
        
        Args:
            session_id: Session's ID
        
        Returns:
            TherapySession object or None
        """
        return TherapySession.query_active().filter_by(id=session_id).first()
    
    @staticmethod
    def create(
        person_id: int,
        session_date: date,
        session_price: float,
        user_id: Optional[int] = None,
        pending: bool = True,
        notes: Optional[str] = None
    ) -> Tuple[bool, Optional[TherapySession], str]:
        """
        Create a new therapy session.
        
        Args:
            person_id: Patient's ID
            session_date: Date of the session
            session_price: Price of the session
            user_id: ID of user creating the session
            pending: Payment status (default True)
            notes: Optional notes
        
        Returns:
            Tuple of (success, session, message)
        """
        # Validate person exists
        person = Person.query_active().filter_by(id=person_id).first()
        if not person:
            return False, None, "Paciente no encontrado."
        
        # Validate price
        if session_price <= 0:
            return False, None, "El precio debe ser mayor a cero."
        
        # Business rule: Date cannot be more than 7 days in the future
        max_future_date = date.today() + timedelta(days=7)
        if session_date > max_future_date:
            return False, None, "No se pueden agendar sesiones con más de 7 días de anticipación."
        
        try:
            session = TherapySession(
                person_id=person_id,
                session_date=session_date,
                session_price=float(session_price),
                pending=pending,
                notes=notes,
                created_by_id=user_id
            )
            db.session.add(session)
            db.session.commit()
            
            # Audit log
            AuditLog.log_create(
                table_name='therapy_sessions',
                record_id=session.id,
                new_values={
                    'person_id': person_id,
                    'person_name': person.name,
                    'session_date': session_date.isoformat(),
                    'session_price': session_price,
                    'pending': pending
                },
                user_id=user_id,
                ip_address=request.remote_addr if request else None
            )
            
            logger.info(f"Session created: ID {session.id} for patient {person.name}")
            return True, session, "Sesión agregada correctamente."
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating session: {str(e)}")
            return False, None, "Error al crear la sesión. Intente nuevamente."
    
    @staticmethod
    def update(
        session_id: int,
        session_date: date,
        session_price: float,
        user_id: Optional[int] = None,
        pending: Optional[bool] = None,
        notes: Optional[str] = None
    ) -> Tuple[bool, Optional[TherapySession], str]:
        """
        Update an existing therapy session.
        
        Args:
            session_id: Session's ID
            session_date: New date
            session_price: New price
            user_id: ID of user updating
            pending: New payment status (or None to keep current)
            notes: New notes
        
        Returns:
            Tuple of (success, session, message)
        """
        session = SessionService.get_by_id(session_id)
        if not session:
            return False, None, "Sesión no encontrada."
        
        # Validate price
        if session_price <= 0:
            return False, None, "El precio debe ser mayor a cero."
        
        try:
            old_values = session.to_dict()
            
            session.session_date = session_date
            session.session_price = float(session_price)
            if pending is not None:
                session.pending = pending
            session.notes = notes
            session.updated_by_id = user_id
            
            db.session.commit()
            
            # Audit log
            AuditLog.log_update(
                table_name='therapy_sessions',
                record_id=session.id,
                old_values=old_values,
                new_values=session.to_dict(),
                user_id=user_id,
                ip_address=request.remote_addr if request else None
            )
            
            logger.info(f"Session updated: ID {session_id}")
            return True, session, "Sesión actualizada correctamente."
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating session {session_id}: {str(e)}")
            return False, None, "Error al actualizar la sesión. Intente nuevamente."
    
    @staticmethod
    def delete(session_id: int, user_id: Optional[int] = None, soft: bool = True) -> Tuple[bool, str]:
        """
        Delete a therapy session.
        
        Args:
            session_id: Session's ID
            user_id: ID of user deleting
            soft: Whether to soft delete (default True)
        
        Returns:
            Tuple of (success, message)
        """
        session = SessionService.get_by_id(session_id)
        if not session:
            return False, "Sesión no encontrada."
        
        try:
            old_values = session.to_dict()
            
            if soft:
                session.soft_delete(user_id)
            else:
                db.session.delete(session)
            
            db.session.commit()
            
            # Audit log
            action = AuditAction.SOFT_DELETE if soft else AuditAction.DELETE
            AuditLog.log(
                action=action,
                table_name='therapy_sessions',
                record_id=session_id,
                old_values=old_values,
                user_id=user_id,
                ip_address=request.remote_addr if request else None
            )
            
            logger.info(f"Session deleted: ID {session_id} (soft={soft})")
            return True, "Sesión eliminada correctamente."
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting session {session_id}: {str(e)}")
            return False, "Error al eliminar la sesión. Intente nuevamente."
    
    @staticmethod
    def toggle_payment_status(session_id: int, user_id: Optional[int] = None) -> Tuple[bool, Optional[bool], str]:
        """
        Toggle payment status of a session.
        
        Args:
            session_id: Session's ID
            user_id: ID of user toggling
        
        Returns:
            Tuple of (success, new_pending_status, message)
        """
        session = SessionService.get_by_id(session_id)
        if not session:
            return False, None, "Sesión no encontrada."
        
        try:
            old_pending = session.pending
            new_pending = session.toggle_pending(user_id)
            db.session.commit()
            
            # Audit log
            AuditLog.log_update(
                table_name='therapy_sessions',
                record_id=session.id,
                old_values={'pending': old_pending},
                new_values={'pending': new_pending},
                user_id=user_id,
                ip_address=request.remote_addr if request else None
            )
            
            status_text = "pendiente" if new_pending else "pagada"
            logger.info(f"Session {session_id} marked as {status_text}")
            return True, new_pending, f"Sesión marcada como {status_text}."
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error toggling session {session_id}: {str(e)}")
            return False, None, "Error al actualizar el estado. Intente nuevamente."
    
    @staticmethod
    def get_session_with_person(session_id: int, person_id: int) -> Optional[Dict[str, Any]]:
        """
        Get session data along with person info for edit form.
        
        Args:
            session_id: Session's ID
            person_id: Person's ID
        
        Returns:
            Dictionary with session and person data
        """
        result = db.session.query(
            Person.name,
            TherapySession.session_date,
            TherapySession.session_price,
            TherapySession.pending,
            TherapySession.notes
        ).join(
            TherapySession, Person.id == TherapySession.person_id
        ).filter(
            Person.id == person_id,
            TherapySession.id == session_id,
            Person.deleted_at.is_(None),
            TherapySession.deleted_at.is_(None)
        ).first()
        
        if not result:
            return None
        
        return {
            'name': result[0],
            'date': result[1],
            'price': result[2],
            'pending': result[3],
            'notes': result[4]
        }
    
    @staticmethod
    def calculate_totals(person_id: Optional[int] = None) -> Dict[str, float]:
        """
        Calculate payment totals.
        
        Args:
            person_id: Optional person ID to filter by
        
        Returns:
            Dictionary with pending_total, paid_total, grand_total
        """
        query = TherapySession.query_active()
        if person_id:
            query = query.filter_by(person_id=person_id)
        
        sessions = query.all()
        
        pending_total = sum(s.session_price for s in sessions if s.pending)
        paid_total = sum(s.session_price for s in sessions if not s.pending)
        
        return {
            'pending_total': pending_total,
            'paid_total': paid_total,
            'grand_total': pending_total + paid_total
        }
    
    @staticmethod
    def get_recent_sessions(limit: int = 10) -> List[TherapySession]:
        """
        Get most recent sessions.
        
        Args:
            limit: Maximum sessions to return
        
        Returns:
            List of recent TherapySession objects
        """
        return TherapySession.query_active().order_by(
            TherapySession.session_date.desc(),
            TherapySession.created_at.desc()
        ).limit(limit).all()
