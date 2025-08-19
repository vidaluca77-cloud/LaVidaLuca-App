"""
Audit logging service for tracking security events.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..models.audit import AuditLog


class AuditLogService:
    """Service for audit logging."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_event(
        self,
        action: str,
        resource: str,
        success: bool,
        user_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ):
        """Log an audit event."""
        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=error_message,
            details=details or {}
        )
        
        self.db.add(audit_entry)
        self.db.commit()
    
    def log_auth_event(
        self,
        action: str,
        user_id: Optional[str],
        email: str,
        success: bool,
        ip_address: str,
        user_agent: str,
        error_message: Optional[str] = None,
        additional_details: Optional[Dict] = None
    ):
        """Log authentication-related events."""
        details = {
            "email": email,
            **(additional_details or {})
        }
        
        self.log_event(
            action=action,
            resource="authentication",
            user_id=user_id,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
            error_message=error_message
        )
    
    def log_session_event(
        self,
        action: str,
        user_id: str,
        session_id: str,
        success: bool,
        ip_address: str,
        user_agent: str,
        device_name: Optional[str] = None
    ):
        """Log session-related events."""
        details = {
            "session_id": session_id,
            "device_name": device_name
        }
        
        self.log_event(
            action=action,
            resource="session",
            user_id=user_id,
            resource_id=session_id,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
    
    def log_admin_action(
        self,
        action: str,
        admin_user_id: str,
        target_user_id: str,
        success: bool,
        ip_address: str,
        user_agent: str,
        reason: Optional[str] = None,
        additional_details: Optional[Dict] = None
    ):
        """Log admin actions on users."""
        details = {
            "target_user_id": target_user_id,
            "reason": reason,
            **(additional_details or {})
        }
        
        self.log_event(
            action=f"admin_{action}",
            resource="user_management",
            user_id=admin_user_id,
            resource_id=target_user_id,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
    
    def log_security_event(
        self,
        action: str,
        user_id: Optional[str],
        success: bool,
        ip_address: str,
        user_agent: str,
        threat_level: str = "medium",
        details: Optional[Dict] = None
    ):
        """Log security-related events."""
        event_details = {
            "threat_level": threat_level,
            **(details or {})
        }
        
        self.log_event(
            action=action,
            resource="security",
            user_id=user_id,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            details=event_details
        )
    
    def get_audit_logs(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        success: Optional[bool] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> tuple[List[AuditLog], int]:
        """Get filtered audit logs."""
        query = self.db.query(AuditLog)
        
        # Apply filters
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        if action:
            query = query.filter(AuditLog.action.ilike(f"%{action}%"))
        
        if resource:
            query = query.filter(AuditLog.resource == resource)
        
        if success is not None:
            query = query.filter(AuditLog.success == success)
        
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        logs = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
        
        return logs, total
    
    def get_security_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get security summary for the specified number of days."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total events
        total_events = self.db.query(AuditLog).filter(
            AuditLog.timestamp >= start_date
        ).count()
        
        # Failed events
        failed_events = self.db.query(AuditLog).filter(
            AuditLog.timestamp >= start_date,
            AuditLog.success == False
        ).count()
        
        # Events by action
        action_stats = self.db.query(
            AuditLog.action,
            self.db.func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.timestamp >= start_date
        ).group_by(AuditLog.action).all()
        
        # Events by resource
        resource_stats = self.db.query(
            AuditLog.resource,
            self.db.func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.timestamp >= start_date
        ).group_by(AuditLog.resource).all()
        
        # Top IP addresses
        ip_stats = self.db.query(
            AuditLog.ip_address,
            self.db.func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.timestamp >= start_date,
            AuditLog.ip_address.isnot(None)
        ).group_by(AuditLog.ip_address).order_by(
            self.db.text('count DESC')
        ).limit(10).all()
        
        return {
            "period_days": days,
            "total_events": total_events,
            "failed_events": failed_events,
            "success_rate": (total_events - failed_events) / total_events * 100 if total_events > 0 else 0,
            "events_by_action": [{"action": action, "count": count} for action, count in action_stats],
            "events_by_resource": [{"resource": resource, "count": count} for resource, count in resource_stats],
            "top_ip_addresses": [{"ip_address": ip, "count": count} for ip, count in ip_stats]
        }
    
    def cleanup_old_logs(self, days_to_keep: int = 90) -> int:
        """Clean up audit logs older than specified days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        deleted_count = self.db.query(AuditLog).filter(
            AuditLog.timestamp < cutoff_date
        ).delete()
        
        self.db.commit()
        return deleted_count