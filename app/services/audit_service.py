"""
Audit service for tracking and querying audit logs.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging

from app.extensions import db
from app.models.audit_log import AuditLog
from app.utils.constants import AuditAction

logger = logging.getLogger(__name__)


class AuditService:
    """Service for audit log operations."""

    @staticmethod
    def get_recent_activity(limit: int = 50) -> List[AuditLog]:
        """
        Get recent audit log entries.

        Args:
            limit: Maximum entries to return

        Returns:
            List of AuditLog entries
        """
        return AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(limit).all()

    @staticmethod
    def get_user_activity(user_id: int, limit: int = 100) -> List[AuditLog]:
        """
        Get audit log entries for a specific user.

        Args:
            user_id: User's ID
            limit: Maximum entries to return

        Returns:
            List of AuditLog entries
        """
        return AuditLog.get_for_user(user_id, limit).all()

    @staticmethod
    def get_record_history(
        table_name: str, record_id: int, limit: int = 50
    ) -> List[AuditLog]:
        """
        Get audit history for a specific record.

        Args:
            table_name: Name of the table
            record_id: ID of the record
            limit: Maximum entries to return

        Returns:
            List of AuditLog entries
        """
        return AuditLog.get_for_record(table_name, record_id, limit).all()

    @staticmethod
    def get_login_attempts(
        user_id: Optional[int] = None, days: int = 7
    ) -> List[AuditLog]:
        """
        Get login attempts for security monitoring.

        Args:
            user_id: Optional user ID to filter by
            days: Number of days to look back

        Returns:
            List of login-related AuditLog entries
        """
        since = datetime.utcnow() - timedelta(days=days)

        query = AuditLog.query.filter(
            AuditLog.action.in_([AuditAction.LOGIN, AuditAction.LOGIN_FAILED]),
            AuditLog.timestamp >= since,
        )

        if user_id:
            query = query.filter(AuditLog.record_id == user_id)

        return query.order_by(AuditLog.timestamp.desc()).all()

    @staticmethod
    def get_security_summary(days: int = 7) -> Dict[str, Any]:
        """
        Get security summary for dashboard.

        Args:
            days: Number of days to summarize

        Returns:
            Dictionary with security statistics
        """
        since = datetime.utcnow() - timedelta(days=days)

        login_success = AuditLog.query.filter(
            AuditLog.action == AuditAction.LOGIN, AuditLog.timestamp >= since
        ).count()

        login_failed = AuditLog.query.filter(
            AuditLog.action == AuditAction.LOGIN_FAILED, AuditLog.timestamp >= since
        ).count()

        password_resets = AuditLog.query.filter(
            AuditLog.action == AuditAction.PASSWORD_RESET, AuditLog.timestamp >= since
        ).count()

        return {
            "login_success": login_success,
            "login_failed": login_failed,
            "password_resets": password_resets,
            "period_days": days,
        }

    @staticmethod
    def cleanup_old_logs(days: int = 365) -> int:
        """
        Delete audit logs older than specified days.

        Args:
            days: Age threshold in days

        Returns:
            Number of deleted entries
        """
        threshold = datetime.utcnow() - timedelta(days=days)

        deleted = AuditLog.query.filter(AuditLog.timestamp < threshold).delete()

        db.session.commit()

        logger.info(f"Cleaned up {deleted} audit log entries older than {days} days")
        return deleted
