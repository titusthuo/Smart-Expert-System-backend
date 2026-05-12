import logging

from django.dispatch import receiver

logger = logging.getLogger(__name__)
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset token creation and sends email with custom reset URL
    """
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:8081')
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_url": f"{frontend_url}/reset-password/{reset_password_token.key}",
    }

    # Render email templates
    email_html_message = render_to_string("email/user_reset_password.html", context)
    email_plaintext_message = render_to_string("email/user_reset_password.txt", context)

    # Create and send email
    msg = EmailMultiAlternatives(
        subject="Password Reset Request - Smart Expert Mental Health Support",
        body=email_plaintext_message,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@smarthealth.com'),
        to=[reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    
    try:
        msg.send()
        logger.info("Password reset email sent to %s", reset_password_token.user.email)
    except Exception as e:
        logger.error("Failed to send email to %s: %s", reset_password_token.user.email, e)
