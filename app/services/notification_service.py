import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from .email_service import EmailService

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.email_service = EmailService()
        
    def notify_user(
        self,
        user: User,
        notification_type: str,
        data: Dict[str, Any],
        db: Optional[Session] = None
    ) -> bool:
        """
        Send notification to user based on type
        """
        if notification_type == "welcome":
            return self.send_welcome_notification(user)
        elif notification_type == "password_reset":
            return self.send_password_reset_notification(user, data.get("reset_token"))
        elif notification_type == "item_created":
            return self.send_item_created_notification(user, data.get("item_title"))
        else:
            logger.warning(f"Unknown notification type: {notification_type}")
            return False
            
    def send_welcome_notification(self, user: User) -> bool:
        """
        Send welcome notification to new user
        """
        return self.email_service.send_welcome_email(user.email, user.username)
        
    def send_password_reset_notification(self, user: User, reset_token: str) -> bool:
        """
        Send password reset notification
        """
        if not reset_token:
            logger.error("Reset token is required for password reset notification")
            return False
            
        return self.email_service.send_password_reset_email(
            user.email, user.username, reset_token
        )
        
    def send_item_created_notification(self, user: User, item_title: str) -> bool:
        """
        Send notification when item is created
        """
        if not item_title:
            logger.error("Item title is required for item created notification")
            return False
            
        subject = "New Item Created"
        html_content = f"""
        <html>
            <body>
                <h1>New Item Created</h1>
                <p>Hi {user.username},</p>
                <p>Your item "{item_title}" has been created successfully.</p>
                <p>Best regards,<br>The Team</p>
            </body>
        </html>
        """
        return self.email_service.send_email(user.email, subject, html_content)
