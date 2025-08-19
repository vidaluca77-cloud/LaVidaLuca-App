"""
Email service for contact forms and notifications.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from ..core.config import settings
from ..schemas.activity import ContactForm


class EmailService:
    """Email service for sending notifications and contact form submissions."""
    
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
        self.from_email = settings.from_email
    
    async def send_contact_form_submission(self, form_data: ContactForm) -> bool:
        """Send contact form submission via email."""
        
        if not self._is_configured():
            return False
        
        subject = f"Contact Form: {form_data.subject}"
        
        # Create email content
        content = f"""
        New contact form submission from La Vida Luca website:
        
        Name: {form_data.name}
        Email: {form_data.email}
        Subject: {form_data.subject}
        
        Message:
        {form_data.message}
        
        Activity Interest: {form_data.activity_interest or 'None specified'}
        
        ---
        This message was sent from the La Vida Luca contact form.
        Reply directly to this email to respond to the sender.
        """
        
        return await self._send_email(
            to_email="contact@lavidaluca.fr",
            subject=subject,
            content=content,
            reply_to=form_data.email
        )
    
    async def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new user."""
        
        if not self._is_configured():
            return False
        
        subject = "Bienvenue dans La Vida Luca !"
        
        content = f"""
        Bonjour {user_name},
        
        Bienvenue dans la communauté La Vida Luca !
        
        Votre compte a été créé avec succès. Vous pouvez maintenant :
        - Découvrir notre catalogue d'activités
        - Recevoir des suggestions personnalisées
        - Participer aux activités et soumettre vos réalisations
        - Rejoindre notre communauté d'apprentissage
        
        Nous sommes ravis de vous accompagner dans votre parcours d'apprentissage !
        
        L'équipe La Vida Luca
        https://lavidaluca.fr
        """
        
        return await self._send_email(
            to_email=user_email,
            subject=subject,
            content=content
        )
    
    async def send_notification_email(
        self,
        to_email: str,
        subject: str,
        content: str
    ) -> bool:
        """Send general notification email."""
        
        if not self._is_configured():
            return False
        
        return await self._send_email(to_email, subject, content)
    
    def _is_configured(self) -> bool:
        """Check if email service is properly configured."""
        return bool(
            self.smtp_host and
            self.smtp_user and
            self.smtp_password and
            self.from_email
        )
    
    async def _send_email(
        self,
        to_email: str,
        subject: str,
        content: str,
        reply_to: Optional[str] = None
    ) -> bool:
        """Send email via SMTP."""
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if reply_to:
                msg['Reply-To'] = reply_to
            
            # Attach content
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            # Log error (in production, use proper logging)
            print(f"Failed to send email: {e}")
            return False