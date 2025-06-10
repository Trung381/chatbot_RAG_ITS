import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME
        self.tls = settings.SMTP_TLS
        
    def _create_message(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str, 
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> MIMEMultipart:
        """
        Create email message
        """
        message = MIMEMultipart()
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        if cc:
            message["Cc"] = ", ".join(cc)
        if bcc:
            message["Bcc"] = ", ".join(bcc)
            
        message.attach(MIMEText(html_content, "html"))
        return message
        
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Send email
        """
        if not self.host or not self.port:
            logger.warning("SMTP settings not configured, skipping email sending")
            return False
            
        message = self._create_message(to_email, subject, html_content, cc, bcc)
        
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                if self.tls:
                    server.starttls()
                if self.user and self.password:
                    server.login(self.user, self.password)
                    
                recipients = [to_email]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                    
                server.sendmail(self.from_email, recipients, message.as_string())
                logger.info(f"Email sent to {to_email}")
                return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
            
    def send_welcome_email(self, to_email: str, username: str) -> bool:
        """
        Send welcome email to new user
        """
        subject = f"Welcome to {settings.PROJECT_NAME}!"
        html_content = f"""
        <html>
            <body>
                <h1>Welcome to {settings.PROJECT_NAME}!</h1>
                <p>Hi {username},</p>
                <p>Thank you for registering with us.</p>
                <p>Best regards,<br>The {settings.PROJECT_NAME} Team</p>
            </body>
        </html>
        """
        return self.send_email(to_email, subject, html_content)
        
    def send_password_reset_email(self, to_email: str, username: str, reset_token: str) -> bool:
        """
        Send password reset email
        """
        subject = "Password Reset Request"
        html_content = f"""
        <html>
            <body>
                <h1>Password Reset Request</h1>
                <p>Hi {username},</p>
                <p>You requested to reset your password. Please use the following token:</p>
                <p><strong>{reset_token}</strong></p>
                <p>If you didn't request this, please ignore this email.</p>
                <p>Best regards,<br>The {settings.PROJECT_NAME} Team</p>
            </body>
        </html>
        """
        return self.send_email(to_email, subject, html_content)
