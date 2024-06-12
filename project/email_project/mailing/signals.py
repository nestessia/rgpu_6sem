from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmailMessage, CustomUser
from .tasks import send_email_task
import os

@receiver(post_save, sender=EmailMessage)
def send_email_on_create(sender, instance, created, **kwargs):
    if created:
        subject = instance.subject
        message = instance.message
        from_email = os.getenv('EMAIL_HOST_USER')
        recipient_list = list(CustomUser.objects.filter(is_staff=False, is_active=True).values_list('email', flat=True))
        send_email_task.delay(subject, message, from_email, recipient_list)
